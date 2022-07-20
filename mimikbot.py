#Start command: python3 mimikbot.py

import discord, generator

client = discord.Client()

marker_list = {}
default_marker = '$'
message_limit = 50

say_command = 'say '
generate = 'gen'
generate_old = 'oldGen'
change_marker = 'changeCommandMarker '

g = generator.generator("smalldictionary.txt")

@client.event
async def on_guild_join(guild):
    marker_list[guild] = default_marker

async def update_status():
    game = discord.Game("$mimikbothelp")
    await client.change_presence(status=discord.Status.online, activity=game)    

async def get_marker(guild):
    return marker_list[guild]

@client.event
async def on_ready():
    for guild in client.guilds:
        marker_list[guild] = default_marker
    print('We have logged in as {0.user}'.format(client))
    await update_status()

@client.event
async def on_message(message):

    marker = await get_marker(message.guild)

    if message.author == client.user:
        return

    if message.content.startswith(marker + 'hello'):
        await message.channel.send('Hello!')

    if message.content.startswith(marker + say_command):
        if len(message.content) > len(say_command):
            await message.channel.send(message.content[len(say_command):])
    
    if message.content.startswith("$mimikbothelp"):
        await message.channel.send(marker + say_command + "[message]: MimikBot will say [message]. \n"
            + marker + generate + ": MimikBot will generate one message based on the previous " + str(message_limit) + " messages in the channel. \n"
            + marker + generate + " n: MimikBot will generate n messages based on the previous " + str(message_limit) + " messages in the channel. \n"
            + marker + change_marker + "[new command marker]: MimikBot will only respond to messages starting with [new command marker] "
                + "instead of " + marker + ". \n"
            + "$mimikbothelp: Displays this help message. Note that the $ command marker does NOT change using the " + change_marker + "command.")

    #Output error message to channel if user uses call incorrectly
    if message.content.startswith(marker + generate):
        g.reset_grammar()
        async for m in message.channel.history(limit=message_limit):
            if not m.content.startswith(marker) and m.author != client.user:
                g.addMessage(m.content)
        try:
            n = min(int(message.content.replace(marker+generate, '').strip()), 10)
        except ValueError:
            n = 1
        for _ in range(n):
            await message.channel.send(str(g.generate("~SENTENCE")))

    '''if message.content.startswith(marker + generate_old):
        g.reset_grammar()
        async for m in message.channel.history(limit=message_limit):
            if not m.content.startswith(marker) and m.author != client.user:
                g.addMessage(m.content, False)
        await message.channel.send(str(g.generate("~STRUCTURE")))'''

    if message.content.startswith(marker + change_marker):
        marker_list[message.guild] = message.content.replace(marker+change_marker, '')
        await message.channel.send('Changed marker to: ' + marker_list[message.guild])
        await update_status()
        
bot_token = 'redacted'
client.run(bot_token)
