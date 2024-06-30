# chatBot
Mashup of the SDK for ChatGPT from OpenAI and Transcribe + Polly from AWS to create a way to chat with ChatGPT using voice. Originally created as a way to give my son a chatty friend which was powered by ChatGPT. Now it is set to translate English to Japanese by default but can easily be changed. 

## How to use
Create a new virtual environment: 

`python -m venv chatBotEnv`

Activate the environment:

`source ./chatBotEnv/bin/activate`

Add your environment variables:

```
export OPENAI_API_KEY="your-openai-key"
export AWS_DEFAULT_REGION="your-aws-region"
export AWS_ACCESS_KEY_ID=your-aws-key
export AWS_SECRET_ACCESS_KEY=your-secret-aws-key
```

Clone the repo and enter the repository folder:

```cd chatBot```

Install the requirements:

`pip install -r requirements.txt`

Start the chat bot: 

```python ./startChat.py```

To exit: 

Use CTRL+C or say "terminate" and it will exit

## To do
The current version doesn't save chat state. Therefore each interaction is stand-alone. To make ChatGPT aware of previous statements it will need to be sent the entire chat history with each interaction. This is not useful for translation, which is the current default of this script, but would be desirable for other types of iteraction. Will add this feature down the line. 
