from difflib import SequenceMatcher
import requests   
from bs4 import BeautifulSoup  
import re
import discord 
from discord import app_commands
from discord.ext import commands 
import os
from dotenv import load_dotenv

#--------------test branch------------#

load_dotenv('.env')
bot = commands.Bot(command_prefix="!", intents = discord.Intents.default() )

@bot.event
async def on_ready():
    print("Bot is ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

def returnLoop():
    cardSearchResult()
    
def spellChecker(firstName, secondName):
    s = SequenceMatcher(None, firstName, "bcde")
    url = 'https://dreamborn.ink/cards/%s/%s' % (firstName, secondName)
    r = requests.get(url, timeout=10.000)
    
    
@bot.tree.command(name="cardsearch")
@app_commands.describe(card_to_find = "Card to find?")
async def cardSearchResult(interaction: discord.Interaction, card_to_find: str):
    userInput = card_to_find
    #---card has to be in [first name - second name] format
    #---splits the card into two names---#
    cardResult = userInput.split("-",1)
    firstName = cardResult[0].replace(" ", "-")
    if firstName[0] == '-':
        firstName = firstName[1:]
    if firstName[-1] == '-':
        firstName = firstName[:-1]

    secondName = cardResult[1].replace(" ", "-")    
    if secondName[0] == '-':
        secondName = secondName[1:]
    if secondName[-1] == '-':
        secondName = secondName[:-1]
    #-------------------------------------#    
    url = 'https://dreamborn.ink/cards/%s/%s' % (firstName, secondName)
   
    r = requests.get(url, timeout=10.000)
    if r.status_code == 404:
        interaction.response.send_message(f"mispelled try again")
    else:
        r.text
        soup = BeautifulSoup(r.text,'html.parser')
        tcgPrice = soup.findAll('div', class_="flex items-center justify-end")
        array = [item.get_text() for item in soup.findAll('div', class_="flex items-center justify-end")]
        newArr = [] #array with just prices
        for i in array:
            pattern = re.compile(r'\-?\d+\.\d+')
            diffPrices = list(map(float, re.findall(pattern, i)))
            newArr.append(diffPrices)
            
        if len(newArr) < 3:
            await interaction.response.send_message(f"Non-foil price: {newArr[0]}\nFoil price: {newArr[1]} \n {url}")
        elif len(newArr) > 2:
            await interaction.response.send_message(f"Non-foil price: {newArr[0]}\nFoil price: {newArr[1]} \nEnchanted price: {newArr[2]} \n {url}")
       
bot.run(os.getenv('TOKEN'))


