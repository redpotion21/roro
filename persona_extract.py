from ollama import chat
#import json
#from utils import toFurigana
#from aivisTTS import AivisAdapter
#from pydub import AudioSegment
#from pydub.playback import play
#import pygame
#import shutil

#code from https://medium.com/@jonigl/using-ollama-with-python-a-simple-guide-0752369e1e55

#emoji filtering needed.
with open('persona//sample.txt', 'r', encoding='utf-8') as file:
    sample = file.read()
with open('instruction3.txt', 'r', encoding='utf-8') as file:
    instruction = file.read()

system_prompt = sample + instruction
#print(system_prompt)
#pygame.mixer.init()
#dialougue_counter = 0

# Initialize an empty message history
messages = []
Go = True
while Go:
    user_input = input('Chat : ')
    if user_input.lower() == 'exit':
        break
    # Get streaming response while maintaining conversation history
    response_content = ""
    for chunk in chat(
        'phi4',
        messages=messages + [
            {'role': 'user', 'content': system_prompt},
        ],
        stream=True
    ):
        if chunk.message:
            response_chunk = chunk.message.content
            print(response_chunk, end='', flush=True)
            response_content += response_chunk
    # Add the exchange to the conversation history
    #response_content_json = json.loads(response_content[8:len(response_content)-4])
    #japanese_text = response_content_json["Japanese"]
    #english_text = response_content_json["English"]
    #print('\n')
    #print('JP : ' + toFurigana(japanese_text))
    #print('\n')
    #print('EN : ' + english_text)
    #adapter = AivisAdapter()
    #adapter.save_voice(japanese_text)
    #voice = AudioSegment.from_wav("output.wav")
    #voice = AudioSegment.silent(duration=100) + voice
    #play(voice)
    #namae = "dialougue//output" + str(dialougue_counter) + ".wav"
    #shutil.copy("output.wav", namae)
    #dialougue_counter+=1
    #pygame.mixer.music.load(namae)
    #pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy():
    #    pygame.time.Clock().tick(10)
    print('\n')  # Add space after response
    Go = False