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

        # ML Random Hero & Role Picker (1 Squad)
        if message.content.lower().startswith('!sh squad '):
            try:
                player_number = int(message.content[len('!sh squad '):])
                mymessage = await message.channel.send('Yang main react message ku yuk!')
                await mymessage.add_reaction('\U0001F44D')
            except:
                await message.channel.send('Salah format euy, kasih angka la')
                return
            players = []
            while(len(players) != player_number):
                input = await client.wait_for('raw_reaction_add')
                if (input.message_id == mymessage.id and str(input.emoji) == '👍'):
                    players.append('<@'+str(input.member.id)+'>')
            result = mlpicker.getrandomsquad(players)
            response = ''
            for res in result: response += f'{res.id} main {res.hero} jadi {res.role}\n'
            await message.channel.send(response+'goodluck kalian! \U0001F60A')

client.run(env.TOKEN())