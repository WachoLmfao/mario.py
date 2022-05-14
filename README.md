# mario.py
Multipurpose discord bot with 2455 lines of code, Currency, moderation, fun, mario custom commands and much more
Don't forget to change your token in the last line.
Also few commands as !bak are optimized for me, example:

  @bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def bak(ctx):
  if ctx.author.id == YOUR_ID_HERE:
    await ctx.send("Well, since you won the giveaway here you go 1000000 coins!")
    amounts[str(YOUR_ID_HERE)]['coins'] += 10000000
    _save()
  else:
    await ctx.send("BACK OFF! THIS IS PRIVATE COMMAND!")
  
 
