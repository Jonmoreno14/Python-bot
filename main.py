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


#  delimeter _-_ space in front/back of hyphen possibly.... #


class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

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
    
    if compare_strings(userInput, "Ursula - deceiver of all"):
        
        async def results(finalName):
            #------------name----to-----link-----------------#   
           
            nameToLink = foundName.replace(" ","-")
            url = 'https://lorcanaplayer.com/lorcana-card-list/%s' % (nameToLink)
            print(foundName)
            print(url)
            globalLineCount = 0
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
                url = 'https://lorcanaplayer.com/lorcana-card-list/%s-%s' % (firstNameLink,secondNameLink)
            elif len(cardFullName) ==0:
                url = 'https://lorcanaplayer.com/lorcana-card-list/%s' % (nameToLink)
            else:
                firstNameLink = firstName.replace(" ","-")
                url = 'https://lorcanaplayer.com/lorcana-card-list/%s' % (nameToLink)
            
            
            #----------get--the--prices----------------------#
            print(url) ##problem
            r = requests.get(url, timeout=10.000)
           
            if r.status_code == 404:
                await interaction.response.send_message(f"mispelled, try [card first name - card second name]")
                print("issue here")
                cardList.seek(0)
                
            else:
                r.text
                soup = BeautifulSoup(r.text,'html.parser')
                array = [item.get_text() for item in soup.findAll('span', class_="btn-price")]
                newArr = [] #array with just prices
                for i in array:
                    pattern = re.compile(r'\-?\d+\.\d+')
                    diffPrices = list(map(float, re.findall(pattern, i)))
                    newArr.append(str(diffPrices))
                            
                print(array)
                print(newArr)
                p1 = newArr[0]
                p1 = p1[1:]
                p1 = p1[:-1]
                p2 = newArr[1]
                p2 = p2[1:]
                p2 = p2[:-1]
                p1 = float(p1)
                p2 = float(p2)
                
                await interaction.response.send_message(f"[Non-foil price]: ${"%.2f" % p1},   €{"%.2f" % (p1*(0.92))}\n[Foil price]: ${"%.2f" % p2},   €{"%.2f" % (p2*(0.92))} \n {url}")
        
        await results(foundName)
    else:
        cardList.seek(0)
        await interaction.response.send_message(f"mispelled, try [card first name - card second name]")
        
        os.execl(sys.executable, sys.executable, *sys.argv)
    globalLineCount = 0

   

bot.run(os.getenv('TOKEN'))


