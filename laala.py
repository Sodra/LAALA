import openai
from transformers import GPT2TokenizerFast
from colorama import init, Fore, Back, Style
from typing import List
import sys
init()




if "boring" in sys.argv:
    with open('boring_mode.txt', 'r') as file:
        system_desu = file.read().strip()
if "big" in sys.argv:
    with open('big_text.txt', 'r') as file:
        system_desu = file.read().strip()
else:
    with open('laala_prompt.txt', 'r') as file:
        system_desu = file.read().strip()

#def debugMode(history_token_size : int) -> None:
#    if "debug" in sys.argv:
#        print("")
#        print("The current context size is: ", history_token_size)

# Message History Class
# Contains Message History for gpt context

#class historyTokenManager:
#    def __init__(self):

class MessageHistoryStore:
    def __init__(self):
        self.message_history = []

    #INPUT: "USER" "HELLO"
    #OUTPUT: [{"role": "USER", "content": "HELLO"}, 1]
    def entryFormatter(self, prompt, messageSide):
        self.dictionaryCreator = {"role": messageSide, "content": prompt}
        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        self.tokenList = tokenizer(prompt)
        self.tokenCount = len(self.tokenList[0])
        print('Current tokenCount: ', self.tokenCount)
        #TODO: Straight up, just countToken(prompt) and add to the tuple. ezpz
        self.tupleToEntry = (self.dictionaryCreator, self.tokenCount)
        return self.tupleToEntry

    def newEntry(self, prompt, messageSide):
        addThisThingToHistory = self.entryFormatter(prompt, messageSide)
        self.message_history.append(addThisThingToHistory)

    def formattedHistoryForAPI(self):
        self.historyDictionariesOnly = [item[0] for item in self.message_history]
        return self.historyDictionariesOnly

    def sendRequestToAPI(self):
        self.messagesToSend = self.formattedHistoryForAPI()
        self.rawAPIResponse = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
        		messages = self.messagesToSend
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

