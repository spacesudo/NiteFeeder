import json
import random
import time
import requests
from dbhelper import Users
import telebot
from telebot import types

QUIZ_URL = 'https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=multiple'

db = Users()
db.setup()

bot = telebot.TeleBot('Token')

def get_quiz():
    try:
        response = requests.get(QUIZ_URL)
        response.raise_for_status()  
        data = response.json()
        return data['results'][0] 
    except Exception as e:
        print("Error fetching quiz:", e)
        return None

def rando(opts):
    return random.sample(opts, 4)


def get_username(user_id):
    try:
        user = bot.get_chat(user_id)
        if user.username:
            return user.username
        else:
            return user.first_name
    except Exception as e:
        print(e)
        return None
    
    
def check(user_id, chat_id):
    try: 
        member = bot.get_chat_member(chat_id, user_id) 
        if member.status in ["member", "administrator", "creator"]: 
            return True
        else: 
            return False
    except Exception as e: 
        print("Error checking membership:", e) 
        return False


@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    try:
        if message.chat.id == -1001803357579:
            lead = db.get_all_stats()
            print(f"{lead}")
            x = dict(lead)
            sorted_users = sorted(x.items(), key=lambda x: x[1], reverse=True)
            msg = ""
            for user, stats in sorted_users:
            msg += f"{user} : {stats}\n"
            bot.send_message(message.chat.id, msg, parse_mode='Markdown')

    except Exception as e:
        print(e)

def poll(message):
    quiz = get_quiz()
    if quiz:
        question = quiz['question']
        global correct_answer
        correct_answer = quiz['correct_answer']
        print(correct_answer)
        incorrect_answers = quiz['incorrect_answers']
        opts = rando([correct_answer] + incorrect_answers)
        print(opts)
        global ind
        ind = opts.index(correct_answer)
        print(ind)
        poll_message = bot.send_poll(message.chat.id, question, options=opts, type="quiz", is_anonymous=False, correct_option_id=ind, open_period=300)
        poll_id = poll_message.poll.id
        bot.pin_chat_message(message.chat.id, poll_message.message_id)
        print(poll_id)

"""1803357579"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == -1001803357579:
        owner_id = message.chat.id
        db.add_user(owner_id)
        print(owner_id)
        welcome_message = """
        *Welcome to NightFeeder Bot!!!*

Your Task is to feed your Kiwi Atleast Once in every 30 minutes before she runs out of Life!!!

You have 10 minutes to answer each quiz before your time runs out!!!

Answer Quizes as fast as you can to feed your bot and brag your points in the official NightFeeder Community
        """
        photo = open("img.jpg", 'rb')
        bot.send_photo(message.chat.id, photo, welcome_message)
        while True:
            poll(message)
            time.sleep(1800)
    else:
        bot.reply_to(message, "to use this bot, please join https://t.me/nitefeedereth (Join group from Portal)")

        
@bot.poll_answer_handler(func=lambda poll_answer: poll_answer.option_ids[0] == ind)
def handle(poll_answer):
    user_id = poll_answer.user.id
    print(poll_answer.poll_id)
    db.add_user(user_id)
    print(f'User {get_username(user_id)} answered correctly!')
    x = db.get_points(user_id)
    x += 10
    db.update_points(x, user_id)
    print(db.get_points(user_id))
    caption = f"@{get_username(user_id)} Gained 50 Points and has fed his kiwi with {random.randint(1,10)} Bottles of Milk "
    photo = open("img.jpg", 'rb')
    bot.send_photo(-1001803357579, photo, caption)
        

bot.infinity_polling()
