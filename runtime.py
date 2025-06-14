import os
import time
import sys
import subprocess
import time
from colorama import Back
import keyboard
import threading
import shutil
import asyncio
from core.rt_serve import runtimeEngine

global anim, prevData, loopbackToModel, data, runtime
prevData = ""
loopbackToModel = ""
anim = 1

# Retrieve and export api
api_path = os.path.expanduser("~/.rtconf/api.txt")
try:
    with open(api_path, "r") as file:
        api = file.read().strip()
        os.environ["GROQ_API_KEY"] = api
        print("API key set successfully.")
except FileNotFoundError:
    print(f"File not found: {api_path}")
# Initialize Runtime Backend
runtime = runtimeEngine()


def clear_memory():
    global prevData, loopbackToModel, runtime
    prevData = ""
    loopbackToModel = ""
    os.system("tput bel")
    runtime = runtimeEngine()
    print(Back.RED + "Memory Reset !" + Back.BLACK)


async def commGPT(data):
    global prevData, loopbackToModel, anim, runtime
    data = data.replace("clr_mem", "")
    try:
        __commOS = await runtime.mcp_call(data)
        return __commOS
    except Exception as e:
        # Fallback to regular prediction if online call fails
        print(f"Online call failed: {e}")
        print("Falling back to legacy mode...")
        return runtime.predict(data)


# def execute_script(language, script_content):
#     script_file_name = "TempScript"
#     executable_name = "temp"
#     save_file = data.replace(" ", "_")

#     print(f"Executing {language} script")

#     with open(script_file_name, "w") as write_temp:
#         script_lines = script_content.split("\n")[1:]
#         print(script_lines)
#         for line in script_lines:
#             write_temp.write(line.replace("python", "#python") + "\n")

#         with open(save_file, "w") as write_temp_2:
#             script_lines = script_content.split("\n")[1:]
#             for line in script_lines:
#                 write_temp_2.write(line + "\n")

#     # if language.lower() == "c":
#     #     print("Compiling Resource...")
#     #     os.system(f"gcc {script_file_name} -o {executable_name}")
#     #     os.system(f"./{executable_name}")
#     # elif language.lower() == "python":
#     #     print(Back.MAGENTA + "Initializing Python Interpreter...\n" + Back.RESET)
#     #     run_result = subprocess.run(f"python {script_file_name}", shell=True, capture_output=True)

#     #     if run_result.returncode != 0:
#     #         print("Error during execution:\n", run_result.stderr.decode())
#     #         return 2
#     #     print("\nProgram Completed" + Back.RESET)
#     #     return 0
#     #     # os.system(f"./{executable_name}")
#     # else:
#     #     os.system(f"chmod +x {script_file_name}")
#     #     os.system(f"./{script_file_name}")

#         print(Back.MAGENTA + "Initializing Python Interpreter...\n" + Back.RESET)
#         # run_result = subprocess.run(f"python {script_file_name}", shell=True, capture_output=True)
#         print(open(script_file_name, "r").read())
#         os.system(f"python {script_file_name}")
#         print("\nProgram Completed" + Back.RESET)
#         return 0

#     os.system(f"rm {script_file_name}")

# def execute_script(language, script_content):
#     script_file_name = f"TempScript.{language.lower()}"
#     executable_name = "temp"

#     print(f"\n// Executing {language} script")

#     with open(script_file_name, "w") as write_temp:
#         script_lines = script_content.split("\n")[1:]
#         if "python" in script_lines[0]:
#             script_lines[0] = script_lines[0].replace("python", "#python")
#         for line in script_lines:
#             write_temp.write(line + "\n")

#     if language.lower() == "c":
#         print("Compiling Resource...")
#         os.system(f"gcc {script_file_name} -o {executable_name}")
#         os.system(f"./{executable_name}")
#     else:
#         print(Back.MAGENTA + "Initializing Python Interpreter...\n" + Back.RESET)
#         os.system(f"python {script_file_name}")
#         #os.system(f"./{executable_name}")

#     os.system(f"rm {script_file_name}")

def loading_animation():
    global anim
    x = 0
    while True:
        if anim == 0:
            print("Runtime is processing the input", end="")
            print("", end="", flush=True)
            time.sleep(0.5)
            if x <= 3:
                x += 1
                print("." * x, end="", flush=True)
            else:
                x = 0
            print(
                "\033[K", end="", flush=True
            )  # Clear the line from the cursor position to the end
            print("\r", end="", flush=True)
        else:
            time.sleep(0.5)
            continue


# run_loading_animation()
if __name__ == "__main__":
    os.system("clear")
    terminal_width, _ = shutil.get_terminal_size()
    current_line_length = 0
    get_input_memory = 0
    print(
        Back.GREEN
        + " | ♜ RunTime v2.0 | "
        + Back.BLACK
    )
    print("\n")
    print(
        "TriFusionAI | This is an Experimental system !, Recommended to run with 'safeMode' flag..."
    )
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    while True:
        print(Back.BLACK)
        inputPart = ""
        get_input = ""
        while inputPart != "q":
            get_input = get_input + " " + inputPart
            inputPart = input(Back.BLUE + "[RSH]$ > ")
            if inputPart == "clr_mem":
                clear_memory()
            elif inputPart == "exit":
                anim = 1
                time.sleep(0.5)
                print("Deactivating The Virtual Environment...")
                os.system("exit()")
        # run_loading_animation(1)
        # loading_thread.join()
        print("\n" + Back.BLUE + "Runtime (⌐■_■) \n" + Back.BLACK, end="")
        anim = 0

        try:
            if get_input == "clr_mem":
                anim = 1
                clear_memory()
                continue
            elif get_input == "exit":
                anim = 1
                print("Deactivating The Virtual Environment...")
                os.system("deactivate")
                os.system("exit()")
                break
            elif get_input == "-r":
                anim = 1
                get_input = get_input_memory
                break
            get_input_memory = get_input
            # while True:
            if True:
                data = asyncio.run(commGPT(get_input))
                data = data.replace("**Python**", "")
                anim = 1
                time.sleep(0.8)
                print("\n")
                loopbackToModel = data
                for char in data:
                    if char != "`":
                        # current_line_length += 1
                        # if current_line_length >= terminal_width:
                        #     sys.stdout.write("\n")
                        #     sys.stdout.flush()
                        #     current_line_length = 0
                        # time.sleep(0.01)
                        sys.stdout.write("\033[1m" + char)
                        sys.stdout.flush()
                # if "```" in data:
                #     if len(sys.argv) > 1:
                #         if sys.argv[1] == "safeMode":
                #             print(
                #                 "Runtime Is running in Safemode !, Script Execution is not permitted..."
                #             )
                #     else:
                #         script_data = data.replace("```", "")
                #         script_language = script_data.split("\n")[0].lower()
                #         # execute_script(script_language, script_data)
        except Exception as e:
            print("\nAn error occurred:", e)
            print("/!\\")
            anim = 1
