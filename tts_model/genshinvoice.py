import requests
import winsound
import re
import logging

"""
online generator: https://genshinvoice.top/v2/
video demo: https://www.bilibili.com/video/BV1hp4y1K78E/
github repo (only for training): https://github.com/fishaudio/Bert-VITS2
"""

URL_TEMPLATE = "https://genshinvoice.top/api?speaker={}&text={}&format=wav&length={}&noise=0.5&noisew={}&sdp_ratio=0.2"

class VoicePlayer:
    def __init__(self, speaker: str, length: float, noisew: float) -> None:
        self.speaker = speaker
        self.length = str(length)
        self.noisew = str(noisew)
        
        self.punctuations = [c for c in "。？！"]
        self.punctuations_regx = "(" + "|".join([p + "+" for p in self.punctuations]) + ")"
        
    def request_and_play(self, text: str, edit):
        print("genshinvoice started.")
        
        sentences = self._separate_sentences(text)
            
        i = 0
        for s in sentences:
            print(f"sentence {i}: {s}")
            url = URL_TEMPLATE.format(self.speaker, s, self.length, self.noisew)
            print(f"sending url: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                # TODO: why sometimes will got stuck
                print("wave file received")
                if i == 0:
                    edit.clear()
                edit.appendPlainText(s)
                print("text appended.")
                try:
                    winsound.PlaySound(response.content, winsound.SND_MEMORY | winsound.SND_NODEFAULT)
                except Exception as e:
                    print(e)
                    print("one sentence was skipped")
                finally:
                    pass
            else:
                logging.warning("a request failed.")
            i += 1
            
        print("genshinvoice finished.")
        
        
    def _separate_sentences(self, text: str):
        """separate sentences if tails with punctuations."""
        text = text.replace("\n", "").replace(" ", "")
        blocks = re.split(self.punctuations_regx, text)
        new_blocks = []
        i, j = 0, 0
        while j < len(blocks):
            while j < len(blocks) and (len(blocks[j]) == 0 or blocks[j][0] in [c for c in "。？！"]):
                j += 1
            b = "".join(blocks[i:j])
            if len(b) > 0:
                new_blocks.append(b)
            i = j
            j += 1
        return new_blocks

            

