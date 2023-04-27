import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
import asyncio
import threading
from Sel import check,getcode,givecode,login,acceptnumber,join,seen
import pytz
import datetime
import re
import config

time_zone = pytz.timezone('Asia/Tehran')
now = datetime.datetime.now(time_zone)
time = now.strftime("%Y-%m-%d %H:%M:%S")
bot = telebot.TeleBot(config.token)
admin = config.admin
channelcheckout = config.channelcheckout
mincoin = config.mincoin

texts = {"start" : "✋🏻 سلام کاربر گرامی به ربات دریافت اکانت خوش آمدید \n👇🏻 برای ارسال اکانت میتوانید از دکمه زیر استفاده کنید",
  "getcode" : "👇🏻 لطفا شماره مجازی خود را به همراه پیش شماره ارسال کنید",
  "loading" : "🔄 در حال پردازش لطفا منتظر باشید ...",
  "error" : "مشکلی پیش امده لطفا دوباره تلاش کنید",
  "supportok" : "☑️ پیام شما با موفقیت ارسال شد منتظر پاسخ پشتیبانی باشید",
  "startpanel" : "👨‍💼به پنل مدیریت خوش آمدید👨‍💼",
  "givetedad" : "🔢 تعداد اکانت مورد نظر (نباید بیشتر از تعداد اکانت های موجود روی ربات باشد)", 
  "giveusernameseen" : "🔗 لینک پست مورد نظر را ارسال نمایید \n مثال :\n https://t.me/Khabar_Fouri/308884",
  "giveusername" : "🆔 کانال مورد نظر همراه @",
  "givecode" : "👇🏻 لطفا شماره مجازی مورد نظر را به همراه پیش شماره ارسال کنید",
  "support" : "👮🏻 همکاران ما در خدمت شما هستن \n\n\n• سعی بخش پشتیبانی بر این است که تمامی پیام های دریافتی در کمتر از ۱۲ ساعت پاسخ داده شوند، بنابراین تا زمان دریافت پاسخ صبور باشید\n\n• لطفا پیام، سوال، پیشنهاد و یا انتقاد خود را در قالب یک پیام واحد به طور کامل ارسال کنید 👇🏻"
}



keystart = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btnsendacc = telebot.types.KeyboardButton('📤 ارسال اکانت')
btnsupport = telebot.types.KeyboardButton('☎️ پشتیبانی')
btncheckout = telebot.types.KeyboardButton('✅ تسویه حساب')
btnhesab = telebot.types.KeyboardButton('👤 حساب کاربری')
keystart.add(btnsendacc)
keystart.add(btnhesab, btnsupport)
keystart.add(btncheckout)

keypanel = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btngivecode = telebot.types.KeyboardButton('📥 دریافت کد 📥')
btnjoin = telebot.types.KeyboardButton('➕ جوین ➕')
btnseen = telebot.types.KeyboardButton('👁 سین 👁')
btnnumbers = telebot.types.KeyboardButton('☎️ شماره ها ☎️')
keypanel.add(btngivecode)
keypanel.add(btnjoin, btnseen)
keypanel.add(btnnumbers)

keyback = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btnback = telebot.types.KeyboardButton('برگشت 🔙')
keyback.add(btnback)

keybackpanel = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btnbackpanel = telebot.types.KeyboardButton('🔙 بازگشت 🔙')
keybackpanel.add(btnbackpanel)

def addcoin(chatid,coin):
  with open('users/'+chatid+'.json', 'r') as f:
    data = json.load(f)
  data['coin'] = str(int(data['coin'])+int(coin))
  with open('users/'+chatid+'.json', "w") as f:
    json.dump(data, f)

