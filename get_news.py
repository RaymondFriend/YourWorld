keyword = "tech"

import requests

def get_news_articles(api_key, query, language='en', page_size=10):
    url = f'https://newsapi.org/v2/everything'
    params = {
        'apiKey': api_key,
        'q': query,
        'language': language,
        'pageSize': page_size
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json()['articles']
        return articles
    else:
        print(f"Failed to fetch articles. Error: {response.status_code}")
        return []

# Replace 'YOUR_API_KEY' with your actual API key from NewsAPI
api_key = "e2f29d109cf04ff987e713b82d7539c8"

# Example usage: searching for articles related to the keyword
articles = get_news_articles(api_key, keyword)
for article in articles:
    print(article['title'], "-", article['url'])