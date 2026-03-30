from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import sqlite3
import os

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

folder = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(folder, "data.db")

data = sqlite3.connect(db_path)
cur = data.cursor()

max_history = 50

class bot:
    def __init__(self, guild, channel, insert):
        self.guild = guild
        self.channel = channel
        self.users = []
        self.last_message = None
        self.is_typing = False
        self.chat_history_ids = None
        self.step = False
        if insert:
            cur.execute("INSERT INTO channels VALUES (?,?)", (guild, channel))
            data.commit()

    def generate_reply(self, user_in, reply):
        #encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(user_in + tokenizer.eos_token, return_tensors='pt')

        #append the new user input tokens to the chat history
        bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if self.step else new_user_input_ids

        if reply:

            #generated history
            self.chat_history_ids = model.generate(
            bot_input_ids, 
            max_new_tokens=20,
            do_sample=True,
            top_p=0.7,
            temperature=0.7,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
            ) 

            #last ouput tokens from bot
            message = (tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))

        #reset history if over the limit
        if self.step:
            if self.chat_history_ids.shape[-1] > max_history:
                self.chat_history_ids = self.chat_history_ids[:, -max_history:]

        
        if reply:
            self.step = True
            return message
        else: return