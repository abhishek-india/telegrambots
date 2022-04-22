from hashlib import new
import telebot
from bs4 import BeautifulSoup
import requests
from tldextract import extract
import urllib3
import certifi
import codecs
import os
import random

TOKEN = " "
bot = telebot.TeleBot(TOKEN)

user_agent=[
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0',
'Mozilla/5.0 (X11; Linux; rv:74.0) Gecko/20100101 Firefox/74.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/73.0',
'Mozilla/5.0 (X11; OpenBSD i386; rv:72.0) Gecko/20100101 Firefox/72.0',
'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:71.0) Gecko/20100101 Firefox/71.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20191022 Firefox/70.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20190101 Firefox/70.0',
'Mozilla/5.0 (Windows; U; Windows NT 9.1; en-US; rv:12.9.1.11) Gecko/20100821 Firefox/70',
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:69.2.1) Gecko/20100101 Firefox/69.2',
'Mozilla/5.0 (Windows NT 6.1; rv:68.7) Gecko/20100101 Firefox/68.7',
'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0',
'Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0',
'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 Firefox/62.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/62.0']

HEADERS = ({'User-Agent':random.choice(user_agent)})

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)


newline='\n'

def soup_creator(link):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    # r = http.request('GET', link, preload_content=False, headers={'User-Agent': _UserAgent})
    r = http.request('GET', link, preload_content=False,headers=HEADERS)
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


@bot.message_handler(commands=['tutorialbar'])
def tutorialbar(message):
    os.system("cls||clear")
    msg=bot.send_message(message.chat.id, "Working on tutorialbar")
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
    while index!=12:
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



@bot.message_handler(commands=['coursevania'])
def coursevania(message):
    os.system("cls||clear")
    msg=bot.send_message(message.chat.id, "Working on coursvania")
    var=''
    cid=msg.chat.id
    mid=msg.message_id
    pagelinks=[] #all page links of all the coupon in www.tutorialbar.com/
    print("Working on List \n")
    url= requests.get("https://www.coursevania.com")
    soup= BeautifulSoup(url.text, "html.parser")

    for div_a in soup.find_all('div',{'class':'stm_lms_recent_courses'}):
        for div_b in div_a.find_all('div', {'class':'stm_lms_courses__single stm_lms_courses__single_animation no-sale style_1'}):
            for div_c in div_b.find_all('div',{'class':'stm_lms_courses__single--image'}):
                for link in div_c.find_all("a"):
                    pagelinks.append(link.get("href"))
                    # print(link.get("href"))
    index=0
    count=1
    while index<10:
        soup=soup_creator(pagelinks[index])
        coupon_title=''
        couponlink=''
        for coupon in soup.find_all('div',{'class':'stm-lms-buy-buttons'}):
            for link in coupon.find_all("a"):
                couponlink=link.get("href")
                #print(couponlink)
        soup=soup_creator(couponlink)
        coupon_title = soup.select('h1.clp-lead__title')[0].text.strip()
        var=var+coupon_title+newline+couponlink+newline+newline
        scount="Prepared "+str(count)
        bot.edit_message_text(text=scount,chat_id=cid,message_id=mid)
        # print(coupon_title)
        # print(couponlink)
        # print('')
        index+=1
        count+=1
    print("DONE")
    bot.edit_message_text(text=str(var),chat_id=cid,message_id=mid,disable_web_page_preview=True)
    # bot.reply_to(message,str(var),disable_web_page_preview=True)



@bot.message_handler(commands=['discudemy'])
def discudemy(message):
    os.system("cls||clear")
    msg=bot.send_message(message.chat.id, "Working on Discudemy")
    cid=msg.chat.id
    mid=msg.message_id
    pagelinks=[] #all page links of all the coupon in discudemy.com/language/english
    var=''

    os.system("cls||clear")
    print("Working on List \n")

    url= requests.get("https://www.discudemy.com/language/english/",headers=HEADERS)
    soup= BeautifulSoup(url.text, "html.parser")
    for div_b in soup.find_all('article', {'class':'ui four stackable cards m15'}):
        for link in div_b.find_all("a"):
            pagelinks.append(link.get("href"))

    index=0
    count=1
    while index!=15:  
        soup=soup_creator(pagelinks[index])
        n=0
        page2links='' #all links from page 2 and link for page 3 is in index 12
        for a in soup.find_all('a', href=True):
            if (n==12):
                page2links=a['href']
                break
            n=n+1
        soup=soup_creator(page2links)

        couponlink=''
        singlebox = soup.find(class_="ui attached segment")
        for link in singlebox.find_all("a"):
            couponlink=link.get("href")
            break
        # print(couponlink)

        #To go to coupon website
        soup=soup_creator(couponlink)
        
        coupon_title = soup.select('h1.clp-lead__title')[0].text.strip()
        var=var+coupon_title+newline+couponlink+newline+newline
        
        print(f"Prepared {count} \n")
        scount="Prepared "+str(count)
        bot.edit_message_text(text=scount,chat_id=cid,message_id=mid)
        count=count+1
        index=index+1
    bot.edit_message_text(text=str(var),chat_id=cid,message_id=mid,disable_web_page_preview=True)


@bot.message_handler(commands=['coursefolder'])
def coursefolder(message):
    os.system("cls||clear")
    msg=bot.send_message(message.chat.id, "Working on coursefolder")
    var=''
    cid=msg.chat.id
    mid=msg.message_id
    pagelinks=[] #all page links of all the coupon in www.tutorialbar.com/
    print("Working on List \n")
    url= requests.get("https://coursefolder.net/free-udemy-coupon.php",headers=HEADERS)
    soup= BeautifulSoup(url.text, "html.parser")

    for link in soup.find_all('a',{'class':'font-title--card'}):
        pagelinks.append(link.get("href"))
    
    index=0
    while index!=25:
        soup=soup_creator(pagelinks[index])
        ctitle=soup.find("h3",{"class":"font-title--sm"}).get_text().strip()
        # print(ctitle)
        couponlink = str(soup.find('button', {'class':'button button-lg button--primary w-100'}))
        findex=77
        lindex=couponlink.find("','")
        couponlink=couponlink[findex:lindex]
        # print(couponlink)
        var=var+newline+ctitle+newline+couponlink+newline
        index=index+1
        scount="Prepared "+str(index+1)
        bot.edit_message_text(text=scount,chat_id=cid,message_id=mid)
    bot.edit_message_text(text=str(var),chat_id=cid,message_id=mid,disable_web_page_preview=True)
    # bot.reply_to(message,str(var),disable_web_page_preview=True)


#bot.polling()
# bot.polling(none_stop=False, interval=0, timeout=20)
bot.infinity_polling()
