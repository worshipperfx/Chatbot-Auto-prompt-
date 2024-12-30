# modules we will need for different purposes in the software
import requests  # this is to send request using API to the chatbot to be able communication between the chatbot and the software
import json  # JSON module to store our information such as user prompts acts as a light version database
import time  # this gets the current time to be used in the software if there are tasks with fixed certain time
import schedule  # this allows the software to schedule tasks at specific times
import sys
import re

class API_key_manager:
    def __init__(self):
        self.api_key = None
        self.config_file = "config.json"
        self.load_api_key()  # Load the API key on initialization

    def load_api_key(self):
        try:
            with open(self.config_file) as config_file:
                config = json.load(config_file)
                self.api_key = config.get("api_key")
                if self.api_key:
                    print("API key loaded successfully")
                else:
                    print("API key not found. Please enter it.")
        except FileNotFoundError:
            print("Configuration file not found. Please enter your API key.")

    def request_api_key(self):
        api_key = input("Please input your API key to connect with the bot: ")
        permission = input("Do you want to store this API key in this application? (yes/no): ")
        
        if permission.lower() == "yes":
            config_dict = {"api_key": api_key}
            with open(self.config_file, "w") as config_file:
                json.dump(config_dict, config_file)
                print("API key saved successfully.")
        else:
            print("API key will not be saved; you will need to enter it manually each time.")
        
        self.api_key = api_key  # Update the stored API key
        return self.api_key  # Return the API key

class Chatbot:
    def __init__(self, name="Chatgpt", api_key_manager=None):
        self.name = name
        self.api_key_manager = api_key_manager if api_key_manager else API_key_manager()
        if not self.api_key_manager.api_key:
            self.api_key_manager.request_api_key()

    def send_prompt(self, prompt, file=None): 
        api_key = self.api_key_manager.api_key or self.api_key_manager.request_api_key()

        # Correct API endpoint for chat models like gpt-3.5-turbo
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Ensure proper structure of the data with the messages parameter
        data = {
            "model": "gpt-3.5-turbo",  # or "gpt-4" if you want to use that model
            "messages": [{"role": "user", "content": prompt}]  # Ensure this structure is correct
        }

        if file:
            print(f"Sending request with {file} to {self.name}.")
        else:
            print(f"Sending request to {self.name}: {prompt}")

        try:
            # Send POST request to the correct API endpoint
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                # Return the response from the model
                return result['choices'][0]['message']['content']
            else:
                print(f"Response failed with status code {response.status_code}")
                print(f"Response: {response.text}")
                return None
            
        except Exception as e:
            print(f"An error occurred: {e}")


class Task:
    def __init__(self, prompt, is_simple=True):
        self.prompt = prompt
        self.is_simple = is_simple

    def run(self, chatbot):
        print(f"Running task: {self.prompt}")
        response = chatbot.send_prompt(self.prompt)
        print(f"Response from chatbot model: {response}")

class Task_Scheduler:
    def __init__(self):
        self.tasks = []  # Set self.tasks as an empty list to store scheduled tasks

    def validate_time_format(self, time_str):
        pattern_re = r"^(?:[01]\d|2[0-3]):(?:[0-5]\d)$"
        return re.match(pattern_re, time_str) is not None

    def add_tasks(self, task, time_str, chatbot):  # Added chatbot as a parameter
        print(f"Task '{task.prompt}' scheduled at {time_str}.")
        schedule.every().day.at(time_str).do(task.run, chatbot=chatbot)  # Pass the chatbot instance here
        self.tasks.append(task)  # To add each task to the list

    def run_pending(self):
        while True:  # This checks the scheduled tasks by the user and runs them when their time comes
            schedule.run_pending()
            time.sleep(60)  # Pause for 60 seconds before checking again

class Prompt_Manager:
    def __init__(self, file_name = 'prompts.json'):
        self.file_name = file_name
        self.prompts = self.load_prompts()

    def load_prompts(self):
        try:
            with open(self.file_name,"r") as file:
                return json.load(file)
        except(FileNotFoundError, json.JSONDecodeError):
            return {"simple" : [], "interactive" : []}

    def save_prompt(self,prompt, is_simple ):
        category = "simple" if  is_simple  else "interactive"
        self.prompts[category].append(prompt)
        self.save_prompts()

    def save_prompts(self):
        with open(self.file_name, "w" ) as file:
            json.dump(self.prompts, file, indent = 4)

    def get_prompts(self, is_simple = True):
        category = "simple" if is_simple else "interactive"
        return self.prompts.get(category, [])

