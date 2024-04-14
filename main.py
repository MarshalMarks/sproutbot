import nextcord
from nextcord.ext import commands
import sys, os, random, asyncio
from datetime import datetime, timedelta

# Globals/Settings
ANNOUNCEMENT_WEEKDAY = 6 # 0:Monday, 6:Sunday
CHANNEL_ID = 1178200739911307314

# Format and verify global settings
# [TODO]

def exit_program(message):
    print(f'An error occurred: {message}')
    sys.exit(0)

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

def update_database():
    file = open("prompts.txt", "w")
    for prompt in prompts:
        file.write(f'{prompt}\n')
    file.close()

# Load bot access token as variable
if not os.path.isfile('./TOKEN.txt'):
    file = open("TOKEN.txt", "w")
    file.write("[Replace this line with the bot access token]")
    file.close()
    exit_program('a token file was not found! Please open TOKEN.txt and insert the bot access token to continue.')
token = open('TOKEN.txt').readline().rstrip()
print('$ Access token successfully loaded as variable')

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
    await schedule_weekly_message()

@client.command()
async def ping(ctx):
    await ctx.send(pingMessages[random.randint(0, len(pingMessages) - 1)])

@client.command()
async def info(ctx):
    await ctx.send("My name is Sproutbot! I was created by Clay Marks (https://github.com/MarshalMarks) to automate the collection and announcement of prompts for a series of community music creation events called Sprouts, which was initially created and run by Milo Henderson (@geminiworkshops). You can find my source code at https://github.com/MarshalMarks/sproutbot. Feel free to use the \"$sprout commands\" command to get to know my functionality a bit better!")

@client.command()
async def commands(ctx):
    embed = nextcord.Embed(title="Commands")
    embed.add_field(name="$sprout ping", value="Sends a message if Sproutbot is online", inline=False)
    embed.add_field(name="$sprout info", value="Shows info about Sproutbot", inline=False)
    embed.add_field(name="$sprout commands", value="Displays this list of Sproutbot commands", inline=False)
    embed.add_field(name="$sprout add <prompt>", value="Adds a new prompt to the prompt list", inline=False)
    embed.add_field(name="$sprout list", value="Displays the current list of prompts", inline=False)
    embed.add_field(name="$sprout delete <index>", value="Deletes a prompt from the prompt list (1-indexed)", inline=False)    
    embed.add_field(name="$sprout announce", value="Announces the next prompt", inline=False)
    await ctx.send(content=None, embed=embed)

@client.command()
async def add(ctx, *, arg):
    prompts.append(arg)
    update_database()
    print(f'$ \"{arg}\" successfully added to the prompt list')
    await ctx.send(f'Added {arg} to the prompt list! :D')

@client.command()
async def list(ctx):
    if len(prompts) == 0:
        await ctx.send('The prompt list is empty :( use $sprout add <prompt> to add a prompt!')
        return
    embed = nextcord.Embed()
    output = ''
    for i, prompt in enumerate(prompts):
        output += f'{i+1}) {prompt}\n'
    embed.add_field(name='Prompts', value=output, inline=True)
    await ctx.send(content=None, embed=embed)

@client.command()
async def delete(ctx, index:int):
    if len(prompts) == 0:
        await ctx.send('There are no prompts to delete! You can add one with $sprout add <prompt>')
    elif index <= 0 or index > len(prompts):
        await ctx.send(f'That index is out of bounds! It needs to be between 1 and {len(prompts)}.')
    else:
        prompt = prompts[index-1]
        del prompts[index-1]
        update_database()
        print(f'$ Successfully deleted prompt \"{prompt}\" from index {index}')
        await ctx.send(f'Deleted prompt \"{prompt}\"  from the database!')

async def schedule_weekly_message():
    while True:
        now = datetime.now()
        print(now)
        then = now.replace(hour=0, minute=0, second=1)
        if then < now:
            then += timedelta(days=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = client.get_channel(CHANNEL_ID)

        weekday = now.strftime('%A')
        if now.weekday() == ANNOUNCEMENT_WEEKDAY and len(prompts) > 0:
            await channel.send(f'The next prompt starts today! It\'ll take place from today until next {weekday}. The prompt for this one is **\"{prompts[0]}\"**!')
            del prompts[0]
            update_database()
            await asyncio.sleep(1)

if __name__ == '__main__':
    client.run(token)