"""https://flothesof.github.io/pyqt-microphone-fft-application.html"""

# class taken from the SciPy 2015 Vispy talk opening example 
# see https://github.com/vispy/vispy/pull/928
import pyaudio
import threading
import atexit
import numpy as np
from collections import deque
import time

class MicrophoneRecorder(object):
    def __init__(self, volume_thresh, silence_thresh_sec, listen_period_ms, rate=4000, chunksize=1024):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.bit_width = 'int16'  # should be aligned with pyaudio.paInt16
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()  # to protect frames
        # self.stop = False  # control whether the recorder is on or off
        self.frames = deque(maxlen=self.rate*10)
        atexit.register(self.close)
        
        self.volume_thresh = volume_thresh
        self.silence_thresh_num = silence_thresh_sec * 1000 // listen_period_ms
        self.silence_num = 0
        self.output_frames = []
        self.is_recording = False
        
    def close(self):
        # with self.lock:
        #     self.stop = True
        self.stream.close()
        self.p.terminate()

    ### methods to write frames
    def new_frame(self, data, frame_count, time_info, status):
        # Note that data is for input and frame_count is for output.
        data = np.fromstring(data, self.bit_width)
        with self.lock:
            self.frames.extend(data)
            # if self.stop:
            #     return None, pyaudio.paComplete
        return None, pyaudio.paContinue
    
    def start(self):
        self.stream.start_stream()
    
    ### methods to output frames
    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = deque(maxlen=self.rate*10)  # clear frames
            return frames
        
    def listen(self):
        """ collect audio frames and judge if continuing to process"""        
        # gets the latest frames        
        frames = self.get_frames()
        frames = np.asarray(frames, dtype=np.float64)
        # print(frames.shape)
        
        if len(frames) > 0:
            volumne =  np.sqrt(np.mean(frames**2))
            print("time:\t", time.time(),"volume:\t", volumne)
            if self.is_recording:
                if volumne < self.volume_thresh:
                    self.silence_num += 1
                    if self.silence_num > self.silence_thresh_num:
                        self.is_recording = False
                        output = self.output_frames
                        self.output_frames = []
                        output = np.asarray(output)
                        print("output frames shape:", output.shape)
                        return output
                else:
                    self.output_frames.extend(frames)
            else:
                if volumne > self.volume_thresh:
                    self.is_recording = True
                    self.silence_num = 0
                    self.output_frames.extend(frames)
                    
        return None