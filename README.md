# AutoPrompt AI – Task Scheduling with ChatGPT via API

AutoPrompt AI is a lightweight automation tool that connects to ChatGPT using the OpenAI API. It allows users to input prompts directly or schedule them to be executed at a later time. The project was originally developed before OpenAI introduced its built-in scheduled task feature, and serves as an early experiment in AI-driven prompt automation.

## Features

- Connects to ChatGPT via OpenAI's API
- Offers both immediate and scheduled prompt execution
- Simple command-line interface for interaction
- Option to select from multiple chatbot labels (ChatGPT, BAT, Gemini)
- Provides prompt execution logs and feedback in the terminal

## How It Works

1. **Prompt Type Selection**  
   The user chooses between a simple automated task or a more complex task involving file uploads (the latter is not implemented in this version).

2. **Chatbot Selection**  
   The tool currently connects only to ChatGPT. Options for BAT and Gemini are included in the menu as placeholders but do not have functionality implemented.

3. **Prompt Execution**  
   - If executed immediately, the prompt is sent to ChatGPT, and the response is returned in real-time.
   - If scheduled, the user enters a time, and the tool sends the prompt at the exact specified time.

4. **Limitations on Notifications**  
   Because the tool uses an older version of the ChatGPT API, it does not support system notifications. When asked to send a notification, ChatGPT may respond with suggestions such as using Siri, Google alarms, or setting reminders manually.

## Example Use Cases

- **Immediate Prompt**:  
  _"You're a developer experiencing a performance slowdown in your application. How would you approach the problem?"_

- **Scheduled Prompt**:  
  _"Remind me to check the latest AI research papers at 21:13."_

## Project Structure

Chatbot-Auto-prompt/
├── autoprompt.py # Main application script

├── requirements.txt # Dependencies

└── README.md # Project documentation


## Limitations

- Notifications cannot be triggered due to API constraints
- Scheduled prompts run on basic time matching, not system timers
- BAT and Gemini chatbot options are not functional
- No web interface or GUI, only CLI interaction

## Background

This project was created before OpenAI introduced its own task scheduling feature in ChatGPT. Although that update made this tool less necessary in practical terms, developing it provided valuable experience in automation logic, prompt scheduling, and API integration.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Developed by [Marvellous Chitenga](https://github.com/worshipperfx)



