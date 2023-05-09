import langchain, os, re, sys, ftfy, textwrap

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
guildIDsToListen = [483363452023472139] #main server
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

def split_string_for_multiple_discord_messages(text):
    chunks = textwrap.wrap(text, 1800, replace_whitespace=False)
    return chunks

##############################################################
class modelIO:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(laala_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
            SystemMessagePromptTemplate.from_template("Respond as LAALA")
        ])

        self.channelMemories = {}
        self.llm = ChatOpenAI(temperature=1.15)
        self.memory = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1024, return_messages=True)
        self.conversation = ConversationChain(
            prompt=self.prompt,
            llm=self.llm, 
            verbose=True, 
            memory=self.memory
        )

    def makeMemoryForAllChannels(self, bingle):
        #print(bingle)
        #make memory for each channel by assigning a memory for each channel
        self.memory2 = {}
        for channel in bingle:
            self.memory2[channel.id] = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1024, return_messages=True)
        self.channelMemories = self.memory2
        #return memory
        #i have to split something here but i dont know
        #list into dic i think
        #and then that has individual ConversationTokenBufferMemory
        #then you need to pass in the what channel is this thing
    
    def remove_shim_from_history_before_sending(self):
         #replace the messagesPlaceholder in the chat prompt template?
         pass
    
    def remove_labels(self, rawLaalaResponse):
        #Removes laala: at the beginning, for shim use
        self.label = r'(?i)\blaala\b:'
        self.label2 = r'(?i)\bresponse\b:'
        self.cleanedLaalaResponse = re.sub(self.label, '', rawLaalaResponse)
        self.cleanedLaalaResponse2 = re.sub(self.label2, '', self.cleanedLaalaResponse)
        return self.cleanedLaalaResponse2
    
    #def remove_labels(self, rawLaalaResponse):
    #    return rawLaalaResponse

    def predictPerChannel(self, currentMessage, channelid):
        if channelid not in self.channelMemories:
            self.channelMemories[channelid] = ConversationTokenBufferMemory(llm=self.llm, max_token_limit=1024, return_messages=True)
        if(self.channelMemories[channelid]):    
            self.conversation = ConversationChain(
                prompt=self.prompt,
                llm=self.llm, 
                verbose=True, 
                memory=self.channelMemories[channelid]
            )

        return self.conversation.predict(input=currentMessage)
            

    def sendToModel(self, username, messagecontent, channelid):
        #Send to remove_label cleaner to remove laala: at the beginning
        cleanedMessageContent = self.remove_labels(messagecontent)

        #Send to the model directly
        self.currentMessage = f"{username}: {cleanedMessageContent}"
        return self.predictPerChannel(self.currentMessage, channelid)
    
    def addToHistory(self, username, messagecontext, channelid):
        self.currentMessage = f"{username}: {messagecontext}"
        self.channelMemories[channelid].chat_memory.add_user_message(self.currentMessage)
    
aipart = modelIO()
print("sup")

##############################################################
##############################################################
##############################################################

def split_string_for_multiple_discord_messages(text):
    chunks = textwrap.wrap(text, 1800, replace_whitespace=False)
    return chunks

async def long_ass_message(message, big_message):
    split_discord_messages = split_string_for_multiple_discord_messages(big_message)
    for chunks in split_discord_messages:
        await message.channel.send(ftfy.fix_text(chunks))

async def long_ass_message_reply(message, big_message):
    split_discord_messages = split_string_for_multiple_discord_messages(big_message)
    for chunks in split_discord_messages:
        await message.reply(ftfy.fix_text(chunks))

@bot.event
async def on_message(message):

    if message.author.id == bot.user.id \
            or message.guild.id not in guildIDsToListen \
            or not (message.channel.id in channelIDsToListen or ALL_CHANNELS or isinstance(message.channel, discord.Thread)):
        return
    #isinstance(ctx.channel, discord.Thread)
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
    if message.reference:
        repliedMessage = await message.channel.fetch_message(message.reference.message_id)
        if repliedMessage.author.id == bot.user.id:
            #If message is a reply to laala
            await message.channel.typing()
            laalaResponse = aipart.sendToModel(message.author.display_name, message.content, message.channel.id)
            #await message.reply(ftfy.fix_text(laalaResponse))
            await long_ass_message_reply(message, laalaResponse)
            return

    #If "laala" is found in the message content
    if re.search(pattern, message.content):
        await message.channel.typing()
        laalaResponse = aipart.sendToModel(message.author.display_name, message.content, message.channel.id)
        #await message.reply(ftfy.fix_text(laalaResponse))
        await long_ass_message_reply(message, laalaResponse)
        return
    else:
        aipart.addToHistory(message.author.display_name, message.content, message.channel.id)

@bot.event
async def on_ready():
    #bingle = bot.get_channel(1071518668896346162)
    #await bingle.send("**## LAALA ONLINE c: ##**")

    #Sends all channels in the 
    text_channel_list = []
    selected_guild = bot.get_guild(guildIDsToListen[0])
    for channel in selected_guild.text_channels:
        text_channel_list.append(channel)
    aipart.makeMemoryForAllChannels(text_channel_list)
    #await bot.change_presence(activity=discord.Game(name="## LAALA ONLINE c: ##"))

bot.run(discord_bot_key)

#!laalaoff
#!laalarestart
#!*
