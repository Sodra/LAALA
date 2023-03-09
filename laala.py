import openai
from transformers import GPT2TokenizerFast
from colorama import init, Fore, Back, Style
init()

max_context_size = 2048
max_response_size = 300
max_history_size = max_context_size - max_response_size


tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# count tokens of message content
def count_tokens(payload):
    tokend = tokenizer.encode(payload)
    num_tokens = len(tokend)
    return num_tokens

# strip token count from history tuple, return api responses only
def strip_count(message_history : tuple) -> list:
    stripped_history = [i[0] for i in message_history]
    return stripped_history

# pop messages exceeding the user-defined history context size
def pop_history(history_token_size):
    while history_token_size > max_history_size:
        history_token_size -= message_history[0][1]
        message_history.pop(0)
    return history_token_size

with open('api.key', 'r') as file:
    priTicket = file.read().strip()
openai.api_key = str(priTicket)

with open('laala_prompt.txt', 'r') as file:
    system_desu = file.read().strip()
    system_desu_count = count_tokens(system_desu)

#initialPrompt = r"Introduce yourself at first with 'Beep Boop~ LAALA Here~', Do not re-introduce yourself afterwards."
#{"role": "user", "content": initialPrompt}

#PINK = '\033[38;5;218m'

chatHistory = []

print("## LAALA ONLINE c: ##\n")

# TODO: Separate the initial system_desu prompt from the regular history so it doesn't get removed once context limit is hit
message_history = [
                ({"role": "user", "content": system_desu}, system_desu_count),
            ]

messages = strip_count(message_history)

history_token_size = sum(t[1] for t in message_history)

firstMessage = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages = strip_count(message_history)
    )
print(Fore.LIGHTRED_EX + "LAALA: Beep Boop~ LAALA Here~ " + firstMessage.choices[0].message.content.lstrip('\n') + Style.RESET_ALL)

firstMessage.choices[0].message.content = "Beep Boop~ LAALA Here~ " + firstMessage.choices[0].message.content

while True:
    # Send the prompt to the OpenAI API
    print("")
    prompt = input(Fore.CYAN + "You: ")
    prompt_tokens = count_tokens(prompt)
    message_history.append(tuple([{"role": "user", "content": prompt}, prompt_tokens]))
    history_token_size += prompt_tokens
    history_token_size = pop_history(history_token_size)
    messages = strip_count(message_history)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages = messages
    )
    
    rawMessage = completion.choices[0]
    message = rawMessage.message.content.lstrip('\n')
    message_tokens = count_tokens(message)
    history_token_size += message_tokens
    message_history.append(tuple([rawMessage.message, message_tokens]))
    print("")
    print(Fore.LIGHTRED_EX + "LAALA: " + message + Style.RESET_ALL)
    print("")
    print("The current context size is: ", history_token_size)
    
# rawMessage.message
""" {
  "content": "Beep Boop~ LAALA Here~",
  "role": "assistant"
}
"""