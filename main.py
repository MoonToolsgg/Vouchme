import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore, init
from pystyle import Center
import os
import json
import ctypes

config = json.load(open("config.json", encoding="utf-8"))
init()
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def title():
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f"Back UP My Vouches | dsc.gg/nyxtools | nyxtools.sellauth.com")
    else:
        os.system("title back up my vouches")

vouch_count = 1

embed_color = int(config['hex_embed_color'], 16)
activity = discord.Activity(type=discord.ActivityType.playing, name=config['status'])
bot = discord.Bot(command_prefix="/", activity=activity, status=discord.Status.online, intents=discord.Intents.all())

@bot.event
async def on_ready():
   print(Fore.WHITE + "\n[" + Fore.GREEN + "+" + Fore.WHITE + "]" + Fore.MAGENTA + f" Logged in as {bot.user}")

@bot.slash_command(name='vouch',stars= int,description='Give a vouch to someone!', guild_ids=[int(config['guild_id'])])
async def vouch(ctx,message: str,stars = discord.Option(str, "select how many stars", choices=['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐']),attachment = discord.Option(discord.Attachment, "upload image/video proof", required=False)):
    global vouch_count
    

    if ctx.channel_id != int(config['vouch_command_channel']):
        await ctx.response.send_message("This command can only be used in the designated channel.", ephemeral=True)
        return
    
    user = ctx.user
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stars_count = stars.count('⭐')

    embed = discord.Embed(title="New Vouch Created!", color=embed_color)
    embed.add_field(name="Vouch:", value=message, inline=False)
    embed.add_field(name="Stars:", value=stars, inline=False)
    embed.add_field(name="Vouched by:", value=f"{user.mention}", inline=True)
    embed.add_field(name="Vouched on:", value=current_date, inline=True)
    embed.add_field(name="Vouch Number:", value=vouch_count, inline=True)
    embed.set_thumbnail(url=user.display_avatar.url)
    
    if attachment:
        embed.add_field(name="Image Proof:", value="", inline=False)
        embed.set_image(url=attachment.url)
    
    await ctx.respond(embed=embed)

    vouch_info = {
        'vouch': message,
        'stars': stars_count,
        'vouched_by_name': user.name,
        'vouched_by_avatar_url': user.display_avatar.url,
        'vouched_on': current_date,
        'vouch_number': vouch_count,
        'attachment': attachment.url if attachment else None
    }
    
    with open(f'vouches/{vouch_count}.json', 'w') as f:
        json.dump(vouch_info, f)
    
    vouch_count += 1

@bot.slash_command(name='backupvouches',description='Backup all vouches!', guild_ids=[int(config['guild_id'])])
async def backupvouches(ctx):
    if ctx.channel_id != int(config['backup_command_channel']):
        await ctx.response.send_message("This command can only be used in the designated channel.", ephemeral=True)
        return
    
    if not os.listdir('vouches'):
        await ctx.response.send_message("No vouches to backup!", ephemeral=True)
        return
    

    
    for filename in os.listdir('vouches'):
        with open(f'vouches/{filename}', 'r') as f:
            vouch = json.load(f)
            stars_display = '⭐' * vouch['stars']
            embed = discord.Embed(title="Backed Up Vouch!", color=embed_color)
            embed.add_field(name="Vouch:", value=vouch['vouch'], inline=False)
            embed.add_field(name="Stars:", value=stars_display, inline=False)
            embed.add_field(name="Vouched by:", value=f"{vouch['vouched_by_name']}", inline=True)
            embed.add_field(name="Vouched on:", value=vouch['vouched_on'], inline=True)
            embed.add_field(name="Vouch Number:", value=vouch['vouch_number'], inline=True)
            embed.set_thumbnail(url=vouch['vouched_by_avatar_url'])
            
            if vouch['attachment']:
                embed.set_image(url=vouch['attachment'])
            
            await ctx.respond(embed=embed)

clear()
title()
print(Fore.LIGHTMAGENTA_EX + Center.XCenter("""
███╗   ██╗██╗   ██╗██╗  ██╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
████╗  ██║╚██╗ ██╔╝╚██╗██╔╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██╔██╗ ██║ ╚████╔╝  ╚███╔╝        ██║   ██║   ██║██║   ██║██║     ███████╗
██║╚██╗██║  ╚██╔╝   ██╔██╗        ██║   ██║   ██║██║   ██║██║     ╚════██║
██║ ╚████║   ██║   ██╔╝ ██╗       ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝\n"""))
bot.run(config['bot_token'])
