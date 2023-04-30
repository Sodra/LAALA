import langchain, os, re, sys

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

channelIDsToListen = [1071518668896346162] #bingle channel
guildIDsToListen = [274453805792362507] #dank emojis
adminRoleIDsToListen = [483366907777384460, 483366907777384461] #consul
adminUserIDsToisten = [237773697811742720] #soda

pattern = r'[Ll][Aa][Ll][Aa]'

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



##############################################################
##############################################################
##############################################################

class modelIO:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("STRICTLY FOLLOW THE FIRST MESSAGE"),
            HumanMessagePromptTemplate.from_template(laala_prompt),
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
print("sup")



@bot.event
async def on_message(message):

    #If the message isn't sent by laala
    if message.author.id != bot.user.id:

        #If allowed in the server scope
        if message.guild.id in guildIDsToListen:

            #If allowed in the channel scope
            if message.channel.id in channelIDsToListen:

                #If admin role is found in user who sent message
                try:
                    roles = [role.id for role in message.author.roles]
                    if any(role_id in adminRoleIDsToListen for role_id in roles):

                        #If laalaoff found in message, shut the bot down
                        if "!laalaoff" in message.content:
                            await message.channel.send("seeya, nerds~")
                            sys.exit()

                except AttributeError:
                    print("Probably clyde detected")
                
                #If message is a reply
                if message.reference:
                    repliedMessage = await message.channel.fetch_message(message.reference.message_id)
                    
                    #If message is a reply to laala
                    if repliedMessage.author.id == bot.user.id:
                        await message.reply("wow dat me")
                    
                #If "laala" is found in the message content
                if re.search(pattern, message.content):
                    await message.channel.typing()
                    f"{message.author.display_name}: {message.content}"
                    modelIO.sendToModel()
                    await message.reply(input)

@bot.event
async def on_ready():
    bingle = bot.get_channel(1071518668896346162)
    await bingle.send("**## LAALA ONLINE c: ##***")
    #await bot.change_presence(activity=discord.Game(name="## LAALA ONLINE c: ##"))



bot.run(discord_bot_key)

#!laalaoff
#!laalarestart
#!*