@bot.message_handler(func=lambda msg: msg.text in ["✅ تسویه حساب", "👤 حساب کاربری", "برگشت 🔙", "☎️ پشتیبانی", "/start", "📤 ارسال اکانت"] and msg.text not in ["📥 دریافت کد 📥","➕ جوین ➕","👁 سین 👁","☎️ شماره ها ☎️","🔙 بازگشت 🔙","/panel"] )
def send_welcome(message):
    chatid = str(message.from_user.id)
    text = str(message.text)
    if os.path.isfile('users/'+chatid+'.json') == False:
      data = {"status":"ok","number":"","hashcode":"","coin":"0","chatidanswer" : ""}
      with open('users/'+chatid+'.json', "w") as f:
        json.dump(data, f)
      bot.reply_to(message, texts['start'],reply_markup=keystart)
    else:
      with open('users/'+chatid+'.json', 'r') as f:
        data = json.load(f)
      
      if(text == "/start" or text == "برگشت 🔙"):
        with open('users/'+chatid+'.json', 'r') as f:
          data = json.load(f)
        data['status'] = "ok"
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message, texts['start'],reply_markup=keystart)
      
      if(text == "📤 ارسال اکانت"):
        data['status'] = "getcode"
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message, texts['getcode'],reply_markup=keyback)
      if(text == "☎️ پشتیبانی"):
        data['status'] = "support"
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message, texts['support'],reply_markup=keyback )
      if(text == "👤 حساب کاربری"):
        
        with open('users/'+chatid+'.json', 'r') as f:
          data = json.load(f)
        coin = data['coin']
        bot.reply_to(message,"🆔 شناسه : "+chatid+"\n🪙 تعداد سکه شما : "+coin+"\n⏳ تاریخ : "+time,reply_markup=keystart )
      if(text == "✅ تسویه حساب"):
        with open('users/'+chatid+'.json', 'r') as f:
          data = json.load(f)
        coin = data['coin']
        data["status"] = "checkout"
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message,"🆔 شناسه : "+chatid+"\n🪙 تعداد سکه شما : "+coin+"\nشماره کارت خود را با نام صاحب حساب وارد کنید \nمثال : 123456789123456 علی فداکار",reply_markup=keyback )
        
