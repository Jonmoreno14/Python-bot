from difflib import SequenceMatcher
import requests   
from bs4 import BeautifulSoup  
import re
import discord 
from discord import app_commands
from discord.ext import commands 
import os
from dotenv import load_dotenv
import pandas as pd
import re
import json

url = 'https://lorcanaplayer.com/lorcana-card-list/'
   
r = requests.get(url, timeout=10.000)
r.text
soup = BeautifulSoup(r.text,'html.parser')
cardList = open("card-list.txt","w")

def updateCardList():
    cardNameFinder = soup.findAll('body', class_="card-name" )
    array = [item.get_text() for item in soup.findAll('td', class_="card-name")]
    length = len(array)
    for i in range(length):
        #print(array[i])
        cardList.write(str(array[i])+"\n")
    print("List updated!")
    
updateCardList()
cardList.close()

