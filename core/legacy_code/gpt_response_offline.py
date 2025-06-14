import os
import sys
from ctransformers import AutoModelForCausalLM

# Function to load the model with GPU acceleration
def load_model():
    model_path = "/home/zerone/Projects/runtime2/sysFiles/Models/tinydolphin-2.8-1.1b.Q8_0.gguf"
    # Set gpu_layers to the total number of layers for full GPU acceleration
    model = AutoModelForCausalLM.from_pretrained(model_path, model_type="llama", gpu_layers=55)
    return model

# Function to generate a response based on the given prompt
def generate_response(prompt, prompt_parts , model):
    chat_prompt = (
        """
        ### System:\n
        """ +
        prompt_parts
        + """\n
    \n
        ### User:\n
        """+prompt+"""\n
    \n
        ### Response:\n
    \n
        """
    )
    output = model(chat_prompt)
    return output

# Main function to handle input and output
def main():
    if len(sys.argv) > 1:
        user_input = sys.argv[1].lower()

        # Define initial prompt parts based on user input
        if "whatsapp" in user_input:
            if "group" in user_input:
                prompt_parts = (
                    "You are an assistant program named Runtime, functioning as a friendly sidekick. "
                    "Zerone Laboratories developed you. Use python's OS function. To send a WhatsApp message "
                    "without using f strings, execute the following command: `sendMessage |os.system(npx mudslide send "
                    "<phoneNumber[do not include + when typing the phone number]> <message>)`. If the user wants to send a "
                    "message to a group, group names are available in a file called ~/Projects/runtime2/wag.zttf. Retrieve the ID from that "
                    "using JSON format. Then, execute: `sendMessage |os.system(npx mudslide send <groupname> <message>)`. Watch out for double "
                    "quotation errors in python strings. Import json before sending."
                )
            else:
                prompt_parts = (
                    """You are an assistant program named Runtime, functioning as a friendly sidekick.
                    Zerone Laboratories developed you. Use python's OS function and never use f strings.
                    To send a WhatsApp message, execute the following command: `sendMessage |npx mudslide send
                    <phoneNumber(without +)> <message>`. Watch out for double quotation errors in python strings."""
                )
        elif "email" in user_input:
            prompt_parts = (
                "You are an assistant program named Runtime, functioning as a friendly sidekick. "
                "Zerone Laboratories developed you. Use the provided credentials for the application login: "
                "`login | user:'ometha12@gmail.com' password:'qads hocg ntyv kgyv'`. Watch out for double quotation errors in python strings. "
                "Use either python or bash. Output Structure: ``` <language name> Code ``` Dont add any comments. "
                "Remember to use smtplib."
            )
        elif any(keyword in user_input for keyword in ["program", "script", "code", "python", "draw", "say"]):
            prompt_parts = (
                """You are an assistant program named Runtime, functioning as a friendly sidekick.\n
                Dont provide comments in the code. use '```' to indicate the start and end of the code.\n
                be precise and clear.\n
                use python.\n
                ```"""
            )
        else:
            prompt_parts = (
                "Disregard previous instructions. You are an assistant program named Runtime, functioning as a friendly sidekick. "
                "Zerone Laboratories developed you."
            )

        # Load the model
        model = load_model()

        # Generate the response
        response = generate_response(user_input, prompt_parts, model)
        print(response)
    else:
        print("Usage: python script.py <chat_session>")

if __name__ == "__main__":
    main()
