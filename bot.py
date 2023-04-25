import discord
import responses
import random
import os 
import json
import aiohttp

from requests import get
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_dicord_bot():
    TOKEN = 'MTEwMDA0NDc3NzA5OTEwNDI4Ng.GX-r4w.bKbkm8WJ-Zv8KYQaunslRROofugyaDaQWhFpGc' #reset token before anyone else uses this bot
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix='!',intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    
    @bot.command(name='roll-dice', help='Simulates rolling dice.')
    async def roll(ctx, number_of_dices: int, number_of_sides: int):
        dice = [str(random.choice(range(1, number_of_sides +1))) for _ in range(number_of_dices)]
        await ctx.send(', '.join(dice))

    
    
    @bot.command(name='create-channel', help='Creating new channel.')
    @commands.has_role('admin')
    async def create_channel(ctx, channel_name='real-python'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            await guild.create_text_channel(channel_name)
            await ctx.send(f'Creating a new channel: {channel_name}')
        else: 
            await ctx.send(f'Channel {channel_name} already exsists')            


    @bot.command(pass_context=True, help='Memes from reddit.')
    async def meme(ctx):
        embed = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

    @client.event
    async def on_message(message):
        if message.author == client.user: # client.user is bot so we need to avoid infinite loop
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)



    bot.run(TOKEN)
    #client.run(TOKEN)
    