import openai
from transformers import GPT2TokenizerFast
from colorama import init, Fore, Back, Style
init()

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

with open('api.key', 'r') as file:
    priTicket = file.read().strip()
openai.api_key = str(priTicket)

with open('laala_prompt.txt', 'r') as file:
    system_desu = file.read().strip()

#initialPrompt = r"Introduce yourself at first with 'Beep Boop~ LAALA Here~', Do not re-introduce yourself afterwards."
#{"role": "user", "content": initialPrompt}

#PINK = '\033[38;5;218m'

chatHistory = []

print("## LAALA ONLINE c: ##\n")

message_history = [
                ({"role": "user", "content": system_desu}, 4),
            ]

messages = strip_count(message_history)

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
    messages = strip_count(message_history)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages = messages
    )
    
    rawMessage = completion.choices[0]
    message = rawMessage.message.content.lstrip('\n')
    message_tokens = count_tokens(message)
    message_history.append(tuple([rawMessage.message, message_tokens]))
    print("")
    print(Fore.LIGHTRED_EX + "LAALA: " + message + Style.RESET_ALL)
    
# rawMessage.message
""" {
  "content": "Beep Boop~ LAALA Here~",
  "role": "assistant"
}
"""