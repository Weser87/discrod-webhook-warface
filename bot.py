import requests
import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
#from config import settings
import time
from bs4 import BeautifulSoup
import lxml
from datetime import datetime


LASTLINK = 'last_link.txt'
LINK = 'https://pc.warface.com/news/'
first_run = True
webhook_id = 'ID'
webhook_token = 'TOKEN'
#webhook_id = settings['id']
#webhook_token = settings['token']


def get_links(file=LASTLINK):
    last_link = []
    txt_file = open(file)

    for line in txt_file:
        last_link.append(line)
    
    txt_file.close()
    return last_link


def add_link(link:str, file=LASTLINK):
    txt_file = open(file, 'a')
    txt_file.write(link + '\n')
    txt_file.close()


webhook = Webhook.partial(webhook_id, webhook_token, adapter=RequestsWebhookAdapter())

#async def news_parser():
while True:
    link_adding = True
    #last_link = get_last_link()
    last_links = get_links()
    news_page = requests.get(LINK)
    news_page = BeautifulSoup(news_page.text, features='lxml')

    for item in news_page.find_all("li", {"class": "views-row"}):
        link = item.find('a', href=True)
        link = 'https://pc.warface.com' + link['href']
        if link + '\n' not in last_links:
            add_link(link)
            print(link)
            
            news_title = item.find("div", {"class": "views-field-title"})
            news_title = news_title.find('a', href=True)
            news_title_text = news_title.text
            news_title = '[' + news_title_text + ']' + '(' + link + ')'
            news_description = item.find('p')
            news_description = news_description.text
            news_image = item.find('img')
            news_image = news_image['src']

            embed = discord.Embed(
                title = news_title_text,
                url = link,
                description = news_description,
                timestamp = datetime.now()
                #author = 'Warface News'
            )
            embed.set_image(url=news_image)
            embed.set_footer(text="Warface News", icon_url="https://upload.wikimedia.org/wikipedia/ru/b/be/Warface.png")
            webhook.send(embed=embed)
            #await news_sender(embed)
    #await asyncio.sleep(10)
    time.sleep(600)
