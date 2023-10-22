from huggingsound import SpeechRecognitionModel
from huggingsound.speech_recognition.decoder import Decoder, GreedyDecoder
from huggingsound.utils import get_chunks, get_waveforms, get_dataset_from_dict_list

from tqdm import tqdm
from typing import Optional
import numpy as np
import torch
import time


class Model(SpeechRecognitionModel):
    def transcribe(self, paths: list[str], batch_size: Optional[int] = 1, decoder: Optional[Decoder] = None) -> list[dict]:
        """ 
        Transcribe audio files.

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
        print(sampling_rate)
        result = []

        for paths_batch in tqdm(list(get_chunks(paths, batch_size))):

            waveforms = get_waveforms(paths_batch, sampling_rate)
            print("numpy array shape")
            print([w.shape for w in waveforms])

            inputs = self.processor(waveforms, sampling_rate=sampling_rate, return_tensors="pt", padding=True, do_normalize=True)
            print("torch tensor shape")
            print([t.shape for t in inputs.input_values])

            with torch.no_grad():
                if hasattr(inputs, "attention_mask"):
                    logits = self.model(inputs.input_values.to(self.device),attention_mask=inputs.attention_mask.to(self.device)).logits
                else:
                    logits = self.model(inputs.input_values.to(self.device)).logits

            result += decoder(logits)

        return result 

model = Model("wbbbbb/wav2vec2-large-chinese-zh-cn")
audio_paths = ["C:\\Users\\sheye\\repos\ReLaiF\\s2.wav", "C:\\Users\\sheye\\repos\ReLaiF\\s5.m4a"]
tik = time.perf_counter()
transcriptions = model.transcribe(audio_paths)
print(time.perf_counter() - tik)
print(transcriptions)