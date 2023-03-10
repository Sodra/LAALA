import openai
from transformers import GPT2TokenizerFast
from colorama import init, Fore, Back, Style
import sys
init()

max_context_size = 2048
# TODO: make response size affect API request, currently doesn't actually affect response size, only for context limit calc
max_response_size = 300
max_history_size = max_context_size - max_response_size


tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# Message History Class
# Contains Message History for gpt context
class MessageHistoryStore:
    def __init__(self):
        self.message_history = [
            ({},1),
            ({},1),
            ({},1),
            ({},1),
        ]
    
    def newUserEntry(self, prompt):
        #prompt -> {prompt}
        self.userDictionary = {"role": "user", "content": prompt}
        
        #prompt -> tokens
        self.userTokens = countTokens(prompt)
        
        #takes prompt, formats to correct ({"role": "user", "content": prompt}, 1)
        self.message_history.append(tuple(self.userDictionary, self.userTokens))
        
        
    def newRespEntry(self, responseDict):
        #responseDict is {"role": "assistant", "content": "bingle"}
        self.respTokens = countTokens(responseDict.content)
        self.message_history.append(tuple(responseDict.content, self.respTokens))
        
    def sendQuery(self, formatedListOfDicts):
    
    def recieveQuery():
    
    

start of loop
    take the prompt you want to send (initial or input)
        messageHistory = MessageHistoryStore(dictionaryContainingInitialPrompt)
        or
        messageHistory.newEntry(prompt)
            # newEntry will turn prompt --> ({prompt}, 3)
    send gpt the messageHistory
        messageHistory.sendQuery()
    ---
    recieve the response
        response = messageHistory.recieveQuery()
    add response to the messageHistory
        messageHistory.newEntry(response)
    print response
        print(response)
    
go to start

# count tokens of message content
def countTokens(payload : str) -> int:
    tokend = tokenizer.encode(payload)
    num_tokens = len(tokend)
    return num_tokens

# strip token count from history tuple, return api responses only
def stripCount(message_history : tuple) -> list:
    stripped_history = [i[0] for i in message_history]
    return stripped_history

# pop messages exceeding the user-defined history context size
def popHistory(history_token_size : int) -> int:
    while history_token_size > max_history_size:
        history_token_size -= message_history[0][1]
        message_history.pop(0)
    return history_token_size

# starts by asking for your You: input, returns the raw string of your input.
def inputYourPrompt() -> str:
    prompt = input(Fore.CYAN + "You: ")
    return prompt

# append sent or recieved message to message history
def appendHistoryToSend(message_history : list, prompt : str, prompt_tokens : int, append_type : str) -> list:
    if append_type == 'prompt':
        message_history.append(tuple([{"role": "user", "content": prompt}, prompt_tokens]))
    elif append_type == 'response':
        message_history.append(tuple([rawMessage.message, message_tokens]))
    else:
        input('Error: no valid append type selected')
    return message_history

with open('api.key', 'r') as file:
    priTicket = file.read().strip()
openai.api_key = str(priTicket)

# switches from normal mode to boring mode if "boring" argument is passed
if "boring" in sys.argv:
    with open('boring_mode.txt', 'r') as file:
        system_desu = file.read().strip()
        system_desu_count = countTokens(system_desu)
else:
    with open('laala_prompt.txt', 'r') as file:
        system_desu = file.read().strip()
        system_desu_count = countTokens(system_desu)

def debugMode(history_token_size : int) -> None:
    if "debug" in sys.argv:
        print("")
        print("The current context size is: ", history_token_size)

chatHistory = []

print("## LAALA ONLINE c: ##\n")

# TODO: Make this a proper class/object with sane returns
# TODO: Separate the initial system_desu prompt from the regular history so it doesn't get removed once context limit is hit
# I tried to make this all fancy because its types in types, but it didnt like my formatting. Will fix with class.
message_history =[(
            {"role": "user", "content": system_desu}, system_desu_count
        ),
    ]

messages = stripCount(message_history)

#4000 = sum(500,500,500,500)
history_token_size = sum(t[1] for t in message_history)

firstMessage = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages = stripCount(message_history)
    )
print(Fore.LIGHTRED_EX + "LAALA: Beep Boop~ LAALA Here~ " + firstMessage.choices[0].message.content.lstrip('\n') + Style.RESET_ALL)

firstMessage.choices[0].message.content = "Beep Boop~ LAALA Here~ " + firstMessage.choices[0].message.content

while True:
    # Send the prompt to the OpenAI API
    print("")
    prompt = inputYourPrompt()
    
    prompt_tokens = countTokens(prompt)
    
    #message_history.append(tuple([{"role": "user", "content": prompt}, prompt_tokens]))
    appendHistoryToSend(message_history, prompt, prompt_tokens, 'prompt')

    history_token_size += prompt_tokens
    history_token_size = popHistory(history_token_size)
    messages = stripCount(message_history)
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages = messages
    )
    
    rawMessage = completion.choices[0]
    message = rawMessage.message.content.lstrip('\n')
    message_tokens = countTokens(message)
    history_token_size += message_tokens
    #message_history.append(tuple([rawMessage.message, message_tokens]))
    #append_history_to_send(message_history, rawMessage.message, message_tokens)
    appendHistoryToSend(message_history, rawMessage, message_tokens, 'response')
    print("")
    print(Fore.LIGHTRED_EX + "LAALA: " + message + Style.RESET_ALL)
    
    #print("")
    #print("The current context size is: ", history_token_size)
    debugMode(history_token_size)
# rawMessage.message
""" {
  "content": "Beep Boop~ LAALA Here~",
  "role": "assistant"
}
"""
