import datetime
import math
import pickle
import random
from datetime import timedelta, date, time
from discord import Permissions
from colorama import Fore, Style
import discord
import json  
import asyncio
from discord.ext import commands, tasks
from discord.utils import get
import os
import time


bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print(''' 
██████╗░██╗░██████╗░█████╗░░█████╗░██████╗░██████╗░░░░██████╗░██╗░░░██╗
██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗░░░██╔══██╗╚██╗░██╔╝
██║░░██║██║╚█████╗░██║░░╚═╝██║░░██║██████╔╝██║░░██║░░░██████╔╝░╚████╔╝░
██║░░██║██║░╚═══██╗██║░░██╗██║░░██║██╔══██╗██║░░██║░░░██╔═══╝░░░╚██╔╝░░
██████╔╝██║██████╔╝╚█████╔╝╚█████╔╝██║░░██║██████╔╝██╗██║░░░░░░░░██║░░░
╚═════╝░╚═╝╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝╚═╝░░░░░░░░╚═╝░░░''')
  #THIS BOT IS FULLY CREATED BY NEWACHO#0001. USING OF THIS BOT IS... acceptable :D

@bot.command()
async def ping(ctx):
    latency = bot.latency
    await ctx.send(f"Pong! {latency}ms")


@bot.command()
async def hi(ctx, member: discord.Member):
    await ctx.send(f"Hello! {member}")


