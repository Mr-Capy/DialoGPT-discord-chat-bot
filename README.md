# DialoGPT-Discord-Chat-Bot
This project is a lightweight discord chat bot based on DialoGPT.


## Commands and Features
### /set_dialo
Sets the bot to reply to messages in the channel. You can set the bot on multiple channels and servers. Only administrators or users with mod roles can use this command.

### /remove_dialo
Cancels /set_dialo - the bot will ignore the message in the channel. Only administrators or users with mod roles can use this command.

### /set_mod_role
This command allows administrators to set what roles can use the bot's command. Only administrators can use this command.

### /remove_mod_role
Removes the permission to use the bot's command from the chosen role. Only administrators can use this command.

### Reply Chance
The bot replies to users with 80% chance divided by number of users who sent messages to the channel over the past 1 minute. If the bot does not reply, it appends message to chat history instead. This is done to prevent channels from overflooding with bot's messages.

Note: the lowest the chance can get is 10% and the bot always replies if mentioned.

You can adjust or remove this feature in the line 132: 
```python
if random.randint(1,10) <= math.ceil(8/len(bots[id].users)):
```

### Chat History
The chat history stores last 50 tokens, or 35-40 words.

You can adjust this number by changing max_history in model.py:
```python
max_history = 50
```
The chat history gets cleared if no user typed over past 2 minutes.

You can adjust this number or delete this feature in main.py in the line 107:
```python
if difTime >= 2:
    bots[id].chat_history_ids = None
    bots[id].step = False
```

### Bot's Behavior
You can adjust bot's behavior if you change values in model.py in the lines 44 - 47:
```python
do_sample=True,
top_k=50,
top_p=0.95,
temperature=0.7,
```
- **do_sample** - If False, the model always chooses the most likely token. However, this can make the responses less creative and more predictable. If True, the model uses the values below to generate response.

- **top_k** - The number of most likely tokens the model considers. The higher the values increase randomness and vice versa.

- **top_p** - The model chooses the most likely tokens that make up p% of the probability mass. The higher the values increase randomness and vice versa.

- **temperature** - Scales the randomness of the model's responses. The higher the values increase randomness and vice versa.


## Installation
### 1. Clone this repository
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
Note that you should replace requirements.txt with its path

### 3. Create database
Run create_database.py
```python
python create_database.py
```
Note that you should replace create_database.py with its path

### 4. Replace the token
Open main.py and go to the bottom of the file. There, find 'Your Token' and replace it with your bot's token.
```python
client.run('Your Token')
```

## Usage
### Run the bot
Run main.py
```bash
python main.py
```
Note that you should replace main.py with its path


## Acknowledgements

This project relies on several open-source libraries and models:

- **discord.py** – Python API wrapper for Discord.  
  https://github.com/Rapptz/discord.py

- **sqlite3** – Built-in Python library providing a lightweight SQL database engine.  
  https://docs.python.org/3/library/sqlite3.html

- **PyTorch** – Machine learning framework developed by Meta AI.  
  https://pytorch.org/

- **Transformers** – Machine learning library for natural language processing developed by Hugging Face.  
  https://github.com/huggingface/transformers

- **DialoGPT** – Conversational AI model developed by Microsoft.  
  https://github.com/microsoft/DialoGPT

These libraries and models are used under their respective open-source licenses.  
This repository does not redistribute their source code or model files unless otherwise stated.