#Necessary imports
from asyncio import events
import string
import secrets
from turtle import left
from typing import KeysView
import requests
from aiohttp import request
import nextcord, asyncio, json
from PIL import Image, ImageFont, ImageDraw
from nextcord import ButtonStyle, Embed, File, Color, User
from nextcord.ui import Button, View
import textwrap
import random
import time
import os

from numpy import imag, isin

#Allow JSON files to be used within the bot
HG = json.load(open("help.json"))
menuBoi = json.load(open("memeMenu.json"))

#Using 'Nextcord' due to this build being the updated and modern approach to discord.py
#Has same capabilities of discord.py 
intents = nextcord.Intents.all()
intents.message_content = True 
intents.members = True

from nextcord.ext import commands
#Bot responds to certain keywords so long as '!' prefix is at front
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

#Built functions used to link JSON to bot
#Allows users to select which page to look over
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

#Bot cooldown so command is not spammed 
#'bot.command' serves as keyword; what the command will do when the user types it into a channel
@commands.cooldown(1, 5, commands.BucketType.user)
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

@commands.cooldown(1, 5, commands.BucketType.user)
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
#Small test unit to ensure bot is active and listening to user input
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name='hi')
async def hi(ctx):
    msg = await ctx.send(f'Hello {ctx.author.mention}')
    
@commands.cooldown(1, 5, commands.BucketType.user)
#Takes tagged users and creates artificial scenario 
@bot.command(name='battle')
async def battle(ctx, user1: nextcord.Member, user2: nextcord.Member):
    event = random.randint(1, 5)
    result = random.randint(1, 15)
    if user1 == user2:
        await ctx.send("You cannot battle yourself. Mention another fighter and try again!")
        return
    await ctx.send(f'The Battle Between **{user1.display_name}** and **{user2.display_name}** will now begin!')
    time.sleep(3)
    if event == 1:
        await ctx.send(f'Both **{user1.display_name}** and **{user2.display_name}** are fighting mercilessly!')
    if event == 2:
        await ctx.send(f'**{user2.display_name}** takes the high ground!')
    if event == 3:
        await ctx.send(f'**{user1.display_name}** is planning a sneak attack!')
    if event == 4:
        await ctx.send(f'**{user1.display_name}** and **{user2.display_name}** are becoming increasingly tired!')
    if event == 5:
        await ctx.send("The battle is becoming increasingly tense!")
    time.sleep(2)
    if result == 1:
        await ctx.send(f'Both **{user1.display_name}** and **{user2.display_name}** have killed eachother off!')
        time.sleep(1)
        await ctx.send("This battle is a draw!")
        return
    if result == 2:
        await ctx.send(f'Both **{user1.display_name}** and **{user2.display_name}** decide to spare eachothers lives!')
        time.sleep(1)
        await ctx.send("This battle is a draw!")
        return
    if result == 3:
        await ctx.send(f'Both **{user1.mdisplay_name}** and **{user2.display_name}** run away, what cowards!')
        time.sleep(1)
        await ctx.send("This battle has no result!")
        return
    if result == 4:
        await ctx.send(f'**{user1.display_name}** beheads **{user2.display_name}**!')
        time.sleep(1)
        await ctx.send(f"{user1.mention} Wins!")
        return
    if result == 5:
        await ctx.send(f'**{user1.display_name}** quickscopes **{user2.display_name}** in the head!')
        time.sleep(1)
        await ctx.send(f"{user1.mention} Wins!")
        return
    if result == 6:
        await ctx.send(f'**{user2.display_name}** permanently deletes **{user1.display_name}** from existance!')
        time.sleep(1)
        await ctx.send(f"{user2.mention} Wins!")
        return
    if result == 7:
        await ctx.send(f'**{user1.display_name}** decides to spare **{user2.display_name}**!')
        time.sleep(1)
        await ctx.send("Just kidding, they stab them in the heart!")
        await ctx.send(f"{user1.mention} Wins!")
        return
    if result == 8:
        await ctx.send(f'**{user2.display_name}** throws a Nokia at **{user1.display_name}**, killing them instantly!')
        time.sleep(1)
        await ctx.send(f"{user2.mention} Wins!")
        return
    if result == 9:
        await ctx.send(f'**{user2.display_name}** creates an NFT of **{user1.display_name}**, ruining their life completely!')
        time.sleep(1)
        await ctx.send(f"{user2.mention} Wins (Worst way to go)!")
        return
    if result == 10:
        await ctx.send(f'**{user1.display_name}** forces **{user2.display_name}** to play League of Legends. **{user2.display_name}** never recovers from this!')
        time.sleep(1)
        await ctx.send(f"{user1.mention} Wins!")
        return
    if result == 11:
        await ctx.send(f'**{user2.display_name}** forces **{user1.display_name}** to play Valorant as Brimstone. **{user1.display_name}** has enough and shoots themselves!')
        time.sleep(1)
        await ctx.send(f"{user2.mention} Wins (Brimmy with that stimmy)!")
        return
    if result == 12:
        await ctx.send(f'**{user1.display_name}** chops off **{user2.display_name}** limbs!!')
        time.sleep(1)
        await ctx.send(f"{user1.mention} Wins!")
        return
    if result == 13:
        await ctx.send(f'**{user1.display_name}** makes **{user2.display_name}** a discord Moderator!')
        time.sleep(1)
        await ctx.send(f"{user1.mention} Wins!")
        return
    if result == 14:
        await ctx.send(f'**{user2.display_name} forces **{user1.display_name}** to go to Great Yarmouth. The mere thought obliterates **{user1.display_name}**!')
        time.sleep(1)
        await ctx.send(f"{user2.mention} Wins!")
        return
    if result == 15:
        await ctx.send(f'**{user2.display_name}** makes **{user1.display_name}** draw furry fanart!')
        time.sleep(1)
        await ctx.send(f"{user2.mention} Wins!")
        return


