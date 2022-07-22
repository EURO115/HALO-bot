#Necessary imports
import string
import secrets
import nextcord, asyncio, json
from PIL import Image, ImageFont, ImageDraw
from nextcord import ButtonStyle, Embed, File
from nextcord.ui import Button, View
import youtube_dl
import textwrap
import random
import os

HG = json.load(open("help.json"))
menuBoi = json.load(open("memeMenu.json"))

intents = nextcord.Intents.all()
intents.message_content = True 
intents.members = True

from nextcord.ext import commands
#Bot responds to certain keywords so long as '!' prefix is at front
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

def createHelp(pageNum=0, inline=False):
    pageNum = pageNum % len(list(HG))
    pageTitle = list(HG)[pageNum]
    embed=Embed(color=0x0080ff, title=pageTitle)
    for key, val in HG[pageTitle].items():
        embed.add_field(name=bot.command_prefix+key, value=val, inline=inline)
        embed.set_footer(text=f"Page {pageNum+1} of {len(list(HG))}")
    return embed

def createMemeMenu(pageNum=0, inline=False):
    pageNum = pageNum % len(list(menuBoi))
    pageTitle = list(menuBoi)[pageNum]
    embed=Embed(color=0x0080ff, title=pageTitle)
    for val, key in menuBoi[pageTitle].items():
        embed.add_field(name=key, value=val, inline=inline)
        embed.set_footer(text=f"Page {pageNum+1} of {len(list(menuBoi))}")
    return embed

@bot.command(name="memeMenu")
async def memeMenu(ctx):
    currentPage = 0

    async def nx_callback(interaction):
        nonlocal currentPage, send_message
        currentPage += 1
        await send_message.edit(embed=createMemeMenu(pageNum=currentPage), view=newView)

    async def prev_callback(interaction):
        nonlocal currentPage, send_message
        currentPage -= 1
        await send_message.edit(embed=createMemeMenu(pageNum=currentPage), view=newView)

    button = Button(label=">", style=ButtonStyle.blurple)
    button.callback = nx_callback
    prevButton = Button(label="<", style=ButtonStyle.red)
    prevButton.callback = prev_callback

    newView = View(timeout=180)
    newView.add_item(prevButton)
    newView.add_item(button)
    send_message = await ctx.send(embed=createMemeMenu(), view=newView)


@bot.command(name="help")
async def Help(ctx):
    currentPage = 0

    async def nx_callback(interaction):
        nonlocal currentPage, send_message
        currentPage += 1
        await send_message.edit(embed=createHelp(pageNum=currentPage), view=newView)

    async def prev_callback(interaction):
        nonlocal currentPage, send_message
        currentPage -= 1
        await send_message.edit(embed=createHelp(pageNum=currentPage), view=newView)

    button = Button(label=">", style=ButtonStyle.blurple)
    button.callback = nx_callback
    prevButton = Button(label="<", style=ButtonStyle.red)
    prevButton.callback = prev_callback

    newView = View(timeout=180)
    newView.add_item(prevButton)
    newView.add_item(button)
    send_message = await ctx.send(embed=createHelp(), view=newView)

# ----------- Small interactive/Fun commands --------------

#Command which responds with .send() whenever someone writes the function name 
@bot.command(name='hi')
async def hi(ctx):
    msg = await ctx.send(f'Hello {ctx.author.mention}')
    happy = '😃'
    meh = '😐'
    sad = '😔'
    crying = '😭'
    angry = '😠'
    await msg.add_reaction(happy), await msg.add_reaction(meh), await msg.add_reaction(sad), await msg.add_reaction(crying),
    await msg.add_reaction(angry)

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '😃':
        await user.send("Glad to see you are doing well :)")
        if user.respond == '1':
            await user.send("FUCK!")
    if reaction.emoji == '😐':
        await user.send("")
    if reaction.emoji == '😔':
        await user.send("Joe mama")
    if reaction.emoji == '😭':
        await user.send("Joe mama")
    if reaction.emoji == '😠':
        await user.send("Joe mama")

