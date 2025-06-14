#!/usr/bin/env python3
"""
Test script to start MCP servers programmatically with UV
"""

import os
import sys
import subprocess
import time
import signal
import atexit

def start_mcp_servers():
    """Start MCP servers programmatically using UV"""
    # Store server processes for cleanup
    server_processes = []
    
    def cleanup_servers():
        """Clean up server processes on exit"""
        print("\nCleaning up MCP servers...")
        for proc in server_processes:
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
        print("Servers stopped.")
    
    # Register cleanup function
    atexit.register(cleanup_servers)
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nReceived interrupt signal, shutting down...")
        cleanup_servers()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Path to MCP directory
    mcp_dir = os.path.join(os.path.dirname(__file__), "core", "mcp")
    
    if not os.path.exists(mcp_dir):
        print(f"Error: MCP directory not found at {mcp_dir}")
        return False
    
    try:
        print("Starting MCP servers with UV...")
        print(f"Working directory: {mcp_dir}")
        
        # Start weather server (port 8000)
        print("Starting weather server on port 8000...")
        weather_cmd = ["uv", "run", "python", "mcp_servers/weather_server.py"]
        weather_proc = subprocess.Popen(
            weather_cmd,
            cwd=mcp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        server_processes.append(weather_proc)
        
        # Start calculator server (port 8001) 
        print("Starting calculator server on port 8001...")
        calc_cmd = ["uv", "run", "python", "mcp_servers/calculator_server.py"]
        calc_proc = subprocess.Popen(
            calc_cmd,
            cwd=mcp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        server_processes.append(calc_proc)
        
        # Give servers time to start
        print("Waiting for servers to initialize...")
        time.sleep(5)
        
        # Check if servers are running
        servers_running = True
        for i, proc in enumerate(server_processes):
            server_name = "Weather" if i == 0 else "Calculator"
            if proc.poll() is not None:
                servers_running = False
                print(f"✗ {server_name} server failed to start")
                # Print error output
                stdout, stderr = proc.communicate()
                if stdout:
                    print(f"STDOUT: {stdout.decode()}")
                if stderr:
                    print(f"STDERR: {stderr.decode()}")
            else:
                print(f"✓ {server_name} server is running (PID: {proc.pid})")
        
        if servers_running:
            print("\n✓ All MCP servers are running successfully!")
            print("Servers will run until you press Ctrl+C")
            
            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
                
            return True
        else:
            print("\n✗ Some servers failed to start")
            cleanup_servers()
            return False
            
    except FileNotFoundError:
        print("✗ UV not found. Please install UV first:")
        print("curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    except Exception as e:
        print(f"✗ Error starting MCP servers: {e}")
        cleanup_servers()
        return False

if __name__ == "__main__":
    print("MCP Server Test Script")
    print("======================")
    success = start_mcp_servers()
    if not success:
        sys.exit(1)
