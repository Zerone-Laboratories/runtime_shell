from typing import List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Rigel Tool", port=8001)


@mcp.tool()
def current_time() -> str:
    """Returns the current time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def execute_system_command(command: str) -> str:
    """Run a Linux Command on the shell"""
    import subprocess
    import shlex
    import os

    try:
        # Expanded list of commands that typically need elevated privileges
        sudo_commands = [
            'apt', 'apt-get', 'yum', 'dnf', 'pacman', 'zypper',
            'systemctl', 'service', 'mount', 'umount',
            'fdisk', 'parted', 'mkfs', 'fsck',
            'chmod', 'chown', 'chgrp', 'passwd', 'usermod', 'groupmod',
            'iptables', 'ufw', 'firewall-cmd', 'nft',
            'modprobe', 'rmmod', 'insmod',
            'sysctl', 'update-grub', 'grub-install'
        ]

        # Clean and validate command
        command = command.strip()
        if not command:
            return "Error: Empty command"

        cmd_parts = shlex.split(command)
        if not cmd_parts:
            return "Error: Invalid command format"

        # Check if command exists in PATH
        base_command = cmd_parts[0]
        if not any(os.path.isfile(os.path.join(path, base_command)) and os.access(os.path.join(path, base_command), os.X_OK)
                  for path in os.environ.get("PATH", "").split(os.pathsep)):
            # Try common system paths
            common_paths = ['/bin', '/usr/bin', '/sbin', '/usr/sbin', '/usr/local/bin']
            found = False
            for path in common_paths:
                if os.path.isfile(os.path.join(path, base_command)) and os.access(os.path.join(path, base_command), os.X_OK):
                    found = True
                    break
            if not found:
                return f"Error: Command '{base_command}' not found in PATH or common system directories"

        # Improved sudo detection
        needs_sudo = (
            any(base_command == sudo_cmd or base_command.endswith('/' + sudo_cmd) 
                for sudo_cmd in sudo_commands) or
            # Check if command is in system directories that typically require sudo
            any(base_command.startswith(path) for path in ['/sbin/', '/usr/sbin/'])
        )

        # Prepare environment
        env = os.environ.copy()
        
        if needs_sudo:
            # Check if pkexec is available
            if not any(os.path.isfile(os.path.join(path, 'pkexec')) 
                      for path in env.get("PATH", "").split(os.pathsep)):
                return "Error: pkexec not available for elevated privileges"
            
            full_command = ['pkexec', '--user', 'root'] + cmd_parts
            env['PKEXEC_TITLE'] = f"RIGEL System Command: {base_command}"
        else:
            full_command = cmd_parts

        # Execute with better error handling
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            timeout=60,  # Increased timeout
            env=env,
            cwd=os.getcwd()  # Explicit working directory
        )

        # Format output more clearly
        output_parts = []
        
        if result.stdout and result.stdout.strip():
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
        
        if result.stderr and result.stderr.strip():
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")
        
        output_parts.append(f"Exit code: {result.returncode}")
        
        # Add success/failure indicator
        status = "SUCCESS" if result.returncode == 0 else "FAILED"
        output_parts.insert(0, f"Command: {command}")
        output_parts.insert(1, f"Status: {status}")
        
        return "\n\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after 60 seconds"
    except FileNotFoundError as e:
        return f"Error: Command not found or not executable: {e}"
    except PermissionError:
        return f"Error: Permission denied executing '{command}'. Try with elevated privileges."
    except OSError as e:
        return f"Error: System error executing command: {e}"
    except Exception as e:
        return f"Error: Unexpected error executing '{command}': {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="sse")