@commands.cooldown(1, 5, commands.BucketType.user)
#Command used to test the import of emojis and external media 
@bot.command(name='fart')
async def fart(ctx, user: nextcord.Member):
    await ctx.send(f'{ctx.author.mention} is about to commence the greatest fart of all time!')
    time.sleep(2)
    await ctx.send("😃")
    time.sleep(1)
    await ctx.send("😐")
    time.sleep(1)
    await ctx.send("😣")
    time.sleep(1)
    await ctx.send("😣")
    time.sleep(1)
    await ctx.send("😫")
    time.sleep(1)
    await ctx.send("The great fart travels. With no stopping in sight")
    time.sleep(2)
    await ctx.send("😫💨")
    time.sleep(2)
    await ctx.send("But wait.....THE FART HAS EVOLVED!!!")
    time.sleep(2)
    await ctx.send("😫🔥💨")
    time.sleep(1)
    ctx.send(f"{ctx.author.mention} fart is so extreme it has become THERMAL!!")
    time.sleep(3)
    await ctx.send("😫🔥        💨")
    time.sleep(1)
    await ctx.send("😫🔥            💨")
    time.sleep(1)
    await ctx.send("😫🔥                💨")
    time.sleep(1)
    await ctx.send("😫🔥                    💨")
    time.sleep(1)
    await ctx.send(f"{ctx.author.mention} RELEASES MORE FARTS INTO THE ATMOSPHERE!!!")
    time.sleep(3)
    await ctx.send("😫🔥💨💨💨💨💨💨")
    time.sleep(1)
    await ctx.send("😫🔥💨💨💨💨💨💨💨💨")
    time.sleep(1)
    await ctx.send("😫🔥💨💨💨💨💨💨💨💨💨💨")
    time.sleep(1)
    await ctx.send(f"OH GOD THE WORLD IS FILLING WITH FARTS, WHAT HAVE YOU DONE {ctx.author.mention}")
    time.sleep(5)
    await ctx.send("OH DEAR GOD THE EARTH!!")
    time.sleep(3)
    await ctx.send("💨          🌍")
    time.sleep(1)
    await ctx.send("💨      🌍")
    time.sleep(1)
    await ctx.send("💨  🌍")
    time.sleep(1)
    await ctx.send("🔥🔥🔥")
    time.sleep(3)
    await ctx.send("And so ends the world ending fart. Thank you for watching!")

