#!/usr/bin/env python3

import openai
from colorama import init, Fore, Back, Style
from typing import List
import sys
import tiktoken
init()


#def debugMode():
#elif "debug" in sys.argv:
#    pass

if "boring" in sys.argv:
    with open('boring_mode.txt', 'r') as file:
        system_desu = file.read().strip()
    print("Boring Mode Activated")
elif "big" in sys.argv:
    with open('big_text.txt', 'r', encoding='utf-8') as file:
        system_desu = file.read().strip()
else:
    with open('laala_prompt.txt', 'r') as file:
        system_desu = file.read().strip()



    

#TODO make thie use python logging
#TODO proper name logging, will attach to discord integration
class chatLog:
    def writeToLogBeginning(self):
        with open('chat.log', 'a', encoding='utf-8') as file:
            file.write(f'##### LAALA ONLINE c: #####\n\n')
    
    def writeToLog(self, role, prompt):
        if role == "user":
            role = "You"
        elif role == "assistant":
            role = "LAALA"
        with open('chat.log', 'a', encoding='utf-8') as file:
            file.write(f'{role}: {prompt}\n\n')
    
    def __init__(self):
        self.writeToLogBeginning()

# Message History Class
# Contains Message History for gpt context
max_context_size = 4096
# response size affects API request
max_response_size = 300
#max_history_size = max_context_size - max_response_size

class tokenizerClass:
    def __init__(self):
        self.tokenModel = tiktoken.encoding_for_model('gpt-3.5-turbo')

    def tokenizer(self, prompt2):
        self.splitIntoTokens = self.tokenModel.encode(prompt2)
        #print(self.splitIntoTokens)
        return len(self.splitIntoTokens)

class historyTokenManager:
    def __init__(self):
        #print("bingle")
        #self.tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.tokenizer = tokenizerClass()
    
    def countTokens(self, prompt):
        #self.tokenList = self.tokenizer(prompt)
        #self.tokenCount = len(self.tokenList[0])
        self.tokenCount = self.tokenizer.tokenizer(prompt)
        #print('Current tokenCount: ', self.tokenCount)
        return self.tokenCount
    
    def maxTokenSize(self):
        self.maxTokenSizeNum = max_context_size
        self.maxTokenResponseSize = max_response_size
        self.maxHistorySize = self.maxTokenSizeNum - self.maxTokenResponseSize
        return self.maxHistorySize

    #def countTotalTokens(self):
    #    self.tokenHistorySum = sum()

    def currentAmountOfTokens(self, x): #this returns the number of tokens in the history right now.
        return sum(item[1] for item in x)

    def popTokens(self, message_history): #return whole message_history, with tokens popped
        #print(help(message_history))

        #self.currentAmountOfTokens = sum(item[1] for item in message_history)
        self.totalAllowedTokens = self.maxTokenSize()
        while self.currentAmountOfTokens(message_history) > self.totalAllowedTokens:
            #print("Message history is currently " + str(self.currentAmountOfTokens(message_history)) + ", popping.")
            message_history.pop(1)
        #print("Message history is currently " + str(self.currentAmountOfTokens(message_history)) + ", popping complete.")
        return message_history

#yo if you add "Answer as LAALA" to every last prompt it totally works, you can even remove it per history so it doesn't stay in context
class MessageHistoryStore:
    def __init__(self):
        self.message_history = []
        self.historyTokenManager = historyTokenManager()
        self.chatLog = chatLog()

    #INPUT: "USER" "HELLO"
    #OUTPUT: [{"role": "USER", "content": "HELLO"}, 1]
    def entryFormatter(self, prompt, messageSide):
        self.dictionaryCreator = {"role": messageSide, "content": prompt}
        self.tupleToEntry = (self.dictionaryCreator, self.historyTokenManager.countTokens(prompt))
        return self.tupleToEntry

    def newEntry(self, prompt, messageSide):
        addThisThingToHistory = self.entryFormatter(prompt, messageSide)
        self.chatLog.writeToLog(messageSide, prompt)
        self.message_history.append(addThisThingToHistory)

    def formattedHistoryForAPI(self):
        self.historyDictionariesOnly = [item[0] for item in self.message_history]
        return self.historyDictionariesOnly

    def sendRequestToAPI(self):
        #self.message_history = self.historyTokenManager.popTokens(self.message_history)
        self.historyTokenManager.popTokens(self.message_history)
        self.messagesToSend = self.formattedHistoryForAPI()
        #print("Sending this many tokens to the API: " + str(self.historyTokenManager.currentAmountOfTokens(self.message_history)))
        self.rawAPIResponse = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
        		messages = self.messagesToSend,
                max_tokens=max_response_size
            )
        ###Response
        self.AI_Response = self.rawAPIResponse.choices[0].message.content
        self.newEntry(self.AI_Response, "assistant")
        return self.AI_Response

    #####
    #send request
    #####

    def receiveResponse(self):
        self.AI_message = self.sendRequestToAPI()
        return self.AI_message

    def makeRequestToSend(self, prompt):
        self.newEntry(prompt, "user")

class LAALA_UI:
    def printLAALA(self, x):
        print(Fore.LIGHTRED_EX + "LAALA: " + x)
        print("")

    def askLAALA(self):
        self.prompt = input(Fore.CYAN + "You: ")
        print("")
        return self.prompt

    def convoLoop(self, MessageHistoryStore):
        MessageHistoryStore.makeRequestToSend(self.askLAALA())
        self.printLAALA(MessageHistoryStore.receiveResponse())
        self.convoLoop(MessageHistoryStore)

    def __init__(self, MessageHistoryStore):
        MessageHistoryStore.makeRequestToSend(system_desu)
        self.printLAALA(MessageHistoryStore.receiveResponse())
        self.convoLoop(MessageHistoryStore)


with open('api.key', 'r') as file:
    priTicket = file.read().strip()
openai.api_key = str(priTicket)

def inputYourPrompt():
    prompt = input(Fore.CYAN + "You: ")
    return prompt



print("## LAALA ONLINE c: ##\n")

MessageHistoryStore = MessageHistoryStore()
LAALA = LAALA_UI(MessageHistoryStore)


#MessageHistoryStore.newEntry("bingle", "user")
'''while True:
    thisIsYourPrompt = LAALA.askLAALA()
    print("")
    MessageHistoryStore.makeRequestToSend(thisIsYourPrompt)
    print(Fore.LIGHTRED_EX + "LAALA: " + MessageHistoryStore.receiveResponse().lstrip())
    print("")'''
#print(MessageHistoryStore.receiveResponse())
#print(MessageHistoryStore.message_history)
#print(MessageHistoryStore.receiveResponse())

