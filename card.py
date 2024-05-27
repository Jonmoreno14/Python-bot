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
    
def spellChecker(fullName):
    isTrue = False
    f = open('card-list.txt', 'r')
    lines = f.readlines()
    
    def compare_strings(string1, string2):
        if SequenceMatcher(None, string1, string2).ratio() >= 0.7:
            print("success: " + fullName)
            
            return 
            #go to new functioun to print out result.
        else:
            print("didnt find")
            
    for line in lines:
        compare_strings(fullName,line.strip())            
        #SequenceMatcher(None, string1, string1).ratio()
        #pattern = re.compile(string2)
        #match = re.search(pattern, string1)
        #print(match)
    return True
    
@bot.tree.command(name="cardsearch")
@app_commands.describe(card_to_find = "Card to find?")
async def cardSearchResult(interaction: discord.Interaction, card_to_find: str):
    userInput = card_to_find
    #---card has to be in [first name - second name] format
    #---splits the card into two names---#
    cardResult = userInput.split("-",1)
    firstName = cardResult[0]
    firstName = firstName[:-1]
    secondName = cardResult[1]
    secondName = secondName[1:]
    
    
    
    # give results the spell corrected one IFFFF found  #
    async def results(firstName, secondName):
        #-------------------------------------#    
        firstNameLink = firstName.replace(" ","-")
        secondNameLink = secondName.replace(" ","-")
        print(firstNameLink+"\n")
        print(secondNameLink+" ")
        url = 'https://dreamborn.ink/cards/%s/%s' % (firstNameLink,secondNameLink)

        r = requests.get(url, timeout=10.000)
        if r.status_code == 404:
            await interaction.response.send_message(f"mispelled, try [card first name - card second name]")
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
   
    fullName = str(firstName) + " - "+ str(secondName)
    if spellChecker(fullName):
        await results(firstName, secondName)
    else:
        print("spot 3")
    

bot.run(os.getenv('TOKEN'))


