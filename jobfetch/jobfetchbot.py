import telebot
from bs4 import BeautifulSoup
import requests
import time
import os

from telebot.types import Message

TOKEN = "YOUR TOKEN"
bot = telebot.TeleBot(TOKEN)

_UserAgent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
newline='\n'

def soup_creator(link):
    headers = { 'User-Agent': _UserAgent}
    url=requests.get(link,headers=headers)
    soup= BeautifulSoup(url.text, "html.parser")
    return soup

def pagelinksgen(ulink,tag,classname):
    pagelink=[]
    soup= soup_creator(ulink)
    for div_b in soup.find_all(tag,{'class':classname}):
        for h3 in div_b.find_all('h3'):
            for link in h3.find_all("a"):
                pagelink.append(link.get("href"))
    return pagelink

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['joblist1'])
def JobList(message):
    msg=bot.send_message(message.chat.id, "Working on List")
    cid=msg.chat.id
    mid=msg.message_id
    pagelinks=[]
    var=''
    os.system("cls||clear")
    print("Working on List \n")
    ulink='https://jobs4fresher.com/'   #Please take permisiion from respective site
    tag='article'
    classname='jeg_post jeg_pl_sm format-quote'
    pagelinks=pagelinksgen(ulink,tag,classname)
    index=0
    count=1
    while index!=24:
        soup=soup_creator(pagelinks[index])
        job_title = soup.select('h1.jeg_post_title')[0].text.strip()
        var=var+job_title+newline
        for h4 in soup.find_all('h4'):
            for link in h4.find_all("a"):
                var=var+link.get("href")+newline+newline
                scount="Prepared "+str(count)
                bot.edit_message_text(text=scount,chat_id=cid,message_id=mid)
        index=index+1
        count=count+1
    print("Done job4freshers List")
    bot.edit_message_text(text=str(var),chat_id=cid,message_id=mid,disable_web_page_preview=True)
    # bot.reply_to(message,str(var),disable_web_page_preview=True)

bot.polling()
#tb.polling(none_stop=False, interval=0, timeout=20)
