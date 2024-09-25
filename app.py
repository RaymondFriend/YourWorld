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

from secret_api_stuff.api_keys import get_news_api
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key=get_news_api())

# Define your endpoint to receive search queries
@app.route('/search', methods=['POST'])
def search_articles():
    search_query = request.json.get('searchQuery')

    # Call your Python function/module here using the search_query
    # Fetch articles from the NewsAPI or perform required operations
    articles = all_articles = newsapi.get_everything(q=search_query,
                                    #   sources='',
                                    #   domains='',
                                      from_param='2023-12-30',
                                      to='2024-01-28',
                                      language='en',
                                      sort_by='relevancy')["articles"]

    return jsonify({'articles': articles})  # Return the fetched articles as JSON

from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

### TASK CLASSIFIER
task_classifier = pipeline("zero-shot-classification")
task_candidate_labels = ['conversational task', 'summarization task', 'translation task', 'analyzing sentiment task']
# call like task_classifier(input, candidate_labels=task_candidate_labels)

### SENTIMENT-ANALYSIS CLASSIFIER
#   identify the model 
sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
#   instantiate the model
sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
#   instantiate the tokenizer for this model
sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
#   combine into a classifier
sentiment_classifier = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)
# call like sentiment_classifier(input)[0]['label']

### TRANSLATION
#   identify the model
translator_model_name = 't5-small'
#   instantiate the tokenizer for this model
translator_tokenizer = AutoTokenizer.from_pretrained(translator_model_name)
#   translator
translator = pipeline("translation", model=translator_model_name, tokenizer=translator_tokenizer)
# call like translator(input)[0]['translation_text']
# translation_XX_to_YY

### SUMMARIZER
#   identify the model 
summarization_model_name = "Falconsai/text_summarization"
#   instantiate the tokenizer for this model
summarization_tokenizer = AutoTokenizer.from_pretrained(summarization_model_name)
#   combine into a classifier
summarizer = pipeline("summarization", model=summarization_model_name, tokenizer=summarization_tokenizer)
# call like sentiment_classifier(input)[0]['summary_text']

# Define your endpoint to receive AI response queries
@app.route('/AI_response', methods=['POST'])
def AI_respond():
    input = request.json.get('input')
    # Step 1: decide which task this is
    task_switcher = {
        'conversational task': 'conversational',
        'summarization task' : 'summarization',
        'translation task': 'translation',
        'analyzing sentiment task': 'sentiment-analysis'
    }
    task_class = task_classifier(input, candidate_labels=task_candidate_labels)['labels'][0]
    print(f"I believe this is a {task_class} request")
    task = task_switcher[task_class]
    print(f"I'm going to use the {task} model for this")

    # Step 2: apply the appropriate model
    if(task == 'sentiment-analysis'):
        res = sentiment_classifier(input)[0]
        percent = f"{res['score']:.0%}"
        output = f"I believe hat text to be {res['label'].lower()} with confidence rating of {percent}"
    elif(task == "conversational"):
        output = "I can converse about that..."
    elif(task == "summarization"):
        output = "Sure, here is a summary of that: " + summarizer(input, max_length=30, min_length=10, do_sample=False)[0]['summary_text']
    elif(task == "translation"):
        output = "Here is my translation: " + translator(input)[0]['translation_text']

    print(f"the output is {output}")
    # Step 3: return the decoded output from whichever task's model was used
    return jsonify({'output': output}) 

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
