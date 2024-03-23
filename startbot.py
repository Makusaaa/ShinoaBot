import os
import discord
import env
import mlpicker
# from dotenv import load_dotenv
# load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user :
        return
    
    # Default Response
    if message.content.startswith('!sh'):
        if message.content == '!sh':
            await message.channel.send('Ooiiii aku sekarang 24/7 online selama setahun thanks to AWS :D ')
    
        # ML Random Hero & Role Picker (1 Player)
        if message.content.lower().startswith('!sh pick'):
            player = mlpicker.getrandomhero(message.author.id)
            await message.channel.send(f'<@{player.id}> kamu main {player.hero} jadi {player.role} ya')

client.run(env.TOKEN())