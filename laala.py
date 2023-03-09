import openai
from colorama import init, Fore, Back, Style
init()

def historizer(just_put_every_request_in_here_whatever):
    with open('chat.log', 'a') as file:
        file.write(str(just_put_every_request_in_here_whatever) + "\n")

with open('api.key', 'r') as file:
    priTicket = file.read().strip()
openai.api_key = str(priTicket)

with open('laala_prompt.txt', 'r') as file:
    system_desu = file.read().strip()

chatHistory = []

print("## LAALA ONLINE c: ##\n")

messages = [
                {"role": "user", "content": system_desu},
            ]

firstMessage = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages=messages
    )
print(Fore.LIGHTRED_EX + "LAALA: Beep Boop~ LAALA Here~ " + firstMessage.choices[0].message.content.lstrip('\n') + Style.RESET_ALL)

firstMessage.choices[0].message.content = "Beep Boop~ LAALA Here~ " + firstMessage.choices[0].message.content

while True:
    # Send the prompt to the OpenAI API
    print("")
    prompt = input(Fore.CYAN + "You: ")
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
		messages=messages
    )
    
    rawMessage = completion.choices[0]
    messages.append(rawMessage.message)
    message = rawMessage.message.content.lstrip('\n')
    print("")
    print(Fore.LIGHTRED_EX + "LAALA: " + message + Style.RESET_ALL)
    
# rawMessage.message
""" {
  "content": "Beep Boop~ LAALA Here~",
  "role": "assistant"
}
"""