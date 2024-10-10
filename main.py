# Triggered Words
import nextcord
from nextcord.ext import commands
import json
import asyncio
from datetime import timedelta


with open('config.json') as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix='!', intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    print(f'⭐ Bot is ready & online, coded by https://github.com/vkecodes')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.author.guild_permissions.administrator:
        return 

    if any(role.id in config["whitelisted_roles"] for role in message.author.roles):
        return 

    message_content_lower = message.content.lower()

    for word in config["blacklisted_words"]:
        if word.lower() in message_content_lower:  
            embed = nextcord.Embed(
                description=f"{message.author.mention}, you have been muted for saying a **blacklisted word**.",
                color=nextcord.Color.light_grey() 
            )
            embed.set_footer(text="⭐ Credits: https://github.com/vkecodes")
            
            await message.channel.send(embed=embed)
            await message.delete()

            timeout_duration = timedelta(seconds=config["timeout_duration"])

            await message.author.timeout(timeout_duration)

            dm_embed = nextcord.Embed(
                description="> You have been timed out for saying a **blacklisted** word.",
                color=nextcord.Color.light_grey()
            )
            try:
                await message.author.send(embed=dm_embed)
            except nextcord.Forbidden:
                print(f"Couldn't send a DM to a user")

            break
    else:
        for trigger in config["auto_trigger"]:
            if any(word.lower() in message_content_lower for word in trigger["words"]): 
                await message.reply(trigger["response"])
                break

    await bot.process_commands(message)
bot.run(config["token"])
