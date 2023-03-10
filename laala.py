import openai
from transformers import GPT2TokenizerFast
from colorama import init, Fore, Back, Style
from typing import List
import sys
init()



#tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# Message History Class
# Contains Message History for gpt context



class MessageHistoryStore:
    def __init__(self):
        self.message_history = []

    #INPUT: "USER" "HELLO"
    #OUTPUT: [{"role": "USER", "content": "HELLO"}, 1]
    def entryFormatter(self, prompt, messageSide):
        self.dictionaryCreator = {"role": messageSide, "content": prompt}
        self.tupleToEntry = (self.dictionaryCreator, 1)
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
        		messages = self.messagesToSend,
        		temperature = 1
            )
        ###Response
        self.AI_Response = self.rawAPIResponse.choices[0].message
        self.newEntry(self.AI_Response, "assistant")
        return self.AI_Response

    def getResponse(self):
        self.AI_message = self.sendRequestToAPI()
        return self.AI_message

    def sendRequest(self, prompt):
        self.newEntry(prompt, "user")
        self.getResponse()

with open('api.key', 'r') as file:
    priTicket = file.read().strip()
openai.api_key = str(priTicket)

def inputYourPrompt() -> str:
    prompt = input(Fore.CYAN + "You: ")
    return prompt



print("## LAALA ONLINE c: ##\n")

MessageHistoryStore = MessageHistoryStore()
MessageHistoryStore.newEntry("bingle", "user")
MessageHistoryStore.sendRequest("bingle")
print("########")
print(MessageHistoryStore.getResponse())
