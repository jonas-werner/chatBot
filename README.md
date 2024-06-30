# chatBot
Mashup of the SDK for ChatGPT from OpenAI and Transcribe + Polly from AWS to create a way to chat with ChatGPT using voice. Originally created as a way to give my son a chatty friend which was powered by ChatGPT. Now it is set to translate English to Japanese by default but can easily be changed. 

## To do
The current version doesn't save chat state. Therefore each interaction is stand-alone. To make ChatGPT aware of previous statements it will need to be sent the entire chat history with each interaction. This is not useful for translation, which is the current default of this script, but would be desirable for other types of iteraction. Will add this feature down the line. 
