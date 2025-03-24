import json
import os
from datetime import datetime
from score_model import VnindexScore, SentimentScore

class ScoreDaily:
    def __init__(self, score_file="score_daily.json"):
        self.vnindex_score = VnindexScore()
        self.sentiment_score = SentimentScore()
        self.base_score = 50
        self.score_file = score_file

    def load_last_score(self):
        """Load the last recorded score from score_daily.json"""
        if not os.path.exists(self.score_file):
            return None
        with open(self.score_file, "r") as f:
            try:
                scores = json.load(f)
                if scores:
                    last_date = max(scores.keys())  # Lấy ngày mới nhất
                    return scores[last_date]  # Lấy score của ngày mới nhất
            except json.JSONDecodeError:
                return None
        return None

    def save_score(self, score):
        """Save the new score to score_daily.json"""
        today = datetime.today().strftime("%Y-%m-%d")
        scores = {}

        # Load existing scores
        if os.path.exists(self.score_file):
            with open(self.score_file, "r") as f:
                try:
                    scores = json.load(f)
                except json.JSONDecodeError:
                    pass  # Nếu file trống hoặc lỗi, bỏ qua

        scores[today] = score  # Ghi lại score mới

        with open(self.score_file, "w") as f:
            json.dump(scores, f, indent=4)

    def generate_score_daily(self):
        """Generate the daily score based on Vnindex and Sentiment scores"""
        vnindex_score = self.vnindex_score.generate_vnindex_score()
        sentiment_score = self.sentiment_score.generate_sentiment_score()
        last_score_daily = self.load_last_score()

        if last_score_daily is None:
            score_daily = self.base_score + vnindex_score + sentiment_score
        else:
            score_daily = last_score_daily + vnindex_score + sentiment_score

        self.save_score(score_daily)
        return score_daily
