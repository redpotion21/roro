from aivisTTS import AivisAdapter
from pydub import AudioSegment
from pydub.playback import play
import pygame
import shutil
from utils.furigana import toFurigana
import re

class IOmaster():
    def __init__(self, config):
        self.TTS_enabled = config.get("TTS_enabled")
        self.Furigana_enabled = config.get("Furigana_enabled")
        if self.TTS_enabled == "True":
            self.TTS_enabled = True
        else:
            self.TTS_enabled = False
        if self.Furigana_enabled == "True":
            self.Furigana_enabled = True
        else:
            self.Furigana_enabled = False
        if self.TTS_enabled:
            self.adapter = AivisAdapter()
            pygame.mixer.init()
            self.counter = 0  
        
    def out(self, sentence):
        if self.Furigana_enabled ==True:
            furi = toFurigana(sentence)
            print(furi)
        if  self.TTS_enabled:
            parts = re.split(r'([。！？])', sentence)
            trash = 0
            tmp = ''
            phrases = []
            for i in parts:
                if trash == 0:
                    tmp+=i
                    trash+=1
                else:
                    trash = 0
                    tmp+=i
                    phrases.append(tmp)
                    tmp = ''
            for phrase in phrases:
                self.adapter.save_voice(phrase)
                namae = "dialougue//output" + str(self.counter) + ".wav"
                shutil.copy("output.wav", namae)
                self.counter+=1
                while pygame.mixer.music.get_busy():#wait if there is already sound playing
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.load(namae)
                pygame.mixer.music.play()
        