@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=False,
                                          read_messages=False)
        await member.add_roles(mutedRole)
    embed = discord.Embed(
        title=f"",
        description=
        f"<:314691591484866560:967764141416783932> **{member.mention} was muted. Reason: {reason}**",
        colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    print(f'{member} was muted for {reason}')
    embed = discord.Embed(title='', description=f"You have been muted for: **{reason}** by {ctx.message.author.mention} in **{guild}**", colour=discord.Colour.red())

    await member.send(embed=embed)

      

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    print(f'{member} was unmuted')
    embed = discord.Embed(
        title=f"",
        description=f"<:314691591484866560:967764141416783932> **{member.mention} was unmuted** ",
        colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    await member.remove_roles(mutedRole, reason=reason)
    embed = discord.Embed(title='', description=f"You have been unmuted for: **{reason}** by {ctx.message.author.mention} in {guild}", colour=discord.Colour.red())
  
    await member.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    print(f'{member} was warned')
    embed = discord.Embed(
        title="",
        description=
        f"<:314691591484866560:967764141416783932> **{member.mention} was warned**",
        colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    embed = discord.Embed(title='', description=f"You have warned for: **{reason}** by {ctx.message.author.mention}", colour=discord.Colour.red())
  
    await member.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearwarn(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title=f"",
        description=
        f"<:314691591484866560:967764141416783932> ***{member.mention}'s warn was cleared***",
        colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    await member.send(f" Your warn has been cleared")
    print(f'{member}s warn was cleared')


@bot.command(pass_context=False)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    embed = discord.Embed(
        title="",
        description=
        f"<:314691591484866560:967764141416783932> ***Chat purged by {ctx.author.mention}***",
        colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    await ctx.message.delete()
    print(f'Chat purged by {ctx.author.mention}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title=f"",
            description=f"<:314691684455809024:967760470633222184> You do not have permissions to run this command.",
            colour=discord.Colour.red())
        await ctx.send(embed=embed)
        print('Not enough permissions')
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title=f"",
            description="<:314691684455809024:967760470633222184> Invalid argument",
            colour=discord.Colour.red())
        await ctx.send(embed=embed)
        print('Invalid argument')




@bot.command(pass_context=True)
async def changenick(ctx, *,member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(
        f'> <:314691591484866560:967764141416783932> ***Nickname was changed for {member.mention}*** '
    )


member_count = 0


@bot.command(name='membercount')
async def membercount(ctx):
    embed = discord.Embed(
        title="",
        description=
        f"<:314691591484866560:967764141416783932> ***There is {ctx.guild.member_count} members***",
        colour=discord.Colour.green())
    await ctx.send(embed=embed)


@bot.command()
async def avatar(ctx, member: discord.Member):
  embed = discord.Embed(title="", description=f"**{member}'s avatar**")
  embed.set_image(url=f"{member.avatar_url}")

  await ctx.send(embed=embed)

@bot.command()
async def av(ctx, member: discord.Member):
  embed = discord.Embed(title="", description=f"**{member}'s avatar**")
  embed.set_image(url=f"{member.avatar_url}")

  await ctx.send(embed=embed)


@bot.command()
async def pfp(ctx, member: discord.Member):
  embed = discord.Embed(title="", description=f"**{member}'s avatar**")
  embed.set_image(url=f"{member.avatar_url}")

  await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = "no reason provided"
    await ctx.guild.kick(member)
    print(f'{member} was kicked')
    embed = discord.Embed(
        title=f"",
        description=
        f"<:314691591484866560:967764141416783932> **{member.mention} was kicked for {reason}**",
        colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    embed = discord.Embed(title='', description=f"You have kicked for: **{reason}** by {ctx.message.author.mention}", colour=discord.Colour.red())
  
    await member.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        reason = "no reason provided"
    await ctx.guild.ban(member)
    print(f'{member} was banned for {reason}')
    embed = discord.Embed(
        title=f"",
        description=
        f"<:314691591484866560:967764141416783932> **{member.mention} was banned for {reason}**",
        colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)
    embed = discord.Embed(title='', description=f"You have banned for: **{reason}** by {ctx.message.author.mention}", colour=discord.Colour.red())
  
    await member.send(embed=embed)


@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            print(f'{member} was unbanned')
    embed = discord.Embed(title="", description=f"**<:314691591484866560:967764141416783932> {member} was unbanned**", colour=discord.Colour.green())
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)

format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

@bot.command()
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=discord.Color.green()
    )
  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)

@bot.command()
@commands.has_permissions(administrator=True)
async def modbot(ctx):
    await ctx.send('''
███╗░░░███╗░█████╗░██████╗ ░██████╗░░█████╗░████████╗
████╗░████║██╔══██╗██╔══██ ╗██╔══██╗██╔══██╗╚══██╔══╝
██╔████╔██║██║░░██║██║░░██ ║██████╦╝██║░░██║░░░██║░░░
██║╚██╔╝██║██║░░██║██║░░██ ║██╔══██╗██║░░██║░░░██║░░░
██║░╚═╝░██║╚█████╔╝██████╔ ╝██████╦╝╚█████╔╝░░░██║░░░
╚═╝░░░░░╚═╝░╚════╝░╚═════╝ ░╚═════╝░░╚════╝░░░░╚═╝░░░''')

@bot.command()
async def gayrate(ctx, *, member: discord.Member):
        responses =[
1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 , 99 , 100
        ]
        embed = discord.Embed(title="gayrate machine", description=f"{member} is {random.choices(responses)}% gay :rainbow_flag: ")
        await ctx.send(f"> <a:903063474547064892:969520800522727434> {ctx.message.author.mention} You have an unread alert! Type !alert to read it!")
        await ctx.send(embed=embed)

@bot.command()
async def simprate(ctx, *, member: discord.Member):
        responses =[
1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 , 99 , 100
        ]
        embed = discord.Embed(title="simprate machine", description=f"{member} is {random.choices(responses)}% simp")
        await ctx.send(f"> <a:903063474547064892:969520800522727434> {ctx.message.author.mention} You have an unread alert! Type !alert to read it!")
        await ctx.send(embed=embed)

@bot.command()
async def epicgamerrate(ctx, *, member: discord.Member):
        responses =[
1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 , 99 , 100
        ]
        embed = discord.Embed(title="epicgamerrate machine", description=f"{member} is {random.choices(responses)}% epic gamer :sunglasses: ")
        await ctx.send(f"> <a:903063474547064892:969520800522727434> {ctx.message.author.mention} You have an unread alert! Type !alert to read it!")
        await ctx.send(embed=embed)

@bot.command()
async def pp(ctx, *, member: discord.Member):
        responses =[
1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12
        ]
        embed = discord.Embed(title="pp r8 machine", description=f"{member}s {random.choices(responses)} inch")
        await ctx.send(f"> <a:903063474547064892:969520800522727434> {ctx.message.author.mention} You have an unread alert! Type !alert to read it!")
        await ctx.send(embed=embed)

@bot.command()
async def whorerate(ctx, *, member: discord.Member):
        responses =[
1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10 , 11 , 12 , 13 , 14 , 15 , 16 , 17 , 18 , 19 , 20 , 21 , 22 , 23 , 24 , 25 , 26 , 27 , 28 , 29 , 30 , 31 , 32 , 33 , 34 , 35 , 36 , 37 , 38 , 39 , 40 , 41 , 42 , 43 , 44 , 45 , 46 , 47 , 48 , 49 , 50 , 51 , 52 , 53 , 54 , 55 , 56 , 57 , 58 , 59 , 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79 , 80 , 81 , 82 , 83 , 84 , 85 , 86 , 87 , 88 , 89 , 90 , 91 , 92 , 93 , 94 , 95 , 96 , 97 , 98 , 99 , 100
        ]
        embed = discord.Embed(title="whorerate machine", description=f"{member} is {random.choices(responses)}% whore :peach: ")
        await ctx.send(f"> <a:903063474547064892:969520800522727434> {ctx.message.author.mention} You have an unread alert! Type !alert to read it!")
        await ctx.send(embed=embed)

@bot.command()
async def randomizer(ctx):
  await ctx.send(random.randint(0,1000))

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    embed = discord.Embed(title=f"", description = f"<:314691591484866560:967764141416783932> ***{ctx.channel.mention} Is now locked***", colour=discord.Colour.green())
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title=f"", description = f"<:314691591484866560:967764141416783932> ***{ctx.channel.mention} Is now unlocked***", colour=discord.Colour.green())
    await ctx.send(embed=embed)

@bot.command()
async def report(ctx, member: discord.Member, *, reason=None):
  embed = discord.Embed(title="", description = f"Thanks for submitting a report on **{member}** for: **{reason}**! Staffs will review it and reach out", colour=discord.Colour.green())
  await ctx.send(embed=embed)
  embed = discord.Embed(title='', description=f"You have been reported for: **{reason}** by {ctx.message.author.mention}")
  await member.send(embed=embed)

@bot.command()
async def help(ctx):
  page1 = discord.Embed(title="Moderation help", description="**Ban:** \n Ban a user/!ban @user reason \n **Unban:** \n Unban a user/!unban @user.tag \n **Mute:** \n Mute a member so they can't talk/!mute @user reason \n **Unmute:** \n Unmute a user so they can speak/!unmute @user \n **Warn:** \n Warn a user/!warn @user Reason \n **Clearwarn:** \n Clear a members warn/!clearwarn @user \n **Lockdown:** \n Locks channel/!lockdown \n **Unlock:** \n ")
  page1.add_field(name="Page 1/4", value="!page2 for more commands")
  await ctx.send(embed=page1)

@bot.command()
async def page2(ctx, *,content="2"):
    page2 = discord.Embed(title="Fun commands help", description="**Gayrate:** \n See if your friends are gay/!gayrate @user \n **Epicgamerrate:** \n See if your friend is epicgamer/ !epicgamerrate @user \n **Whorerate:** \n Is your gf a hoe? Check if she is/!whorerate @user \n **Simprate:** \n See if ur friend is a simp/!simprate @user \n **pp:** \n Says for itself/!pp @user")
    page2.add_field(name="Page 2/4", value="!page3 for more commands")
    await ctx.send(embed=page2)

@bot.command()
async def page3(ctx, *,content="3"):
     page3 = discord.Embed(title="Misc. commands", description="**Avatar:** \n See avatars/!avatar @user \n **Membercount:** \n See how many members are there/!membercount \n **Purge:** \n !purge {amount} \n **Ping:** \n Shows latency/!ping \n **Serverinfo:** \n Says for itself/!serverinfo")
     page3.add_field(name="Page 3/4", value="!page4 for more commands")
     await ctx.send(embed=page3)

@bot.command()
async def page4(ctx):
  embed = discord.Embed(title="Mario games!", description="**Mariokart** \n Type !mariokart to get more info \n **Marioparty:** \n type !marioparty to get more info")
  embed.add_field(name="More commands coming soon!",value="Currently 20+ commands")
  await ctx.send(embed=embed)
      

@bot.command()
async def changelog(ctx):
  embed = discord.Embed(title="Changelog", description="Commands on this server start with !")
  embed.add_field(name="!changelong", value="Added on 4/29/22, shows latest changes in the bot")
  embed.add_field(name="!mail", value="Added on 4/29/22, mails a user content you typed")
  embed.add_field(name="!help(command)", value="Added on 5/1/22, shows help on certain commands")
  embed.add_field(name="!kill/kiss/hug/slap", value="Added on 5/2/22, shows a gif related to the command")
  embed.add_field(name="!8ball (question)", value="Added on 5/2/22, answers a question by randomizer")
  embed.add_field(name="!meme", value="Added on 5/3/22 Shows cool memes (imo)")
  embed.add_field(name="!trivia", value="Added on 5/4/22, trivia questions time!")

  await ctx.send(embed=embed)

@bot.command()
async def mail(ctx, member: discord.Member, *,content):
    channel = await member.create_dm() 
    await channel.send(f"> <a:903063474547064892:969520800522727434> {member.mention} **You have an unread mail from {ctx.message.author.mention}:** {content}")
    embed = discord.Embed(title="", description=f"<a:903063474547064892:969520800522727434> **Mail sent to {member}**",         colour=discord.Colour.green())
    await ctx.send(embed=embed)

@bot.command()
async def helpmute(ctx, *words):
  embed = discord.Embed(title="Command: !mute", description="Commands on this server start with !")
  embed.add_field(name="Example:", value="!mute @user >reason<")

  await ctx.send(embed=embed)

@bot.command()
async def helpunmute(ctx, *words):
  embed = discord.Embed(title="Command: !unmute", description="Commands on this server start with !")
  embed.add_field(name="Example:", value="!unmute @user >reason<")

  await ctx.send(embed=embed)

@bot.command()
async def helpwarn(ctx, *words):
  embed = discord.Embed(title="Command: !warn", description="Commands on this server start with !")
  embed.add_field(name="Example:", value="!warn @user >reason<")

  await ctx.send(embed=embed)

@bot.command()
async def helpclearwarn(ctx, *words):
  embed = discord.Embed(title="Command: !clearwarn", description="Commands on this server start with !")
  embed.add_field(name="Example:", value="!clearwarn @user")

  await ctx.send(embed=embed)

@bot.command()
async def sex(ctx):
  await ctx.send('https://cdn.discordapp.com/attachments/910830387465449502/969545757734617098/MemeFeedBot-11-1.mov')

@bot.command()
async def friends(ctx):
  await ctx.send('https://cdn.discordapp.com/attachments/964608273762365443/969862426168295445/Screenshot_20220429-201536_YouTube.jpg')

@bot.command()
async def server(ctx):
  await ctx.send(f'{ctx.message.author.mention} https://discord.gg/dpy')

@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
        responses = [ 
          "It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Outlook good.",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Better not tell you now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Outlook not so good.",
                    "Very doubtful."
        ]
        await ctx.send(f':8ball: {random.choices(responses)} {ctx.message.author.mention}')
        await ctx.send(f"> <a:903063474547064892:969520800522727434> {ctx.message.author.mention} You have an unread alert! Type !alert to read it!")

@bot.command()
async def rating(ctx, member: discord.Member):
    variable_list = [
        ':star:',
        ':star::star:',
        ':star::star::star:',
        ':star::star::star::star:',
        ':star::star::star::star::star:',
    ]

    embed = discord.Embed(
        colour=0xc81f9f,
        title="Rating",
        description=f"{member.mention} {random.choice(variable_list)} is your rating"
    )
    embed.set_footer(text=f"{ctx.message.guild.name}")
    embed.timestamp = datetime.datetime.utcnow()

    await ctx.send(embed=embed)

@bot.command()
async def kill(ctx, member: discord.Member):
    embed = discord.Embed(title="", description=f"**{ctx.message.author} killed {member}, oof**", color = 0x9b59b6) #You can add a text in there if you want
#embed.add_field(name="**Add something**", value="Or delete this.", inline=False) 
    embed.set_image(url="https://cdn.weeb.sh/images/B1VnoJFDZ.gif")
    await ctx.send(embed=embed) #This sends the message in the DMs change to "ctx.send" to send it in chat

@bot.command()
async def slap(ctx, member: discord.Member):
    embed = discord.Embed(title="", description=f"**{ctx.message.author} slapped {member}, deserves it!**", color = 0x9b59b6) #You can add a text in there if you want
#embed.add_field(name="**Add something**", value="Or delete this.", inline=False) 
    embed.set_image(url="https://cdn.weeb.sh/images/HkskD56OG.gif")
    await ctx.send(embed=embed) #This sends the message in the DMs change to "ctx.send" to send it in chat

@bot.command()
async def hug(ctx, member: discord.Member):
    embed = discord.Embed(title="", description=f"**{ctx.message.author} hugged {member}, cute**", color = 0x9b59b6) #You can add a text in there if you want
#embed.add_field(name="**Add something**", value="Or delete this.", inline=False) 
    embed.set_image(url="https://cdn.weeb.sh/images/SywetdQvZ.gif")
    await ctx.send(embed=embed) #This sends the message in the DMs change to "ctx.send" to send it in chat

@bot.command()
async def kiss(ctx, member: discord.Member):
    embed = discord.Embed(title="", description=f"**{ctx.message.author} kissed {member}, OWO**", color = 0x9b59b6) #You can add a text in there if you want
#embed.add_field(name="**Add something**", value="Or delete this.", inline=False) 
    embed.set_image(url="https://cdn.weeb.sh/images/ByoCoT_vW.gif")
    await ctx.send(embed=embed) #This sends the message in the DMs change to "ctx.send" to send it in chat

@bot.command()
async def python(ctx):
    embed = discord.Embed(title="", description=f"") #You can add a text in there if you want
#embed.add_field(name="**Add something**", value="Or delete this.", inline=False) 
    embed.set_image(url="https://cdn.discordapp.com/attachments/964608273762365443/970733010381062185/1200px-Python-logo-notext.svg.png")
    await ctx.send(embed=embed) #This sends the message in the DMs change to "ctx.send" to send it in chat

@bot.command()
async def meme(ctx):
 possible_responses = [
        'https://i.redd.it/26hypslsn1x81.jpg',
        'https://i.redd.it/znn3oeft41x81.gif',
        'https://i.redd.it/b5j9dh9bw1x81.jpg',
        'https://i.redd.it/d67bkddc03x81.jpg',
        'https://i.redd.it/09szzkuhg4x81.png',
        'https://i.redd.it/nsdgp4uho4x81.gif',
        'https://i.redd.it/ctd81c64l0x81.jpg',
        'https://i.redd.it/6zvmpjre60x81.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988072516878356/imagem_2021-04-13_103209.png',
        'https://media.discordapp.net/attachments/796871137530347520/955801510078476390/SPOILER_FKAjDQAXMAAVoFz.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988284039798874/IMG_2429.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988573601968148/images_48.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988712391503922/Screenshot_2022_0503_153102.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970992679674605588/SmartSelect_20220503-201718_Gallery.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970998007606702130/unknown-2-1.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970998860006703154/unknown.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970999001304404008/image0-1.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/971003432011956224/gayshit.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/971003523934326784/TimeForSex.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/971003961429602314/FB_IMG_1651220080756.jpg',
        'https://i.redd.it/26hypslsn1x81.jpg',
        'https://i.redd.it/znn3oeft41x81.gif',
        'https://i.redd.it/b5j9dh9bw1x81.jpg',
        'https://i.redd.it/d67bkddc03x81.jpg',
        'https://i.redd.it/09szzkuhg4x81.png',
        'https://i.redd.it/nsdgp4uho4x81.gif',
        'https://i.redd.it/ctd81c64l0x81.jpg',
        'https://i.redd.it/6zvmpjre60x81.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988072516878356/imagem_2021-04-13_103209.png',
        'https://media.discordapp.net/attachments/796871137530347520/955801510078476390/SPOILER_FKAjDQAXMAAVoFz.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988284039798874/IMG_2429.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988573601968148/images_48.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970988712391503922/Screenshot_2022_0503_153102.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970992679674605588/SmartSelect_20220503-201718_Gallery.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/970998007606702130/unknown-2-1.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970998860006703154/unknown.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/970999001304404008/image0-1.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/971003432011956224/gayshit.png',
        'https://cdn.discordapp.com/attachments/934062419733536768/971003523934326784/TimeForSex.jpg',
        'https://cdn.discordapp.com/attachments/934062419733536768/971003961429602314/FB_IMG_1651220080756.jpg',
        'https://i.redd.it/a3s9ojszx6x81.jpg',
        'https://i.redd.it/cp5tn8gt52x81.jpg',
        'https://i.redd.it/bw3kxylvh7x81.jpg',
        'https://i.redd.it/fooa7ao7q2x81.jpg',
        'https://i.redd.it/cz1xi6wzv2x81.gif',
        'https://i.redd.it/4kek57sk57x81.gif',
        'https://i.redd.it/z22zr6dcj8x81.png',
        'https://i.redd.it/2b1bdhd4p3x81.png',
        'https://i.redd.it/h7wzmqblz1x81.jpg',
        'https://i.redd.it/1qjj6r38iwv81.jpg',
        'https://i.redd.it/4nx3lzcturv81.jpg',
        'https://i.redd.it/es4h5a9zfmv81.jpg',
        'https://i.redd.it/98uqhrr0rlv81.jpg',
        'https://i.redd.it/mp8jd6moepv81.gif',
        'https://i.redd.it/7uzcxa2mipv81.jpg',
        'https://i.redd.it/4nx3lzcturv81.jpg',
        'https://i.redd.it/es4h5a9zfmv81.jpg',
        'https://i.redd.it/98uqhrr0rlv81.jpg',
        'https://i.redd.it/mp8jd6moepv81.gif',
        'https://i.redd.it/7uzcxa2mipv81.jpg',
]
 await ctx.send(random.choice(possible_responses))

@bot.command()
async def info(ctx):
  embed = discord.Embed(title="**Information**", description="*Created by NeWacho#0001*")
  embed.add_field(name="Created on 4/0/22", value="Moment of writing: 5/3/22")
  embed.add_field(name="** **", value="** **")
  embed.add_field(name="** **", value="** **")
  embed.add_field(name="Themes of the bot:", value="Fun and moderation!")
  embed.add_field(name="** **", value="** **")
  embed.add_field(name="** **", value="** **")
  embed.add_field(name="Beta testing", value="We are currently open for beta testers, for more info type !betatesters")

  await ctx.send(embed=embed)

@bot.command()
async def betatesters(ctx):
  embed = discord.Embed(title="**Beta testing**", description="By NeWacho#0001")
  embed.add_field(name="We are looking for beta testers", value="Welcome, you've had interest of participating in beta testing of discord.py bot? Great! In order to do that, you'd have to apply. Only few would be selected (currently 0/10). Good luck! https://docs.google.com/forms/d/1u11Du9Y43J3YBCstj7gRXw5NSlP5ieezPRJTwOs_UA8/viewform?edit_requested=true")

  await ctx.send(embed=embed)

@bot.command()
async def alert(ctx):
  embed = discord.Embed(title="**Beta testing**", description="By NeWacho#0001")
  embed.add_field(name="We are looking for beta testers", value="Welcome, you've had interest of participating in beta testing of discord.py bot? Great! In order to do that, you'd have to apply. Only few would be selected (currently 0/10). Good luck! https://docs.google.com/forms/d/1u11Du9Y43J3YBCstj7gRXw5NSlP5ieezPRJTwOs_UA8/viewform?edit_requested=true")

  await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
 possible_responses = [
   'You use discord cause you cant socialize irl, BUT STILL FAIL! HAHHA LOSER',
   'You are what happens when women drink during pregnancy',
'When I look at you, I wish I could meet you again for the first time… and walk past.',
'You are the sun in my life… now get 93 million miles away from me.',
'You have such a beautiful face… But let’s put a bag over that personality.',
'There is someone out there for everyone. For you, it’s a therapist.',
'I would smack you, but I’m against animal abuse.',
'If I wanted to kill myself, I would simply jump from your ego to your IQ.',
'I can’t wait to spend my whole life without you.',
'Whoever told you to be yourself, gave you a bad advice',
'I didn’t mean to offend you… but it was a huge plus.',
'I don’t hate you, but if you were drowning, I would give you a high five.',
'If I throw a stick, will you leave me too?',
'Sorry I can’t think of an insult dumb enough for you to understand.',
'I don’t know what makes you so stupid, but it works.',
'Whatever doesn’t kill you, disappoints me.',
'It is hilarious how you are trying to fit your entire vocabulary into one sentence.',
'I like the way you comb your hair, so horns don’t show up.',
'Have a nice day… somewhere else.',
'I told my therapist about you; she didn’t believe me.',
'Did you know your incubator had tinted windows? That explains a lot.',
'The last time I saw something like you, it was behind metal grids.',
'If I had a dollar every time you shut up, I would give it back as a thank you.',
'You were so happy for the negativity of your Covid test, we didn’t want to spoil the happiness by telling you it was IQ test.',
'Honey, only thing bothering me is placed between your ears.',
'Only thing that is pleasing about our relationship is that you are no longer in it.',

]
 await ctx.send(random.choice(possible_responses))
 await ctx.send('https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg')

@bot.command()
async def roast(ctx):
 possible_responses = [
   'You use discord cause you cant socialize irl, BUT STILL FAIL! HAHHA LOSER',
   'You are what happens when women drink during pregnancy',
'When I look at you, I wish I could meet you again for the first time… and walk past.',
'You are the sun in my life… now get 93 million miles away from me.',
'You have such a beautiful face… But let’s put a bag over that personality.',
'There is someone out there for everyone. For you, it’s a therapist.',
'I would smack you, but I’m against animal abuse.',
'If I wanted to kill myself, I would simply jump from your ego to your IQ.',
'I can’t wait to spend my whole life without you.',
'Whoever told you to be yourself, gave you a bad advice',
'I didn’t mean to offend you… but it was a huge plus.',
'I don’t hate you, but if you were drowning, I would give you a high five.',
'If I throw a stick, will you leave me too?',
'Sorry I can’t think of an insult dumb enough for you to understand.',
'I don’t know what makes you so stupid, but it works.',
'Whatever doesn’t kill you, disappoints me.',
'It is hilarious how you are trying to fit your entire vocabulary into one sentence.',
'I like the way you comb your hair, so horns don’t show up.',
'Have a nice day… somewhere else.',
'I told my therapist about you; she didn’t believe me.',
'Did you know your incubator had tinted windows? That explains a lot.',
'The last time I saw something like you, it was behind metal grids.',
'If I had a dollar every time you shut up, I would give it back as a thank you.',
'You were so happy for the negativity of your Covid test, we didn’t want to spoil the happiness by telling you it was IQ test.',
'Honey, only thing bothering me is placed between your ears.',
'Only thing that is pleasing about our relationship is that you are no longer in it.',

]
 await ctx.send(random.choice(possible_responses))

@bot.command()
async def trivia(ctx):
  possible_responses = [
    'What does “www” stand for in a website browser?',
    'How long is an Olympic swimming pool (in meters)?',
    'What countries made up the original Axis powers in World War II?',
    'What geometric shape is generally used for stop signs?',
    'What is "cynophobia"?',
    'What punctuation mark ends an imperative sentence?',
    'How many languages are written from right to left?',
    'What is the name of the biggest technology company in South Korea?',
    'What was the first toy to be advertised on television?',
    'What was the first feature-length animated movie ever released? (Hint: It was a Disney Movie)'
    'What TV series showed the first interracial kiss on American network television?',
    'What were the four main characters names in the TV series "Golden Girls" that ran from 1985-1992?',
    'Who created Sherlock Holmes?',
    'What are the names of Cinderella’s stepsisters?',
    'The biggest selling music single of all time is?',
    'When Walt Disney was a child, which character did he play in his school function?',
  ]
  
  embed = discord.Embed(title="Trivia question", description=f"{random.choice(possible_responses)}")
  await ctx.send(embed=embed)

@bot.command()
async def next(ctx):
  possible_responses = [
    'What does “www” stand for in a website browser?',
    'How long is an Olympic swimming pool (in meters)?',
    'What countries made up the original Axis powers in World War II?',
    'What geometric shape is generally used for stop signs?',
    'What is "cynophobia"?',
    'What punctuation mark ends an imperative sentence?',
    'How many languages are written from right to left?',
    'What is the name of the biggest technology company in South Korea?',
    'What was the first toy to be advertised on television?',
    'What was the first feature-length animated movie ever released? (Hint: It was a Disney Movie)'
    'What TV series showed the first interracial kiss on American network television?',
    'What were the four main characters names in the TV series "Golden Girls" that ran from 1985-1992?',
    'Who created Sherlock Holmes?',
    'What are the names of Cinderella’s stepsisters?',
    'The biggest selling music single of all time is?',
    'When Walt Disney was a child, which character did he play in his school function?',
  ]
  
  embed = discord.Embed(title="Trivia question", description=f"{random.choice(possible_responses)}")
  await ctx.send(embed=embed)

#Command call example: !hello @Mr_Spaar
#Discord.py will transform the mention to a discord.Member object
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.mention}')

#Command call example: !announce A new version of my bot is available!
#"content" will contain everything after !announce (as a single string)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def announce(ctx, *, content):
  embed = discord.Embed(title="Announcement", description=f"From {ctx.message.author.mention}")
  embed.add_field(name="The announcement:", value=f"{content}")
  await ctx.send(embed=embed)

@bot.command()
async def quiz(ctx):
    embed = discord.Embed(title="", description="")
  
    embed.add_field(name='Who killed John F Kennedy?', value = " A - Lee Harvey Oswald, B -  John C. McAdams, C - Vincent Bugliosi.")
    embed.set_footer(text="You have 12 seconds")
    await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

    except asyncio.TimeoutError:
     await ctx.send('You took too long...')

    else:
        if msg.content == "A":
            await ctx.send("<:314691591484866560:967764141416783932> That is correct! Next question:")
            embed = discord.Embed(name="", description="")
            embed.add_field(name="Which British king was famous for having six wives?", value = 'A. King George the 6th B. King George the 5th C. King George the 3rd D. Henry the 8th')
            embed.set_footer(text="You have 11 seconds")
            await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=11.0)

    except asyncio.TimeoutError:
     await ctx.send('You took too long...')

    else:
        if msg.content == "D":
            await ctx.send("<:314691591484866560:967764141416783932> That is correct! Next question:")
            embed = discord.Embed(name="", description="")
            embed.add_field(name=" In a bingo game, which number is represented by the phrase “two little ducks”?", value = 'A - 19 B - 22, C - 45 or D - 2')
            embed.set_footer(text="You have 9 seconds")
            await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=9.0)

    except asyncio.TimeoutError:
     await ctx.send('You took too long...')

    else:
        if msg.content == "B":
            await ctx.send("<:314691591484866560:967764141416783932> That is correct! Next question:")
            embed = discord.Embed(name="", description="")
            embed.add_field(name=" According to Greek mythology, who was the first woman on earth?", value = 'A - Pandora, B - Samora, C - Faora or D - Maora')
            embed.set_footer(text="You have 7 seconds")
            await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=7.0)

    except asyncio.TimeoutError:
     await ctx.send('You took too long...')

    else:
        if msg.content == "A":
            await ctx.send("<:314691591484866560:967764141416783932> That is correct! Next question:")
            embed = discord.Embed(name="", description="")
            embed.add_field(name=" Which singer’s real name is Stefani Joanne Angelina Germanotta?", value = 'A - Lady Gaga, B - Taylor swift, C - Madonna or D - Rihanna')
            embed.set_footer(text="You have 5 seconds")
            await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=5.0)

    except asyncio.TimeoutError:
     await ctx.send('You took too long...')
    else:
          if msg.content == "A":
            await ctx.send("<:314691591484866560:967764141416783932> That is correct! Next question:")
            embed = discord.Embed(name="", description="")
            embed.add_field(name="The only known monotremes in the animal kingdom are the echidna and which other creature?", value = 'A - The platypus, B - Monkeys, C - Gorillas or D - Human')
            embed.set_footer(text="You have 5 seconds")
            await ctx.send(embed=embed)

    try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=5.0)

    except asyncio.TimeoutError:
     await ctx.send('You took too long...')

    else:
        if msg.content == "A":
          await ctx.send("<:314691591484866560:967764141416783932> That is correct!")
          embed = discord.Embed(title='', description="")
          embed.add_field(name=f"Quiz ended!", value=f":tada: {ctx.message.author.mention} won :tada:")
          await ctx.send(embed=embed)
        else:
            await ctx.send("<:314691684455809024:967760470633222184> Wrong!")

