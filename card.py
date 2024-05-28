from difflib import SequenceMatcher
import sys
import requests   
from bs4 import BeautifulSoup  
import re
import discord 
from discord import app_commands
from discord.ext import commands 
import os
from dotenv import load_dotenv

#--------------TEST---BRANCH-!-!-!-!-!-!-!---------#

# add auto updater function to this code, or just access the otehr file.#

# current issue; after it successfully finds, it needs to restart the loop, but its continuing. need to reset loop#

#  delimeter _-_ space in front/back of hyphen possibly.... #

load_dotenv('.env')
bot = commands.Bot(command_prefix="!", intents = discord.Intents.default() )

global cardList 
cardList = open("card-list.txt","r")

@bot.event
async def on_ready():   
    print("Bot is ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

global isTrue
global finalName
isTrue = False
global foundName
global globalLineCount
globalLineCount = 0
def compare_strings(cardFullName, nameInList):
    print(str(cardFullName)+" vs " + str(nameInList))
    if SequenceMatcher(None, cardFullName, nameInList).ratio() >= 0.87: #if 87% similar then true.
        print("FOUNDDDDDDDDD")
        global foundName
        foundName = nameInList
        isTrue = True 
        globalLineCount = 0
    else:
        print("Not found: ")
        isTrue = False
        
    if isTrue == True:
        return isTrue
    else:
        listSize = sum(1 for _ in open('card-list.txt'))  
        for globalLineCount in cardList:
            if compare_strings(cardFullName.lower(),globalLineCount.strip().lower()):
                finalName = globalLineCount.strip()
                isTrue = True
                cardList.seek(0)
                break           
    return isTrue
    
@bot.tree.command(name="cardsearch")
@app_commands.describe(card_to_find = "first name - second name")
async def cardSearchResult(interaction: discord.Interaction, card_to_find: str):
    userInput = card_to_find
    global cardFullName #inputed by user
    global firstName
    global secondName
    #---card has to be in [first name - second name] format
    #---splits the card into two names---#
    cardFullName = userInput.split("-",1)
    firstName = cardFullName[0]
    firstName = firstName[:-1]
    
    if compare_strings(userInput, "Ursula - deceiver of all"):
        
        async def results(finalName):
            #------------name----to-----link-----------------#   
            cardFullName = foundName.split("-",1)
            firstName = cardFullName[0]
            #firstName = firstName[:-1]
            if len(cardFullName) == 2:
                firstName = firstName[:-1]
                secondName = cardFullName[1] 
                secondName = secondName[1:]
                secondName = cardFullName[1] 
                secondName = secondName[1:]
                firstNameLink = firstName.replace(" ","-")
                secondNameLink = secondName.replace(" ","-")
                url = 'https://dreamborn.ink/cards/%s/%s' % (firstNameLink,secondNameLink)
            else:
                firstNameLink = firstName.replace(" ","-")
                url = 'https://dreamborn.ink/cards/%s' % (firstNameLink)
            print(foundName)
            print(url)
            globalLineCount = 0
            #------------name----to-----link-----------------# 
            
            r = requests.get(url, timeout=10.000)
            if r.status_code == 404:
                await interaction.response.send_message(f"mispelled, try [card first name - card second name]")
                cardList.seek(0)
                
            else:
                r.text
                soup = BeautifulSoup(r.text,'html.parser')
                array = [item.get_text() for item in soup.findAll('div', class_="flex items-center justify-end")]
                newArr = [] #array with just prices
                for i in array:
                    pattern = re.compile(r'\-?\d+\.\d+')
                    diffPrices = list(map(float, re.findall(pattern, i)))
                    newArr.append(diffPrices)
                    
                if len(newArr) < 3:
                    await interaction.response.send_message(f"Non-foil price: ${newArr[0]}\nFoil price: ${newArr[1]} \n {url}")
                elif len(newArr) > 2:
                    await interaction.response.send_message(f"Non-foil price: ${newArr[0]}\nFoil price: ${newArr[1]} \nEnchanted price: ${newArr[2]} \n {url}")    
        await results(foundName)
    else:
        cardList.seek(0)
        await interaction.response.send_message(f"mispelled, try [card first name - card second name]")
        
        os.execl(sys.executable, sys.executable, *sys.argv)
    globalLineCount = 0

   

bot.run(os.getenv('TOKEN'))


