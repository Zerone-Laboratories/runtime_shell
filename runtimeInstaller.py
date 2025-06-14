import os

print("Initializing the installation...")
print("TriFusion - Runtime Shell v2.0")
print("Setting up the runtime environment...")
os.system("pip install -r requirements.txt")

print("\n\nTesting gpt response output")
api = input("Enter GROQ API[visit: https://console.groq.com/keys]:")

config_dir = os.path.expanduser("~/.rtconf")
os.makedirs(config_dir, exist_ok=True)

api_file_path = os.path.join(config_dir, "api.txt")
with open(api_file_path, "w") as f:
    f.write(api)

api = open(os.path.expanduser("~/.rtconf/api.txt"), "r").read()
os.environ["GROQ_API_KEY"] = api

os.system("python core/db_conn.py")

print("Testing the runtimeEngine")
from core.rt_serve import runtimeEngine
runtime = runtimeEngine()
print(runtime.predict("Say Hello to the user"))

print("\n\n!!! Check complete, to run the program, To start the system, type :python runtime.py !!!")
print("\nIf any issues occurred while setting up the workers or the API, re-run this script to reconfigure...")
print("\n\nTriFusion\n\n")
