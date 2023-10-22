import requests
import winsound
import io

"""
online generator: https://genshinvoice.top/v2/
video demo: https://www.bilibili.com/video/BV1hp4y1K78E/
github repo (only for training): https://github.com/fishaudio/Bert-VITS2
"""

URL_TEMPLATE = "https://genshinvoice.top/api?speaker={}&text={}&format=wav&length=1&noise=0.5&noisew=0.9&sdp_ratio=0.2"

class VoicePlayer:
    def __init__(self, speaker: str) -> None:
        self.speaker = speaker
        
    def request_and_play(self, text: str):
        text = text.split("\n")[0]  # cut off long paragraph
        text = text.replace(" ", "")
        blocks = text.split("。")
        for block in blocks:
            print(block)
            url = URL_TEMPLATE.format(self.speaker, block)
            response = requests.get(url)
            if response.status_code == 200:
                winsound.PlaySound(response.content, winsound.SND_MEMORY)

            

