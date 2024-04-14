import nextcord
from nextcord.ext import commands
import sys
import os
import random
from datetime import datetime

def exit_program(message):
    print(f'An error occurred: {message}')
    sys.exit(0)

# Load bot access token as variable
if not os.path.isfile('./TOKEN.txt'):
    file = open("TOKEN.txt", "w")
    file.write("[Replace this line with the bot access token]")
    file.close()
    exit_program('a token file was not found! Please open TOKEN.txt and insert the bot access token to continue.')
token = open('TOKEN.txt').readline().rstrip()
print('$ Access token successfully loaded as variable')

# Load local prompt list as array
if not os.path.isfile('./prompts.txt'):
    print('$ prompt.txt not found')
    file = open("prompts.txt", "a")
    file.close()
    print('$ Successfully created an empty prompt.txt file')
else:
    print('$ prompt.txt found')
prompts = [line.rstrip() for line in open('./prompts.txt')]
print('$ List of prompts loaded into memory:')
print(f'$ {prompts}')

# Initialize Discord
intents = nextcord.Intents.all()
intents.members = True
command_prefix="$sprout "
client = commands.Bot(command_prefix, intents=intents)

pingMessages = []
pingMessages.append('I\'m up and running!')
pingMessages.append('Hello! Hope you\'re doing well.')
pingMessages.append('Sproutbot is online!')
pingMessages.append('My name is Sproutbot. Nice to meet you!')

@client.event
async def on_ready():
    print(f'$ We have logged in as {client.user.name}')

@client.command(name="ping")
async def SendMessage(ctx):
    await ctx.send(pingMessages[random.randint(0, len(pingMessages) - 1)])

@client.command(name="info")
async def SendMessage(ctx):
    await ctx.send("My name is Sproutbot! I was created by Clay Marks (https://github.com/MarshalMarks) to automate the collection and announcement of prompts for a series of community music creation events called Sprouts, which was initially created and run by Milo Henderson (@geminiworkshops). You can find my source code at https://github.com/MarshalMarks/sproutbot. Feel free to use the \"$sprout commands\" command to get to know my functionality a bit better!")

@client.command(name="commands")
async def SendMessage(ctx):
    embed = nextcord.Embed(title="Commands")
    embed.add_field(name="$sprout ping", value="Sends a message if Sproutbot is online", inline=False)
    embed.add_field(name="$sprout info", value="Shows info about Sproutbot", inline=False)
    embed.add_field(name="$sprout commands", value="Displays this list of Sproutbot commands", inline=False)
    embed.add_field(name="$sprout add <prompt>", value="Adds a new prompt to the prompt list", inline=False)
    embed.add_field(name="$sprout list", value="Displays the current list of prompts", inline=False)
    embed.add_field(name="$sprout delete <index>", value="Deletes a prompt from the prompt list (1-indexed)", inline=False)    
    embed.add_field(name="$sprout announce", value="Announces the next prompt", inline=False)
    await ctx.send(content=None, embed=embed)

if __name__ == '__main__':
    client.run(token)