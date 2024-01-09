from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

# Handling CORS preflight requests for all routes
@app.route('/', methods=['OPTIONS'])
def handle_options_request():
    return '', 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # Adjust as needed
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

import secrets.api_keys as api_keys
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=api_keys.get_news_api())

# Define your endpoint to receive search queries
@app.route('/search', methods=['POST'])
def search_articles():
    search_query = request.json.get('searchQuery')

    # Call your Python function/module here using the search_query
    # Fetch articles from the NewsAPI or perform required operations
    articles = all_articles = newsapi.get_everything(q=search_query,
                                    #   sources='',
                                    #   domains='',
                                      from_param='2023-12-07',
                                      to='2024-01-06',
                                      language='en',
                                      sort_by='relevancy')["articles"]

    return jsonify({'articles': articles})  # Return the fetched articles as JSON

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
