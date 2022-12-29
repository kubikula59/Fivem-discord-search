import os
import requests
import json
from datetime import datetime
import discord
import discord_slash
from discord_slash import SlashCommand
from discord.ext import commands


# Example, change this as you want
server_endpoint = "https://main.tror.eu/players.json"

discord_api_key = os.environ['DISCORDAPIKEY']
client = discord.Client() 
slash = SlashCommand(client, sync_commands=True)

# Log to console on startup
@client.event
async def on_ready():
  print("Succesfully logged as {0.user}".format(client))

# Search by ID
@slash.slash(name="software_id", description="Získá identifikátory hráče na základě ingame ID.",
             options=[discord_slash.manage_commands.create_option(name="id", description="Zadejte ID hráče", option_type=4, required=True)])
async def software_id(ctx: discord_slash.SlashContext, id):
  source = requests.get(server_endpoint)
  json_data = json.loads(source.text)
  api_data_size = len(json_data)
  for i in range(api_data_size):
    if(json_data[i]["id"] == int(id)):
      for u in range(30):
        all_identifiers = json_data[i]["identifiers"][u]
        if("discord") in all_identifiers:
          prettyDiscord = json_data[i]["identifiers"][u]
          discordId = prettyDiscord.replace('discord:', '')

          userndiscrim = requests.get("https://discord.com/api/v9/users/" + discordId, headers={"Authorization" : discord_api_key})
          userndiscrim2 = json.loads(userndiscrim.text)

          for y in range(30):
            all_identifiers = json_data[i]["identifiers"][y]
            if("steam") in all_identifiers:
              prettySteam = json_data[i]["identifiers"][y]
              steamHex = prettySteam.replace('steam:', '').strip().upper()

              # Convert steam hex to normal value
              conversion_table = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10 , 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
              decimal = 0
              power = len(steamHex) -1

              for digit in steamHex:
                decimal += conversion_table[digit]*16**power
                power -= 1
              
              # Complete links that will be provided to user
              steamfulllink = "https://steamcommunity.com/profiles/" + str(decimal)
              discordlink = "<@" + discordId + ">" + " " + userndiscrim2["username"] + "#" + userndiscrim2["discriminator"]

              embedVar = discord.Embed(title="", description="", color=0x096bff)
              embedVar.add_field(name="[+] Discord", value=discordlink, inline=False)
              embedVar.add_field(name="[+] Steam", value=steamfulllink, inline=False)
              embedVar.set_footer(text=datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
              await ctx.send(embed=embedVar)
              return


# Search by steam nick
@slash.slash(name="software_steam", description="Získá identifikátory hráče na základě steamu",
             options=[discord_slash.manage_commands.create_option(name="steam", description="Zadejte steam nick hráče", option_type=3, required=True)])
async def software_id(ctx: discord_slash.SlashContext, steam):
  source = requests.get(server_endpoint)
  json_data = json.loads(source.text)
  api_data_size = len(json_data)

  for i in range(api_data_size):
    if(json_data[i]["name"] == steam):
      for u in range(30):
        all_identifiers = json_data[i]["identifiers"][u]
        if("discord") in all_identifiers:
          prettyDiscord = json_data[i]["identifiers"][u]
          discordId = prettyDiscord.replace('discord:', '')

          userndiscrim = requests.get("https://discord.com/api/v9/users/" + discordId, headers={"Authorization" : discord_api_key})
          userndiscrim2 = json.loads(userndiscrim.text)

          for y in range(30):
            all_identifiers = json_data[i]["identifiers"][y]
            if("steam") in all_identifiers:
              prettySteam = json_data[i]["identifiers"][y]
              steamHex = prettySteam.replace('steam:', '').strip().upper()

              # Convert steam hex to normal value
              conversion_table = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10 , 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
              decimal = 0
              power = len(steamHex) -1

              for digit in steamHex:
                decimal += conversion_table[digit]*16**power
                power -= 1

              # Complete links that will be provided to user
              steamfulllink = "https://steamcommunity.com/profiles/" + str(decimal)
              discordlink = "<@" + discordId + ">" + " " + userndiscrim2["username"] + "#" + userndiscrim2["discriminator"]
                  
              embedVar = discord.Embed(title="", description="", color=0x096bff)
              embedVar.add_field(name="[+] Discord", value=discordlink, inline=False)
              embedVar.add_field(name="[+] Steam", value=steamfulllink, inline=False)
              embedVar.set_footer(text=datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
              await ctx.send(embed=embedVar)
              return
              