@bot.command()
async def nitro(ctx):
  await ctx.send('disсоrd.gift/OAS94J6H9SK44 https://cdn.discordapp.com/attachments/964886252711190549/972099887971835954/nitro.png')


@bot.command()
async def fuck(ctx):
 possible_responses = [
'You use discord cause you cant socialize irl, BUT STILL FAIL! HAHHA LOSER',
'You are what happens when women drink during pregnancy',
'When I look at you, I wish I could meet you again for the first time… and walk past.',
'You are the sun in my life… now get 93 million miles away from me.',
'You have such a beautiful face… But let’s put a bag over that personality.',
'There is someone out there for everyone. For you, it’s a therapist.',
'I would smack you, but I’m against animal abuse.',
'If I wanted to kill myself, I would simply jump from your ego to your IQ.',
'I can’t wait to spend my whole life without you.',
'If I wanted to kill myself, I would simply jump from your ego to your IQ.',
'I can’t wait to spend my whole life without you.',
'If I wanted to kill myself, I would simply jump from your ego to your IQ.',
'I can’t wait to spend my whole life without you.',
]
 await ctx.send(random.choice(possible_responses))

@bot.command()
async def code(ctx):
  await ctx.send(f'{ctx.message.author.mention} bro u fr thought id give u 1000+ lines code?')

"""
1st Value is item name
2nd Value is description
3rd value is the price to buy and 4th value is the price to sell
5th Value is if you can buy it
6th Value is if it is useable
7th value is the ID for the item
"""
great_shop = [["Cube", "A fun collectible you can use to get cubing", "200", "35", True, False, "cube"], ["Laptop", "A laptop used for certain commands such as ``c pct``", "3750", "1000", True, False, "laptop"], ["Alcohol", "What you can use to bet on certain commands and get more coins if you win but lose more coins if you lose!", "8000", "2500", True, True, "alcohol"], ["Padlock", "Use this item to protect yourself from getting robbed", "10000", "3500", True, True, "padlock"], ["Textbook", "An item that will help you get better jobs: check the list using ``c work list``", "15000", "4000", True, False, "book"], ["Fishing Pole", "An item that is very important when you want to fish (obviously)", "20000", "5500", True, False, "fishingpole"], ["Trout", "A fish that you can get and is common", "You can't buy this.", "50", False, False, "trout"], ["Mackeral", "A fish that you can get and is also common", "You can't buy this", "75", False, False, "mackeral"], ["Turtle", "An aquatic creature that is rare", "You can't buy this", "800", False, False, "turtle"], ["Jellyfish", "An aquatic creature that is quite rare", "You can't buy this", "900", False, False, "jellyfish"], ["Octopus", "An aquatic creature that is rare and can be sold for some money", "You can't buy this", "999", False, False, "octopus"], ["Whale", "A legendary fish that for some reason people can't catch", "You can't buy this", "5000", False, False, "whale"], ["Shark", "A totally uncommon fish that you came across and was actually able to get.", "You can't buy this item.", "15500", False, False, "shark"], ["Coin Fish", "The most epic fish in the world that almost no one has seen", "You can't buy this", "275830", False, False, "coinfish"], ["Game", "A collectible in which you can collect games to be a great gamer!", "50000", "18000", True, False, "game"], ["Senic", "A rare collectible that is combined with the fast sanic and the best letter in the whole world: :regional_indicator_e:", "1750000", "500000", True, False, "senic"], ["Ultimate Gold Coin", "Such an amazing coin that few have the money to buy it.", "25000000", "7500000", True, False, "ultimategoldcoin"]]

