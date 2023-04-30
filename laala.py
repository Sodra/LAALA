import langchain, os, re, sys, ftfy

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

channelIDsToListen = [1071518668896346162, 1083806446094917682] #bingle channel
guildIDsToListen = [274453805792362507, 483363452023472139] #dank emojis
adminRoleIDsToListen = [483366907777384460, 483366907777384461] #consul
adminUserIDsToisten = [237773697811742720] #soda
ALL_CHANNELS = False

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



##############################################################
##############################################################
##############################################################

class modelIO:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(laala_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
            SystemMessagePromptTemplate.from_template("Respond as LAALA")
        ])

        self.llm = ChatOpenAI(temperature=1.15)
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
    
    def remove_labels(self, rawLaalaResponse):
        #Removes laala: at the beginning, for shim use
        self.label = r'(?i)\blaala\b:'
        self.label2 = r'[Rr][Ee][Ss][Pp][Oo][Nn][Ss][Ee]: '
        self.cleanedLaalaResponse = re.sub(self.label, '', rawLaalaResponse)
        self.cleanedLaalaResponse2 = re.sub(self.label2, '', self.cleanedLaalaResponse)
        return self.cleanedLaalaResponse2
    
    #def remove_labels(self, rawLaalaResponse):
    #    return rawLaalaResponse

    def sendToModel(self, username, messagecontent):
        #Send to remove_label cleaner to remove laala: at the beginning
        cleanedMessageContent = self.remove_labels(messagecontent)

        #Send to the model directly
        self.currentMessage = f"{username}: {cleanedMessageContent}"
        return self.conversation.predict(input=self.currentMessage)
    
aipart = modelIO()
print("sup")

##############################################################
##############################################################
##############################################################

@bot.event
async def on_message(message):

    if message.author.id == bot.user.id \
            or message.guild.id not in guildIDsToListen \
            or not (message.channel.id in channelIDsToListen or ALL_CHANNELS):
        return

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
    
    #If message is a reply, and replying to laala
    if message.reference and repliedMessage.author.id == bot.user.id:
        repliedMessage = await message.channel.fetch_message(message.reference.message_id)
        
        #If message is a reply to laala
        await message.channel.typing()
        laalaResponse = aipart.sendToModel(message.author.display_name, message.content)
        await message.reply(ftfy.fix_text(laalaResponse))

    #If "laala" is found in the message content
    elif re.search(pattern, message.content):
        await message.channel.typing()
        laalaResponse = aipart.sendToModel(message.author.display_name, message.content)
        await message.reply(ftfy.fix_text(laalaResponse))

@bot.event
async def on_ready():
    bingle = bot.get_channel(1071518668896346162)
    await bingle.send("**## LAALA ONLINE c: ##***")
    #await bot.change_presence(activity=discord.Game(name="## LAALA ONLINE c: ##"))

bot.run(discord_bot_key)

#!laalaoff
#!laalarestart
#!*