@bot.message_handler(func=lambda msg: msg.text not in ["✅ تسویه حساب", "👤 حساب کاربری", "برگشت 🔙", "☎️ پشتیبانی", "/start", "📤 ارسال اکانت"] and msg.text in ["📥 دریافت کد 📥","➕ جوین ➕","👁 سین 👁","☎️ شماره ها ☎️","🔙 بازگشت 🔙","/panel"] )
def panel(message):
  if(message.from_user.id == int(admin)):
    chatid = str(message.from_user.id)
    text = str(message.text)
    if os.path.isfile('users/admin/'+chatid+'.json') == False:
      data = {"status":"ok","channel":"","msgid":"","tedad" : ""}
      with open('users/admin/'+chatid+'.json', "w") as f:
        json.dump(data, f)
    else:
      with open('users/admin/'+chatid+'.json', 'r') as f:
        data = json.load(f)
      if(text == "/panel" or text == "🔙 بازگشت 🔙"):
        with open('users/admin/'+chatid+'.json', 'r') as f:
          data = json.load(f)
        data['status'] = "ok"
        data['msgid'] = ""
        data['channel'] = ""
        with open('users/admin/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message, texts['startpanel'],reply_markup=keypanel)
      
      if(text == "👁 سین 👁"):
        with open('users/admin/'+chatid+'.json', 'r') as f:
          data = json.load(f)
        data['status'] = "givetedadseen"
        with open('users/admin/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message, texts['givetedad'],reply_markup=keybackpanel)
      if(text == "➕ جوین ➕"):
        with open('users/admin/'+chatid+'.json', 'r') as f:
          data = json.load(f)
        data['status'] = "givetedad"
        with open('users/admin/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message, texts['givetedad'],reply_markup=keybackpanel)
      if(text == "📥 دریافت کد 📥"):
        with open('users/admin/'+chatid+'.json', 'r') as f:
          data = json.load(f)
        data['status'] = "givecode"
        with open('users/admin/'+chatid+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message, texts['givecode'],reply_markup=keybackpanel)
      if(text == "☎️ شماره ها ☎️"):
        bot.reply_to(message, texts['loading'],reply_markup=keypanel)
        numbers = ""
        for n in os.listdir("acc"):
          if n.endswith(".session"):
            number = os.path.splitext(n)[0]
            mmd = asyncio.run(check(number))
            parts = mmd.split()
            if parts[0] == "true" :
              numbers = numbers+"\n"+number+" : "+parts[2]
        keydeletaccs = InlineKeyboardMarkup()
        keydeletaccs.add(InlineKeyboardButton("حذف اکانت های دیلیت شده", callback_data ="deletaccs"))
        bot.reply_to(message, "لیست اکانت ها\n"+numbers,reply_markup=keydeletaccs)


@bot.message_handler(func=lambda message: True)
def status(message):
    chatid = str(message.from_user.id)
    text = str(message.text)
    with open('users/'+chatid+'.json', 'r') as f:
      data = json.load(f)
    with open('users/admin/'+admin+'.json', 'r') as f:
      dataadmin = json.load(f)
    
    if(dataadmin['status'] == "givetedadseen"):
      dataadmin['status'] = "giveusernameseen"
      dataadmin['tedad'] = text
      with open('users/admin/'+chatid+'.json', "w") as f:
        json.dump(dataadmin, f)
      bot.reply_to(message, texts['giveusernameseen'],reply_markup=keybackpanel)
    elif(dataadmin['status'] == "givetedad"):
      dataadmin['status'] = "giveusername"
      dataadmin['tedad'] = text
      with open('users/admin/'+chatid+'.json', "w") as f:
        json.dump(dataadmin, f)
      bot.reply_to(message, texts['giveusername'],reply_markup=keybackpanel)
    elif(dataadmin['status'] == "giveusername"):
      bot.reply_to(message, text=texts['loading'],reply_markup=keybackpanel)
      dataadmin['status'] = "ok"
      username = text
      with open('users/admin/'+chatid+'.json', "w") as f:
        json.dump(dataadmin, f)
      tedad = dataadmin['tedad']
      username = text
      async def main(number, username): 
        mmd = await asyncio.create_task(join(number, username)) 
        return mmd
      mmd = asyncio.run(main(tedad, username))
      bot.reply_to(message, text='درحال جوین'+mmd,reply_markup=keypanel)
    elif(dataadmin['status'] == "giveusernameseen"):
      bot.reply_to(message, text=texts['loading'],reply_markup=keybackpanel)
      dataadmin['status'] = "ok"
      with open('users/admin/'+chatid+'.json', "w") as f:
        json.dump(dataadmin, f)
      tedad = dataadmin['tedad']
      userandmsg = text.split("https://t.me/")[1]
      print(userandmsg)
      username = "@"+userandmsg.split("/")[0]
      msgid = userandmsg.split("/")[1]
      print(username+msgid)
      async def main(number, username,msgid): 
        mmd = await asyncio.create_task(seen(number, username,msgid)) 
        return mmd
      mmd = asyncio.run(main(tedad,username,msgid))
      bot.reply_to(message, text='درحال سین زدن'+mmd,reply_markup=keypanel)
          

      
    elif(dataadmin['status'] == "givecode"):
      mmd = asyncio.run(givecode(text))
      parts = mmd.split()
      if(parts[0] == "true"):
        data['status'] = "ok"
        with open('users/admin/'+admin+'.json', "w") as f:
          json.dump(data, f)
        bot.reply_to(message,"✅ آخرین کد دریافتی شماره "+parts[1]+" "+parts[2],reply_markup=keypanel)
      else:
        bot.reply_to(message,texts['error'],reply_markup=keypanel)
        data['status'] = "ok"
        with open('users/admin/'+admin+'.json', "w") as f:
          json.dump(data, f)
    
    elif(data['status'] == "getcode"):
      mmd = asyncio.run(getcode(text))
      parts = mmd.split()
      if(parts[0] == "true"):
        bot.reply_to(message,"🔢 کد ارسال شده به شماره "+parts[1]+" را وارد کنید",reply_markup=keyback)
        data['status'] = "waitforlogin"
        data['number'] = text
        data['hashcode'] = parts[2]
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
      else:
        bot.reply_to(message,texts['error'],reply_markup=keystart)
        data['status'] = "ok"
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
    elif(data['status'] == "waitforlogin"):
      bot.reply_to(message,texts['loading'],reply_markup=keyback)
      number = data['number']
      mmd = asyncio.run(login(number,text,data['hashcode']))
      parts = mmd.split()
      data['status'] = "ok"
      with open('users/'+chatid+'.json', "w") as f:
        json.dump(data, f)
      if(parts[0] == "true"):
        keyaccept = InlineKeyboardMarkup()
        keyaccept.add(InlineKeyboardButton("تایید ✅", callback_data="acceptaccunt "+parts[1]))
        bot.reply_to(message,"✅ ربات با موفقیت وارد "+parts[1]+" شد از اکانت خارج و تمام نشست های ان را پاک کنید سپس با استفاده از دکمه زیر شماره را تایید کنید",reply_markup=keyaccept)
      else:
        bot.reply_to(message,texts['error'],reply_markup=keystart)
    elif(data['status'] == "support"):
      keyanswerreport = InlineKeyboardMarkup()
      keyanswerreport.add(InlineKeyboardButton("پاسخ", callback_data ="answerreport "+chatid))
      bot.send_message(admin,"📞 یک گزارش جدید از کاربر "+chatid+"دریافت شد\nمتن گزارش : "+text,reply_markup=keyanswerreport )
      bot.reply_to(message, texts['supportok'],reply_markup=keystart)
    elif(data['status'] == "answer"):
      chatidanswer = data["chatidanswer"]
      bot.send_message(chatidanswer,"🔔 شما یک پیام جدید از سوی پشتیبانی ربات دارید \nپیام : "+text,reply_markup=keystart )
      bot.reply_to(message,"پاسخ شما با موفقیت ارسال شد\nدریافت کننده : "+chatidanswer+"\nمتن پیام : "+text,reply_markup=keystart )
      data["status"] = "ok"
      data["chatidanswer"] = ""
      with open('users/'+chatid+'.json', "w") as f:
        json.dump(data, f)
    elif(data['status'] == "checkout"):
      coin = data["coin"]
      if(mincoin <= int(coin)):
        keyokcheckout = InlineKeyboardMarkup()
        keyokcheckout.add(InlineKeyboardButton("✅تایید واریز✅", callback_data ="checkoutok "+chatid))
        bot.send_message(channelcheckout,"🔔 یک درخواست تسویه جدید\nکاربر : "+chatid+"\nشماره کارت : "+text,reply_markup=keyokcheckout )
        bot.reply_to(message,"✅ تسویه با موفقیت انجام شد\nتا چند روز آینده پول به حساب مورد نظر واریز خواهد شد\nشماره کارت "+text,reply_markup=keystart )
        data["status"] = "ok"
        data["coin"] = "0"
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
      else:
        bot.reply_to(message,"🚫 حداقل تسویه "+str(mincoin)+" سکه است",reply_markup=keystart )
        data["status"] = "ok"
        with open('users/'+chatid+'.json', "w") as f:
          json.dump(data, f)
    

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chatidcall = call.message.chat.id
    if os.path.isfile('users/'+str(chatidcall)+'.json') == False:
      data = {"status":"ok","phone":"","hashcode":"","coin":"0","chatidanswer" : ""}
      with open('users/'+str(chatidcall)+'.json', "w") as f:
        json.dump(data, f)
      print("j")
    else:
      print("mmd")
      with open('users/'+str(chatidcall)+'.json', 'r') as f:
        data = json.load(f)
      with open('users/admin/'+admin+'.json', 'r') as f:
        dataadmin = json.load(f)
      parts = call.data.split()
      if parts[0] == "acceptaccunt":
        acceptaccunt = Sel.acceptnumber(parts[1])
        result = acceptaccunt.split()
        if result[0] == "true" :
          if result[1] == "ok" :
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="🎉 تبریک، شماره "+result[2]+" تایید شد و 1 سکه به حسابتان اضافه شد!",reply_markup=keystart)
            addcoin(chatidcall,"1")
          if result[1] == "no" :
            lst = acceptaccunt.split('\n')
            devices = '\n'.join(lst[1:])
            bot.send_message(chat_id=call.message.chat.id, text="شماره "+result[2]+" دارای نشست فعال است \nنشست ها \n" +devices, reply_markup=keystart)
        else:
          bot.send_message(call.message.chat.id,texts['error'],reply_markup=keystart)
      if parts[0] == "answerreport":
        bot.send_message(admin,"شما درحال پاسخ به کاربر "+parts[1]+" هستید \nپاسخ خود را ارسال کنید",reply_markup=keyback )
        data["status"] = "answer"
        data["chatidanswer"] = parts[1]
        with open('users/'+str(chatidcall)+'.json', "w") as f:
          json.dump(data, f)
      if parts[0] == "checkoutok":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='تسویه با موفقیت انجام شد')
        bot.send_message(parts[1],"💰 واریز با موفقیت انجام شد",reply_markup=keystart )
      if parts[0] == "deletaccs":
        numbers = ""
        for n in os.listdir("acc"):
          if n.endswith(".session"):
            number = os.path.splitext(n)[0]
            mmd = asyncio.run(check(number))
            parts = mmd.split()
            if parts[0] == "true" :
              if parts[2] == "🔴":
                os.remove(f"acc/{parts[1]}.session")
                numbers =f"{numbers}\n{number} : deleted"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'اکانت {parts[1]} با موفقیت حذف شد')
                
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'حذف اکانت های دیلیت شده با موفقیت انجام شد\nاکانت های حذف شده\n{numbers}')
bot.polling()