@bot.command()
async def copypasta(ctx, numb: int):
    if numb == 1:
        await ctx.send("You sent me a message first, yeah. I live in Smethwick Birmingham if you want to FUCKING brawl. COME down, Smethwick, ask for Danny G, I'LL COME OUT MY HOUSE, AND I'LL BREAK YOUR FUCKING LEGS! YOU LITTLE PRICK! HEAR WHAT I'M SAYING?! HEAR WHAT I'M, FUCKING SAYING?! COME BIRMINGHAM AND I WILL FUCK YOU UP, COME BIRMINGHAM NOW, AND I WILL FUCK YOU UP! I TOLD YOU WHERE I LIVE, YOU WANT TO KNOW WHERE I LIVE?! I LIVE IN FUCKING SMETHWICK, NOW COME, AND I'LL KILL YAH. What's my problem? What's my problem? You, is my fucking problem. Shut your fucking mouth I'LL FIND OUT WHERE YOU LIVE AND I WILL COME AND FUCK YOU UP IN YOUR OWN HOUSE. SHUT THE FUCK UP YOU DON'T KNOW WHO I AM GEEZER, I AM A FUCKING MONSTER. DON'T FUCK ME ABOUT AND I'LL COME TO YOUR HOUSE AND I WILL FUCK YOU UP IN YOUR OWN HOUSE. I TOLD YOU WHERE I LIVE. COME TO MY HOUSE, SMETHWICK, COME TO MY HOUSE AND WE'LL SEE WHO KNOCKS WHO OUT MATE I'LL BREAK YOUR FUCKING FACE. SERIOUSLY MATE I'LL BREAK YOUR FACE, I WILL BREAK YOU OPEN, I SWEAR TO GOD YOU LITTLE PRICK. YOU SOUND LIKE YOU'RE 17 YOU LITTLE KNOBHEAD. I'VE GOT FUCKING KIDS OLDER THAN YOU MAN, I GOT KIDS THAT WILL FUCK YOU UP YOU DICKHEAD.")
    if numb == 2:
        await ctx.send("As a person who has lots of sex all the time, I can say that this game is 100% accurate to having sex with sexy women. like I do. everyday. this game did not make me horny, however. I am not gay. I just have too much sex with real women to spend more than 15 minutes in this game. on the other hand, I would recommend this game to people who do not have sex (unlike me because i have lots of sex with women lot) as there is a naked woman in it and she is naked. she kinda looks like one of my many girlfriends with who i have sex with a lot. i have lots of sex. i also very handsome and women ALWAYS want to have sex with me because i am very muscular and handsome and very good at video games. all my girlfriends say I'm very good at sex and playing video games and being handsome. one of my girlfriends asked me to have sex with her but i told her i was playing a sex game instead so she started crying and became a lesbian and killed herself because i did not have sex with her. i have sex with women. not men. i am not gay. i am very cool and handsome so girls always have sex with me because i am very cool and sexy. my penis is very big. all my girlfriends like my penis because it is very big and i am very good at sex with my women. every woman ive had sex with is very sexy and so am i. i have lots of sex. i am also very handsome and sexy and i have lots of sex.")

@bot.command()
async def flip(ctx, choice):
    options = ["H", "T"]
    result = random.choice(options)
    await ctx.send(f"Time to play: Heads or Tails. You have chosen: {choice} ")
    if choice != "H" and choice != "T":
        await ctx.send("Game failed: Please choose either 'H' or 'T'!")
    else:
        await ctx.send(f"The coin has been flipped, revealed to be: {result} ")
        if result == choice:
            await ctx.send("You win")
        else:
            await ctx.send("You lose")

@bot.command()
async def createPassword(ctx, user: nextcord.Member, *, length: int, password=None):
    await ctx.send("New password generated. Sending over to dms!")
    letters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(letters)
                for i in range(length))

    await user.send(f"Your new generated password is: {password}.")

