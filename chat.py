# Following this tutorial: https://www.youtube.com/watch?v=7jMIsmwocpM

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

# user_input_ids = None
# bot_input_ids = None
# chat_history_ids = None

# def main(): 
#     input = "I need you to give me one word to look up about today's news. What is that one word?"
#     output = get_response(input)
#     print(output)
#     intput = "Can you make sure that the first letter is capitalized in your previous respose?"
#     output = get_response(output)
#     print(output)

# def get_response(input):
#     global user_input_ids, bot_input_ids, chat_history_ids

#     # encode the new user input, add the eos_token and return a tensor in Pytorch
#     user_input_ids = tokenizer.encode(str(input) + tokenizer.eos_token, return_tensors='pt')
    
#     # append the new user input tokens to the chat history
#     if(chat_history_ids is not None):
#         bot_input_ids = torch.cat([chat_history_ids, user_input_ids], dim=-1)
#     else:
#         bot_input_ids = user_input_ids
#     # generated a response while limiting the total chat history to 1000 tokens, 
#     chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
#     # last output tokens from the bot
#     return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)


# if __name__ == "__main__":
#     main()


# Tutorial on having a chat in the command line
# # Let's chat for 5 lines
for step in range(5):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(input(">> User:") + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # pretty print last ouput tokens from bot
    print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
