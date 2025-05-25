from ollama import chat
import json
from utils import toFurigana
from aivisTTS import AivisAdapter
from pydub import AudioSegment
from pydub.playback import play
import pygame
import shutil

with open('config.json', 'r') as f:
    config = json.load(f)

Translate_auto = False
TTS_out = True
furigana = True
models = ['phi4',"freerainboxbox/phi4:14b-q3_K_S"]
model = config.get('ollama_model')#models[1]
#code from https://medium.com/@jonigl/using-ollama-with-python-a-simple-guide-0752369e1e55

#emoji filtering needed.
with open(config.get('persona_filename'), 'r', encoding='utf-8') as file: # put your own desired personality for persona.txt file
    persona = file.read()
with open(config.get('instruction_filename'), 'r', encoding='utf-8') as file:
    out_format = file.read()

system_prompt = persona + '\n\n' +out_format
#print(system_prompt)
pygame.mixer.init()
dialougue_counter = 0

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
    if Translate_auto:
        response_content_json = json.loads(response_content[8:len(response_content)-4])
        japanese_text = response_content_json["Japanese"]
        english_text = response_content_json["English"]
        print('\n')
        print('JP : ' + toFurigana(japanese_text))
        print('\n')
        print('EN : ' + english_text)
    else:
        japanese_text = response_content
        if furigana:
            print(toFurigana(japanese_text))
        else:
            print(japanese_text)
    if TTS_out:
        adapter = AivisAdapter()
        adapter.save_voice(japanese_text)
        #voice = AudioSegment.from_wav("output.wav")
        #voice = AudioSegment.silent(duration=100) + voice
        #play(voice)
        namae = "dialougue//output" + str(dialougue_counter) + ".wav"
        shutil.copy("output.wav", namae)
        dialougue_counter+=1
        pygame.mixer.music.load(namae)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    messages += [
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': response_content},
    ]
    print('\n')  # Add space after response