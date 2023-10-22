from huggingsound import SpeechRecognitionModel
from huggingsound.speech_recognition.decoder import Decoder, GreedyDecoder
from huggingsound.utils import get_chunks, get_waveforms, get_dataset_from_dict_list

from tqdm import tqdm
from typing import Optional
import numpy as np
import torch

MODEL_NAME = "wbbbbb/wav2vec2-large-chinese-zh-cn"

class Wav2Vec2(SpeechRecognitionModel):
    def __init__(self) -> None:
        super().__init__(MODEL_NAME)
        
        
    @property
    def sampling_rate(self):
        return self.processor.feature_extractor.sampling_rate
        
    
    def regonize_once(self, audio_arrays: list[np.ndarray]):
        print("voice recognization started")
        print("audio arrays shape are:", [a.shape for a in audio_arrays])
        transcriptions = self.transcribe(audio_arrays)
        print("voice regonization result:")
        print(transcriptions)
        print("voice recognization finished")
        return transcriptions[0]["transcription"]
    
    
    def transcribe(self, audio_arrays: list[str], batch_size: Optional[int] = 1, decoder: Optional[Decoder] = None) -> list[dict]:
        """ 
        override transcribe to pass audio numpy arrays instead of paths.

        Parameters:
        ----------
            paths: list[str]
                List of paths to audio files to transcribe

            batch_size: Optional[int] = 1
                Batch size to use for inference

            decoder: Optional[Decoder] = None
                Decoder to use for transcription. If you don't specify this, the engine will use the GreedyDecoder.

        Returns:
        ----------
            list[dict]:
                A list of dictionaries containing the transcription for each audio file:

                [{
                    "transcription": str,
                    "start_timesteps": list[int],
                    "end_timesteps": list[int],
                    "probabilities": list[float]
                }, ...]
        """

        if not self.is_finetuned:
            raise ValueError("Not fine-tuned model! Please, fine-tune the model first.")
        
        if decoder is None:
            decoder = GreedyDecoder(self.token_set)

        sampling_rate = self.processor.feature_extractor.sampling_rate
        print("processor sampling rate is:", sampling_rate)
        result = []

        for audio_arrays_batch in tqdm(list(get_chunks(audio_arrays, batch_size))):

            waveforms = audio_arrays_batch
            print("numpy array shape is:")
            print(w.shape for w in waveforms)

            inputs = self.processor(waveforms, sampling_rate=sampling_rate, return_tensors="pt", padding=True, do_normalize=True)
            print("torch tensor shape is:")
            print(t.shape for t in inputs.input_values)

            with torch.no_grad():
                if hasattr(inputs, "attention_mask"):
                    logits = self.model(inputs.input_values.to(self.device),attention_mask=inputs.attention_mask.to(self.device)).logits
                else:
                    logits = self.model(inputs.input_values.to(self.device)).logits

            result += decoder(logits)

        return result 