@bot.event
async def on_ready():
    global amounts
    try:
      with open('amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        amounts = {}
    print("Bot online!")

@bot.command(aliases=['help_command'])
async def helpcur(ctx, type_help = "None", page=1):
  if type_help == "None":
    embed = discord.Embed(title="Help Command", description = "Welcome to the Help Command. Look at what commands the bot has to offer! If there is a <> around some words, that means that what you put to substitute those words are optional Also [] around some words means that an input is required. However, first you need to choose what category you need help with. Type in the page number if you want also.", color = discord.Colour.blue())
    embed.add_field(name = "``c help currency``", value = "Used if you need help with the currency system for the bot.", inline = False)
    embed.add_field(name = "``c help moderation``", value = "Commands that will help you run the server.", inline = False)
    embed.add_field(name = "``c help work``", value = "Work has its own category because this bot has to do with business. Commands have to do with work. It can overlap with ``c help currency`` but not really.", inline = False)
  elif type_help == "currency":
    if page == 1:
      embed = discord.Embed(title="Help Currency Command", description = "Here are all the commands having to do with currency and about them: ", color = discord.Colour.green())
      embed.add_field(name = "c bal <user>", value = "See how much money you have in your wallet and bank or what other users have in their wallet and bank.", inline = False)
      embed.add_field(name = "c beg", value = "When you want more money and you hope that someone gives some to you by using this command.", inline = False)
      embed.add_field(name = "c buy [item] <amount>", value = "Just buy an item from the shop, that's all.", inline = False)
      embed.add_field(name = "c betbot", value = "Bet against the bot a certain amount of coins.", inline = False)
      embed.add_field(name = "c betplayer <player>", value = "Bet some coins against a player. Follow the instructions that the bot says in order to see what outcome you have.", inline = False)
      embed.add_field(name = "c daily", value = "Be glad to get your daily number of coins.", inline = False)
      embed.add_field(name = "c dep [amount]", value = "Deposit money into your bank based on how much money you want to go in your bank", inline = False)
      embed.add_field(name = "c fish", value = "Get some fish using your trusty fishing pole.", inline = False)
      embed.add_field(name = "c hackathon", value = "Participate in some hackathons that you might have to pay for to get coins. You don't have to do anything for this just watch what results you get. However, if you do get a lot of coins and use this command, this command could possibly make you lose lots and lots of coins so just be careful and you might get lucky.")
      embed.add_field(name = "c inv", value = "See what items you have in your inventory", inline = False)
      embed.add_field(name = "c pct", value = "Just post some coding projects not only for upvotes but for coins.", inline = False)
      embed.add_field(name = "c rich", value = "See who the richest people are using the bot ~~so you can rob them~~")
      embed.set_footer(text=f"Page {page} out of 2")
    elif page == 2:
      embed = discord.Embed(title="Help Currency Command", description = "Here are all the commands having to do with currency and about them: ", color = discord.Colour.green())
      embed.add_field(name = "c rob", value = "Rob someone because they have a lot of coins or some other reason. Try not to get caught by the police!", inline = False)
      embed.add_field(name = "c search", value = "When you go to a certain place to look for some coins.", inline = False)
      embed.add_field(name = "c shop", value = "When you go into the great shop and look for items you might want to buy", inline = False)
      embed.add_field(name = "c stats <user>", value = "See your\'s or other\'s stats (like money and number of commands)", inline = False)
      embed.add_field(name = "c stream", value = "Stream a video, post it, and see how many views, likes or dislikes, and coins you get. This command can be risky though so watch out...")
      embed.add_field(name = "c with [amount]", value = "Withdraw money out from the bank and put it into your wallet", inline = False)
    else:
      await ctx.send(f"Um no such page number as {page}")
  elif type_help == "moderation":
    if page == 1:
      embed = discord.Embed(title = "Help Moderation Command", description = "Here are all the commands that have to with moderating a server and about them: ", color = discord.Colour.green())
      embed.add_field(name = "c ban [user] <reason>", value = "Ban people who are not paying attention to the server rules are for other reasons.", inline = False)
      embed.add_field(name = "c remove <amount>", value = "Remove messages for some reason...", inline = False)
      embed.add_field(name = "c unban [user]", value = "Unban people because of some random reason.", inline = False)
      embed.add_field(name = "c suggest [suggestion]", value = "Suggest things that will be able to help the bot or improve the server.", inline = False)
      embed.add_field(name = "c decision [number] [accepted?] <reason>", value = "Decide if a suggestion is approved or rejected and why that decision was made.", inline = False)
      embed.set_footer(text=f"Page {page} out of 1")
    else:
      await ctx.send(f"Um no such page number as {page}")
  elif type_help == "work":
    embed = discord.Embed(title = "Help Work Command", description = "Here are all the commands that have to do with the collection of work commands and about them:", color = discord.Colour.green())
    if page == 1:
      embed.add_field(name = "c work list", value = "Simply look at the work list too see what job you want to take on and the requirements you need to take on the job", inline = False)
      embed.set_footer(text = f"Page {page} out of 1")
    else:
      await ctx.send(f"Um no such page number as {page}")
  else:
    embed = discord.Embed(title = "What?", description = f"There is no category named {type_help} for help so look back at the ``c help`` command to see what categories you can look at.")
  await ctx.send(embed=embed)

@bot.command()
async def stats(ctx, user:discord.Member=None):
  user=ctx.author if not user else user
  uid = str(user.id)
  if not uid in amounts:
    amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': '0'}
  embed = discord.Embed(title=f"{user.name}\'s Stats", description = "Here are your stats with this bot:", color = discord.Colour.blue())
  embed.add_field(name = "Balance Stats", value = f"Wallet: {amounts[uid]['coins']} \nBank: {amounts[uid]['bank-coins']}/{amounts[uid]['bank-space']}", inline = False)
  embed.add_field(name = "Command Stats", value = f"Total Commands: {amounts[uid]['commands']}")
  string = ""
  if amounts[uid]['job'] == "None":
    string = "Currently doesn't have a job"
  else:
    string = f"Currently works as a {amounts[uid]['job']}"
  embed.add_field(name = "Current Job", value = string, inline = False)
  await ctx.send(embed=embed)
  _save()
   
@bot.command(aliases=['bal', 'money'])
async def balance(ctx, user:discord.Member=None):
    user=ctx.author if not user else user
    uid = str(user.id)
    if not uid in amounts:
        amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
    await ctx.send(embed = discord.Embed(title=f"{user.name}\'s Balance :money_mouth:", description=f'{user.name} has **{amounts[uid]["coins"]}** coins in the users wallet.\n{user.name} has **{amounts[uid]["bank-coins"]}/{amounts[uid]["bank-space"]}** coins in the bank.\n{user.name} has a total amount of **{amounts[uid]["coins"] + amounts[uid]["bank-coins"]}** coins.', color = discord.Colour.green()))
    amounts[uid]['bank-space'] += random.randint(1, 50)
    amounts[uid]['commands'] += 1
    _save()  

@bot.command()
async def shop(ctx):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  embed = discord.Embed(title="The Great Shop", description = "Where you can buy items", color = discord.Colour.blue())
  for i in range(len(great_shop)):
    if great_shop[i][4] == True:
      embed.add_field(name=(great_shop[i][0] + " - " + great_shop[i][2] + " coins - ID: ``" + great_shop[i][6] + "``"), value = great_shop[i][1], inline = False)
  amounts[uid]['bank-space'] += random.randint(1, 50)
  amounts[uid]['commands'] += 1
  await ctx.send(embed=embed)
  _save()

@bot.command()
async def buy(ctx, item, amount=1):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  for i in range(len(great_shop)):
    if great_shop[i][6].lower() == item.lower():
      if str(amount).isdigit():
        if amounts[uid]['coins'] >= (int(great_shop[i][2]) * int(amount)) and amount >= 1:
          try:
            amounts[uid][great_shop[i][6].lower()] += amount
          except KeyError:
            amounts[uid][great_shop[i][6].lower()] = 0
            _save()
            amounts[uid][great_shop[i][6].lower()] += amount
          amounts[uid]['bank-space'] += random.randint(1, 50)
          amounts[uid]['commands'] += 1
          await ctx.send(embed = discord.Embed(title="Transaction Complete", description=f"You got {amount} {(great_shop[i][0]).lower()}s for {int(great_shop[i][2]) * amount} coins.", color = discord.Colour.green()))
          amounts[uid]['coins'] -= (int(great_shop[i][2]) * int(amount))
          _save()
          break
        else:
          await ctx.send("Are you ok? Because you don't have enough money to buy this many items or you can't buy 0 or negative number of items.")
          break
      else:
        await ctx.send("You need to enter in an integer stupid.")
        break
    elif great_shop[i][6].lower() != item.lower() and i == len(great_shop) - 1:
      await ctx.send("You should check the shop using ``c shop`` in order to buy items because you put in an item taht does not exist.")

@bot.command(aliases=['inventory'])
async def inv(ctx):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  keys_list = list(amounts[uid])
  values = amounts[uid].values()
  values_list = list(values)
  embed = discord.Embed(title="Your Inventory:", description="Here are what items you have in your inventory: ", color = discord.Colour.blue())
  embed1 = discord.Embed(title = "Your Inventory:", description="Unfortunately, you have nothing in your inventory.", color = discord.Colour.orange())
  inventory_items = False
  for i in range(9, len(amounts[uid])):
    if values_list[i] != 0:
      inventory_items = True
      embed.add_field(name=f"{keys_list[i]}", value = f"{values_list[i]} owned", inline = False)
  if inventory_items == False:
    await ctx.send(embed=embed1)
  else:
    await ctx.send(embed=embed)
  amounts[uid]['bank-space'] += random.randint(1, 50)
  amounts[uid]['commands'] += 1
  _save()

@bot.command()
async def sell(ctx, item, amount=1):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  for i in range(len(great_shop)):
    if great_shop[i][6].lower() == item.lower():
      if str(amount).isdigit():
        if amount <= amounts[uid][great_shop[i][6].lower()]:
          earn_coins = int(great_shop[i][3]) * amount
          amounts[uid][great_shop[i][6].lower()] -= amount
          amounts[uid]['coins'] += earn_coins
          await ctx.send(embed=discord.Embed(title="Transaction Complete", description=f"You sold {amount} {(great_shop[i][0]).lower()}s for a total of {earn_coins} coins.", color = discord.Colour.green()))
          amounts[uid]['bank-space'] += random.randint(1, 50)
          amounts[uid]['commands'] += 1
          _save()
          break
        else:
          await ctx.send("Are you ok? Check your items using ``c inv`` next time because you don't even have that many items.")
          break
      else:
        await ctx.send("Stupid for the amount you need to put **a number that is at least 1**")
        break
    elif great_shop[i][6].lower() != item.lower() and i == len(great_shop) - 1:
      await ctx.send("Seroiusly you need to check the shop using ``c shop`` to find the id that you are using because the item you put does not exist.")
  _save()

@bot.command()
async def use(ctx, item):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  for i in range(len(great_shop)):
    try:
      if great_shop[i][6] == item and great_shop[i][5] == True and amounts[uid][great_shop[i][6]] >= 1:
        name = item + "_use"
        if amounts[uid][name] == False:
          amounts[uid][great_shop[i][6]] -= 1
          amounts[uid][name] = True
          title = f"You successfully used the {great_shop[i][6]} item!"
          color = discord.Colour.green()
          if great_shop[i][6] == "alcohol":
            amounts[uid]['alcohol_times'] = 10
            description = "You used the alcohol item and you are not drunk! Now for the next 10 bets or whatever gambling command you use, you can earn twice the money if you win but lose twice the money if you lose."
            break
          elif great_shop[i][6] == "padlock":
            description = "Nice, you used the padlock item. Now the person who robs you next time will only have a 0.1% chance of being able to rob your wallet!"
            break
        else:
          await ctx.send(f"You are already using the {great_shop[i][6]} item!")
          break
      elif great_shop[i][6] != item and great_shop[i][5] != True and amounts[uid]  [great_shop[i][6]] == 0 and i == len(great_shop) - 1:
        print("f")
        print(i)
        title = "What?"
        description = "I have no clue you need to check your inventory or something cause you can't use this item or don't have the item."
        color = discord.Colour.orange()
    except KeyError:
      title = "What?"
      description = "I have no clue you need to check your inventory cause you can't use this item or don't have the item."
      color = discord.Colour.orange()
  _save()
  await ctx.send(embed=discord.Embed(title=title, description=description, color=color))

"""
1st item is job name
2nd item is the description
3rd item is the salary
4th item is the wallet req
5th item is the bank space req
6th item is the book req
7th item is a dictionary of req items
8th item is the id
9th item is the page number
"""
jobs = [["Student", "You are a student and just learning things.", "100 - 500", "0", "50", "0", {"cube": 1}, "student", "1"], ["Youtuber", "Go on YouTube and stream some nice videoes.", "250 - 1000", "250", "150", "0", {"cube": 3}, "youtuber", "1"], ["Internet Surfer", "You are a random person who took on a job in which you surf the Internet idk.", "750 - 1500", "1000", "1500", "0", {"cube": 5, "laptop": 2}, "surfer", "2"]]

@bot.command()
async def work(ctx, job_action = "none", page = "1"):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  if job_action == "list":
    embed = discord.Embed(title = "The Great Job List", description = "This is called Anonymous Business Coder for a reason. The work commands will be one of the largest commands that this bot has to offer. To pick the jobs you want, simply do ``c work [id]`` Here are the possible jobs you can get with this bot:\n", color = discord.Colour.blue())
    job_found = False
    for i in range(len(jobs)):
      if page == jobs[i][8]:
        job_found = True
        list_of_items = ""
        for a in range(len(jobs[i][6])):
          keys_list = list(jobs[i][6].keys())
          values_list = list(jobs[i][6].values())
          list_of_items += f"\n{keys_list[a].capitalize()}: {values_list[a]}"
        embed.add_field(name = f"==============================================\n__{jobs[i][0]}__", value = f"Description: {jobs[i][1]}\nSalary: {jobs[i][2]}\n\n**Requirements:**\nWallet Coins: {jobs[i][3]}\nBankspace Needed: {jobs[i][4]}\nBooks Needed: {jobs[i][5]}\n\n**Items Needed:** {list_of_items}\n\n**Getting ID:**\nIf you want to get this job use the id ``{jobs[i][7]}``.", inline = False)
        embed.set_footer(text = f"Page {page} out of 2")
      elif page != jobs[i][8] and i == len(jobs) - 1 and job_found == False:
        await ctx.send(f"Currently, there is no page {page} so I have no clue what you are doing...")
      if i == len(jobs) - 1 and job_found == True:
        await ctx.send(embed=embed)
  elif job_action == "resign":
    await ctx.send("In Progress")
  elif job_action == "none":
    await ctx.send("In Progress")
  else:
    for i in range(len(jobs)):
      if job_action == jobs[i][7]:
        list_of_req = ""
        for b in range(len(jobs[i][6])):
          keys_list = list(jobs[i][6].keys())
          values_list = list(jobs[i][6].values())
          try:
            if amounts[uid][keys_list[b]] >= values_list[b]:
              await ctx.send("Yes")
            else:
              list_of_req += f"\nYou need {values_list[b] - amounts[uid][keys_list[b]]} more {keys_list[b]} items."
            print(list_of_req)
          except KeyError:
            list_of_req += f"You need {values_list[b] - amounts[uid][keys_list[b]]} more {keys_list[b]} items."
            print(list_of_req)
        break
      elif job_action != jobs[i][7] and i == len(jobs) - 1:
        await ctx.send(f"Look at the list by typing in the command ``c job list`` again because apparently, there is no id name ``{job_action}`` in the job list.")

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@bot.command()
async def daily(ctx):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  if amounts[uid]['dailytime'] == 0:
    coins = random.randint(5000, 10000)
    await ctx.send(f"Here you have like {coins} coins.")
    amounts[uid]['dailytime'] = myconverter(datetime.datetime.now())
    amounts[uid]['coins'] += coins
    amounts[uid]['bank-space'] += random.randint(1, 50)
    amounts[uid]['commands'] += 1
  else:
    time_conversion = datetime.datetime.strptime(str(amounts[uid]['dailytime']), "%Y-%m-%d %H:%M:%S.%f")
    time_conversion1 = datetime.datetime.strptime(myconverter(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
    change_day = time_conversion + timedelta(days=1)
    time_difference = change_day - time_conversion1
    total_seconds1 = round(time_difference.total_seconds())
    if total_seconds1 < 0:
      coins = random.randint(5000, 10000)
      await ctx.send(f"Here you have like {coins} coins.")
      amounts[uid]['dailytime'] = (myconverter(datetime.datetime.now()))
      amounts[uid]['coins'] += coins
      amounts[uid]['bank-space'] += random.randint(1, 50)
      amounts[uid]['commands'] += 1
    else:
      coins = 0
      hours = math.floor(total_seconds1/3600)
      minutes = math.floor(((total_seconds1) - (hours * 3600))/60)
      seconds = round((total_seconds1) - (hours*3600) - (minutes*60))
      await ctx.send(embed = discord.Embed(title="Cooldown Active", description=f"Stop using this command because literally it\'s called daily for a reaosn. Wait {hours} hours, {minutes} minutes, {seconds} seconds before getting your daily number of coins.", color = discord.Colour.orange()))
    coins = 0
  _save()

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def rob(ctx, user:discord.Member="None"):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  if user == "None":
    await ctx.send("You need to provide a **user** to rob because you can't just rob no one.")
  elif user.name == ctx.author.name:
    await ctx.send("Don't even try robbing yourself because you already own the coins and blah blah blah do you have common sense?")
  else:
    if amounts[uid]['coins'] < 1500:
      await ctx.send("You need at least 1500 coins to rob.")
    else:
      if amounts[str(user.id)]['coins'] < 1500:
        await ctx.send("The person you are robbing is too poor don't try it.")
      else:
        if amounts[str(user.id)]['padlock_use'] == True:
          amounts[str(user.id)]['padlock_use'] = False
          coin_chances = random.random()
          if coin_chances <= 0.7:
            loss_percentage = random.randint(25, 50)
            coins1 = int(amounts[uid]['coins'] * (loss_percentage/100) * -1)
            coins2 = coins1 * -1
            title = "The person you tried to rob had a padlock and you didn't succeed getting the money!"
            description = f"You at least broke the padlock but it took too long because suddenly look who was standing in front of you {user.name}. The user demanded you gave some coins to the person and if you won't you will get tortured. You had no choice but to give the person {loss_percentage}% of your coins (aka {coins1 * -1} coins). Now you had {int(amounts[uid]['coins'] + coins1)} coins while {user.name} has {int(amounts[str(user.id)]['coins'] + coins2)} coins."
            color = discord.Colour.red()
            await user.send(f"{ctx.author.name} tried to rob you, but you had a padlock active and cool they had to pay you {coins2} coins!")
          elif coin_chances > 0.7 and coin_chances <= 0.9:
            loss_percentage = random.randint(25, 50)
            coins1 = int(amounts[uid]['coins'] * (loss_percentage/100) * -1)
            coins2 = 0
            title = "The person you tried to rob had a padlock and you didn't succeed getting the money!"
            description = f"Well, at least you broke the padlock. But you took too long because as soon as you know it, the police were there. You ended up having to pay a fine of {coins1 * -1} coins which is {loss_percentage}% less coins than what you had before and now you have {int(amounts[uid]['coins'] + coins1)} coins."
            color = discord.Colour.red()
            await user.send(f"{ctx.author.name} tried to rob you, but you had a padlock active and the police caught the user!")
          else:
            gain_percentage = random.randint(10, 50)
            coins2 = int(amounts[str(user.id)]['coins'] * (gain_percentage/100)) * -1
            coins1 = coins2 * -1
            if gain_percentage <= 25:
              title = "You stole a small chunk of the person's money!"
            else:
              title = "You stole a nice chunk of the person's money!"
            description = f"Nice, you were able to break the padlock and had enough time to get coins. However, you felt rushed because you didn't want the police to come so you stole {gain_percentage}% (aka {coins1} coins) of their coins now making them have {amounts[str(user.id)]['coins'] + coins2} coins and you having {amounts[uid]['coins'] + coins1} coins."
            color = discord.Colour.green()
            await user.send(f"{ctx.author.name} tried to rob you, but you had a padlock active **but** they were able to break it and get away with {coins1} coins.")
        else:
          coin_chances = random.random()
          if coin_chances <= 0.45:
            loss_percentage = random.randint(10, 50)
            coins1 = int(amounts[uid]['coins'] * (loss_percentage/100)) * -1
            coins2 = coins1 * -1
            title = "You tried to steal and the person didn't have a padlock but you failed!"
            description = f"Apparently, you tried to steal some money from the wallet except suddenly when you looked behind you saw {user.name} behind you! {user.name} threatened to give them some money so you ended giving the person {loss_percentage}% of the money (aka {coins2} coins) so now you have {amounts[uid]['coins'] + coins1} while {user.name} has a good amount of {amounts[str(user.id)]['coins'] + coins2}"
            color = discord.Colour.red()
            await user.send(f"{ctx.author.name} tried to rob you, and luckily they had to pay you {coins2} coins because they didn't succeed.")
          elif coin_chances > 0.45 and coin_chances <= 0.75:
            loss_percentage = random.randint(10, 50)
            coins1 = int(amounts[uid]['coins'] * (loss_percentage/100)) * -1
            coins2 = 0
            title = "You tried to steal and the person didn't have a padlock but you still failed!"
            description = f"You tried to steal money from their wallet and then suddenly you were handcuffed by the police and taken to jail. You had to pay a fine of {coins1 * -1} coins so therefore you have {loss_percentage}% less coins and now have {amounts[uid]['coins'] + coins1} coins."
            color = discord.Colour.red()
            await user.send(f"{ctx.author.name} tried to rob you, and luckily the police caught the user and the user had to pay a fine!")
          else:
            gain_percentage = random.randint(5, 90)
            coins2 = int(amounts[str(user.id)]['coins'] * (gain_percentage/100)) * -1
            coins1 = coins2 * -1
            if gain_percentage <= 25:
              title = "You stole a small chunk of the person's money."
            elif gain_percentage > 25 and gain_percentage <= 50:
              title = "You stole a nice chunk of the person's money."
            elif gain_percentage > 50 and gain_percentage <= 80:
              title = "You stole a good chunk of the person's money."
            else:
              title = "You stole a big chunk of the person's money."
            description = f"You stole their money easily and you did not take too long to steal it. Also, no one caught you robbing so that was great! You stole {gain_percentage}% of their money so now {user.name} has {amounts[str(user.id)]['coins'] + coins2} while you have {amounts[uid]['coins'] + coins1} coins."
            color = discord.Colour.green()
            await user.send(f"{ctx.author.name} robbed you and the user succeeded! They got away with {coins1} coins!")
        amounts[uid]['coins'] += coins1
        amounts[str(user.id)]['coins'] += coins2
        amounts[uid]['bank-space'] += random.randint(1, 50)
        amounts[uid]['commands'] += 1
        await ctx.send(embed=discord.Embed(title = title, description = description, color = color))
        _save()


@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def betplayer(ctx, user:discord.Member="None"):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  def check1(msg):
    try:
      return msg.content.lower() == "accept bet" and msg.author.id != int(uid) and amounts[str(msg.author.id)]['coins'] >= 1000
    except KeyError:
      return False
  def check2(msg):
    return msg.content.lower() == "accept bet" and msg.author.id == user.id
  def check3(msg):
    return msg.content.isdigit() and msg.author.id == ctx.author.id and int(msg.content) <= 500000 and int(amounts[uid]['coins']) > int(msg.content) and int(msg.content) >= 1000
  def check4(msg):
    try:
      return msg.content.isdigit() and msg.author.id == user.id and int(msg.content) <= 500000 and int(amounts[str(user.id)]['coins']) > int(msg.content) and int(msg.content) >= 1000
    except AttributeError:
      return msg.content.isdigit() and msg.author.id == author and int(msg.content) <= 500000 and int(amounts[str(msg.author.id)]['coins']) > int(msg.content) and int(msg.content) >= 1000
  person_good = False
  if amounts[uid]['coins'] >= 1000:
    try:
      if user == "None":
        message = await ctx.send(f"No players were requested. Anyone can type ``accept bet`` to bet against {ctx.author.name}. Whoever wants to do this has 1 minute to do so. The person must have at least 1,000 coins.")
        msg = await bot.wait_for("message", timeout=60, check=check1)
        person_good = True
      elif user != "None" and amounts[str(user.id)]['coins'] >= 1000 and user.id != ctx.author.id:
        message = await ctx.send(f"{user.mention} was requested for the bet. {user.name}, please type in ``accept bet`` if you accept this bet. You have 1 minute to do so.")
        msg = await bot.wait_for("message", timeout=60, check=check2)
        person_good = True
      else:
        await ctx.send("The person doesn't have **1000** coins like you do so you can't bet with them. You need to try again. Also, another reason why you could have gotten this message is because you can't bet with yourself.")
      if person_good == True:
        try:
          message = await ctx.send(f"{user.mention} has accepted the bet! {ctx.author.mention}, you will go first. You need to choose a number between 1000 and 500,000.")
        except AttributeError:
          message = await ctx.send(f"{msg.author.mention} has accepted the bet! {ctx.author.mention}, you will go first. You need to choose a number between 1000 and 500,000. You have 30 seconds to do so.")
        sum_of_bet = 0
        msg1 = await bot.wait_for("message", timeout=30, check=check3)
        msg1 = int(msg1.content)
        if amounts[uid]['alcohol_use'] == True:
          msg1 = msg1 * 2
          amounts[uid]['alcohol_times'] -= 1
          if amounts[uid]['alcohol_times'] == 0:
            amounts[uid]['alcohol_use'] = False
          await ctx.send(f"Well, you had alcohol so your bet actually came up to {msg1} coins.")
        try:
          message = await ctx.send(f"Cool, so now it is {user.mention}'s turn to choose a bet number. This will be added up at the end. Again, this has to be a number between 1000 and 500,000. Also, you have 30 seconds to do this.")
        except AttributeError:
          message = await ctx.send(f"Cool, so now it is {msg.author.mention}'s turn to choose a bet number. This will be added up at the end. Again, this has to be a number between 1000 and 500,000. Also, you have 30 seconds to do this.")
        author = msg.author.id
        msg2 = await bot.wait_for("message", timeout=30, check=check4)
        msg2 = int(msg2.content)
        if amounts[str(msg.author.id)]['alcohol_use'] == True:
          msg2 = msg2 * 2
          amounts[str(msg.author.id)]['alcohol_times'] -= 1
          if amounts[str(msg.author.id)]['alcohol_times'] == 0:
            amounts[str(msg.author.id)]['alcohol_use'] = False
          await ctx.send(f"Well, you had alcohol so your bet actually came up to {msg2} coins.")
        sum_of_bet = msg1 + msg2
        person1_roll = random.randint(1, 2)
        person2_roll = random.randint(1, 2)
        if person1_roll > person2_roll:
          coins1 = sum_of_bet
          coins2 = msg2 * -1
          title = f"{ctx.author.name} won!"
          description = f"Congratulations {ctx.author.name}, you won the bet! The total money that was betted is {sum_of_bet} coins. While {ctx.author.name} gets {amounts[uid]['coins'] + sum_of_bet} coins, unfortunately {msg.author.name} now has {amounts[uid]['coins'] - msg2} coins. Here are the results: \n\n{ctx.author.name} rolled {person1_roll}\n{msg.author.name} rolled {person2_roll}"
          description = f"Congratulations {ctx.author.name}, you won the bet! The total money that was betted is {sum_of_bet} coins. While {ctx.author.name} now has {amounts[uid]['coins'] + sum_of_bet} coins, unfortunately {msg.author.name} now has {amounts[str(msg.author.id)]['coins'] - msg2} coins. Here are the results: \n\n{ctx.author.name} rolled {person1_roll}\n{msg.author.name} rolled {person2_roll}"
          color = discord.Colour.green()
        elif person1_roll < person2_roll:
          coins1 = msg1 * -1
          coins2 = sum_of_bet
          title = f"{msg.author.name} won!"
          description = f"Congratulations {msg.author.name}, you won the bet! The total money that was betted is {sum_of_bet} coins. While {msg.author.name} now has {amounts[str(msg.author.id)]['coins'] + sum_of_bet} coins, unfortunately {ctx.author.name} has {amounts[uid]['coins'] - msg1} coins. Here are the results: \n\n{ctx.author.name} rolled {person1_roll}\n{msg.author.name} rolled {person2_roll}"
          color = discord.Colour.green()
        else:
          coins1 = int(sum_of_bet/4)
          coins2 = int(sum_of_bet/4)
          title = f"{ctx.author.name} and {msg.author.name} did not win or lose!"
          description = f"In fact, both of you got the same number. Therefore, we will divide the sum of the bet, {sum_of_bet}, by 2 and split it up for each of you. Therefore, each of you will get {int(sum_of_bet/4)} coins. {ctx.author.name} now has {amounts[uid]['coins'] + int(sum_of_bet/4)} coins while {msg.author.name} now has {amounts[str(msg.author.id)]['coins'] + int(sum_of_bet/4)} coins. Here are the results: \n\nBoth of you got {person1_roll}."
          color = discord.Colour.orange()
        amounts[uid]['coins'] += coins1
        amounts[str(msg.author.id)]['coins'] += coins2
        if amounts[uid]['coins'] < 0:
          await ctx.send(f"{ctx.author.name}, you had a negative amount of money. You already have insurance for this so they already paid your debt for you. You now have 0 coins again.")
          amounts[uid]['coins'] = 0
        elif amounts[str(msg.author.id)]['coins'] < 0:
          await ctx.send(f"{msg.author.name}, you had a negative amount of money. You already have insurance for this so they already paid your debt for you. You now have 0 coins again.")
          amounts[str(msg.author.id)]['coins'] = 0
        await ctx.send(embed=discord.Embed(title=title, description=description, color=color))
        amounts[uid]['bank-space'] += random.randint(1, 50)
        amounts[uid]['commands'] += 1
        _save()
    except asyncio.TimeoutError:
      await message.edit(content="No one ended up responding so the player bet was cancelled.")
  else:
    await ctx.send("You need **1000** coins to bet against a player are you fine?")

@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def betbot(ctx, amount):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  if amount == "all":
    if amounts[uid]['coins'] >= 500000:
      amount = 500000
    else:
      amount = amounts[uid]['coins']
  if int(amount) < 1000:
    await ctx.send("Bruh, you have to bet at least 1000 coins for this.")
  elif int(amount) > 500000:
    await ctx.send("Bruh you can't even bet that many coins at once so you have to bet at most 500,000 coins.")
  elif amounts[uid]['coins'] < int(amount):
    await ctx.send("Are you ok? You don't even have that many coins!")
  else:
    bot_roll = random.randint(3, 20)
    person_roll = random.randint(1, 20)
    if person_roll < bot_roll:
      color = discord.Colour.red()
      title = "You lost against the bot and lost your coins!"
      coins = (int(amount) * -1)
      add = False
      if amounts[uid]['alcohol_use'] == True:
        amounts[uid]['alcohol_times'] -= 1
        coins = coins * 2
        add = True
        if amounts[uid]['alcohol_times'] == 0:
          amounts[uid]['alcohol_use'] = False
      description = f"\n\nYou noob you lost to the bot! Your bet was **{amount}** coins so therefore you ended up losing those coins and now you have **{str(int(amounts[uid]['coins'] - int(amount)))}** coins. Here were the results: \n\nYou rolled {person_roll}. \nAnonymous Business Coder rolled {bot_roll}."
      if add == True:
        description += f"\n\nYou also had some alcohol so uh OOF now you have **{amounts[uid]['coins'] + int(coins)}** coins (because you lost 2 times more coins for your bet since really you did a bet of **{str(int(coins) * -1)}** coins)"
    elif person_roll > bot_roll:
      percentage_win = random.randint(5, 100)
      color = discord.Colour.green()
      title = "You won against the bot and won coins!"
      original_amount = amount
      amount = int(amount) * (percentage_win/100)
      coins = amount
      add = False
      if amounts[uid]['alcohol_use'] == True:
        amounts[uid]['alcohol_times'] -= 1
        percentage_win1 = percentage_win * 2
        coins = coins * 2
        add = True
        if amounts[uid]['alcohol_times'] == 0:
          amounts[uid]['alcohol_use'] = False
      description = f"You won against the bot nice and now you get **{percentage_win}%** more coins compared to your bet. Your bet was **{original_amount}** coins so therefore you now have **{str(int(amounts[uid]['coins'] + amount))}** coins. Here were the results: \n\nYou rolled {person_roll}. \nAnonymous Business Coder rolled {bot_roll}."
      if add == True:
        description += f"\n\nYou also had some alcohol so big money big money. Now the percentage that you go was actually **{percentage_win1}%** so NICE (because you had some nice alcohol). Anyways now you have **{str(int(amounts[uid]['coins'] + int(coins)))}** coins."
    else:
      color = discord.Colour.orange()
      title = "You tied against the bot and unfortunately lost some coins."
      percentage_lose = random.randint(25, 75)
      original_amount = amount
      amount = int(amount) * (percentage_lose/100) * -1
      coins = amount
      add = False
      if amounts[uid]['alcohol_use'] == True:
        amounts[uid]['alcohol_times'] -= 1
        add = True
        if amounts[uid]['alcohol_times'] == 0:
          amounts[uid]['alcohol_use'] = False
      description = f"You tied against the bot so you ended up losing **{percentage_lose}%** of your coins compared to your bet! Your bet was **{original_amount}** and now you have **{str(int(amounts[uid]['coins'] + coins))}** coins. Here were the results: \n\nBoth of you got {person_roll}."
      if add == True:
        description += f"\n\nOOF! You had alcohol but guess what? You actually tied so yeah for this situation alcohol didn't matter. You still have the same number of coins you had before. However, you still lost a chance. (like one of your ten chances)"
    amounts[uid]['coins'] += int(coins)
    if amounts[uid]['coins'] < 0:
      amounts[uid]['coins'] = 0
      await ctx.send("You can't have debt for this so your insurance took care of your debt.")
    await ctx.send(embed=discord.Embed(title=title, description=description, color=color))
    amounts[uid]['bank-space'] += random.randint(1, 50)
    amounts[uid]['commands'] += 1
  _save()

@bot.command()
async def rich(ctx):
  uid = str(ctx.author.id)
  rich_people = {}
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  for a in range(len(amounts)):
    keys_list = list(amounts)
    values_list = list(amounts[keys_list[a]].values())
    rich_people[keys_list[a]] = int(values_list[0])
  rich_people = sorted(rich_people.items(), key=lambda rich: rich[1], reverse=True)
  embed = discord.Embed(title = "Richest People with the Currency Bot", description = f"A list of the richest people who are using the Currency Bot", color = discord.Colour.blue())
  i = 0
  for a in range(len(rich_people)):
    try:
      username = bot.get_user(int(rich_people[a][0])).name
      i += 1
    except AttributeError:
      continue
    if i == 1:
      embed.add_field(name = f":first_place: {username}: ", value = f"{rich_people[a][1]} coins", inline = False)
    elif i == 2:
      embed.add_field(name = f":second_place: {username}: ", value = f"{rich_people[a][1]} coins", inline = False)
    elif i == 3:
      embed.add_field(name = f":third_place: {username}: ", value = f"{rich_people[a][1]} coins", inline = False)
    else:
      digits_list = list(str(i))
      string = ""
      for j in range(len(digits_list)):
        if digits_list[j] == "0":
          string += ":zero:"
        elif digits_list[j] == "1":
          string += ":one:"
        elif digits_list[j] == "2":
          string += ":two:"
        elif digits_list[j] == "3":
          string += ":three:"
        elif digits_list[j] == "4":
          string += ":four:"
        elif digits_list[j] == "5":
          string += ":five:"
        elif digits_list[j] == "6":
          string += ":six:"
        elif digits_list[j] == "7":
          string += ":seven:"
        elif digits_list[j] == "8":
          string += ":eight:"
        elif digits_list[j] == "9":
          string += ":nine:"
      embed.add_field(name = f"{string} {username}:", value = f"{rich_people[a][1]} coins", inline = False)
    amounts[uid]['bank-space'] += random.randint(1, 50)
    amounts[uid]['commands'] += 1
    _save()
  await ctx.send(embed=embed)

@commands.cooldown(1, 60, commands.BucketType.user)
@bot.command()
async def hackathon(ctx):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  try:
    if amounts[uid]['laptop'] >= 1:
      times = 1
      if amounts[uid]['coins'] >= 5000:
        times += 1
        if amounts[uid]['coins'] >= 20000:
          times += 1
          if amounts[uid]['coins'] >= 100000:
            times += 1
            if amounts[uid]['coins'] >= 500000:
              times += 1
      random_competition = random.randint(1, times)
      if random_competition == 1:
        coin_chance = random.random()
        if coin_chance <= 0.9:
          coins = random.randrange(10, 50, 5)
          description = f"You ended up participating in a free hackathon. You didn't do so well on it but since you at least participated you got {coins} coins."
        elif coin_chance > 0.9 and coin_chance <= 0.96:
          coins = random.randrange(100, 250, 10)
          description = f"You participated in a free hackathon and got 3rd place! The prize for 3rd place in this competition is {coins} coins."
        elif coin_chance > 0.96 and coin_chance < 0.995:
          coins = random.randrange(350, 750, 10)
          description = f"You participated in a free hackathon and got 2nd place! The prize for 2nd place in this competition is {coins} coins."
        else:
          coins = random.randrange(1000, 2500, 50)
          description = f"You participated in a free hackathon and got 1st place! The grand prize for the competition is {coins} coins."
      elif random_competition == 2:
        coin_chance = random.random()
        coin_fee = random.randrange(2500, 5000, 100)
        if coin_chance <= 0.95:
          coins = random.randrange(100, 500, 10)
          description = f"You participated in a hackathon that had around 50 - 100 people in it. There was a coin fee for this one which is {coin_fee} coins and unfortunately you didn't win. However, for participation, you got {coins} coins."
        elif coin_chance > 0.95 and coin_chance <= 0.985:
          coins = coin_fee + random.randrange(1000, 2000, 10)
          description = f"You participated in a kind of small hackathon which had a coin fee of {coins} coins. However, congratulations because you got 3rd place in it. Therefore you ended up getting {coins} coins because of your postition."
        elif coin_chance > 0.985 and coin_chance < 0.9985:
          coins = coin_fee + random.randrange(3000, 7500, 50)
          description = f"You participated in a kind of small hackathon which had a fee of {coins} coins. However, you did very well and was able to get 2nd place which led you getting out of the hackathon with {coins} coins."
        else:
          coins = coin_fee + random.randrange(10000, 25000, 100)
          description = f"You participated in a kind of small hackathon which had a fee of {coins} coins. However, you did so well that you were the winner of the hackathon and won the grand prize of {coins} coins."
        coins -= coin_fee
      elif random_competition == 3:
        coin_chance = random.random()
        coin_fee = random.randrange(10000, 20000, 100)
        if coin_chance <= 0.925:
          coins = 0
          description = f"You participated in a statewide hackathon which had a massive fee of {coin_fee} coins. Unfortunately, you were not able to get a good position and there will no coins for participation."
        elif coin_chance > 0.925 and coin_chance <= 0.97:
          coins = 0
          description = f"You participated in a statewide hackathon which had a massive fee of {coin_fee} coins. Unfortunately, you got a trash position and you got so triggered that you broke your laptop AHAHAHAHAHAHAAHHAHAHA."
          amounts[uid]['laptop'] -= 1
        elif coin_chance > 0.97 and coin_chance <= 0.99:
          coins = coin_fee + random.randrange(8000, 15000, 50)
          description = f"You participated in a statewide hackathon that had a fee of {coin_fee} coins. Congratulations cause somehow you were so good that you got 3rd place and walked out with {coins} coins."
        elif coin_chance > 0.99 and coin_chance < 0.99997:
          coins = coin_fee + random.randrange(20000, 45000, 100)
          description = f"You participated in a statewide hackathon that had a fee of {coin_fee} coins. Fortunately, you did so well that you got 2nd place and ended up walking out of the place with a massive amount of {coins} coins."
        else:
          coins = coin_fee + random.randrange(50000, 100000, 100)
          description = f"You participated in a statewide hackathon with a fee of {coin_fee} coins and yet SOMEHOW YOU GOT 1ST LIKE HOW WERE YOU LIKE CHEATING OR SOMETHING? Ok that doesn't matter because anyways the grand prize was {coins} coins so uh yeah."
        coins -= coin_fee
      elif random_competition == 4:
        coin_chance = random.random()
        coin_fee = random.randrange(40000, 100000, 200)
        if coin_chance <= 0.91:
          coins = 0
          description = f"You participated in a nationwide hackathon and did not get a good position. However, you weren't triggered but you didn't any coins. In fact, the fee was really high when you got in and it was like {coin_fee} coins literally."
        elif coin_chance > 0.91 and coin_chance <= 0.9825:
          coins = 0
          description = f"You participated in a nationwide hackathon and got a terrible position. This nationwide hackathon cost {coin_fee} coins and you were so triggered about how much money you wasted that you broke you laptop AHAHAHAHAHA"
          amounts[uid]['laptop'] -= 1
        elif coin_chance > 0.9825 and coin_chance <= 0.994:
          coins = coin_fee + random.randrange(20000, 50000, 100)
          description = f"You participated in a nationwide hackathon that cost {coin_fee} coins and you SOMEHOW GOT 3RD PLACE I MEAN LIKE HOW! Anyways you ended up getting {coins} coins."
        elif coin_chance > 0.994 and coin_chance <= 0.999999:
          coins = coin_fee + random.randrange(75000, 200000)
          description = f"You participated in a nationwide hackathon that cost {coin_fee} coins and you GOT 2ND PLACE DANG YOU HACKER! You got {coins} coins that you were able to put in your wallet."
        else:
          coins = coin_fee + random.randrange(100000, 500000, 1000)
          description = f"You participated in a nationwide hackathon that cost {coin_fee} and you just WERE BEING SUCH A HACKER BECAUSE THERE'S NO WAY YOU COULD HAVE GOTTEN FIRST PLACE I MEAN LIKE HOW!!!!!! Anyways, the grand prize was {coins} coins so be glad you got coins."
        coins -= coin_fee
      else:
        coin_chance = random.random()
        coin_fee = random.randrange(200000, 500000)
        if coin_chance <= 0.875:
          coins = 0
          description = f"You are high because you actually participated in an international competition and it is obvious that you did not win. However you did well but it cost you {coin_fee} coins and you did not get any more coins."
        elif coin_chance > 0.875 and coin_chance <= 0.993:
          coins = 0
          description = f"You are high because you actually participated in an international competition and obviously got a bad position. However, you got so triggered you broke your laptop AHAHAHAHAHA"
          amounts[uid]['laptop'] -= 1
        elif coin_chance > 0.993 and coin_chance <= 0.9985:
          coins = coin_fee + random.randrange(50000, 100000, 500)
          description = f"You are really high because you actually participated in an international competition and YOU WERE LIKE SO SKILLED SOMEHOW I DON'T KNOW HOW BUT SO SKILLED THAT YOU ENDED UP GETTING THIRD PLACE :open_mouth: Therefore, you were able to go home with {coins} coins and also the fee was {coin_fee} coins to participate in this so NICE."
        elif coin_chance > 0.9985 and coin_chance <= 0.99999999:
          coins = coin_fee + random.randrange(250000, 750000, 500)
          description = f"You are hyper because you actually participated in an international competition and HOW DID YOU GET SO GOOD I MEAN LIKE YOU ARE COMPETEING AGAINST PEOPLE ALL OVER THE WORLD LIKE YOU GOT SO GOOD I CAN'T BELIEVE THERE'S NO WAY YOU COULD HAVE POSSIBLY GOTTEN 2nd PLACE I MEAN LIKE I DON'T KNOW HOW YOU DID THAT AND I AM SO SURPRISED THAT I AM NOT RAMBLING...Anyways, that international competition cost {coin_fee} coins but you ended up going home with {coins} coins so uh NICE."
        else:
          coins = coin_fee + random.randrange(1000000, 10000000, 1000)
          description = f"You are very very hyper cause you participated in an international competition and I mean like HOW IS THIS EVEN POSSIBLE WHAT RANK YOU GOT I MEAN LIKE HOW DID YOU DO THIS YOU END UP WALKING INTO AN INTERNATIONAL COMPETITION AGAINST THE WHOLE WORLD AND ENDED UP GETTING THIS CRAZY RANKING AND NOW I AM GOING SO MAD THAT I AM GOING TO IAWHPFIOHWVBOIBHOIQHWAPOIHOIPWHBOIHOIhwHIOUGIUGIOYFUYTDTDYIUHPOIUGYFHGKIUFGHUYGIOUYFGHIOUYTDFGUIHYOUFTDFGUIHOYUTFGUIHOYUFGUIHOYUFGUHIOUYGFDTGFIUHOYUGFGIHOYUGFUGHYGFYUGHIOYTUFGIHOGUFYGHIGUVHIGUFYVHIOJUGYFGIHOUGFYVHGIOGUFYVHIOGUYFGIH...YEAH I KNOW THAT IS RANDOM BUT I MEAN LIKE I STILL DON'T HOW YOU WERE ABLE TO ACCOMPLISH WHAT YOU DID... anyways, in simple terms, you got 1st place by walking into an international competition that cost {coin_fee} coins and now you won the grand prize of {coins} coins."
        coins -= coin_fee
      amounts[uid]['coins'] += coins
      amounts[uid]['bank-space'] += random.randint(1, 50)
      amounts[uid]['commands'] += 1
      await ctx.send(embed=discord.Embed(title = "You participated in a hackathon!", description = description, color = discord.Colour.green()))
      _save()
    else:
      await ctx.send("You need **a laptop** to participate in a hackathon. What do you think you are going to use, a mobile device that doesn't store a lot of data?")
  except KeyError:
    await ctx.send("You need **a laptop** to participate in a hackathon. What do you think you are going to use, a mobile device that doesn't store a lot of data?")

@bot.command()
@commands.cooldown(1, 45, commands.BucketType.user)
async def stream(ctx):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  try:
    if amounts[uid]['laptop'] >= 2:
      coin_chance = random.random()
      if coin_chance <= 0.65:
        views = random.randint(10000, 100000)
        likes = random.randint(2000, 5000)
        coins = random.randint(50, 1000)
        description = f"You streamed a video and posted it. In the end, you got {views} views and {likes} likes. You also got {coins} coins from your fans."
      elif coin_chance > 0.65 and coin_chance <= 0.85:
        views = random.randint(5000, 20000)
        dislikes = random.randint(1000, 2500)
        coins = 0
        description = f"You streamed a video and posted it. Unfortunately, your video was trash because you ended up getting only {views} views and {dislikes} dislikes. Therefore, you got no coins from your fans."
      elif coin_chance > 0.85 and coin_chance <= 0.91:
        views = random.randint(5000, 50000)
        dislikes = random.randint(2500, 4900)
        coins = 0
        description = f"You streamed a video and posted it. Unfortunately, the video was so bad that you got {views} views and {dislikes} dislikes. Your fans were so mad that they staged a raid and stole your laptop!"
        amounts[uid]['laptop'] -= 1
      elif coin_chance > 0.91 and coin_chance <= 0.92:
        views = random.randint(5000, 10000)
        coins = 0
        description = f"You streamed a video and posted it. Unfortunately, your video was like the worst ever since you got {views} views and all of them gave you dislikes. Your fans were so triggered by how bad the video was that they ended up raiding your house and stole both of your laptops you were using to post your videos!"
        amounts[uid]['laptop'] -= 2
      elif coin_chance > 0.92 and coin_chance <= 0.9993:
        views = random.randint(100000, 1000000)
        likes = random.randint(50000, 90000)
        coins = random.randint(2500, 5500)
        description = f"You streamed a video and posted it. A lot of people liked your video and it came in trending. After the popularity of the video died down, you got {views} views in total and the likes were at {likes}. So many of your fans liked it that in total you got {coins} coins."
      else:
        views = random.randint(5000000, 1000000000)
        likes = random.randint(500000, 3550000)
        coins = random.randint(8000, 15000)
        bonus_coins = random.randint(1000, 5000)
        description = f"You streamed a video and posted it. Everyone liked it and watched the video like a hundred times or something. Anyways, it took a while for the popularity to die down and when it did, you had {views} views and {likes} likes. At first, you had {coins} coins from your fans but one of them was so impressed that they gave you an extra {bonus_coins} coins."
        coins += bonus_coins
      amounts[uid]['coins'] += coins
      amounts[uid]['bank-space'] += random.randint(1, 50)
      amounts[uid]['commands'] += 1
      if coins == 0:
        color = discord.Colour.orange()
      else:
        color = discord.Colour.green()
      await ctx.send(embed = discord.Embed(title = "You streamed a video and posted it!", description = description, color = color))
      _save()
    else:
      await ctx.send("You need **2 laptops** for some reason to stream a video.")
  except KeyError:
    await ctx.send("You need a **2 laptops** for some reason to stream a video.")

@bot.command(aliases=['post_coding_thing'])
@commands.cooldown(1, 40, commands.BucketType.user)
async def pct(ctx):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  try:
    if amounts[uid]['laptop'] >= 1:
      coin_possible = random.random()
      if coin_possible <= 0.575:
        coins = random.randint(10, 1000)
        upvotes = random.randint(1, 500)
        choices_of_post = ["game", "mini-game", "simulator"]
        description = f"You ended up posting a {random.choice(choices_of_post)}. Luckily, you were able to get {upvotes} upvotes and you got {coins} coins from your fans!"
      elif coin_possible > 0.575 and coin_possible <= 0.95:
        coins = 0
        downvotes = random.randint(1, 500)
        choices_of_post = ["game", "mini-game", "simulator", "an old project you found"]
        description = f"You ended up posting a {random.choice(choices_of_post)}. Unfortunately, no one liked your post so you got {downvotes} downvotes and therefore no one gave you any coins."
      elif coin_possible > 0.95 and coin_possible <= 0.9675:
        coins = 0
        downvotes = random.randint(1000, 5000)
        choices_of_post = ["begginer's concept", "project with lots of mistakes", "a hacker game"]
        description = f"You ended up posting a {random.choice(choices_of_post)}. Everyone hated your post so much because you got {downvotes} downvotes and all your fans staged a raid on you and took your laptop LMAO."
        amounts[uid]['laptop'] -= 1
      elif coin_possible > 0.9675 and coin_possible <= 0.9997:
        coins = random.randint(1500, 3000)
        bonus_coins = random.randint(500, 1000)
        upvotes = random.randint(1000, 6000)
        choices_of_post = ["epic game", "cool simulator", "cool project"]
        description = f"You ended up posting a {random.choice(choices_of_post)}. A lot of people liked the post a lot so you got {upvotes} upvotes and gave you {coins} coins. One of your fans were so proud of you that the person gave you an extra {bonus_coins} coins!"
        coins += bonus_coins
      else:
        coins = random.randint(7500, 11111)
        upvotes = random.randint(10000, 100000)
        bonus_coins = random.randint(2000, 4000)
        description = f"You ended up posting a surreal project. You got so many upvotes ({upvotes} of them) and your project got featured for weeks in a magazine called Best Coding Projects of the Week. You got {coins} coins at first and then one fan was so impressed that the person gave you {bonus_coins} more coins!"
        coins += bonus_coins
      amounts[uid]['coins'] += coins
      if coins == 0:
        color = discord.Colour.orange()
      else:
        color = discord.Colour.green()
      await ctx.send(embed = discord.Embed(title = "You posted a coding project!", description = description, color = color))
      amounts[uid]['bank-space'] += random.randint(1, 50)
      amounts[uid]['commands'] += 1
      _save()
    else:
      await ctx.send("You need a **laptop** in order to post some coding projects or things.")
  except KeyError:
    await ctx.send("You need a **laptop** in order to post some coding projects or things.")

@bot.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def fish(ctx):
  fish_rarity = random.random()
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  try:
    if amounts[uid]['fishingpole'] >= 1:
      if fish_rarity <= 0.6:
        type_fish = ["trout", "mackeral"]
        fishes = random.randint(1, 10)
        fish = random.choice(type_fish)
        description = f"You were able to catch {fishes} {fish}s."
      elif fish_rarity > 0.6 and fish_rarity <= 0.92:
        fishes = 0
        fish = "none"
        description = "You are such a noob that you did not catch anything during this fishing time."
      elif fish_rarity > 0.92 and fish_rarity <= 0.94:
        fishes = 0
        fish = "none"
        description = "AHAHAHAHA you broke your fishingpole."
        amounts[uid]['fishingpole'] -= 1
      elif fish_rarity > 0.94 and fish_rarity <= 0.975:
        list_of_items = ["cube"]
        fish = random.choice(list_of_items)
        fishes = 1
        description = f"Nice, you got a {fish} item."
      elif fish_rarity > 0.975 and fish_rarity <= 0.995:
        list_of_fish = ["turtle", "jellyfish", "octopus"]
        fishes = random.randint(1, 3)
        fish = random.choice(list_of_fish)
        description = f"Wow, you got lucky because you were able to catch {fishes} {fish}s."
      elif fish_rarity > 0.995 and fish_rarity <= 0.9995:
        list_of_fish = ["whale", "shark"]
        fishes = random.randint(1, 2)
        fish = random.choice(list_of_fish)
        description = f"Dang you just got so lucky today. You were able to catch {fishes} {fish}s."
      else:
        fish = "coinfish"
        fishes = 1
        description = f"HOW DID YOU DO THIS BECAUSE THIS IS LITERALLY IMPOSSIBLE! (Not really but still) You somehow caught a COIN FISH! You are literally such a pro at fishing!"
      if fish != "None":
        try:
          amounts[uid][fish] += fishes
        except KeyError:
          amounts[uid][fish] = 0
          _save()
          amounts[uid][fish] += fishes
      if fishes >= 1:
        color = discord.Colour.green()
      else:
        color = discord.Colour.red()
      await ctx.send(embed = discord.Embed(title = "You fished", description = description, color = color))
      amounts[uid]['bank-space'] += random.randint(1, 50)
      amounts[uid]['commands'] += 1
      _save()
    else:
      await ctx.send("You need a **Fishing Pole** in order to fish. You can't just fish using your hands.")
  except KeyError:
    await ctx.send("You need a **Fishing Pole** in order to fish. You can't just fish using your hands.")

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def beg(ctx):
    donators = ["AnonymousCoder", "jay3332", "a person", "your ego", "the world", 'Aagames', "Jeff", "Joe", "the other begger", "the 10 IQ person", "god", "everyone", "a gamer", "your friend"]
    messages = ["go away", "be quiet", "stop begging your life is not going to change", "shut up and stop begging", "no you", "wait I have some money...oh nvm I don't", "you are too rich right now go away", "beggers are people who have low IQ"] 
    uid = str(ctx.author.id)
    if not uid in amounts:
        amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
    if random.random()<=0.5:
        profit = random.randint(200, 500)
        await ctx.send(embed = discord.Embed(title=f"{ctx.author.name} begged and a person gave the user some coins!", description=f'You got {profit} coins from {random.choice(donators)}.', color = discord.Colour.green()))
    else:
        profit = 0
        await ctx.send(embed = discord.Embed(title=f'Oof! No one gave {ctx.author.name} any coins!', description=f'{random.choice(donators)} told you {random.choice(messages)}.', colour = discord.Colour.red()))
    amounts[uid]['coins'] += profit
    amounts[uid]['bank-space'] += random.randint(1, 50)
    amounts[uid]['commands'] += 1
    _save()

@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def search(ctx):
    places = ["fireplace", "couch", "bedroom", "car", "living room", "sewer", "office", "park"]
    places_chosen = []
    uid = str(ctx.author.id)
    if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
    for i in range(5):
      random_place = random.randint(0, (len(places) - 1))
      places_chosen.append(places[random_place])
      del places[random_place]
    message = await ctx.send(embed=discord.Embed(title=f"{ctx.author.name}\'s Search", description=f"Here are your choices to for where you can search for coins:\n``{places_chosen[0]}`` |  ``{places_chosen[1]}`` |  ``{places_chosen[2]}`` |  ``{places_chosen[3]}`` |  ``{places_chosen[4]}``", color = discord.Colour.blue()))
    try:
      def check(msg):
        return msg.author.id == int(uid)
      msg = await bot.wait_for("message", timeout=10, check=check)
      message_content = msg.content
      search_correct = False
      for i in range(len(places_chosen)):
        if message_content.lower() == places_chosen[i]:
          search_correct = True
      if search_correct == True and message_content.lower() == "fireplace":
        chance_of_coins = random.random()
        if chance_of_coins <= 0.1:
          coins = random.randint(1000, 1500)
          embed = discord.Embed(title="You searched the fireplace and got coins!", description=f"You were extremely lucky that you didn't burn. You were also lucky to find coins that were not burned. Also what crazy person would leave their coins in a fireplace? Anyways, you found {coins} of unburned coins.", color = discord.Colour.green())
        elif chance_of_coins > 0.1 and chance_of_coins <= 0.3:
          coins = 0
          embed = discord.Embed(title="You searched the fireplace and didn't get any coins!", description="You were extremely lucky that you didn't burn. Unfortunately, there was no use to going in because there were no coins in the fireplace. It looks like either no one left coins in the fireplace or someone used the fireplace and burned them all up.", color = discord.Colour.orange())
        elif chance_of_coins > 0.4 and chance_of_coins <= 0.65:
          coins = random.randint(-500, -50)
          embed = discord.Embed(title="You searched the fireplace but got some burns.", description=f"You went into the fireplace but unfortunately it was at the wrong time. You were so into getting coins that you didn't realize the fireplace was burning. Therefore, you ended up getting burned for a little bit before you realized and went out. Luckily, it was an open fireplace. However, you still had to go to the hospital and pay them {coins * -1} coins.", color = discord.Colour.red())
        elif chance_of_coins > 0.65 and chance_of_coins <= 0.99:
          coins = random.randint(-5000, -1000)
          embed = discord.Embed(title="You searched the fireplace and got major burns.", description=f"You went into the fireplace while there was a fire in there. You were so into getting coins that you didn't realize this. For some reason, you were also so obsessed with getting coins that you never realized and someone had to pull you out. You had to go to the hospital to get those treated and had to pay then {coins * -1} coins.", color = discord.Colour.red())
        else:
          coins = amounts[uid]['coins'] * -1
          embed = discord.Embed(title="You searched the fireplace and died.", description=f"In order to get to the firepalce, you had to climb the chimney in order to get down and start searching. However, when you went down the chimney and into the fireplace, you suddenly realized that something was burning inside. You tried to get out but there was no use. You died in the fireplace and also lost all your coins.")
          amounts[uid]['bank-coins'] = 0
          amounts[uid]['bank-space'] = 0
      elif search_correct == True and message_content.lower() == "couch":
        coins = random.randint(5, 200)
        embed = discord.Embed(title="You searched the couch.", description=f"You searched the couch and for some reason you found {coins} coins. What does this person think a couch is, a bank?", color = discord.Colour.green())
      elif search_correct == True and message_content.lower() == "bedroom":
        chance_of_more_coins = random.random()
        if chance_of_more_coins <= 0.999:
          coins = random.randint(1, 500)
          embed = discord.Embed(title="You searched the bedroom.", description=f"You searched your bedroom and you still had some leftover allowance that you never used and put in your wallet. In addition, you also found some coins scattered on the floor. Those coins made you get {coins} coins.", color = discord.Colour.green())
        else:
          coins = random.randint(1000, 5000)
          embed = discord.Embed(title="You searched the bedroom and got very lucky! :money_mouth: :open_mouth:", description=f"You searched your bedroom and found some leftover allowance you never put in your wallet and some coins that were scattered. However, when you looked under your bed, you suddenly saw a bedroom demon under there. That bedroom demon was kind of rich and gave you most of their coins. After that you ended up with {coins} more coins to add to your wallet.", color = discord.Colour.green())
      elif search_correct == True and message_content.lower() == "car":
        chance_of_coins = random.random()
        if chance_of_coins <= 0.35:
          coins = random.randint(1, 1000)
          embed = discord.Embed(title="You searched a car and succeeded! :open_mouth:", description=f"Since you didn\'t own a car, you had to go steal coins from one. You got lucky because no one caught you. Therefore, you were able to run away with {coins} coins.", color = discord.Colour.green())
        else:
          coins = random.randint(-2000, -50)
          embed = discord.Embed(title="You searched a car but failed!", description=f"Since you didn\'t own a car, you had to go steal coins from one. Unfortunately, someone saw you while you were trying to rob the person\'s money in the car. That person phoned the police so while you were running away, the police were able to get you. You unfortunately had to pay {coins * -1} coins in fines.", color = discord.Colour.red())
      elif search_correct == True and message_content.lower() == "living room":
        coins = random.randint(10, 350)
        embed = discord.Embed(title="You searched the living room!", description=f"You searched the living room and found {coins} coins. I wonder why a person would drop it...", color = discord.Colour.green())
      elif search_correct == True and message_content.lower() == "sewer":
        chance_of_more_coins = random.random()
        if chance_of_more_coins <= 0.9:
          coins = random.randint(25, 500)
          embed = discord.Embed(title="You searched the sewer and got coins!", description=f"You searched the sewer and found {coins} coins. I wonder why coins would be in the sewer and why you would go in there.", color = discord.Colour.green())
        else:
          earn_coins = random.randint(400, 420)
          lose_coins = random.randint(380, 400)
          coins = earn_coins - lose_coins
          embed = discord.Embed(title="You searched the sewer, found coins, and lost some.", description=f"You searched the sewer and got {earn_coins} coins! However, while going in the dirty water, you suddenly lost your balance and fell. You were able to get back up, but you lost {lose_coins} of your coins (because you were still carrying them). However, you ended up getting out of the sewer with {coins} more coins.", color = discord.Colour.orange())
      elif search_correct == True and message_content.lower() == "office":
        coins = random.randint(10, 250)
        embed = discord.Embed(title="You searched the office!", description=f"You searched **an** office and got {coins} coins. Since you saw that the **an** was bold, I wonder if this office was yours (as in workspace for school or something) or your parents...", color = discord.Colour.green())
      elif search_correct == True and message_content.lower() == "park":
        coins = random.randint(5, 300)
        embed = discord.Embed(title="You searched the park!", description = f"You searched the park and was able to gather {coins} coins that were on the ground. Looks like you were trying to save the environment (while being greedy and getting more coins).", color = discord.Colour.green())
      else:
        await message.edit(content="That is not an option.")
      if amounts[uid]['coins'] + coins >= 0:
        amounts[uid]['coins'] += coins
      else:
        amounts[uid]['coins'] = 0
      amounts[uid]['bank-space'] += random.randint(1, 50)
      amounts[uid]['commands'] += 1
      await ctx.send(embed=embed)
      _save()
    except asyncio.TimeoutError:
      await message.edit(content="Are you ok? You can\'t just not respond after typing in ``c search``")

@bot.command(aliases=['deposit'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def dep(ctx, amount):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  if amount == "all":
    if amounts[uid]['bank-space'] - amounts[uid]['bank-coins'] >= amounts[uid]['coins']:
      coins = amounts[uid]['coins']
      amounts[uid]['bank-coins'] += amounts[uid]['coins']
      amounts[uid]['coins'] = 0
    else:
      coins = amounts[uid]['bank-space'] - amounts[uid]['bank-coins']
      amounts[uid]['bank-coins'] += coins
      amounts[uid]['coins'] -= coins
    embed = discord.Embed(title = f"{ctx.author.name} deposited coins!", description = f"You deposited {coins} coins to your bank!", color = discord.Color.green())
  elif amount.isdigit():
    coins = amount
    if int(amounts[uid]['bank-space']) - int(amounts[uid]['bank-coins']) >= int(amount):
      amounts[uid]['bank-coins'] += int(amount)
      amounts[uid]['coins'] -= int(coins)
      embed = discord.Embed(title = f"{ctx.author.name} deposited coins!", description = f"You deposited {coins} coins to your bank!", color = discord.Color.green())
    else:
      embed = discord.Embed(title = f"Are you ok?", description = f"Are you actually ok? Because you literally don't have that many coins in your wallet to deposit into your bank.", color = discord.Color.orange())
  else:
    embed = discord.Embed(title = "What?", description = "I have no clue what you put but let me just tell you after you write ``c dep`` that you have to put in an integer or the word all if you want to fill up the whole bank.", color = discord.Colour.orange())
  amounts[uid]['commands'] += 1
  await ctx.send(embed=embed)
  _save()

@bot.command(aliases=['with'])
async def withdraw(ctx, amount):
  uid = str(ctx.author.id)
  if not uid in amounts:
      amounts[uid] = {'coins': 0, 'bank-coins': 0, 'bank-space': 0, 'commands': 0, 'dailytime': 0, 'job': "None", 'alcohol_use': False, 'alcohol_times': 0, 'padlock_use': False}
  if amount == "all":
    coins = amounts[uid]['bank-coins']
    amounts[uid]['bank-coins'] = 0
    amounts[uid]['coins'] += coins
    embed = discord.Embed(title = f"{ctx.author.name} withdrawed coins!", description = f"You withdrawed {coins} coins from the bank and now those coins are in your wallet.", color = discord.Colour.green())
  elif amount.isdigit():
    if int(amount) <= int(amounts[uid]['bank-coins']):
      amounts[uid]['bank-coins'] -= int(amount)
      amounts[uid]['coins'] += int(amount)
      embed = discord.Embed(title = f"{ctx.author.name} withdrawed coins!", description = f"You with drawed {amount} coins from the bank and now those coins are in your wallet.", color = discord.Colour.green())
    else:
      await ctx.send("Um you don't have that much money in your bank.")
  else:
    await ctx.send("Stupid you need to respond with ``c with all`` or ``c with`` and then an integer that has to be less than how many bank coins you have.")
  amounts[uid]['commands'] += 1
  await ctx.send(embed = embed)
  _save()

@bot.command()
@commands.has_any_role("The Bot Owner", "Moderator")
async def bancurrencu(ctx, user:discord.Member="None",*, reason = "No reason provided."):
  ban = True
  if user == "None" or user == ctx.message.author or user.bot == True:
    embed = discord.Embed(title = "You unsuccessfully banned.", description = "I wonder why...oh yeah its because you need to put in a member and not just yourself so don't be so stupid. It also could have been because you put the name of a bot.", color = discord.Colour.orange())
    ban = False
  if ban == True:
    embed = discord.Embed(title = "You successfully banned.", description = f"{user.mention} was banned.", color = discord.Colour.green())
    embed1 = discord.Embed(title = "You were banned.", description = f"Reason: {reason}", color = discord.Colour.red())
    await user.send(embed = embed1)
    await user.ban(reason=reason)
  await ctx.send(embed = embed)

@bot.command()
@commands.has_any_role("The Bot Owner", "Moderator")
async def unbancurrency(ctx, *, member):
  BanList = await ctx.guild.bans()
  MemberDiscrim = member.split('#')
  MemberName = member.split('#' + MemberDiscrim[0])
  user_found = False
  for BanEntry in BanList:
    user = BanEntry.user
    if (MemberName[0]) == (user.name): 
      await ctx.guild.unban(user)
      await ctx.send(embed = discord.Embed(title = "You successfully unbanned!", description = f'{user.mention} has been unbanned by {ctx.author.name}', color = discord.Colour.green()))
      user_found = True
      break
  if user_found == False:
    await ctx.send(embed = discord.Embed(title = "User not found", description = "The user was either probably not banned or is not in this server", color = discord.Colour.orange()))

@bot.command()
@commands.has_any_role("The Bot Owner", "Moderator", "Owner", "Administrator")
async def remove(ctx, amount=1):
  await ctx.channel.purge(limit=amount)
  await ctx.send(embed = discord.Embed(title="Messages successfully purged!", description = f"{ctx.author.mention} just removed {amount} messages.", color = discord.Colour.green()))

@bot.command(aliases=['suggestion'])
async def suggest(ctx, *, suggestion="A suggestion"):
  random_id = str(random.randint(1000000000000000, 9999999999999999))
  guild = discord.utils.get(bot.guilds, name=ctx.message.guild.name)
  if guild is not None:
      channel = discord.utils.get(guild.text_channels, name='suggestions')
  if suggestion != "A suggestion":
    await channel.send(f"{ctx.author.mention} has a suggestion!")
    embed = discord.Embed(title = f"{ctx.author.name}'s Suggestion (When making the decision, use ``{random_id}`` for the id number)", description = suggestion, color = discord.Colour.green())
    msg = await channel.send(embed = embed)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')
    open_file = open('suggestions.txt', "a")
    open_file.write(random_id + "@" + suggestion + "\n")
    open_file.close()
  else:
    await ctx.send("You have to put **a suggestion** dumy.")

@bot.command(aliases=['decision'])
@commands.has_any_role("The Bot Owner", "Owner", "Chief Orca")
async def decide(ctx, id1, accepted,*, reason="No reason provided"):
  guild = discord.utils.get(bot.guilds, name=ctx.message.guild.name)
  if guild is not None:
      channel = discord.utils.get(guild.text_channels, name='decisions')
  open_file = open("suggestions.txt", "r")
  readlines = open_file.readlines()
  for i in range(len(readlines)):
    list1 = readlines[i].split("@")
    if str(list1[0]) == str(id1):
      if accepted.lower() == "yes":
        color = discord.Colour.green()
        title = f"Suggestion #{int(i+1)} Accepted"
      else:
        color = discord.Colour.red()
        title = f"Suggestion #{int(i + 1)} Rejected"
      suggestion = (readlines[int(i)]).split(id1 + "@")
      suggestion_revise = suggestion[1].rstrip("\n")
      embed = discord.Embed(title=title, description = f"Suggestion: {suggestion_revise}\nReason: {reason}", color=color)
      await channel.send(embed=embed)

@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def bak(ctx):
  if ctx.author.id == 900064677982248960:
    await ctx.send("Well, since you won the giveaway here you go 1000000 coins!")
    amounts[str(900064677982248960)]['coins'] += 10000000
    _save()
  else:
    await ctx.send("BACK OFF! THIS IS PRIVATE COMMAND!")

@beg.error
async def beg_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed = discord.Embed(title="Just Stop Begging", description=(f'Begging more won\'t do anything for you. Use this command again after {round(error.retry_after)} seconds.'), color = discord.Colour.orange()))
    else:
      raise error 

@search.error
async def search_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Why are you searching so much?", description=f"Don't search around too much you might tire youself. Wait {round(error.retry_after)} seconds before using this command again.", color = discord.Colour.orange()))
    else:
      raise error

@dep.error
async def dep(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Cooldown Active", description=f"Why are you going to the bank so much? Wait {round(error.retry_after)} seconds before using this command again.", color = discord.Colour.orange()))
    else:
      raise error

@fish.error
async def fish(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Why are you fishing so much?", description=f"If you fish this much, there won't be any fishes to fish from later. Wait {round(error.retry_after)} seconds before using this command again.", color = discord.Colour.orange()))
    else:
      raise error

@pct.error
async def pct(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Why you post?", description=f"It takes time to code a good project. Wait {round(error.retry_after)} seconds before using this command again.", color = discord.Colour.orange()))
    else:
      raise error

@stream.error
async def stream(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Why you post video?", description=f"It takes time to make good videos that people would like. Wait {round(error.retry_after)} seconds before using this command again.", color = discord.Colour.orange()))
    else:
      raise error

@hackathon.error
async def hackathon_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Cooldown Active", description=f"There aren't any hackathons that you can go participate in right now. Wait {round(error.retry_after)} seconds before participating in another one.", color = discord.Colour.orange()))
    else:
      raise error

@betbot.error
async def betbot_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("You need to **specify** the amount ok? You can't just put no number that you will bet on.")
  elif isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Cooldown Active", description=f"If you bet that much, you will be poor in a matter of minutes! Wait {round(error.retry_after)} seconds before using this command again.", color = discord.Colour.orange()))
  else:
    raise error

@betplayer.error
async def betplayer_error(ctx, error):
    minutes = math.floor(round(error.retry_after)/60)
    seconds = round(error.retry_after) - minutes * 60
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Cooldown Active", description=f"If you bet this much, you will literally be poor. Wait {minutes} minutes and {seconds} seconds betting with another player.", color = discord.Colour.orange()))
    else:
      raise error

@rob.error
async def rob_error(ctx, error):
    if isinstance(error, commands.BadArgument):
      await ctx.send("Bruh, I don't know what you put but the member was not found.")
    elif isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Cooldown Active", description=f"If you rob too many times, you or the person who you are trying willll be poor! Wait {round(error.retry_after)} seconds using this command again.", color = discord.Colour.orange()))
    else:
      raise error

@bak.error
async def bak_error(ctx, error):
    minutes = math.floor(round(error.retry_after)/60)
    seconds = round(error.retry_after) - minutes * 60
    if isinstance(error, commands.CommandOnCooldown):
      await ctx.send(embed = discord.Embed(title="Cooldown Active", description=f"Yes, I know you got your dose of coins but just wait. Wait {minutes} minutes and {seconds} seconds before participating in another one.", color = discord.Colour.orange()))
    else:
      raise error

@stats.error
async def stats_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send(embed=discord.Embed(title="Excuse me, who?", description="Like what the title says wait who are you talking about?", color = discord.Colour.orange()))
  else:
    raise error

@balance.error
async def balance_error(ctx, error):
  if isinstance(error, commands.BadArgument):
    await ctx.send(embed=discord.Embed(title="Excuse me, who?", description="Like what the title says wait who are you talking about?", color = discord.Colour.orange()))
  else:
    raise error

@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(embed=discord.Embed(title="NO JUST NO", description = "You don't even have a high enough role to ban people so don't even try it", color = discord.Colour.orange()))
  else:
    raise error

@unban.error
async def unban_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(embed=discord.Embed(title="NO JUST NO", description = "You don't even have a high enough role to unban people so don't even try it", color = discord.Colour.orange()))
  else:
    raise error

@remove.error
async def remove_error(ctx, error):
  if isinstance(error, commands.MissingAnyRole):
    await ctx.send(embed=discord.Embed(title="NO JUST NO", description = "You don't even have a high enough role to remove messages so don't even try it", color = discord.Colour.orange()))
  else:
    raise error
  
def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f) 

@bot.command()
async def marioparty(ctx):
  embed = discord.Embed(title="Mario Party Games!", description=f"Type !start to play")  
  embed.set_image(url="https://64.media.tumblr.com/4ac2c5f35ccaca1af567930c43eb6a15/tumblr_nw4jlfhNdb1s3uawvo2_r1_500.gif")
  await ctx.send(embed=embed)

@bot.command()
async def start(ctx):
  embed = discord.Embed(title="Mario party games!", description="Which game would you like to play? \n **Bustling buttons:** \n Type !bustlingbuttons to choose a button which can kill you! Yay \n **Bumper balloon:** \n Type !bumperballoon to kill mario, luigi, peach or wario! How nice ay? \n **Hexagon heat:** \n !hexagonheat to pick a color and survive... or not \n **Bungling slots** \n Under developement! \n **Lights out:** \n SMASH PEOPLE WITH A HAMMER USING !lightsout")
  embed.set_image(url="https://images-ext-1.discordapp.net/external/dvdGwGL2LYHG5O_bzzNQm08zalg2hrS00KjxFImcsWI/https/giant.gfycat.com/SimpleGrandioseAntarcticfurseal.gif")
  await ctx.send(embed=embed)

@bot.command()
async def bustlingbuttons(ctx):
   responses =[ f"Red", "Green", "White", "Pink", "Yellow"]
   embed = discord.Embed(title="Mario Party Games!", description=f"What colour do you pick?")
   embed.set_image(url="https://i.makeagif.com/media/11-21-2015/4wfHk4.gif")
   await ctx.send(embed=embed)

   try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

   except asyncio.TimeoutError:
     await ctx.send('You took too long...')

   else:
        if msg.content == f"{random.choice(responses)}":
            embed = discord.Embed(name="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and won!**")
            embed.set_image(url="https://i0.wp.com/i.gifer.com/embedded/download/YJBm.gif")
            embed.set_footer(text="Yay lets GOOO")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and died! R.I.P**")
            embed.set_image(url="https://64.media.tumblr.com/85dfa2426b29a8a693ac067218f43a0f/tumblr_mhd2j0PxDV1rrftcdo1_500.gif")
            embed.set_footer(text="oof rip")
            await ctx.send(embed=embed)
          
@bot.command()
async def bumperballoon(ctx):
   responses =[ f"Mario","Luigi","Peach","Wario","mario","luigi","peach","wario"]
   embed = discord.Embed(title="Mario Party Games!", description=f"Which car are you gonna attack?")
   embed.set_image(url="https://thumbs.gfycat.com/MagnificentGrotesqueGoldenmantledgroundsquirrel-size_restricted.gif")
   await ctx.send(embed=embed)

   try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

   except asyncio.TimeoutError:
     await ctx.send('You took too long...')

   else:
        if msg.content == f"{random.choice(responses)}":
            embed = discord.Embed(name="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and won!**")
            embed.set_image(url="https://i0.wp.com/i.gifer.com/embedded/download/YJBm.gif")
            embed.set_footer(text="Yay lets GOOO")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and died cuz he was too bad! R.I.P**")
            embed.set_image(url="https://64.media.tumblr.com/85dfa2426b29a8a693ac067218f43a0f/tumblr_mhd2j0PxDV1rrftcdo1_500.gif")
            embed.set_footer(text="oof rip")
            await ctx.send(embed=embed)

@bot.command()
async def hexagonheat(ctx):
   responses =[ f"Red", "Green", "White", "Pink", "Yellow", "Blue", "Cyan"]
   embed = discord.Embed(title="Mario Party Games!", description=f"Which hexagon are you jumping on?")
   embed.set_image(url="https://i.makeagif.com/media/12-14-2015/QUGHnk.gif")
   await ctx.send(embed=embed)

   try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

   except asyncio.TimeoutError:
     await ctx.send('You took too long...')

   else:
        if msg.content == f"{random.choice(responses)}":
            embed = discord.Embed(name="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and won!**")
            embed.set_image(url="https://i0.wp.com/i.gifer.com/embedded/download/YJBm.gif")
            embed.set_footer(text="Yay lets GOOO")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and died cuz he was too bad! R.I.P**")
            embed.set_image(url="https://64.media.tumblr.com/85dfa2426b29a8a693ac067218f43a0f/tumblr_mhd2j0PxDV1rrftcdo1_500.gif")
            embed.set_footer(text="oof rip")
            await ctx.send(embed=embed)

@bot.command()
async def bunglingslots(ctx):
  responses = [
    "<:downloadiconkey13198251881024706:972916630118080584>", "<:cheszx:972916315469783071>", "<:super_mario_world_gold_mushroom_:972916223526440970>",
  ]
  embed = discord.Embed(title="Mario Party Games!", description=f"Roll timingly so you can get correct slots")
    
  embed.set_image(url="https://64.media.tumblr.com/969e59c9adc82e0b125493d621c32a89/67c333da52d52300-ac/s400x600/63ea9a4123f05a7ba3bfa3bba2eda5318cd02e54.gif")
  await ctx.send(embed=embed)

  try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

  except asyncio.TimeoutError:
       await ctx.send('You took too long...')

  else:
        if msg.content == f"roll":
          await ctx.send(f'{random.choice(responses)} {random.choice(responses)} {random.choice(responses)}')
          responses2 = [f"{ctx.message.author.mention} won!", f"{ctx.message.author.mention} lost"
            
          ]
          embed = discord.Embed(name="Mario party games!", description=f"**{random.choice(responses2)}**")
          embed.set_image(url="https://i0.wp.com/i.gifer.com/embedded/download/YJBm.gif")
          embed.set_footer(text="Party games")
          await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Mario party games!", description=f"**{ctx.message.author.mention} Lost **")
            embed.set_image(url="https://64.media.tumblr.com/2f0fad7a11da74951ddbbe72246b4e62/tumblr_p299vc94KX1s3uawvo1_500.gif")
            embed.set_footer(text="oof rip")
            await ctx.send(embed=embed)

@bot.command()
async def lightsout(ctx):
   responses =[ f"Mario", "Luigi", "Peach",]
   embed = discord.Embed(title="Mario Party Games!", description=f"Who are you attacking ?")
   embed.set_image(url="https://64.media.tumblr.com/2f0fad7a11da74951ddbbe72246b4e62/tumblr_p299vc94KX1s3uawvo1_500.gif")
   await ctx.send(embed=embed)

   try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

   except asyncio.TimeoutError:
     await ctx.send('You took too long...')

   else:
        if msg.content == f"{random.choice(responses)}":
            embed = discord.Embed(name="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and won!**")
            embed.set_image(url="https://i0.wp.com/i.gifer.com/embedded/download/YJBm.gif")
            embed.set_footer(text="Yay lets GOOO")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Mario party games!", description=f"**{ctx.message.author.mention} picked {msg.content} and died cuz he was too bad! R.I.P**")
            embed.set_image(url="https://64.media.tumblr.com/85dfa2426b29a8a693ac067218f43a0f/tumblr_mhd2j0PxDV1rrftcdo1_500.gif")
            embed.set_footer(text="oof rip")
            await ctx.send(embed=embed)

@bot.command()
async def roulette(ctx):
   responses =[ f"!bustlingbuttons", "!bumperballoon", "!hexagonheat","!lightsout","!bunglingslots"]
   embed = discord.Embed(title="Mario Party Games!", description=f"Roulette picked {random.choice(responses)}")
   embed.set_image(url="https://thumbs.gfycat.com/IdioticUnlawfulBird-max-1mb.gif")
   await ctx.send(embed=embed)

@bot.command()
async def mariokart(ctx):
  embed = discord.Embed(title="Mario kart!", description="Its'a me! Mario!")
  embed.set_image(url='https://64.media.tumblr.com/40da7a23ec40b93f6e5f06495e9430d2/tumblr_nnqhxg2JSH1s3uawvo2_r1_540.gif')
  embed.add_field(name="Type !startkart to start playing!", value="Hehee")
  await ctx.send(embed=embed)

@bot.command()
async def startkart(ctx):
  embed = discord.Embed(title="Mario kart!", description="Select player!")
  embed.set_image(url='https://c.tenor.com/Jo9FNYqQiLEAAAAC/character-select-player-select.gif')
  await ctx.send(embed=embed)

  try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

  except asyncio.TimeoutError:
     await ctx.send('You took too long...')

  else:
   if msg.content == "":
                  embed = discord.Embed(name="Mario Kart", description=f"**{ctx.message.author.mention} picked {msg.content}!**")
                  embed.add_field(name="Select map!", value="Pick a map!")                                    
                  embed.set_image(url="https://64.media.tumblr.com/dc77c9d637e7c9bf43d1e06046363b55/tumblr_mgppw8EjGj1rtoyhxo1_500.gif")
                  await ctx.send(embed=embed)
     
   else:
         embed = discord.Embed(name="Mario Kart", description=f"**{ctx.message.author.mention} picked {msg.content}!**")
         embed.add_field(name="Select map!", value="Pick a map!")
         embed.set_image(url="https://64.media.tumblr.com/dc77c9d637e7c9bf43d1e06046363b55/tumblr_mgppw8EjGj1rtoyhxo1_500.gif")
         await ctx.send(embed=embed)

  try:
        msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=12.0)

  except asyncio.TimeoutError:
     await ctx.send('You took too long...')

  else:
   if msg.content == "":
        embed = discord.Embed(title="Game started!", description="Mario kart!")
        embed.set_image(url="https://64.media.tumblr.com/tumblr_lem03aHobm1qbj1hto1_500.gif")
        await ctx.send(embed=embed)

   else:
        embed = discord.Embed(title="Game started!", description="Mario kart! Type !startgame")
        embed.set_image(url="https://64.media.tumblr.com/tumblr_lem03aHobm1qbj1hto1_500.gif")
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def startgame(ctx):
  embed = discord.Embed(title="", description="")
  embed.set_image(url="https://64.media.tumblr.com/tumblr_m2qvhhvSUh1r404njo1_500.gif")
  await ctx.send(embed=embed)

  embed = discord.Embed(title="", description="")
  embed.set_image(url="https://c.tenor.com/JCoMTk0paycAAAAC/mario_kart_64-mario-kart.gif")
  await ctx.send(embed=embed)

  embed = discord.Embed(title="", description="")
  embed.set_image(url="https://thumbs.gfycat.com/FakeDemandingFairyfly-size_restricted.gif")
  await ctx.send(embed=embed)
    
@bot.command()
async def space(ctx):
  embed = discord.Embed(title="Python in space!", description="Pretty fun games here")
  embed.set_image(url="https://i.gifer.com/origin/fe/fe9eebde5e19b66192281164142359e4.gif")
  embed.add_field(name="Which games you would like to play?", value="Type !spacejam for list of games")
  await ctx.send(embed=embed)

@bot.command()
async def spacejam(ctx):
  embed = discord.Embed(title="Welcome to spacejam! Check out some games we got:", description="**!coinspace:** \n Flip a coin in space n see some fun results \n **!spacefight**: \n Fight with fucking aliens and see whats gonna happen \n **!spaceship:** \n Travel far in the galaxy \n **!buyspace** \n BUY THE ENTIRE FUCKING SPACEJAM GALAXY", color=0x8563c7)
  await ctx.send(embed=embed)

@bot.command()
async def coinspace(ctx):
  responses = [
    "A fucking alien came and kill you cuz your sound triggered him. R.I.P", "You flipped a space coin and nothing happened", "You flipped the coin and it landed on tails, then tails came on his helicopter and stole the coin", "You flipped the coin, and died of gravitation that landed the coin right on you making it crush your skull", "Absolutely no shit happened",
  ]
  embed = discord.Embed(title="Coinspace", description="You flipped a coin and:")
  embed.add_field(name=f"<a:coin1:973297395762855967><a:coin1:973297395762855967><a:coin1:973297395762855967>", value=f"{random.choice(responses)}")
  await ctx.send(embed=embed)

@bot.command()
async def spacefight(ctx):
  embed = discord.Embed(title="Searching for aliens nearby...", description="Might take a while")
  embed.set_image(url="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/54fcc526-56ba-455b-b6f1-f710ef71d759/de3nrzj-96343590-69b4-4ff9-b159-0265ed789636.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzU0ZmNjNTI2LTU2YmEtNDU1Yi1iNmYxLWY3MTBlZjcxZDc1OVwvZGUzbnJ6ai05NjM0MzU5MC02OWI0LTRmZjktYjE1OS0wMjY1ZWQ3ODk2MzYuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.T65wxI1fzbQY_1SDp6Ax_31F3ErVaIPOt-cEJGiE5KE")
  await ctx.send(embed=embed)

@bot.command()
async def astral(ctx):
  await ctx.send('Pog')

@bot.command()
async def afric(ctx):
  await ctx.send('Sucks')

@bot.command()
async def atclock(ctx):
  await ctx.send("🎧  Chillin' in life")

@bot.command()
async def wacho(ctx):
  await ctx.send('russian')

@bot.command()
async def news(ctx):
  embed = discord.Embed(title="Ukraine is entering a 'long' phase of war, defense minister says", description="Ukraine forced Russia to reduce its targets to an operational and tactical level and is entering a long phase of war, Ukrainian Defense Minister Oleksiy Reznikov said in a statement posted on Facebook on Friday. \n 'In order to win it now, we must carefully plan resources, avoid mistakes, project our strength so that the enemy, in the end, cannot stand up to us', the defense minister said.")
  
  embed.set_footer(text="Reznikov said that after the initial Russian attack on Feb. 24, Moscow was expecting that Ukraine would capitulate in couple of days and the Kremlin would establish a new Russian system in Ukraine.   \n However, Reznikov said, the Ukrainian army and the entire Ukrainian population repulsed the occupiers and thwarted their plans. \n According to Reznikov, an important change also took place at the international level. \n 'In a month, Ukraine achieved integration in the field of defense, which could not be achieved for 30 years. We receive heavy weapons from our partners. In particular, American 155 mm M777 howitzers are already deployed at the front. Three months ago, this was considered impossible,' Reznikov said")
  
  embed.set_image(url="https://dynaimage.cdn.cnn.com/cnn/digital-images/org/a683d86c-4769-473b-b962-10d12db70a9a.JPG")
  await ctx.send(embed=embed)

bot.run('OTczNjMxNjQ1NDU2NDE2ODM4.GYgSHU.Mc2RmMDX2EqVr-VpWiN9QCYaCl-qxDFG4SGQOQ')