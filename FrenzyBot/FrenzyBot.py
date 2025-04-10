# some random libraries
import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.messages = True  # Add the message intent
intents.message_content = True  # Add the message content intent
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

# A dictionary to store game information
games = {}
log_channel_id = None  # To store the logging channel ID

# it manages the state of each game including user participation and game rules
class Game:
    def __init__(self, channel, chance, cooldown, role, game_id):
        self.channel = channel
        self.chance = chance
        self.cooldown = timedelta(seconds=cooldown)
        self.role = role
        self.paused = False
        self.banned_users = set()
        self.active = True
        self.user_cooldowns = defaultdict(lambda: datetime.min)
        self.user_message_timestamps = defaultdict(list)  # Track message timestamps for spam detection
        self.spam_timestamps = defaultdict(lambda: datetime.min)  # Track users in timeout
        self.game_id = game_id
        self.frenzy_end_time = None  # Track when the frenzy should end
        self.frenzy_multiplier = 1  # Track frenzy multiplier


    #processes incoming messages to determine if a user can participate in the game.
    async def check_message(self, message):
        if not self.active:
            return

        # Check if the user has the required role, if specified
        if self.role and self.role not in message.author.roles:
            return

        # Check if the user is already banned
        if message.author.id in self.banned_users:
            return

        now = datetime.now()

        # this thing Check for spam
        self.user_message_timestamps[message.author.id].append(now)
        # Keep only the last 5 timestamps
        self.user_message_timestamps[message.author.id] = [timestamp for timestamp in self.user_message_timestamps[message.author.id] if (now - timestamp).seconds <= 3]

        if len(self.user_message_timestamps[message.author.id]) >= 4:
            self.spam_timestamps[message.author.id] = now + timedelta(seconds=15)
            remaining_time = int((self.spam_timestamps[message.author.id] - now).total_seconds())
            await message.author.send(f"You are sending messages too quickly in {self.channel.mention}. Please wait for {remaining_time} seconds before your messages count towards the game again.")
            return

        # Check if the user is currently timed out
        if now < self.spam_timestamps[message.author.id]:
            remaining_time = int((self.spam_timestamps[message.author.id] - now).total_seconds())
            await message.author.send(f"Please wait for {remaining_time} more seconds before your messages count towards the game again in {self.channel.mention}.")
            return

        if now < self.user_cooldowns[message.author.id]:
            return

        self.user_cooldowns[message.author.id] = now + self.cooldown

        current_chance = self.chance
        if self.frenzy_end_time and now < self.frenzy_end_time:
            current_chance *= self.frenzy_multiplier # incrase the chances by frenzy multiplier function

        # Determine if the user wins based on chance
        if random.uniform(0, 100) <= current_chance:
            self.active = False
            await self.channel.send(f"{message.author.mention}, you have won the message game! Make a ticket in <#1356907860659011727> to claim your prize.")
            log_channel = bot.get_channel(log_channel_id) # the log_channel_id which is set by admis it call back here
            if log_channel:
                embed = discord.Embed(
                    title="We have a winner!",
                    description=f"{message.author.mention} has won the message game (ID: {self.game_id}).",
                    color=0xe18feb
                )
                await log_channel.send(embed=embed)

    async def start_frenzy(self, length, multiplier, interaction):
        # Check if a frenzy is already active
        if self.frenzy_end_time and datetime.now() < self.frenzy_end_time:
            await interaction.response.send_message("A frenzy is already active for this game.", ephemeral=True)
            return

        self.frenzy_end_time = datetime.now() + timedelta(seconds=length) # custom set time and date
        self.frenzy_multiplier = multiplier
        await self.channel.send(f"A Message Drop frenzy has started from {self.channel.mention}!\n<@&1261807842579583026>")
        log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="Frenzy has just started",
                description=f"Frenzy has just started in {self.channel.mention}.\nResponsible user for this frenzy: {interaction.user.mention}",
                color=0x66adf4
            )
            await log_channel.send(embed=embed)
        await asyncio.sleep(length)
        self.frenzy_end_time = None
        self.frenzy_multiplier = 1

@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync the commands with Discord
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user: # Ignore messages from the bot itself
        return

    for game in games.values():
        if game.channel == message.channel: # Check all active games
            await game.check_message(message)

    await bot.process_commands(message)

@bot.tree.command(name="set_log_channel_message_game", description="Set the log channel for message game commands")
@app_commands.describe(channel="The channel to log message game commands")
@app_commands.checks.has_permissions(administrator=True)
async def set_log_channel_message_game(interaction: discord.Interaction, channel: discord.TextChannel):
    global log_channel_id
    log_channel_id = channel.id
    await interaction.response.send_message(f"Log channel set to {channel.mention}", ephemeral=True)

@bot.tree.command(name="start_message_game", description="Starts a game with a random message drop")
@app_commands.describe(chance="Chance of message drop (0.00001-100%)", cooldown="Cooldown in seconds", role="Role allowed to play")
@app_commands.checks.has_permissions(administrator=True)
async def start_message_game(interaction: discord.Interaction, chance: float, cooldown: int, role: discord.Role = None):
    global log_channel_id
    if log_channel_id is None:
        await interaction.response.send_message("Log channel is not set. Please set the log channel first using the /set_log_channel_message_game command.", ephemeral=True)
        return

    if not (0.00001 <= chance <= 100):
        await interaction.response.send_message("Chance must be between 0.00001 and 100 percent.", ephemeral=True)
        return
    
    game_id = random.randint(1000, 9999)
    while game_id in games:
        game_id = random.randint(1000, 9999)

    game = Game(interaction.channel, chance, cooldown, role, game_id)
    games[game_id] = game
    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        embed = discord.Embed(
            title="New Message Game Started",
            description=f"A new message game with the ID ({game_id}) has started in {interaction.channel.mention}.\nResponsible user for starting this game: {interaction.user.mention}",
            color=0x02fa02
        )
        await log_channel.send(embed=embed)
    await interaction.response.send_message(f"Game has started and the ID of the game has been sent to {log_channel.mention}", ephemeral=True)

