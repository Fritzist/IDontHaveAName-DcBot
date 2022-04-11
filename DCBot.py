import asyncio
import json

import discord
from discord.abc import GuildChannel
from discord.ext import commands
import youtube_dl
import os
import random
import io
import DiscordUtils
import discord
from discord.ext import commands
import DiscordUtils



client = commands.Bot(command_prefix="$")
client.remove_command("help")

@client.event
async def on_ready():
    print('Bin endlich wieder Online, Yeah Yeah')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"$helpDE and $helpEN"),
                                 status=discord.Status.online)




        #Musik

music = DiscordUtils.Music()

@client.command()
async def join(ctx):
    voicetrue =ctx.author.voice
    if voicetrue is None:
        return await ctx.send(f"You are not currently in a voicechannel <@{ctx.message.author.id}>")
    await ctx.author.voice.channel.connect()
    await ctx.send(f"Joined your voice channel <@{ctx.message.author.id}>")

@client.command()
async def leave(ctx):
    voicetrue = ctx.author.voice
    mevoicetrue = ctx.guild.me.voice
    if voicetrue is None:
        return await ctx.send(f"You are not currently in a voicechannel <@{ctx.message.author.id}>")
    if mevoicetrue is None:
        return await ctx.send(f"I am not currently in a voicechannel <@{ctx.message.author.id}>")
    await ctx.guild.voice_client.disconnect()
    await ctx.send(f"Left your voice channel <@{ctx.message.author.id}>")

@client.command()
async def play(ctx, *, url):
    player = music.get_player(guild_id=ctx.guild.id)
    if not player:
        player = music.create_player(ctx, ffmpeg_error_betterfix=True)
    if not ctx.voice_client.is_playing():
        await player.queue(url, search=True)
        song = await player.play()
        await ctx.send(f"Now playing '{song.name}' <@{ctx.message.author.id}>")
    else:
        song = await player.queue(url, search=True)
        await ctx.send(f"{song.name} has been added to the playlist <@{ctx.message.author.id}>")


@client.command()
async def queue(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = (f"{','.join([song.name for song in player.current_queue()])}")
    embed.title = ':musical_note: Music:musical_note: '
    await ctx.send(embed=embed)



@client.command()
async def stop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.pause()
    await ctx.send(f"Paused {song.name} <@{ctx.message.author.id}>")

@client.command()
async def resume(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.resume()
    await ctx.send(f"Resumed {song.name} <@{ctx.message.author.id}>")

@client.command()
async def loop(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.toggle_song_loop()
    if song.is_looping:
        return await ctx.send(f'{song.name} is now looping <@{ctx.message.author.id}>')
    else:
        return await ctx.send(f'{song.name} is not looping <@{ctx.message.author.id}>')

@client.command()
async def nowplaying(ctx):
    player = music.get_player(guild_id=ctx.guild.id)
    song = player.now_playing()
    await ctx.send(song.name)

@client.command()
async def remove(ctx, index):
    player = music.get_player(guild_id=ctx.guild.id)
    song = await player.remove_from_queue(int(index))
    await ctx.send(f'Removed `{song.name}`` from queue <@{ctx.message.author.id}>')


@client.command()
async def bc(ctx):
    guild = ctx.message.guild
    await guild.create_text_channel('Bot-command')



                            #TTT

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def ttt(ctx, p1: discord.Member, ):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = ctx.author

        # print the board

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("<@" + str(player1.id) + "> fängt an /turn")
        elif num == 2:
            turn = player2
            await ctx.send("<@" + str(player2.id) + "> fängt an / turn")
    else:
        await ctx.send('''Es wird bereits gespielt bitte warte kurz. \n
        somebody is playing please wait''')


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " " "won the game!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")



                                #switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send('''Nutze bitte nur Zahlen von 1-9 und die noch nicht belegt sind. \n
                please use only numbers from 1-9 and wich are not used jet''')
        else:
            await ctx.send('''Du bist noch nicht dran bitte warte kurz. \n
            its not ur turn please wait.''')
    else:
        await ctx.send('''Starte bitte ein neues Spiel mit $ttt. \n
        start a new game with $ttt''')


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@ttt.error
async def ttt_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''Bitte makiere die Person mit der du spielen willst. \n
        Please tag the person you want to play with''')

    elif isinstance(error, commands.BadArgument):
        await ctx.send('''Bitte ping die Person an mit der du spielen willst. \n
        Please tag the person you want to play with''')

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''Bitte schreib die Position  wo du dein Marker hinsetzten willst. \n 
        Please write the position where ur marker should be''')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('''Bitte schreib nur 1 Zahl und ganze Zahlen. \n
        please write only 1 number and full numbers''')

                    #Münzenwurf

@client.command()
async def coinflip(ctx):
    bid = ctx.message.content.split(' ')[1]
    bid_param = -3
    if bid.lower() == "number":
        bid_param = -1
    elif bid.lower() == "head":
        bid_param = -2
    else:
        try:
            bid_param = int(bid)
        except:
            bid_param = -3
    if bid_param == -3:
        await ctx.channel.send('wrong entry')
        return
    result = random.randint(0,36)
    if bid_param == -1:
        won = result%2 == 0 and not result == 0
    elif bid_param == -2:
        won = result%2 == 1
    else:
        won = result == bid_param
    if result%2 == 0:
        diedatei = open("Head_Coin.png", "rb")
        fp = io.BytesIO(diedatei.read())
        await ctx.send(file=discord.File(fp, "Head_Coin.png"))
        diedatei.close()
    else:
        diedatei = open("140px-1_euro_coin_Eu_serie_1.png", "rb")
        fp = io.BytesIO(diedatei.read())
        await ctx.send(file=discord.File(fp, "140px-1_euro_coin_Eu_serie_1.png"))
        diedatei.close()

    #if won:
        #await ctx.channel.send('$$$You won but it was luck$$$')
    #else:
        #await ctx.channel.send('You Lost XD be better next Time')


        #await ctx.channel.send(f"You got :) <@{ctx.message.author.id}>")

                        #Roulette

@client.command()
async def roulette(ctx):
    bid = ctx.message.content.split(' ')[1]
    bid_param = -3
    if bid.lower() == "red":
        bid_param = -1
    elif bid.lower() == "black":
        bid_param = -2
    else:
        try:
            bid_param = int(bid)
        except:
            bid_param = -3
    if bid_param == -3:
        await ctx.channel.send('wrong entry')
        return
    result = random.randint(0,36)
    if bid_param == -1:
        won = result%2 == 0 and not result == 0
    elif bid_param == -2:
        won = result%2 == 1
    else:
        won = result == bid_param
    if result % 2 == 0:
        await ctx.channel.send('$$$ Du hast gewonnen!!! $$$')

    else:
        await ctx.channel.send('Leider verloren :(')



                    #Help

@client.command()
async def helpDE(ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = ('''Hier sind alle Commands die man nutzten kann wenn man Hilfe braucht \n
                        $musicHelp \n
                        $rouletteHelp \n
                        $tttHelp \n 
                        $pingHelp \n
                        $helpDE \n
                        $helpEN \n
                        $bcHelp \n
                        $coinHelp \n
                        Wenn das alles nicht gehen sollte schreibt <@488378492396765205> an ''')

    embed.title = ':loudspeaker:HelpDE:loudspeaker:'
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
async def helpEN(ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = ('''These are all commands for the bot \n
                        $musicHelp \n
                        $rouletteHelp \n
                        $tttHelp \n 
                        $pingHelp \n
                        $helpDE \n
                        $helpEN \n
                        $bcHelp \n                    
                        $coinHelp \n
                        If this don't work ask <@488378492396765205> for help''')

    embed.title = ':loudspeaker:HelpEN:loudspeaker:'
    await ctx.send(embed=embed)
    await ctx.message.delete()


