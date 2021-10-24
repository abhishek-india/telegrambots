from hashlib import new
import telebot
from bs4 import BeautifulSoup
import requests
from tldextract import extract
import urllib3
import certifi
import codecs
import time
import os

TOKEN = "TOKEN"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

newline='\n'

def soup_creator(link):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    # r = http.request('GET', link, preload_content=False, headers={'User-Agent': _UserAgent})
    r = http.request('GET', link, preload_content=False)
    reader = codecs.getreader('utf-8')
    if r.status == 200:
        urlContent = reader(r).read()
    else:
        raise Exception("Error while downloading edgar document. HTTP Error : ", r.status)
    soup= BeautifulSoup(urlContent, "html.parser") 
    return soup 

def pagelinksgen(ulink,tag,classname):
    pagelink=[]
    soup= soup_creator(ulink)
    for div_b in soup.find_all(tag,{'class':classname}):
        for h3 in div_b.find_all('h3'):
            for link in h3.find_all("a"):
                pagelink.append(link.get("href"))
    return pagelink


@bot.message_handler(commands=['couponlist1'])
def JobList(message):
    os.system("cls||clear")
    msg=bot.send_message(message.chat.id, "Working on List")
    var=''
    cid=msg.chat.id
    mid=msg.message_id
    pagelinks=[] #all page links of all the coupon in www.tutorialbar.com/
    print("Working on List \n")
    ulink='https://www.tutorialbar.com/'
    tag='div'
    classname='elementor-widget-container'
    pagelinks=pagelinksgen(ulink,tag,classname)
    index=0
    count=1
    while index!=20:
        soup=soup_creator(pagelinks[index])
        couponlink=''
        singlebox = soup.find('div', {'class':'priced_block clearfix'})
        for link in singlebox.find_all("a"):
            couponlink=link.get("href")
            break
        www,website,com= extract(couponlink)
        soup=soup_creator(couponlink)
        coupon_title=''
        if website=='udemy':
            scount="Prepared "+str(count)
            bot.edit_message_text(text=scount,chat_id=cid,message_id=mid)
            coupon_title = soup.select('h1.clp-lead__title')[0].text.strip()
            var=var+coupon_title+newline+couponlink+newline+newline
            count=count+1
        else:
            print("Not FREE \n",index)
        index+=1
    print("Done TutorialBar List")
    #print(var)
    bot.edit_message_text(text=str(var),chat_id=cid,message_id=mid,disable_web_page_preview=True)
    # bot.reply_to(message,str(var),disable_web_page_preview=True)

bot.polling()
#tb.polling(none_stop=False, interval=0, timeout=20)
