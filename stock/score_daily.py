from datetime import datetime
from score_model import VnindexScore, SentimentScore
from database import save_score, get_last_score

class ScoreDaily:
    def __init__(self):
        self.vnindex_score = VnindexScore()
        self.sentiment_score = SentimentScore()
        self.base_score = 50

    def load_last_score(self):
        """Load the last recorded score from database"""
        return get_last_score()

    def save_score(self, score, vnindex_score, sentiment_score):
        """Save the new score to database"""
        save_score(score, vnindex_score, sentiment_score)

    def generate_score_daily(self):
        """Generate the daily score based on Vnindex and Sentiment scores"""
        vnindex_score = self.vnindex_score.generate_vnindex_score()
        sentiment_score = self.sentiment_score.generate_sentiment_score()
        last_score_daily = self.load_last_score()

        if last_score_daily is None:
            score_daily = self.base_score + vnindex_score + sentiment_score
        else:
            score_daily = last_score_daily + vnindex_score + sentiment_score

        self.save_score(score_daily, vnindex_score, sentiment_score)
        return score_daily
