# AI Terminal Assistant

A Python application that converts natural language into terminal commands using Groq's LLM API. Simply describe what you want to do, and the assistant will generate and execute the appropriate command.

## Features

- Convert natural language to terminal commands
- Get explanations of what each command does
- Execute commands in a new terminal window
- Cross-platform support (Linux, macOS, Windows)
- Powered by Groq's DeepSeek model

## Setup

1. Install dependencies:

bash
pip install openai python-dotenv

2. Get a Groq API key from [console.groq.com](https://console.groq.com)

3. Create a `.env` file:

```bash
GROQ_API_KEY=your_api_key_here
```

## Usage

Run the assistant:
```bash
python terminal_assistant.py
```

Example:
```
What command would you like to generate? show all running processes

Explanation: Lists all running processes with detailed information
Generated command: ps aux

Would you like to execute this command? (y/n): 
```

## How It Works

1. Your request is sent to Groq's LLM API
2. The model generates a command and explanation
3. You can review both before execution
4. If approved, the command runs in a new terminal window

## Requirements

- Python 3.6+
- OpenAI Python package (for Groq API compatibility)
- python-dotenv
- A Groq API key

## Security

- Commands execute in a new terminal window
- You must approve each command before execution
- API key is stored securely in `.env`

