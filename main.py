import discord
from discord import app_commands
import datetime
import random
import math
import asyncio

from model import *

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bots = {}

async def load_bots():
    for row in cur.execute("SELECT guild, channel FROM channels").fetchall():
        guild, channel = row
        bots[(guild, channel)] = bot(guild, channel, False)

#cound time difference in minutes
def timeDif(start):
    if start:
        finish = datetime.datetime.now()
        if finish < start:
            finish += datetime.timedelta(days=1)
        
        dif = (finish - start).total_seconds()
        return math.floor(dif / 60)
    else:
        return 3


@client.event
async def on_ready():
    await tree.sync()
    await load_bots()
    print(f'We have logged in as {client.user}')


@tree.command(name="set_mod_role", description="Set the mod dole")
async def set_mod_role(interaction: discord.Interaction, role: discord.Role):
    if interaction.user.guild_permissions.administrator:
        if cur.execute("SELECT 1 FROM mod_roles WHERE guild = ? AND role = ?", (interaction.guild.id, role.id)).fetchone() == None:
            cur.execute("INSERT INTO mod_roles VALUES (?, ?)", (interaction.guild.id, role.id))
            data.commit()
            await interaction.response.send_message("New mod role set")
        else:
            await interaction.response.send_message("This role is already a mod role")
    else:
        await interaction.response.send_message("You don't have permissons to use this command")

@tree.command(name="remove_mod_role", description="Remove the mod dole")
async def remove_mod_role(interaction: discord.Interaction, role: discord.Role):
    if interaction.user.guild_permissions.administrator:
        if cur.execute("SELECT 1 FROM mod_roles WHERE guild = ? AND role = ?", (interaction.guild.id, role.id)).fetchone() != None:
            cur.execute("DELETE FROM mod_roles WHERE guild = ? AND role = ?", (interaction.guild.id, role.id))
            data.commit()
            await interaction.response.send_message("Mod role removed")
        else:
            await interaction.response.send_message("This role is not a mod role")
    else:
        await interaction.response.send_message("You don't have permissons to use this command")

@tree.command(name="set_dialo", description="Set the bot to the channel")
async def set_dialo(interaction: discord.Interaction):
    role_ids = []
    for role in interaction.user.roles:
        role_ids.append(role.id)
    if interaction.user.guild_permissions.administrator or any(item[0] in role_ids for item in cur.execute("SELECT role FROM mod_roles WHERE guild = ?", (interaction.guild.id, )).fetchall()):
        if cur.execute("SELECT 1 FROM channels WHERE guild = ? AND channel = ?", (interaction.guild.id, interaction.channel.id)).fetchone() == None:
            bots[interaction.guild.id, interaction.channel.id] = bot(interaction.guild.id, interaction.channel.id, True)
            await interaction.response.send_message("Dialo channel set")
        else:
            await interaction.response.send_message("This channel already has dialo set")
    else:
        await interaction.response.send_message("You don't have permissons to use this command")

@tree.command(name="remove_dialo", description="Remove the bot to the channel")
async def remove_dialo(interaction: discord.Interaction):
    role_ids = []
    for role in interaction.user.roles:
        role_ids.append(role.id)
    if interaction.user.guild_permissions.administrator or any(item[0] in role_ids for item in cur.execute("SELECT role FROM mod_roles WHERE guild = ?", (interaction.guild.id, )).fetchall()):
        if cur.execute("SELECT 1 FROM channels WHERE guild = ? AND channel = ?", (interaction.guild.id, interaction.channel.id)).fetchone() != None:
            del bots[interaction.guild.id, interaction.channel.id]
            cur.execute("DELETE FROM channels WHERE guild = ? AND channel = ?", (interaction.guild.id, interaction.channel.id))
            data.commit()
            await interaction.response.send_message("Dialo channel removed")
        else:
            await interaction.response.send_message("This channel does not has dialo set")
    else:
        await interaction.response.send_message("You don't have permissons to use this command")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if cur.execute("SELECT 1 FROM channels WHERE guild = ? AND channel = ?", (message.guild.id, message.channel.id)).fetchone() != None:
        id = (message.guild.id, message.channel.id)
        difTime = timeDif(bots[id].last_message)
        if difTime >= 2:
            bots[id].chat_history_ids = None
            bots[id].step = False

        bots[id].last_message = datetime.datetime.now()

        #check users and time they last messaged
        for user in bots[id].users[:]:
            if user[0] == message.author or timeDif(user[1]) >= 1:
                bots[id].users.remove(user)

        bots[id].users.append((message.author, bots[id].last_message))

        #logic of sending messages
        if bots[id].is_typing == False: #if the bot is busy typing, it does not reply, but simply adds user's message to history
            #bot always replies if mentioned
            if client.user.mentioned_in(message):
                async with message.channel.typing():
                        bots[id].is_typing = True
                        await asyncio.sleep(random.randint(3, 5))
                        bots[id].is_typing = False
                        await message.channel.send(bots[id].generate_reply(message.content, True))

            else:
                #probabily the bot sends a message scales down as number of users increases
                if random.randint(1,10) <= math.ceil(8/len(bots[id].users)):
                    async with message.channel.typing():
                        bots[id].is_typing = True
                        await asyncio.sleep(random.randint(3, 5))
                        bots[id].is_typing = False
                        await message.channel.send(bots[id].generate_reply(message.content, True))
                else:
                    bots[id].generate_reply(message.content, False)
        else:
            bots[id].generate_reply(message.content, False)
    

client.run('Your Token')