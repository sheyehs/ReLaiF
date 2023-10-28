from transformers import pipeline
from enum import Enum


class Feeling(Enum):
    SAD = -1
    NORMAL = 0
    HAPPY = 1
    EXCITED = 2

class SentimentAnalyzer:
    def __init__(self) -> None:
        self.model = pipeline(
            model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
            return_all_scores=True
        )
        
    def analyze_once(self, text: str):
        print("sentiment analysis started")
        result = self.model(text)
        result = {t["label"]: t["score"] for t in result[0]}
        print("sentiment analysis result:")
        print(result)
        feeling = Feeling.NORMAL
        if result["positive"] > 0.33:
            if result["positive"] > 0.66:
                feeling = Feeling.EXCITED
            else:
                feeling = Feeling.HAPPY
        elif result["negative"] > 0.33:
            feeling = Feeling.SAD
        print("feeling chosen:", feeling)
        print("sentiment analysis finished")
        return feeling