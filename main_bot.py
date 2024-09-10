import os.path

import Class_users
from Class_client import Client
from Class_clients import Clients
from Class_users import User
from Class_connected_users import Connected_Users
import json
import telebot
from telebot import types

########################################################################################################################-------- ПЕРЕМЕННЫЕ

bot = telebot.TeleBot('7073557228:AAHxo15uAsWyGQ7sRvv8POBqGjX1yNlHFf0')
users = Connected_Users()
# client_q = 0
user_action = {}
#open
SAVE_TO_FILE = True
########################################################################################################################--------- БЛОК ОБРАБОТКИ КОМАНД

@bot.message_handler(commands=['start'])
def init_user(message):
    user_id = message.from_user.id
    #if os.path.exists("admin_"+str(user_id)) :  Реализовать возможности админа
    #    'a'

    if user_id in users.users_connected:
        user = users.users_connected[user_id]
        reply_keyboard_prepare(message)
    else:
        user = Class_users.users_setup(user_id)
        if user:
            users.User_Connect(user)  # =======TO DO решить проблему при которой функции не могут обращаться к методам класса clients из за того что он создается тут а не в зоне основной видимости
            reply_keyboard_prepare(message)
        else:
            msg = bot.send_message(message.chat.id,'Кажется вы еше не зарегестрированы, введите имя что бы зарегестрироваться')
            bot.register_next_step_handler(msg, new_user, user_id)
        # clients_file = user.client_db_name

# def start_bot(message):
#     markup = types.ReplyKeyboardMarkup()
#     btn_add_client = types.KeyboardButton('Добавить клиента')
#     btn_show_clients = types.KeyboardButton('Показать клиентов')
#     btn_complet_training = types.KeyboardButton('Отметить проведенную тренировку')
#     btn_delete_client = types.KeyboardButton('Удалить клиента')
#     markup.add(btn_add_client, btn_show_clients, btn_complet_training, btn_delete_client)
#     bot.send_message(message.chat.id, 'Выберите действие ', reply_markup=markup)

def reply_keyboard_prepare(message):
    #types.ReplyKeyboardRemove()
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Добавить клиента'))

    if users.GetClients(chat_id).IsThereClients():
        markup.add(
            types.KeyboardButton('Показать клиентов'),
                types.KeyboardButton('Отметить проведенную тренировку'),
                types.KeyboardButton('Удалить клиента')
                )
    bot.send_message(chat_id, 'Выберите действие ', reply_markup=markup)




@bot.message_handler(commands=['save'])
def save_data(message):
    #
    users.GetClients(message.from_user.id).save_to_json()
    bot.send_message(message.chat.id, "Данные записаны в файл")


@bot.message_handler(func=lambda message: message.text == 'Добавить клиента')
def handle_message(message):
    ask_for_name(message)


@bot.message_handler(func=lambda message: message.text == 'Отметить проведенную тренировку')
def handle_complete_training(message):
    user_action[message.chat.id] = 'complete_training'
    select_client(message)


@bot.message_handler(func=lambda message: message.text == 'Удалить клиента')
def handle_delete_client(message):
    user_action[message.chat.id] = 'delete'
    select_client(message)


@bot.message_handler(func=lambda message: message.text == 'Показать клиентов')
def client_info(message):
    if users.GetClients(message.from_user.id).IsThereClients():
        cl_info = users.GetClients(message.from_user.id).Clients_info()
        bot.send_message(message.chat.id, cl_info)
        #raise Exception('88',123,678)
    else:
        bot.send_message(message.chat.id, 'Список клиентов пуст')





# @bot.message_handler(func=lambda message : message.text == 'Выключить бота')
# def exit_bot(message):
#     clients.load_to_json()
#     users.Clear()
#     exit()

########################################################################################################################------ БЛОК ОБРАБОТКИ ВЫЗОВА КНОПОК

@bot.callback_query_handler(func=lambda call: call.data.startswith('select_'))
def select_action_with_client(call):
    action = user_action[call.message.chat.id]
    client_name = call.data.replace('select_', '').replace('_', ' ')

    if action == 'delete':
        confirm_delete(call, client_name)
    elif action == 'complete_training':
        users.GetClients(call.from_user.id).Clients_mark_training(client_name)
        #clients.Clients_mark_training(client_name)
        bot.answer_callback_query(call.id, f"Тренировка клиента {client_name} отмечена как пройденная")


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete_') or call.data == 'cancel_delete')
def delete_client(call):
    if call.data.startswith('confirm_delete_'):
        client_name = call.data.replace('confirm_delete_', '').replace('_', ' ')
        result = users.GetClients(call.from_user.id).Clients_delete(client_name)
        bot.send_message(call.message.chat.id, result)
    elif call.data.startswith('cancel_delete'):
        bot.send_message(call.message.chat.id, 'Удаление клиента отменено')
    reply_keyboard_prepare(call.message)


########################################################################################################################------- ОСНОВНОЙ КОД БОТА

def new_user(message, user_id):
    user = message.text
    create_user = User(user, False, user_id, SAVE_TO_FILE)
    users.User_Connect(create_user)
    bot.send_message(message.chat.id, 'Регистрация пройдена')
    reply_keyboard_prepare(message)


def ask_for_name(message):
    #uscli = users.GetClients(message.from_user.id)
    bot.send_message(message.chat.id, 'Введите имя клиента')
    bot.register_next_step_handler(message, ask_for_paid_sessions)


def ask_for_paid_sessions(message):
    client_name = message.text
    msg = bot.send_message(message.chat.id, 'Сколько занятий оплачено? ')
    bot.register_next_step_handler(msg, ask_for_t_cost, client_name)

def ask_for_t_cost(message, client_name):
    paid_sessions = message.text
    bot.send_message(message.chat.id, 'Стоимость одной тренировки?')
    bot.register_next_step_handler(message, to_int, client_name,paid_sessions)

def to_int(message, client_name, p_sessions):
    try:
        paid_sessions = int(p_sessions)
        t_cost = int(message.text)
        create_client(message, client_name, paid_sessions, t_cost)
    except ValueError:
        bot.send_message(message.chat.id, 'Введите целое число')


def create_client(message, client_name, paid_sessions, t_cost):
    users.GetClients(message.from_user.id).Clients_create(client_name)
    users.GetClients(message.from_user.id).Clients_paid_done(client_name, paid_sessions, t_cost)
    bot.send_message(message.chat.id, 'Клиент успешно добавлен ')
    reply_keyboard_prepare(message)

def select_client(message):
    if users.GetClients(message.from_user.id).IsThereClients():
        markup = types.InlineKeyboardMarkup()
        for client in users.GetClients(message.from_user.id).client_list:
            callback_data = f"select_{client.name.replace(' ', '_')}"
            client_button = types.InlineKeyboardButton(client.name, callback_data=callback_data)
            markup.add(client_button)
        # if not users.GetClients(message.from_user.id).client_list:
        #     raise ValueError
        bot.send_message(message.chat.id, 'Выберите клиента', reply_markup=markup)
    else :
        bot.send_message(message.chat.id, 'Клиенты не найдены')


def confirm_delete(call, client_name):
    markup = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton('Да', callback_data=f'confirm_delete_{client_name}')
    no_btn = types.InlineKeyboardButton('Нет', callback_data='cancel_delete')
    markup.add(yes_btn, no_btn)
    bot.send_message(call.message.chat.id, f'Уверены что хотите удалить клиента {client_name}?', reply_markup=markup)


bot.polling()





