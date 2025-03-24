import torch
import pandas as pd
from datetime import datetime, timedelta
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scrape_data import ScrapeFireant, VnIndexScraper

class VnindexScore:
    def generate_vnindex_score(self):
        start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        df = VnIndexScraper().get_vnindex(start_date, end_date)
        
        df['time'] = pd.to_datetime(df['time'])
        df = df.sort_values('time', ascending=False, ignore_index=True)
        df = df[df['time'].dt.weekday < 5]  # Loại bỏ dữ liệu thứ 7, chủ nhật
        
        df['change'] = df['close'].diff(-1)
        
        change = df['change'][0]
        if change > 0:
            vnindex_score = (change / 7.8) * 1  # Mỗi 7.8 điểm tăng -> +1 điểm
        elif change < 0:
            vnindex_score = (change / 7.8) * 2.2  # Mỗi 7.8 điểm giảm -> x2.2
        return vnindex_score

class SentimentScore:
    def __init__(self, model_name="wonrax/phobert-base-vietnamese-sentiment"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    
    def generate_sentiment_score(self):       
        text = ScrapeFireant().scrape()
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        scores = torch.nn.functional.softmax(outputs.logits, dim=-1).detach().numpy()[0]
        
        sentiment_score = scores[1] * 4
        return sentiment_score
