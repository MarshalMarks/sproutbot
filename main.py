import nextcord
from nextcord.ext import commands
import sys, os, random, asyncio
from datetime import datetime, timedelta

WEEKDAY_NAME = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def exit_program(message):
    print(f'An error occurred: {message}')
    sys.exit(0)

def format_weekday_array(array):
    output = []
    for number in array:
        if number >= 0 and number <= 6 and number not in output:
            output.append(number)
    output.sort()
    output.append(output[0])
    return output

def search(array, item):
    try:
        return array.index(item)
    except ValueError:
        return -1

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
    file.write("[Replace this line with the bot access token]\n")
    file.write("[Replace this line with your Sprouts Discord channel ID]\n")
    file.write("[Replace this line with the day of the week the prompt should be sent, in the form of a number from 0 to 6 (0:Monday, 6:Sunday)]")
    file.close()
    exit_program('a token file was not found! Please open TOKEN.txt and fill in the blanks to continue.')
file = open('TOKEN.txt')
token = file.readline().rstrip()
CHANNEL_ID = int(file.readline().rstrip())
weekday_array = [int(number) for number in file.readline().rstrip().split(' ')]
weekday_array = format_weekday_array(weekday_array)
print('$ Formatted weekday array loaded as ' + str(weekday_array))
ANNOUNCEMENT_WEEKDAY = weekday_array[0]
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
    prompt = arg.lower().rstrip()
    if prompt in prompts:
        await ctx.send(f'Whoops, it looks like \"{prompt}\" is already on the list!')
    else:
        prompts.append(prompt)
        update_database()
        print(f'$ \"{prompt}\" successfully added to the prompt list')
        await ctx.send(f'Added {prompt} to the prompt list! :D')

@client.command()
async def list(ctx):
    if len(prompts) == 0:
        await ctx.send('The prompt list is empty :( use $sprout add <prompt> to add a prompt!')
        return
    embed = nextcord.Embed()
    output = ''
    for i, prompt in enumerate(prompts):
        output += f'{i+1}) {prompt}\n'
    embed.add_field(name='Upcoming Prompts', value=output, inline=True)
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
        then = now.replace(hour=0, minute=0, second=1)
        if then < now:
            then += timedelta(days=1)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)

        channel = client.get_channel(CHANNEL_ID)

        next_weekday_index = search(weekday_array, now.weekday())
        if next_weekday_index != -1:
            next_weekday = weekday_array[next_weekday_index + 1]
            print(weekday_array[next_weekday_index + 1])
            if len(prompts) > 0:
                await channel.send(f'The next prompt starts today! It\'ll take place from today until next {WEEKDAY_NAME[next_weekday]}. The prompt for this one is **\"{prompts[0]}\"**!')
                print(f'$ Announced prompt \"{prompts[0]}\"')
                del prompts[0]
                update_database()
                print(f'$ Successfully deleted prompt from list')
                await asyncio.sleep(1)

if __name__ == '__main__':
    client.run(token)