import requests

import json

import time

import os

from datetime import datetime



headers = {"User-Agent": "TrendPulse/1.0"}

CATEGORIES = {"technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],

       "worldnews": ['war', 'government', 'country', 'president', 'election', 'climate', 'attack', 'global'],

       "sports": ['NFL', 'NBA', 'FIFA', 'sport', 'game', 'team', 'player', 'league', 'championship'],

       "science": ['research', 'study', 'space', 'physics', 'biology', 'discovery', 'NASA', 'genome'],

       "entertainment": ['movie', 'film', 'music', 'Netflix', 'game', 'book', 'show', 'award', 'streaming']

       }

def get_category(title):

 title = title.lower()

 for category,keywords in CATEGORIES.items():

  for word in keywords:

   if word in title:

    return category

 return None

def fetch_data():

 url = "https://hacker-news.firebaseio.com/v0/topstories.json"

 ids = requests.get(url, headers = headers).json()[:500]

 collected = []

 category_count = {cat: 0 for cat in CATEGORIES}

 for story_id in ids:

  try:

   res = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", headers = headers)

   data = res.json()

   if not data or 'title' not in data:

    continue

   category = get_category(data['title'])

   if category and category_count[category]<25:

    story = {

      "post_id": data.get('id'),

      'title': data.get('title'),

      'category': category,

      'score': data.get('score', 0),

      'num_comments' : data.get('descendants', 0),

      'author' : data.get('by'),

      'url' : data.get('url'),

      'timestamp' : data.get('time'),

      'collected_at' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    }

    collected.append(story)

    category_count[category]+= 1

   if all(v>=25 for v in category_count.values()):

    break

  except Exception as e:

   print(f"error fetching {story_id}:{e}")

 return collected



def save_json(data):

 os.makedirs("data", exist_ok = True)

 file_name = f"data/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.json"

 with open(file_name, "w") as f:

  json.dump(data, f, indent = 4)

 print(f"collected {len(data)}stories.svaed to{file_name} ")

if __name__ == "__main__":

 data = fetch_data()

 save_json(data)

