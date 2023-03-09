# LAALA
 Loud Advanced AI Learning Assistant

LAALA is your personal AI assistant.

Runs on GPT-3.5-Turbo.

---
LAALA: In Python, you can create a class using the `class` keyword followed by the name of the class. Here is an example of a basic class:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
```

In this example, we've created a `Person` class with two attributes (`name` and `age`) and one method (`say_hello`). The `__init__` method sets the initial values of the `name` and `age` attributes, and the `say_hello` method prints out a greeting using these attributes.

To create an instance of the `Person` class, we can do the following:

```python
person1 = Person("Alice", 30)
```

This creates a new `Person` object with `name` set to "Alice" and `age` set to 30. We can then call the `say_hello` method on this object:

```python
person1.say_hello()
```

This will output:

```
Hello, my name is Alice and I am 30 years old.
```

You: so say i wanted to initialize it with ```message_history =[({"role": "user", "content": system_desu}, system_desu_count)]``` in the __init__

LAALA: Sure, you can add the `message_history` attribute to the `__init__` method like this:

```python
class Chatbot:
    def __init__(self, system_desu):
        self.system_desu = system_desu
        self.message_history = [({"role": "user", "content": system_desu}, 1)]

    def greet_customer(self):
        print("Hi there! How can I assist you today?")
```

In this example, we've added the `message_history` attribute to the `__init__` method and initialized it with a list containing a single tuple. The tuple contains a dictionary with a `'role'` key set to `'user'`, a `'content'` key set to `system_desu`, and the value of `system_desu_count = 1`.

Note that if you want to access the `system_desu` attribute from other methods in the class, you will need to save it as an instance attribute as we have done here with `self.system_desu`.

You: how do i objectname = Chatbot(bingle). how do i bingle

LAALA: If you want to initialize an instance of the `Chatbot` class with `self.system_desu` attribute set to a variable `bingle`, you can do so like this:

```python
bingle = 'hello world'
chatbot_obj = Chatbot(bingle)
```

Here, we've created a variable named `bingle` and set it to the string `'hello world'`. We then create an instance of the `Chatbot` class and set the `system_desu` attribute to the value of `bingle` by passing it as an argument to the `Chatbot` constructor.

Now, you can use the `chatbot_obj` instance to access the `message_history` attribute and call the methods defined in the `Chatbot` class, like this:

```python
print(chatbot_obj.system_desu)  # Output: 'hello world'
chatbot_obj.greet_customer()   # Output: 'Hi there! How can I assist you today?'
```

This will output the value of the `system_desu` attribute and a greeting message from the chatbot.

You: got a list[tuple(dictionary, int), tuple(dictionary, int)], how do I iterace through and grab the dictionaryies inside

LAALA: To iterate through the list of tuples and extract the dictionaries inside each tuple, you can use a for loop with tuple unpacking. Here's an example:

```python
message_history = [
    ({"role": "user", "content": "Hello"}, 1),
    ({"role": "bot", "content": "Hi there!"}, 1),
    ({"role": "user", "content": "How can I help you?"}, 2)
]

for message, count in message_history:
    print(message)
```

In this example, we have a list `message_history` with tuples containing a dictionary and an integer count. We use a for loop to iterate through each tuple, and we unpack each tuple so that we can access the dictionary and count separately. We then print out each dictionary using the `print` function.

This will output:

```text
{'role': 'user', 'content': 'Hello'}
{'role': 'bot', 'content': 'Hi there!'}
{'role': 'user', 'content': 'How can I help you?'}
```

You can modify the code inside the for loop to access the values inside the dictionaries in the way that you need.

You: for message, count? is that in order? do the first one (message) would always be the first in the tuple index?

LAALA: Yes, that's correct! When we use tuple unpacking like `for message, count in message_history`, Python automatically assigns the first item in each tuple to the `message` variable, and the second item to the `count` variable. This means that `message` will always refer to the dictionary inside the tuple, and `count` will always refer to the integer count inside the tuple.

And yes, the order of the items in the tuple matters. In this case, the dictionary is the first item in the tuple and the count is the second item. This means that when we use tuple unpacking, the first variable (`message`) gets assigned to the first item in the tuple, and the second variable (`count`) gets assigned to the second item in the tuple. So `message` will always refer to the dictionary and `count` will always refer to the count integer in each tuple.

---

```class MessageHistory:
	def __init__():
		#list[tuple(dictionary, int)]
		self.message_history =[({"role": "user", "content": system_desu}, system_desu_count)]
		
	#Add new message to history
		#create tuple containing (dictionary, token count of "content")
	
	#return 
	
	
	
	
#list{tuple(dictionary, int)}

#list
{
	tuple(dictionary, int),
	tuple(dictionary, int),
	tuple(dictionary, int),
	tuple(dictionary, int),
	tuple(dictionary, int)
}

for message, count in message_history:
	listOfMessageDictionarys.append(message)```
