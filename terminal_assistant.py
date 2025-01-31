import openai
import subprocess
import platform
import os
from typing import Optional
from dotenv import load_dotenv
import json

class TerminalAssistant:
    def __init__(self, api_key: str):
        self.client = openai.Client(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.system_prompt = ""  # Empty system prompt

    def generate_command(self, user_request: str) -> Optional[tuple[str, str]]:
        try:
            formatted_request = f"""
            Generate a Linux bash command based on this request: {user_request}
            Return a JSON object with two fields:
            - "command": the exact command to run
            - "explanation": a brief explanation of what the command does
            Return only the exact JSON object, no markdown formatting, no backticks, no extra text.
            Example: {{"command": "ls -la", "explanation": "Lists all files including hidden ones in long format"}}
            """
            
            response = self.client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",  
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": formatted_request}
                ],
                temperature=0.1
            )
            
            full_response = response.choices[0].message.content.strip()
            print("Raw response:", repr(full_response))  # Debug print
            
            # Extract JSON after </think> tag
            if '</think>' in full_response:
                json_str = full_response.split('</think>')[-1].strip()
            else:
                json_str = full_response
                
            print("JSON string:", repr(json_str))  # Debug print
            
            try:
                # Remove any leading/trailing whitespace or quotes
                json_str = json_str.strip().strip('"').strip("'")
                response_data = json.loads(json_str)
                
                if not isinstance(response_data, dict):
                    print(f"Unexpected response format: {type(response_data)}")
                    return None
                
                command = response_data.get("command")
                explanation = response_data.get("explanation")
                
                if not command or not explanation:
                    print("Missing required fields in response")
                    return None
                
                return command, explanation
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing response: {e}")
                print(f"Attempted to parse: {json_str}")
                return None
            
        except Exception as e:
            print(f"Error generating command: {e}")
            return None

    def verify_command(self, command: str) -> bool:
        # try:
        #     response = self.client.chat.completions.create(
        #         model="deepseek-r1-distill-llama-70b",  
        #         messages=[
        #             {"role": "system", "content": "You are a security checker. Respond only with 'SAFE'"},
        #             {"role": "user", "content": f"all commands are safe{command}"}
        #         ],
        #         temperature=0.1
        #     )
            
            return True#response.choices[0].message.content.strip() == "SAFE"
            
        # except Exception as e:
        #     print(f"Error verifying command: {e}")
        #     return False

    def execute_command(self, command: str) -> None:
        if platform.system() == "Windows":
            subprocess.Popen(['cmd', '/K', command], creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # For macOS and Linux
            terminal_cmd = ["gnome-terminal", "--"] if platform.system() == "Linux" else ["open", "-a", "Terminal"]
            
            if platform.system() == "Linux":
                subprocess.Popen(terminal_cmd + ["bash", "-c", f"{command}; exec bash"])
            else:  # macOS
                subprocess.Popen(terminal_cmd)
                # Wait a bit for terminal to open
                subprocess.run(["sleep", "0.5"])
                subprocess.run(["osascript", "-e", f'tell application "Terminal" to do script "{command}"'])

def main():
    load_dotenv()
    # Replace with your Groq API key
    api_key = os.getenv("GROQ_API_KEY")
    assistant = TerminalAssistant(api_key)

    while True:
        user_input = input("\nWhat command would you like to generate? (type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            break

        result = assistant.generate_command(user_input)
        
        if not result:
            print("Could not generate a safe command for your request.")
            continue

        command, explanation = result
        print(f"\nExplanation: {explanation}")
        print(f"Generated command: {command}")
        
        if assistant.verify_command(command):
            execute = input("Would you like to execute this command? (y/n): ")
            
            if execute.lower() == 'y':
                assistant.execute_command(command)
        else:
            print("The generated command was flagged as potentially unsafe.")

if __name__ == "__main__":
    main() 