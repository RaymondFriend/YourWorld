import openai

# Replace 'YOUR_API_KEY' with your actual API key from OpenAI
api_key = 'YOUR_API_KEY'
openai.api_key = api_key

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

# Example usage:
# user_input = "Can you summarize the news article?"
# assistant_response = chat_with_gpt(user_input)
# print(assistant_response)