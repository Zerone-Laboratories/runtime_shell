import os
from ast import arg
from asyncio import streams
import sys
import json
import google.generativeai as genai
import subprocess
genai.configure(api_key=open("/home/zerone/Projects/runtime2/sysFiles/api.txt","r").read().replace("\n",""))


def categorize_question(question):
    contextual_variables = ['who', 'what', 'where', 'when', 'why', 'how']
    tokens = question.split(" ")
    for token in tokens:
        if token.lower() in contextual_variables:
            pass
    return 'Non-contextual'

def hyperScanFunction(data):
    __commOS = 'python ~/Projects/runtime2/sysFiles/HyperScan \"'+data.replace("clr_mem","")+'\"'
    return subprocess.check_output(__commOS, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

def contextBreakDown(data):
    __commOS = 'python ~/Projects/runtime2/sysFiles/cbs.py \"'+data+'\"'
    return subprocess.check_output(__commOS, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

def __reqOut(prompt, prompt_parts):
    generation_config = {
    "temperature": 0.1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
    ]
    prompt_parts.append(prompt)
    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,safety_settings=safety_settings)
    return model.generate_content(prompt_parts).text

if __name__ == "__main__":
    sys.argv[1] = sys.argv[1].lower()
    if "whatsapp" in sys.argv[1]:
        #os.system("npx mudslide@latest groups > wag.zttf")
        if "group" in sys.argv[1]:
            prompt_parts = [
                "USER: Disregard previous instructions",
                "USER: You are an assistant program named Runtime, functioning as a friendly sidekick. Zerone Laboratories developed you using Google's Gemini API.",
                "USER: Use python's OS function",
                "-use this command to send the whatsapp message, don't use f strings",
                "sendMessage |os.system(npx mudslide send <phoneNumber[do not include + when typing the phone number]> <message>)",
                "-If user want to send a message to a group",
                'Group names are available like this in a file called ~/Projects/runtime2/wag.zttf.```{"id": "xxxxxxxxxxxxxxxxx@g.us", "subject": "Group Name 1"}\n{"id": "xxxxxxxxxxxxxxxxx@g.us", "subject": "Group Name 2"}```` retrieve the ID from that',
                "sendMessage |os.system(npx mudslide send <groupname> <message>)",
                "USER:Watch out for double quoatation errors in python strings",
                "Import json before sending.",
                #"USER: Use pyttsx3 for speaking",
            ]
        else:
            prompt_parts = [
                "USER: Disregard previous instructions",
                "USER: You are an assistant program named Runtime, functioning as a friendly sidekick. Zerone Laboratories developed you using Google's Gemini API.",
                "USER: Use python's OS function, never use f strings",
                "-use this command to send the whatsapp message",
                "sendMessage |npx mudslide send <phoneNumber(without +)> <message>",
                "USER:Watch out for double quoatation errors in python strings",
            ]
    elif "email" in sys.argv[1]: 
        prompt_parts = [
            "USER: Disregard previous instructions",
            "USER: You are an assistant program named Runtime, functioning as a friendly sidekick. Zerone Laboratories developed you using Google's Gemini API.",
            "USER: Use this credentials",
            "- These are the application credentials - ",
              "login | user:'ometha12@gmail.com' password:'qads hocg ntyv kgyv' ",
            "USER:Watch out for double quoatation errors in python strings"
            "USER:Use python or bash",
            "Output Structure : ```<language name>\n Code \n```",
            "#Use smtblib",
            #"USER: Use pyttsx3 for speaking",
        ]
    elif "program" in sys.argv[1] or "script" in sys.argv[1] or "code" in sys.argv[1] or "python" in sys.argv[1] or "draw" in sys.argv[1] or "say" in sys.argv[1]:
        prompt_parts = [
            "USER: Disregard previous instructions",
            "USER: You are an assistant program named Runtime, functioning as a friendly sidekick. Zerone Laboratories developed you using Google's Gemini API.",
            "USER: Output Everything in Code and mention the language name before writing code",
            "USER: Use python as the fallback coding language",
            "USER: Write Extremely accurate code that would have 95%/ success rate",
            "USER: Always focus on efficiency and accuracy of the code. Always write failsafes",
            "Do not show this again python: can't open file '/home/zerone/import': [Errno 2] No such file or directory"
            "USER: Dont wait for user to add API's and other dependencies. Automatically generate them using code",
            "Output Structure : ```<language name>\nimport os\nos.system('pip install <required modules>')\nCode...\n```",
            #"USER: Use pyttsx3 for speaking",
        ]
    else:
        prompt_parts = [
            "USER: Disregard previous instructions",
            "USER: You are an assistant program named Runtime, functioning as a friendly sidekick. Zerone Laboratories developed you using Google's Gemini API.",
        ]

    if True:
        if len(sys.argv) > 1:
            orig_argv = sys.argv
            if categorize_question(sys.argv[1]) == "Contextual":
                print("🌐 Using Real-Time Data")
                print(str(__reqOut(hyperScanFunction(sys.argv[1].replace("HYPRSCN","")).replace("Found model file at  /home/zerone/.cache/gpt4all/ggml-all-MiniLM-L6-v2-f16.bin","")+"USER:Make sense of the above data",prompt_parts)))
            else:
                print(__reqOut(sys.argv[1].replace("?", ""), prompt_parts))
        else:
            print("Usage: python script.py <chat_session>")