class User_Interaction:
    def __init__(self):
        self.chatbot = None
        self.api_key_manager = API_key_manager()  # Create one instance of API_key_manager
        self.schedule = Task_Scheduler()  # To allow access of the Task_Scheduler class

    def choose_chatbot(self):
        print("Please choose the chatbot you want to connect with:")
        print("1. ChatGPT")
        print("2. Bard")
        print("3. Custom (Enter your own)")

        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":
            self.chatbot = Chatbot(name="Chatgpt", api_key_manager=self.api_key_manager)
        elif choice == "2":
            self.chatbot = Chatbot(name="Gemini", api_key_manager=self.api_key_manager)
        elif choice == "3":
            custom_bot = input("Enter your custom bot name: ")
            self.chatbot = Chatbot(name=custom_bot, api_key_manager=self.api_key_manager)
        else:
            print("Invalid choice. Assigning default bot Chatgpt.")
            self.chatbot = Chatbot(name="Chatgpt", api_key_manager=self.api_key_manager)

        print(f"Connecting to {self.chatbot.name}")
        if not self.api_key_manager.api_key:
         self.api_key_manager.request_api_key()

    def choose_task_type(self):
        while True:
            user_saved_prompts = input("Would you like to use saved prompts?(yes/no)").lower()
            if user_saved_prompts == "yes":
                prompt_manager = Prompt_Manager()
                is_simple_choice = input("Do you want a simple or interactive task?(simple/interactive)").lower()
                if is_simple_choice == "simple":
                    saved_prompts = prompt_manager.get_prompts(is_simple = True)
                else:
                    saved_prompts = prompt_manager.get_prompts(is_simple= False)
                if not saved_prompts:
                    print("No saved prompts available")
                    continue
                print("Your saved prompts: ")
                for idx ,prompt in enumerate(saved_prompts, 1):
                    print(f"{idx} {prompt}")

                selected_prompt = int(input("Please select the number of the prompt that you want to use: "))
                if selected_prompt >= 1 and selected_prompt < len(saved_prompts):
                    self.choose_chatbot()
                    self.api_key_manager.request_api_key()
                    task = Task(saved_prompts[selected_prompt-1], is_simple=(is_simple_choice == "simple"))
                    task.run(self.chatbot)
                    sys.exit("Response ended")   
                else:
                    print("Invalid Range exceeded")
                    continue
            else:
                self.choose_chatbot()

            print("1. Simple or automated task")
            print("2. Complex task with file upload and direct connecting to chatbot")

            choice = input("Choose one of the following options above: ")

            if choice == "1":
                self.simple_task()
                break
            elif choice == "2":
                self.handle_interactive_task()
                break
            else:
                print("Invalid choice, please try again.")

    def simple_task(self):
        user_prompt = input("Enter the prompt you would like to automate: ")
        prompt_manager = Prompt_Manager()
        prompt_manager.save_prompt(user_prompt, is_simple= True)
        task = Task(user_prompt)
        task.run(self.chatbot)  # Run the task immediately

        schedule_choice = input("Would you like to schedule this task (yes/no)? ").lower()
        if schedule_choice == "yes":
            try:
                time_str = input("Enter the schedule time in HH:MM format (24hr): ")
                self.schedule.add_tasks(task, time_str, self.chatbot)  # Pass chatbot as an argument
            except ValueError:
                print("Invalid timestamp")
        else:
            sys.exit("Time scheduling terminated")


    def handle_interactive_task(self):
        user_prompt = input("Enter your prompt: ")
        prompt_manager = Prompt_Manager()
        prompt_manager.save_prompt(user_prompt, is_simple= False)
        file_upload = input("Would you like to upload a file? (yes/no): ").lower()

        if file_upload == "yes":
            file_name = input("Enter file name: ")
            response = self.chatbot.send_prompt(user_prompt, file=file_name)
        else:
            response = self.chatbot.send_prompt(user_prompt)

        print(f"Response from {self.chatbot.name}: {response}")

    def run_scheduler(self):
        self.schedule.run_pending()

if __name__ == "__main__":
    ui = User_Interaction()
    ui.choose_task_type()
    ui.run_scheduler()