@bot.command()
async def rudeball(ctx):
    num = random.randint(1, 10)
    if num == 1:
        await ctx.send("This question is meaningless, go outside and touch grass!")
    if num == 2:
        await ctx.send("Why are you asking me this, I have no idea!")
    if num == 3:
        await ctx.send("Stop talking to me. Go on Valorant and continue being shite!")
    if num == 4:
        await ctx.send("System failed: Try looking on reddit or youtube for your answer!")
    if num == 5:
        await ctx.send("Jesus you sound clapped!")
    if num == 6:
        await ctx.send("You reek of MIDness!")
    if num == 7:
        await ctx.send("No!")
    if num == 8:
        await ctx.send("Imogen all the people!")
    if num == 9:
        await ctx.send("The only answer you need is owning an NFT. Everything else falls into place!")
    if num == 10:
        await ctx.send("Mate idk about this question, all I know is you are the definition of crig!")

@bot.command()
async def mention(ctx):
    await ctx.send(ctx.author.mention)

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Deleted {amount} message(s)")

@bot.command()
async def reminder(ctx, time, *, reminder):
    user = ctx.author.mention
    def convert(time):
        pos = ['s', 'm', 'h', 'd', 'y']
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24, "y": 3600*24*365}
        unit = time[-1]
        if unit not in pos:
            return -1
        try:
            val = int(time[:-1])
        except:
            return -2

        return val * time_dict[unit]

    converted_time = convert(time)

    if converted_time == -1:
        await ctx.send("Incorrect time!")
        return

    if converted_time == -2:
        await ctx.send("Time needs to be a number!")
        return

    await ctx.send(f"Starting reminder for **{reminder}** and will last **{time}**")

    await asyncio.sleep(converted_time)
    await ctx.send(f"{user} Your reminder of **{reminder}** has finished!")






# ------------- FUNNY IMAGE/MEME SEGMENT -----------------

@bot.command(name="imogen")
async def imogen(ctx):
    with open("./images/imogen.jpg", "rb") as f:
        img = File(f)
        await ctx.channel.send(file=img)


#Someone says specch
#Printed onto image
@bot.command(name='redsus')
async def redsus(ctx, *args): #star means we can use any amount of arguments
    msg = " ".join(args)
    font = ImageFont.truetype("./resources/PatrickHand-Regular.ttf", 30)
    img = Image.open("./images/sus.png")
    cx, cy = (305, 255)
    
    lines = textwrap.wrap(msg, width=12)
    print(lines)
    w, h = font.getsize(msg)
    y_offset = (len(lines)*h)/2
    y_text = cy-(h/2) - y_offset

    for line in lines:  
        draw = ImageDraw.Draw(img)
        w, h = font.getsize(line)
        draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font)
        img.save("./images/sus-edited.png")
        y_text += h

    with open("./images/sus-edited.png", "rb") as f:
        img = File(f)
        await ctx.channel.send(file=img)

@bot.command(name='stock')
async def stock(ctx, image_path, top, bottom): #star means we can use any amount of arguments
    msg = " ".join(top)
    msg2 = " ".join(bottom)
    if image_path == "stockbed":
        image_path = "./images/stock.jpg"
    if image_path == "gunfish":
        image_path = "./images/gunfish.jpg"
    if image_path == "girlcamera":
        image_path = "./images/girlcamera.jpg"
    if image_path == "laptoplook":
        image_path = "./images/laptoplook.jpg"
    if image_path == "manegg":
        image_path = "./images/manegg.jpg"
    if image_path == "business":
        image_path = "./images/business.jpg"
    if image_path == "wakeupbabe":
        image_path = "./images/wakeupbabe.jpg"
    if image_path == "coolguy":
        image_path = "./images/coolguy.jpg"
    if image_path == "penguin":
        image_path = "./images/penguin.jpg"
    if image_path == "sadguy":
        image_path = "./images/sadguy.jpg"
    if image_path == "batguy":
        image_path = "./images/batguy.jpg"
    if image_path == "clockgun":
        image_path = "./images/clockgun.jpg"
    font = ImageFont.truetype("./resources/Olive-Days.ttf", 30)
    img = Image.open(image_path)
    cx, cy = (400, 50) #Location of top text
    bx, by = (400, 510) #Location of bottom text
    
    lines = textwrap.wrap(msg, width=60)
    lines2 = textwrap.wrap(msg2, width=60)
    print(lines)
    print(lines2)
    w, h = font.getsize(msg)
    e, o = font.getsize(msg2)
    y_offset = (len(lines)*h)/2
    y_text = cy-(h/2) - y_offset
    y2_offset = (len(lines2)*o)/2
    y2_text = by-(o/2) - y2_offset

    for line in lines:  
        draw = ImageDraw.Draw(img)
        w, h = font.getsize(line)
        draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font, stroke_width=3, stroke_fill='white')
        y_text += h

    for line in lines2:  
        draw = ImageDraw.Draw(img)
        e, o = font.getsize(line)
        draw.text((bx-(e/2), y2_text), line, (0, 0, 0), font=font, stroke_width=3, stroke_fill='white')
        y2_text += o

    img.save("./images/meme-edited.jpg")
    with open("./images/meme-edited.jpg", "rb") as f:
        img = File(f)
        await ctx.channel.send(file=img)


