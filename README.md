# Frenzy Bot Setup and Usage Documentation

Fact : We are all made of stardust [⭐️]


‎ 

## About

**Frenzy Bot** is a [Discord](https://discord.com) bot that treats users to an engaging message-based game in server channels. Prioritizing interactive gameplay, it maximizes user interaction as well as robust admin powers. Users get a chance to win by posting messages in a specific channel, with distinct game features such as cooldown management, spam detection, and admin-controllable option.


## Activity

![Alt](https://repobeats.axiom.co/api/embed/33743cac8e78050c0ee44db1cd79ed13be1cdc09.svg "Repobeats analytics image")

‎ 
‎ 
‎ 

## __Table of Contents__


 >  - [About](#about)
 >  - [Activity](#activity)
 > - [Table of Contents](#table-of-contents)
 > - [Pre-requisites](#pre-requisites)
 > - [Setting Up Environment](#setting-up-environment)
 > - [Installing Dependencies](#installing-dependencies)
 > - [Configuring the Bot](#configuring-the-bot)
 > - [Using the Bot](#using-the-bot)
 > - [Hosting the Bot](#hosting-the-bot)
 > - [Troubleshooting](#troubleshooting)

‎ 
‎ 
‎ 
‎ 

‎ 
‎ 

## Pre-requisites

> Before you begin, ensure you have the following:

- Python 3.13.0: Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- Discord Account and a server: You will need an active Discord account and a server to create a bot and test it.

‎ 
‎ 
‎ 
‎ 

‎ 
‎ 

## Setting Up Environment

> Create a Discord Bot Account:
- Go to the Discord [Developer Portal](https://discord.com/developers/applications).
- Click on "New Application" and enter a name for your bot.
- Navigate to the "Bot" section and click "Add Bot". Confirm the action.


> Save Your Bot Token:
- Under the bot settings, find the “Token” section and click "Copy". You’ll need this token later for configuration.

> Create a New Server (Optional):
- If you don't already have a server for testing, create a new server on Discord. Use the “+” button in the server list to create a new server.

> Invite the Bot to Your Server:

- Under the OAuth2 section, select "URL Generator".
- Under "Scopes", check bot.
- Under "Bot Permissions", check Send Messages, Read Message History, and Read Messages.
- Copy the generated URL and paste it into your browser to invite the bot to your server.

‎ 
‎ 
‎ 
‎ 

‎ 
‎ 

## Installing Dependencies

1. Clone the Repository: Open your terminal and clone the Frenzy Bot repository:
 
 ```python
git clone https://github.com/Zephins/FrenzyBot.git
cd FrenzyBot
```

2. Install the Required Packages: (Ensure you're in the bot's directory.) You can install the required dependencies using pip:

  ```python
pip install -r requirements.txt
```

‎ 
‎ 
‎ 
‎ 

‎ 
‎ 

## Configuring the Bot

> Edit the Bot Token:

- Open the bot's main Python file (e.g., bot.py or main.py).
- Replace the placeholder token in the code with the bot token you copied earlier:

  ```python
  bot.run('YOUR_BOT_TOKEN_HERE')
  ```

‎ 
‎ 
‎ 
‎ 

‎ 
‎ 

##  Using the Bot

- 1. Starting the Message Game: In the text channel where the bot is active, use the command to start a message game:
     ```python
     /start_message_game chance: <number> cooldown: <number> role: <role mention>
     ```
    
  - For example:
    ```python
    /start_message_game chance: 10 cooldown: 5 role: @Players
    ```
    
- 2. Ending the Game: Administrators can end the current game using:
     ```python
     /end_message_game
     ```

- 3. Managing Users: Administrators can ban or unban users from participating in the game with respective commands. For example:
     ```python
     /ban_user_from_message_game @user
     ```
     
     ```python
     /unban_user_from_message_game @user
     ```

- 4. Activating Frenzy Mode: To activate frenzy mode:
     ```python
     /start_frenzy length: <seconds> multiplier: <number>
     ```

- 5. Checking Active Games: You can check all active games currently running with:
     ```python
     /active_games
     ```        

‎ 
‎ 
‎ 
‎ 

‎ 
‎ 

## Hosting the Bot

If you want your bot to be online 24/7, consider hosting it on cloud services. Here are some popular options:

> a. Hosting on Heroku

1. Create a Heroku Account: Sign up on [Heroku](https://www.heroku.com).

2. Install the Heroku CLI: Follow the instructions on Heroku CLI Installation.

3. Create a New Heroku App: In the command line:
   ```bash
   heroku create <app-name>
   ```
4. Set the Bot Token in Heroku:
   ```bash
   heroku config:set DISCORD_TOKEN='YOUR_BOT_TOKEN'
   ```
5. Procfile: Create a file named Procfile in your bot directory with the following content:
   ```bash
   worker: python bot.py
   ```
6. Deploy Your Bot: Commit your changes and push to Heroku:

   ```bash
   git add .
   git commit -m "Deploy Frenzy Bot"
   git push heroku master
   ```

‎ 
‎ 
‎ 
‎ 

‎ 
‎ 

## Troubleshooting

> Bot Won't Start:

- Ensure that you have correctly copied the bot token and have installed all dependencies.
  
> Bot Not Responding:

- Check the permissions of the bot role in your server.
- Make sure you're using the correct command prefixes and input formats.

> Command Errors:

- Ensure that the command parameters are entered correctly, and the role is assigned.


   

<sub><sup>&copy; 2025 [Zephnis](https://github.com/Zephnis)</a>.</sup></sub>
