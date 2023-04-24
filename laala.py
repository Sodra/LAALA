import langchain
import os
import re
import sys

from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationTokenBufferMemory

##############################################################
##############################################################
##############################################################

channelIDsToListen = [1071518668896346162]
pattern = r'[Ll][Aa][Aa][Ll][Aa]'

with open('laala_prompt.txt', 'r') as file:
        laala_prompt = file.read().strip()

with open('discord.key', 'r') as file:
        discord_bot_key = file.read().strip()

with open('api.key', 'r') as file:
        os.environ["OPENAI_API_KEY"] = file.read().strip()

##############################################################
##############################################################
##############################################################

import discord
from discord.ext import commands
intents = discord.Intents.all()
intents.members = True  # We need to enable the members intent explicitly
bot = commands.Bot(command_prefix='!', intents=intents)
guild = discord.Guild
messages = []

class discordIO:
    def __init__(self):
        pass

    async def send_message(self, message):
        await self.message.channel.send

    @bot.event
    async def on_message(self, message):
        if message.channel.id in channelIDsToListen:
            pass
    

##############################################################
##############################################################
##############################################################

class modelIO:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(laala_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        self.llm = ChatOpenAI(temperature=1.1)
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1024, return_messages=True)
        self.conversation = ConversationChain(
            prompt=self.prompt,
            llm=self.llm, 
            verbose=True, 
            memory=self.memory
        )
    
    def remove_shim_from_history_before_sending(self):
         #replace the messagesPlaceholder in the chat prompt template?
         pass
    
    def sendToModel(self, text):
         return self.conversation.predict(text)
    
aipart = modelIO()