@bot.tree.command(name="end_message_game", description="Ends the message game")
@app_commands.describe(game_id="ID of the game to end")
@app_commands.checks.has_permissions(administrator=True)
async def end_message_game(interaction: discord.Interaction, game_id: int):
    global log_channel_id
    if game_id in games:
        games[game_id].active = False
        if games[game_id].frenzy_end_time:
            games[game_id].frenzy_end_time = None  # End the frenzy if active
            games[game_id].frenzy_multiplier = 1  # Reset the multiplier
        del games[game_id]
        log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="Message Game Ended",
                description=f"The message game with the ID ({game_id}) has been ended.\nResponsible user for ending the game: {interaction.user.mention}", # mention the user who ended the game
                color=0xfa0202
            )
            await log_channel.send(embed=embed)
        await interaction.response.send_message("Game ended and logged.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Game {game_id} not found!", ephemeral=True)

@bot.tree.command(name="ban_user_from_message_game", description="Bans a user from playing the message game")
@app_commands.describe(game_id="ID of the game", user="User to ban") 
@app_commands.checks.has_permissions(administrator=True)
async def ban_user_from_message_game(interaction: discord.Interaction, game_id: int, user: discord.User):
    global log_channel_id
    if game_id in games:
        if user.id in games[game_id].banned_users:
            await interaction.response.send_message("User is already banned from this game.", ephemeral=True)
            return
        
        games[game_id].banned_users.add(user.id)
        log_channel = bot.get_channel(log_channel_id) # the log_channel_id which is set by admis it call back here
        # Send a log message to the log channel log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="Manually banned user from message game",
                description=f"{user.mention} has been banned from the message game with the ID ({game_id}).\nResponsible user for banning: {interaction.user.mention}",
                color=0xfdfe06 # yellow color hex
            )
            await log_channel.send(embed=embed)
        await interaction.response.send_message("User banned and logged.", ephemeral=True) 
    else:
        await interaction.response.send_message(f"Game {game_id} not found!", ephemeral=True)

@bot.tree.command(name="unban_user_from_message_game", description="Unbans a user from playing the message game") # unban the user from the game
@app_commands.describe(game_id="ID of the game", user="User to unban")
@app_commands.checks.has_permissions(administrator=True)
async def unban_user_from_message_game(interaction: discord.Interaction, game_id: int, user: discord.User):
    global log_channel_id
    if game_id in games:
        if user.id not in games[game_id].banned_users:
            await interaction.response.send_message("User is not banned from this game.", ephemeral=True)
            return
        
        games[game_id].banned_users.remove(user.id) # Remove the user from the banned lis
        log_channel = bot.get_channel(log_channel_id)
        if log_channel:
            embed = discord.Embed(
                title="Manually unbanned user from message game",
                description=f"{user.mention} has been unbanned from the message game with the ID ({game_id}).\nResponsible user for unbanning: {interaction.user.mention}",
                color=0x02fa02
            )
            await log_channel.send(embed=embed)
        await interaction.response.send_message("User unbanned and logged.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Game {game_id} not found!", ephemeral=True)

@bot.tree.command(name="active_games", description="Lists all active games")
@app_commands.checks.has_permissions(administrator=True)
async def active_games(interaction: discord.Interaction):
    active_game_ids = [game_id for game_id in games if games[game_id].active]
    if active_game_ids:
        await interaction.response.send_message(f"Active games: {', '.join(map(str, active_game_ids))}", ephemeral=True) # list all the active games
    else:
        await interaction.response.send_message("No active games currently.", ephemeral=True)

@bot.tree.command(name="start_frenzy", description="Starts a frenzy with a chance multiplier")
@app_commands.describe(game_id="ID of the game", length="Length of the frenzy in seconds", multiplier="Chance multiplier", frenzy_chance="Chance this frenzy starts")
@app_commands.checks.has_permissions(administrator=True)
async def start_frenzy(interaction: discord.Interaction, game_id: int, length: int, multiplier: float, frenzy_chance: float):
    global log_channel_id
    if game_id not in games:
        await interaction.response.send_message("Game not found!", ephemeral=True)
        return

    game = games[game_id]
    if not game.active:
        await interaction.response.send_message("Game is not active!", ephemeral=True) 
        return

    if game.frenzy_end_time and datetime.now() < game.frenzy_end_time: # Check if a frenzy is already active
        await interaction.response.send_message("A frenzy is already active for this game.", ephemeral=True)
        return

    await interaction.response.send_message("Frenzy mode initiated. Messages will be checked to start frenzy.", ephemeral=True)
    
    def frenzy_check(m):
        return m.channel == game.channel and m.author != bot.user
    
    message_count = 0
    while message_count < 1:  # Wait for one message to ensure the first one doesn't count
        msg = await bot.wait_for('message', check=frenzy_check)
        message_count += 1
    
    while True:
        msg = await bot.wait_for('message', check=frenzy_check) # Wait for a message await funtion aka frenzy check 
        if random.uniform(0, 100) <= frenzy_chance:
            await game.start_frenzy(length, multiplier, interaction)
            break

# Sync command checks with the bot
@set_log_channel_message_game.error
@start_message_game.error
@end_message_game.error
@ban_user_from_message_game.error
@unban_user_from_message_game.error
@active_games.error
@start_frenzy.error
async def admin_check_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You do not have the necessary permissions to run this command.", ephemeral=True)

bot.run('YOUR_BOT_TOKEN') # Replace with your bot token
