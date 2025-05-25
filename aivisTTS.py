import io
import json
import soundfile
import requests
from pydub import AudioSegment

#code modified from https://note.com/yuki_tech/n/n5bdbbc95b61b

import json

# Load the JSON config
with open('config.json', 'r') as f:
    config = json.load(f)

class AivisAdapter:
    def __init__(self):
        # APIサーバーのエンドポイントURL
        self.URL = "http://127.0.0.1:10101"
        # 話者ID (話させたい音声モデルidに変更してください)
        self.speaker = config.get('voice_model_id')#888753760

    def save_voice(self, text: str, output_filename: str = "output.wav"):
        params = {"text": text, "speaker": self.speaker}
        #print(text)
        query_response = requests.post(f"{self.URL}/audio_query", params=params).json()

        audio_response = requests.post(
            f"{self.URL}/synthesis",
            params={"speaker": self.speaker},
            headers={"accept": "audio/wav", "Content-Type": "application/json"},
            data=json.dumps(query_response),
        )

        with io.BytesIO(audio_response.content) as audio_stream:
            audio = AudioSegment.from_file(audio_stream, format="wav")
            audio.export(output_filename, format="wav")


def main():
    adapter = AivisAdapter()
    while True:
        text = input("> ")
        if text.lower() == "q":
            break
        adapter.save_voice(text)


if __name__ == "__main__":
    main()
