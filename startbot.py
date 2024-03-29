import os
import discord
import env
from features import animescrape
from features import cartoonscrape
from features import mangascrape
from features import mlpicker
import asyncio
import requests

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
    
    if message.content.startswith('!sh'):
        # Default Response
        if message.content == '!sh':
            await message.channel.send('Ooiiii aku sekarang 24/7 online selama setahun thanks to AWS :D, function ku:\n!sh pick\n!sh squad *\*[1-5]\**\n!sh anime *\*judul\**\n!sh manga *\*judul\**\n')
    
        # ML Random Hero & Role Picker (1 Player)
        if message.content.lower().startswith('!sh pick'):
            player = mlpicker.getrandomhero(message.author.id)
            await message.channel.send(f'<@{player.id}> kamu main {player.hero} jadi {player.role} ya')

        # ML Random Hero & Role Picker (1 Squad)
        if message.content.lower().startswith('!sh squad '):
            try:
                player_number = int(message.content[len('!sh squad '):])
                if(player_number<1 or player_number>5):
                    await message.channel.send('yang betul la yang main biasa 1-5')
                    return
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

        # Nonton anime colong data dari allmanga.to
        if message.content.lower().startswith('!sh anime '):
            keyword = message.content[len('!sh anime '):]
            anime_list = animescrape.SearchAnime(keyword)
            if len(anime_list) == 0:
                await message.channel.send('Nggak nemu animenya')
                return
            output = ''
            output += 'Anime yang kutemu:\n'
            for i in range(len(anime_list)):
                output += str(i+1)+'. '+anime_list[i].title+'\n'
            await message.channel.send(output)
            await message.channel.send('Mau nonton yg mana?')
            while True:
                try:
                    input = await client.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel, timeout=30.0)
                except asyncio.TimeoutError:
                    await message.channel.send('Lama banget ditanya bknnya jwb males dah')
                    return
                else:
                    if input.content.startswith('!sh'):
                        return
                    if not input.content.isdigit():
                        await message.channel.send('Angka aja woiiii mau yg mana')
                    elif int(input.content) < 1 or int(input.content) > len(anime_list):
                        await message.channel.send('Gaada pilihan itu gmn sih')
                    else:
                        anime = anime_list[int(input.content)-1]
                        break
            await message.channel.send('Episode berapa? aku cek ada sekitar '+str(anime.episodecount)+' episode')
            while True:
                try:
                    input = await client.wait_for('message',check=lambda m: m.author == message.author and m.channel == message.channel, timeout=30.0)
                except asyncio.TimeoutError:
                    await message.channel.send('Lama banget ditanya bknnya jwb males dah')
                    return
                else:
                    if input.content.lower().startswith('!sh'):
                        return
                    if not input.content.isdigit():
                        await message.channel.send('Angka aja woiiii mau episode brp')
                    elif int(input.content) < 1 or int(input.content) > int(anime.episodecount):
                        await message.channel.send('Ga ada episode segitu')
                    else:
                        result = input.content
                        break
            episode = animescrape.GetEpisodeDetail(anime.id,result)
            if episode == 'API Error':
                await message.channel.send(f'Episode {input.content}:API returned null, ngga nemu nih di API nya')
            if episode == 'Episode not found!':
                await message.channel.send(f'Episode {input.content}: Episode not found, blm ada nih data episode nya :(')
            elif episode != None:
                output = animescrape.FormatEpisodeDetail(episode)
                await message.channel.send(output)
            return
        
        # Baca manga colong dari manga4life
        if message.content.lower().startswith('!sh manga '):
            keyword = message.content[len('!sh manga '):]
            result = mangascrape.SearchManga(keyword)
            response = ''
            if len(result) == 0:
                await message.channel.send('Nggak nemu itu')
                return
            for manga in result:
                manga.totalchapter = mangascrape.GetTotalChapter(manga.titlelink)
                response += manga.title+' ['+str(manga.totalchapter)+' Chapter]\nhttps://makusa.masuk.web.id/manga?name='+manga.titlelink+'&chapter='+str(manga.totalchapter)+'\n\n'
            await message.channel.send(response)

        # Nonton Kartun colong dari WCO
        if message.content.lower().startswith('!sh wco '):
            keyword = message.content[len('!sh wco '):]
            result = cartoonscrape.GetAllLinks(keyword)
            if(result == 'Not Link'):
                await message.channel.send('butuhnya link wco ya dari wcofun.net')
                return
            if(result == None):
                await message.channel.send('nggak nemu itu')
                return
            for v in result:
                await message.channel.send('['+v.contents[0]+'](<'+cartoonscrape.GetLink(v['href'])+'>)')

client.run(env.TOKEN())