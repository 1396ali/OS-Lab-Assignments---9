import telebot
from random import randint
from khayyam import JalaliDatetime
from gtts import gTTS
from qrcode import make

bot = telebot.TeleBot("148706402:AAFstsprg2MwEsIjcbs2CdDyL9i4aDeUv5Y")

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Hello (" + message.from_user.first_name + ") - /help")
#

@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(message, 
""" /start: Hello USER \n
    /game: Play GUESS \n 
    /age: Show AGE \n 
    /voice: Convert TEXT \n 
    /max: Maximum NUMBER \n 
    /argmax: Maximum INDEX \n 
    /qrcode: Create QRCODE""")
#

@bot.message_handler(commands=['game'])
def game(message):

    global rand
    rand  = randint(0,10)
    inp = bot.send_message(message.chat.id , 'Enter your guess: [0-10]')
    bot.register_next_step_handler(inp , game_guess)


def game_guess(inp):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    btn_new = telebot.types.KeyboardButton('new')
    btn_exit = telebot.types.KeyboardButton('exit')
    markup.add(btn_new,btn_exit)
    
    if inp.text == 'new':
        inp = bot.send_message(inp.chat.id, 'Again:',reply_markup=markup)
        global rand
        rand = randint(0,10)
        bot.register_next_step_handler(inp, game_guess)

    elif inp.text == 'exit':
        markup = telebot.types.ReplyKeyboardRemove(selective=True)
        inp = bot.send_message(inp.chat.id, 'end - /help',reply_markup=markup)
        bot.send_message(inp, game_guess)
        
    else:
        if int(inp.text) > rand:
            inp = bot.send_message(inp.chat.id , 'is UP' ,reply_markup=markup)
            bot.register_next_step_handler(inp , game_guess)
        elif int(inp.text) < rand:
            inp = bot.send_message(inp.chat.id , 'is DOWN' ,reply_markup=markup)
            bot.register_next_step_handler(inp , game_guess)
        else:
            markup = telebot.types.ReplyKeyboardRemove(selective=True)
            bot.send_message(inp.chat.id , 'YES-END!- /help' ,reply_markup=markup)
            
#

@bot.message_handler(commands=['age'])
def birth(message):
    birthday = bot.send_message(message.chat.id , 'Enter your birthday: [1400/01/01]')
    bot.register_next_step_handler(birthday , date_computing)

def date_computing(birthday):
    temp = birthday.text.split("/")
    dif = JalaliDatetime.now() - JalaliDatetime(temp[0] , temp[1] , temp[2] )
    year = dif.days // 365
    bot.send_message(birthday.chat.id , year )
#

@bot.message_handler(commands=['voice'])
def voice(message):
    user_voice = bot.send_message(message.chat.id , 'Enter your text: [EN]')
    bot.register_next_step_handler(user_voice , voice_creating)

def voice_creating(user_voice):
    convert = gTTS(text = user_voice.text , lang = 'en' , slow = True)
    convert.save('voice.wma')
    convert = open('voice.wma' , 'rb')
    bot.send_voice(user_voice.chat.id , convert )
#

@bot.message_handler(commands=['max'])
def maximum(message):
    arry = bot.send_message(message.chat.id , 'Enter your arry: [1,10,100,50,...]')
    bot.register_next_step_handler(arry , max_searching)

def max_searching(arry):  
    temp = list(map(int, arry.text.split(',')))
    number = max(temp)
    bot.send_message(arry.chat.id , number)
#

@bot.message_handler(commands=['argmax'])
def maximum_index(message):
    arry = bot.send_message(message.chat.id , 'Enter your arry: (index+1)')
    bot.register_next_step_handler(arry , index_searching)

def index_searching(arry):
    temp = list(map(int, arry.text.split(',')))
    ind = temp.index(max(temp))
    bot.send_message(arry.chat.id , (ind+1))
#

@bot.message_handler(commands=['qrcode'])
def qr_code(message):
    qr = bot.send_message(message.chat.id , 'Enter your text: [...]')
    bot.register_next_step_handler(qr , qrcode_creating)

def qrcode_creating(qr):
    qr_image = make(qr.text)
    qr_image.save('QR.png')
    qr_image = open('QR.png' , 'rb')
    bot.send_photo(qr.chat.id , qr_image)
#

@bot.message_handler(func = lambda message: True)
def echo_all(message):
    if message.text == "0":
        bot.reply_to(message, "ok,i'am ON")
    else:
        bot.reply_to(message, "no command defined by this")
#
bot.infinity_polling()
