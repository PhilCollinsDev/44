import telebot
from telebot import types
from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://developerofggm:ParseDataJSON@offer.fl76uwi.mongodb.net/?retryWrites=true&w=majority&appName=Offer'
#MONGO_URI = 'mongodb+srv://developerofggm:ParseDataJSON@offer.fl76uwi.mongodb.net/?retryWrites=true&w=majority&appName=Offer&tlsAllowInvalidCertificates=true'
client = MongoClient(MONGO_URI)
db = client.get_database('test')  
users_collection = db['users']

TOKEN = '7147921772:AAEtT6EZhrbuS_sy1IJj9AcvwrWaxB4oh-Y'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    user_id = user.id
    username = user.username if user.username else "N/A"
    first_name = user.first_name if user.first_name else "N/A"
    last_name = user.last_name if user.last_name else "N/A"

    # Проверка, есть ли пользователь в базе
    existing_user = users_collection.find_one({"user_id": user_id})
    if not existing_user:
        # Если пользователя нет, добавляем его в базу
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "created_at": message.date  # Добавляем дату создания записи
        }
        users_collection.insert_one(user_data)
        print(f"New user added: {user_id} - {username}")

    # Отправка приветственного сообщения
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Play', web_app=types.WebAppInfo(url='https://ton-season.com/'))
    markup.add(btn1)
    
    photo_path = '11.jpeg'
    with open(photo_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="""<b>Welcome to TON Season 🎉</b>
                       
This is your chance to explore the TON ecosystem in a fun and engaging way 🎮  

Unlock TON cards, complete challenges, and earn rewards 💎 

With three exciting seasons ahead, you’ll discover new opportunities, bonuses, and surprises. 

Start your journey in TON today ⭐️""", reply_markup=markup, parse_mode="html")
        
@bot.message_handler(commands=['last20'])
def last20_users(message):
    last_users = users_collection.find({"username": {"$exists": True, "$ne": None}}).sort("_id", -1).limit(20)
    
    usernames = []
    for user in last_users:
        username = user.get('username')
        if username:
            user_id = user.get('user_id')
            if user_id:
                usernames.append(f"<a href=\"tg://user?id={user_id}\">@{username}</a>")
    
    if not usernames:
        bot.send_message(message.chat.id, "Не найдено пользователей с юзернеймами.")
        return

    response = "\n\n".join(usernames)
    bot.send_message(message.chat.id, response, parse_mode="html")
        
@bot.message_handler(commands=['9911'])
def send_message_to_users(message):
    user_ids = users_collection.find({"user_id": {"$type": "string"}}).distinct("user_id")
    count = 0

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Play', web_app=types.WebAppInfo(url='https://ton-season.com/'))
    markup.add(btn1)
    photo_path = '551.png'
    caption = """<b>Don't miss the game!</b>

Less than an hour left until it starts. The game will last 24 hours—hurry to get your chance at a reward!"""

    for user_id in user_ids:
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(user_id, photo, caption=caption, reply_markup=markup, parse_mode='html')
            count += 1
            print(f"Сообщение отправлено пользователю {user_id}. Всего отправлено: {count}")
        except Exception as e:
            print(f"Ошибка при отправке пользователю {user_id}: {e}")

    bot.send_message(message.chat.id, f"Сообщения отправлены {count} пользователям.")
        
@bot.message_handler(commands=['358'])
def amount(message):
    users_count = users_collection.count_documents({"user_id": {"$type": "string"}})
    bot.send_message(message.chat.id, f"Total users: {users_count}")

@bot.message_handler(content_types=['text', 'photo', 'video', 'voice', 'document', 'audio', 'location', 'poll', 'dice', 'animation', 'sticker', 'contact'])
def handle_video_message(message):
    bot.reply_to(message, "Type <b>/start</b>", parse_mode="html")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
