from ollama import chat
import json
from utils import IOMaster

with open('config.json', 'r') as f:
    config = json.load(f)

model = config.get('ollama_model')#models[1]
#code from https://medium.com/@jonigl/using-ollama-with-python-a-simple-guide-0752369e1e55

#emoji filtering needed.
with open(config.get('persona_filename'), 'r', encoding='utf-8') as file: # put your own desired personality for persona.txt file
    persona = file.read()
with open(config.get('instruction_filename'), 'r', encoding='utf-8') as file:
    out_format = file.read()
system_prompt = persona + '\n\n' +out_format
IOMasta = IOMaster.IOmaster(config)

# Initialize an empty message history
messages = []
while True:
    user_input = input('Chat : ')
    if user_input.lower() == 'exit':
        break
    # Get streaming response while maintaining conversation history
    response_content = ""
    for chunk in chat(
        model,
        messages=messages + [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input},
        ],
        stream=True
    ):
        if chunk.message:
            response_chunk = chunk.message.content
            #print(response_chunk, end='', flush=True)
            response_content += response_chunk
    # Add the exchange to the conversation history
    IOMasta.out(response_content)
    messages += [
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': response_content},
    ]
    print('\n')  # Add space after response