@bot.command(name='emoji')
async def emoji(ctx, image_path, top, bottom): #star means we can use any amount of arguments
    msg = " ".join(top)
    msg2 = " ".join(bottom)
    if image_path == "angryface":
        image_path = "./images/angryface.jpg"
    if image_path == "smileyface":
        image_path = "./images/smileyface.jpg"
    if image_path == "joyface":
        image_path = "./images/joyface.jpg"
    if image_path == "quietface":
        image_path = "./images/quietface.jpg"
    if image_path == "nerdface":
        image_path = "./images/nerdface.jpg"
    font = ImageFont.truetype("./resources/Olive-Days.ttf", 32)
    img = Image.open(image_path)
    cx, cy = (400, 50) #Location of top text
    bx, by = (400, 510) #Location of bottom text
    
    lines = textwrap.wrap(msg, width=46)
    lines2 = textwrap.wrap(msg2, width=46)
    print(lines)
    print(lines2)
    w, h = font.getsize(msg)
    e, o = font.getsize(msg2)
    y_offset = (len(lines)*h)/2
    y_text = cy-(h/2) - y_offset
    y2_offset = (len(lines2)*o)/2
    y2_text = by-(o/2) - y2_offset

    for line in lines:  
        draw = ImageDraw.Draw(img)
        w, h = font.getsize(line)
        draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font, stroke_width=3, stroke_fill='white')
        y_text += h

    for line in lines2:  
        draw = ImageDraw.Draw(img)
        e, o = font.getsize(line)
        draw.text((bx-(e/2), y2_text), line, (0, 0, 0), font=font, stroke_width=3, stroke_fill='white')
        y2_text += o

    img.save("./images/meme-edited.jpg")
    with open("./images/meme-edited.jpg", "rb") as f:
        img = File(f)
        await ctx.channel.send(file=img)

@bot.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for current music to stop playing!")
        return

    VoiceChannel = nextcord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
    await VoiceChannel.connect()
    voice = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.send("Video initialised. PLease wait for bot to load in")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(nextcord.FFmpegPCMAudio("song.mp3"))
    await ctx.send(f"Now playing {url}")

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        return await ctx.voice_client.disconnect()
    await ctx.send("I am not connected to a voice channel.")

@bot.command()
async def pause(ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client is None:
        return await ctx.send("I am not connected to a voice channel.")

    if not ctx.voice_client.is_paused():
        return await ctx.send("I am already playing a song.")
        
    ctx.voice_client.resume()
    await ctx.send("The current song has been resumed.")

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandNotFound):
        await ctx.send("Not a usuable command! Check spelling/punctuation to ensure the command goes through!")

#Event which clarifies to me that the bot is now running on the server without running into errors
@bot.event
async def on_ready():
    game = nextcord.Game('!help for full list of commands.')
    await bot.change_presence(status=nextcord.Status.online, activity=game)
    print(f"Logged in as: {bot.user.name}")


#Runs the bot based on the TOKEN the bot provided
#TO-DO: Make this secret
if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])