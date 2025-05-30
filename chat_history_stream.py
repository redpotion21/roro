from ollama import chat
import json
#code from https://medium.com/@jonigl/using-ollama-with-python-a-simple-guide-0752369e1e55

#emoji filtering needed.

with open('persona//persona.txt', 'r', encoding='utf-8') as file: # put your own desired personality for persona.txt file
    persona = file.read()
with open('output_format.txt', 'r', encoding='utf-8') as file:
    out_format = file.read()

system_prompt = persona + out_format
print(system_prompt)

# Initialize an empty message history
messages = []
while True:
    user_input = input('Chat with history: ')
    if user_input.lower() == 'exit':
        break
    # Get streaming response while maintaining conversation history
    response_content = ""
    for chunk in chat(
        'phi4',
        messages=messages + [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input},
        ],
        stream=True
    ):
        if chunk.message:
            response_chunk = chunk.message.content
            print(response_chunk, end='', flush=True)
            response_content += response_chunk
    # Add the exchange to the conversation history
    response_content_json = json.loads(response_content[8:len(response_content)-4])
    japanese_text = response_content_json["Japanese"]
    print(japanese_text)
    messages += [
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': response_content},
    ]
    print('\n')  # Add space after response