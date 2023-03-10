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
        self.message_history = [
            ({},1),
        ]

    #INPUT: "USER" "HELLO"
    #OUTPUT: [{"role": "USER", "content": "HELLO"}, 1]
    def entryFormatter(self, prompt, messageSide):
        self.dictionaryCreator = {"role": messageSide, "content": prompt}
        self.tupleToEntry = (self.dictionaryCreator, 1)
        return self.tupleToEntry

    def newEntry(self, prompt, messageSide):
        addThisThingToHistory = self.entryFormatter(prompt, messageSide)
        self.message_history.append(addThisThingToHistory)

    def sendHistoryToAPI(self):
        self.historyDictionariesOnly = [item[0] for item in self.message_history]
        return self.historyDictionariesOnly

with open('api.key', 'r') as file:
    priTicket = file.read().strip()
openai.api_key = str(priTicket)

def inputYourPrompt() -> str:
    prompt = input(Fore.CYAN + "You: ")
    return prompt



print("## LAALA ONLINE c: ##\n")

MessageHistoryStore = MessageHistoryStore()
MessageHistoryStore.newEntry("bingle", "user")
print(MessageHistoryStore.sendHistoryToAPI())
print("t########")
print(MessageHistoryStore.message_history)