@client.command()
async def musicHelp (ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description =('''Schreibe $join um den Bot in den voicechannel einzuladen. $play und dann ein Songname oder Link. $stop um den Song zu stoppen $resume um das gestoppte Lied wieder zu spielen und $queue um deine queue zu sehen.Schreibe $nowplaying um den song namen zu sehen der gerade gespielt wird, schreibe $loop um dein song in einem loop zu spielen. \n
    Write $join to invite the bot into the voicechannel. $play and then a song name or link. $stop to stop the song $resume to play the stopped song again and $queue to see your queue.Write  $nowplaying to see the song name being played, write  $loop to play your song in a loop. ''')
    embed.title = ':loudspeaker:Music:loudspeaker:'
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
async def rouletteHelp(ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = ('''Schreibe $roulette und red oder black um anzufangen also zb. $roulette black. \n
    Write $roulette and red or black to get started and for example $roulette black.''')
    embed.title = ':game_die:Roulette:game_die:'
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
async def tttHelp(ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = ('''Schreibe $ttt und makiere mit @ die Person mit der du spielen willst. Um zu platzieren nutzte $place und den Platzt. \n
    Write $ttt and tag the person you want to play with. Use $place and the number of the field you want to place.''')
    embed.title = ':o2:TicTacToe:regional_indicator_x:'
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
async def pingHelp(ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = ('''Nutze $ping um den Ping des Bot anzuzeigen lassen. \n
    Use $ping to display the ping from the bot.''')
    embed.title = ':ping_pong: Ping:ping_pong: '
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
async def bcHelp(ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = ('''Wenn du einen Bot-command Channel haben willst nutzte $bc um einen zu erstellen. \n
    If you need a Bot-command Channel use $bc to create one.''')
    embed.title = ':robot:Bot-Channel:robot:'
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
async def coinHelp(ctx):
    embed = discord.Embed()
    embed.color = random.randint(0x000000, 0x999999)
    embed.description = ('''Nutzte $coinflip mit number oder head um das Spiel zu starten. \n
    Use $coinflip number or head to start the game''')
    embed.title = ':moneybag:Coinflip:moneybag:'
    await ctx.send(embed=embed)
    await ctx.message.delete()


    #Ayuwoki Bild & Gif

@client.command()
async def ayuwoki(ctx):
        diedatei = open("ayuwoki.jpeg.jpg", "rb")
        fp = io.BytesIO(diedatei.read())
        await ctx.send(file=discord.File(fp, "ayuwoki.jpeg.jpg"))
        diedatei.close()

@client.command()
async def tanzwoki(ctx):
        diedatei = open("tanzwoki.gif", "rb")
        fp = io.BytesIO(diedatei.read())
        await ctx.send(file=discord.File(fp, "tanzwoki.gif"))
        diedatei.close()

                            #Ping

@client.command(aliases = ['p', 'q'])
async def ping(ctx, arg=None):
    if arg == "pong":
        await ctx.send("Nice Job, you ponged ur self")

    else:
        await ctx.send(f'Pong:ping_pong:! Here is my Ping ik its trash lol: {round(client.latency * 1000)}ms <@{ctx.message.author.id}>')


with open("config.json", "rb") as f:
    config = json.loads(f.read().decode("utf-8"))
client.run(config["token"])

