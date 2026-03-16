import telebot
from datetime import datetime, timedelta

TOKEN = "8795855938:AAEoI3tSshB-Ukokr-cphoPU1hTVA_MQuJ8" #запись токена

bot = telebot.TeleBot(TOKEN)  #создание бота

zapis = {}  #переменная для хранения записей
temp_data = {}  #переменная для хранения временных данных

def get_time_slots():
    slots = []  #список слотов
    tomorrow = datetime.now() + timedelta(days=1)  #завтрашняя дата
    for hour in range(9, 18):  #рабочие часы 9-17
        time_str = tomorrow.strftime(f"%d.%m.%y {hour}:00")  #формат времени
        slots.append(time_str)  #добавление слота
    return slots

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для записи\n\nКоманды:\n/book - записаться\n/myrecord - моя запись\n/cancel - отмена")

@bot.message_handler(commands=['book'])
def book(message):
    chat_id = message.chat.id  #сохранение ID чата
    msg = bot.send_message(chat_id, "Введите ваше имя")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    chat_id = message.chat.id  #сохранение ID чата
    name = message.text  #сохранение имени
    temp_data[chat_id] = {'name': name}  # Сохраняем имя
    slots = get_time_slots()
    free_slots = []  #сохранение свободных слотов
    
    for slot in slots:  #перебор и поиск свободного слота
        if slot not in zapis:  #если слот свободен
            free_slots.append(slot)  #добавление записи в список
    
    if not free_slots:  #если нет свободных записей
        bot.send_message(chat_id, "Извините, на завтра нет свободного времени")
        return
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for slot in free_slots[:8]:
        buttons.append(telebot.types.KeyboardButton(slot))  #создание кнопки
    markup.add(*buttons)  #добавление кнопки
    
    msg = bot.send_message(chat_id, f"Приятно познакомиться, {name}!\nВыберите свободное время", reply_markup=markup)
    bot.register_next_step_handler(msg, get_time)

def get_time(message):
    chat_id = message.chat.id  #сохранение ID чата
    selected_time = message.text  #запоминает выбранное время
    
    if selected_time in zapis:  #если время занято
        bot.send_message(chat_id, "Это время уже занято! Начните заново /book", reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    
    name = temp_data[chat_id]['name']  #получение имени
    zapis[selected_time] = name  #сохранение записи
    
    bot.send_message(chat_id,
                     f"Имя: {name}\n"
                     f"Время: {selected_time}\n\n"
                     f"Ждем Вас!", 
                     reply_markup=telebot.types.ReplyKeyboardRemove())  #функция убирает экранную клавиатуру
    del temp_data[chat_id]  #очистка временных данных

@bot.message_handler(commands=['myrecord'])
def my_record(message):
    chat_id = message.chat.id  #сохранение ID чата
    user_name = message.from_user.first_name  #сохранение имени пользователя
    found = False
    
    for time, name in zapis.items():  # Ищем запись
        if name == user_name:  # Если совпадает
            bot.send_message(chat_id, f"Ваша запись: {time}")
            found = True
            break
    
    if not found:  #если не найдено
        bot.send_message(chat_id, "У вас нет активных записей")

@bot.message_handler(commands=['cancel'])
def cancel(message):
    chat_id = message.chat.id  #сохранение ID чата
    user_name = message.from_user.first_name  #сохранение имени пользователя
    to_delete = None
    
    for time, name in zapis.items():  #поиск записи
        if name == user_name:  #если имя совпадает
            to_delete = time  #запоминает время
            break
    
    if to_delete:
        del zapis[to_delete]  #отмена записи
        bot.send_message(chat_id, " Ваша запись отменена")
    else:  #если нет записи
        bot.send_message(chat_id, "У вас нет активных записей")

@bot.message_handler(commands=['all'])
def all_records(message): #просмотр всех записей в лице админа
    if message.from_user.id == 994957339: #проверка на админа
        if zapis:  #если записи есть
            text = "📋 Все записи:\n\n"
            for time, name in sorted(zapis.items()):  #сортировка по времени
                text += f"👤 {name} - {time}\n"
            bot.send_message(message.chat.id, text)
        else:  #если нет записей
            bot.send_message(message.chat.id, "Записей нет")
    else:  #если нет доступа
        bot.send_message(message.chat.id, "У вас нет доступа")

print("Бот запущен...")
bot.polling(none_stop=True) #запуск бота