#Bot event corresponds to what the bot will do once a user does a certain action i.e. react to message    
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '😃':
        await user.send("Glad to see you are doing well :)")
        if user.respond == '1':
            await user.send("Error!")
    if reaction.emoji == '😐':
        await user.send("")
    if reaction.emoji == '😔':
        await user.send("Sad")
    if reaction.emoji == '😭':
        await user.send("Crying")
    if reaction.emoji == '😠':
        await user.send("Angry")

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
#Small heads or tails game implementation
async def flip(ctx, choice):
    options = ["H", "T"]
    result = random.choice(options)
    await ctx.send(f"Time to play: Heads or Tails. You have chosen: {choice} ")
    if choice != "H" and choice != "T":
        await ctx.send("Command Failed: Please retype command and choose either 'H' or 'T' next time!")
    else:
        await ctx.send(f"The coin has been flipped, revealed to be: {result} ")
        if result == choice:
            await ctx.send("You win")
        else:
            await ctx.send("You lose")

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
#Creates auto password for the user
#Uses the secret import so messages aren't less predictable; better option to random()
#Password gets sent to the user but does not get shown on the bot log or anywhere else part from the users Direct Messages
async def createPassword(ctx, user: nextcord.Member, *, length: int, password=None):
    if length > 20:
        await ctx.send("Command failed. Length size too big, please retype command and select a smaller number!")
        return
    else:
        await ctx.send("New password generated. Sending over to dms!")
        letters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(letters)
                    for i in range(length))

        await user.send(f"Your new generated password is: {password}.")
        await user.send("Please note that while this password uses a variety of keybindings to make it secure, you make sure you save this somewhere secure or edit what we sent you to make it easier for yourself!")
        await user.send("We cannot say absolutely that this password will be good, but rest assured only YOU have knowledge of this. The bot does not save any recordings due to several privacy regulations!")

@commands.cooldown(1, 3, commands.BucketType.user)
@bot.command()
#Another small command using the random.randint method
async def rudeball(ctx):
    #Chooses randokm number from range - output varies from what number is generated
    num = random.randint(1, 10)
    if num == 1:
        await ctx.send("This question is meaningless, go outside and touch grass!")
    if num == 2:
        await ctx.send("Why are you asking me this, I have no idea!")
    if num == 3:
        await ctx.send("Stop talking to me. Go on Valorant and continue being bad!")
    if num == 4:
        await ctx.send("System failed: Try looking on reddit or youtube for your answer!")
    if num == 5:
        await ctx.send("Wow ok!")
    if num == 6:
        await ctx.send("You reek of MIDness!")
    if num == 7:
        await ctx.send("No!")
    if num == 8:
        await ctx.send("Imogen all the people!")
    if num == 9:
        await ctx.send("The only answer you need is owning an NFT. Everything else falls into place!")
    if num == 10:
        await ctx.send("Mate idk about this question, all I know is you are the definition of cringe!")

@commands.cooldown(1, 3, commands.BucketType.user)
@bot.command()
#Mention user - another small test of nextcord functions
async def mention(ctx):
    await ctx.send(ctx.author.mention)

@commands.cooldown(1, 10, commands.BucketType.user)
@bot.command()
#Clears n amount of messages in select channel. Will give warning to make sure user wishes to delete n messages
#Currently accessable to all, however modifying it to ensure select roles have access would be useful for servers with different levels of moderation
async def clear(ctx, amount: int):
    while True:
        if amount > 20:
            await ctx.send("Sorry but you cannot clear that many messages. Please re-type command and select a smaller number!")
            break
        await ctx.send(f"Are you sure you wish to delete {amount} messages? (Y/N)")
        try:
            msg = await bot.wait_for("message", timeout=30, check=lambda message: message.author == ctx.author)
        except asyncio.TimeoutError:
            await ctx.send("Action took too long. Please try again and respond faster to command!")
            break

        if msg.content == "Y":
            await ctx.send("Deleting now!")
            await ctx.channel.purge(limit=amount+2)
            await ctx.send(f"Deleted {amount} message(s)")
            break
        elif msg.content == "N":
            await ctx.send("Clearing Cancelled. No messages will be deleted!")
            break
        else:
            await ctx.send("Command failed. Please send either 'Y' or 'N' in the channel!")
            continue


