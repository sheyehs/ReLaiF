import requests
# import simpleaudio as sa
import winsound
import io

# url = "https://genshinvoice.top/api?speaker=%E8%89%BE%E4%B8%9D%E5%A6%B2&text=%E9%95%BF%E5%B4%8E%E7%B4%A0%E4%B8%96%E7%9A%84%E9%AB%98%E4%B8%AD%E7%94%9F%E6%B4%BB%E9%9D%9E%E5%B8%B8%E5%85%85%E5%AE%9E%E5%92%8C%E7%8B%AC%E7%89%B9%E3%80%82&format=wav&length=1&noise=0.5&noisew=0.9&sdp_ratio=0.2"
url = "https://genshinvoice.top/api?speaker=%E8%89%BE%E4%B8%9D%E5%A6%B2&text=%E5%8F%AA%E8%83%BD%E5%90%88%E6%88%90%E4%B8%AD%E6%96%87%E5%AD%97%E7%AC%A6%E5%92%8C%E9%83%A8%E5%88%86%E6%A0%87%E7%82%B9%E7%AC%A6%E5%8F%B7&format=wav&length=1&noise=0.5&noisew=0.9&sdp_ratio=0.2"
# data = {"eventType": "AAS_PORTAL_START", "data": {"uid": "hfe3hf45huf33545", "aid": "1", "vid": "1"}}
# params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}

response = requests.get(url)

winsound.PlaySound(response.content, winsound.SND_MEMORY)

# from pydub import AudioSegment

# sound = AudioSegment.from_raw(file=response.content, frame_rate=141100)

# play_obj = sa.play_buffer(response.content, 1, 2, 88200)
# play_obj.wait_done()
# wave = sa.WaveObject(audio_data=response.content, num_channels=1, bytes_per_sample=2, sample_rate=88200)
# control = wave.play()
# control.wait_done()

# with open("s3.wav", "wb") as f:
#     f.write(response.content)
    
# with open("s3.wav", "rb") as f:
#     play_obj = sa.play_buffer(f.read(), 1, 2, 88200)
#     play_obj.wait_done()
    
# with open("s3.wav", "rb") as f:
#     winsound.PlaySound(f.read(), winsound.SND_MEMORY)