@commands.cooldown(1, 3, commands.BucketType.user)
@bot.command(name='roast')
#Command which takes the select user pfp and writes ontop of it pre-selected word
async def roast(ctx, user: nextcord.Member):
    #Dictionary containing the words which can be written onto the pfp
    roast = {1: "smelly", 2: "Dumb", 3: "Bad", 4: "Small", 5: "Silly", 6: "Great Yarmouth", 7: "Dummy", 8: "Bad person", 9: "Max", 10: "Rank Iron"}
    x = random.choice(list(roast.values()))
    
    #Takes the users pfp as the basis of what the word will be written on
    img = user.display_avatar
    await img.save("./images/roasted.png")

    #Opens image, modifies and seleetcs where the text will be placed based of 2D co-ords
    msg = " ".join(x)
    font = ImageFont.truetype("./resources/PatrickHand-Regular.ttf", 22)
    image = Image.open("./images/roasted.png")
    new = image.resize((234, 234))
    new.save("./images/roasted.png")
    new_image = Image.open("./images/roasted.png")
    cx, cy = (110, 175) #Represents X and Y axis
    
    lines = textwrap.wrap(msg, width=30)
    print(lines)
    w, h = font.getsize(msg)
    y_offset = (len(lines)*h)/2
    y_text = cy-(h/2) - y_offset

    #For loop for text to be drawn on and image to be saves as different file
    for line in lines:  
        draw = ImageDraw.Draw(new_image)
        w, h = font.getsize(line)
        draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font, stroke_width=1, stroke_fill='white')
        new_image.save("./images/roasted-edit.png")
        y_text += h
    
    #Outputs result
    with open("./images/roasted-edit.png", "rb") as f:
        new_image = File(f)
        await ctx.send(file=new_image)

@commands.cooldown(1, 3, commands.BucketType.user)
@bot.command()
#Command for reminding the user on certain event
#Uses dictionary to define time frame 
async def reminder(ctx, time, *, reminder):
    user = ctx.author.mention
    def convert(time):
        pos = ['s', 'm', 'h', 'd', 'y']
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24, "y": 3600*24*365}
        unit = time[-1]
        if unit not in pos:
            return -1 #If user does not use correct time string a error gets returned
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

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name="imogen")
async def imogen(ctx):
    with open("./images/imogen.jpg", "rb") as f:
        img = File(f)
        await ctx.channel.send(file=img)

#Someone says specch
#Printed onto image
@commands.cooldown(1, 5, commands.BucketType.user)
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

@commands.cooldown(1, 5, commands.BucketType.user)
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

@commands.cooldown(1, 5, commands.BucketType.user)
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

@bot.event
async def on_command_error(ctx, err):
    #Error checking - if command does not exist
    if isinstance(err, commands.CommandNotFound):
        await ctx.send("Not a usuable command! Check spelling/punctuation or use '!help' for any assistance!")
    #Error checking - if command is on cooldown
    if isinstance(err, commands.CommandOnCooldown):
        msg = Embed(title="Cooldown Initiated!", description=f"Please wait {err.retry_after:.2f}s before using this command again!.", color=Color.red())
        await ctx.send(embed=msg)
    #Error checking - if command is missing an argument
    if isinstance(err, commands.MissingRequiredArgument):
        await ctx.send("Missing an argument, please check the command you are using (!help) to make sure you're using it correctly!")
        
#Event which clarifies to me that the bot is now running on the server without running into errors
@bot.event
async def on_ready():
    game = nextcord.Game('!help for full list of commands.')
    await bot.change_presence(status=nextcord.Status.online, activity=game)
    print(f"Logged in as: {bot.user.name}")


#Runs the bot based on the TOKEN the bot provided
#TO-DO: Make this secret if used locally
if __name__ == '__main__':
    bot.run(os.environ["DISCORD_TOKEN"])
