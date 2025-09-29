import random
import os
import json

from datetime import datetime, timedelta

from config import Config, load_config


import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from data import *
from keyboards import *
import functions

# Токен Бота
config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
CHANNEL_USERNAME = "@a2b_agency"  # Юзернейм канала (с @)
CHANNEL_ID = -1002497549820

# Объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Абсолютный путь к папке с картинками
media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
print(media_dir)

# Абсолютный путь к папке с базой данных
database_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
database_file = database_dir + "\database.json"
print(database_file)

# Загрузка базы данных, в которой будут хранятся данные пользователей

with open (database_file, "r") as file:
    database = json.load(file)
    keys = list(database)
    for i in keys:
        database[int(i)] = database.pop(i)
    print(database)


# Функция сохранения датабазы
async def save_database(database, message):
    print(database)

    database[message.from_user.id]['last message']= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(database[message.from_user.id]['last message'])
    print(datetime.strptime(database[message.from_user.id]['last message'], format_string))

    with open(database_file, "r") as file:
        old_database = json.load(file)

    print(database)
    with open(database_file, "w") as file:
        json.dump(database, file)

    old_database_file = database_dir + "\old_database.json"
    with open(old_database_file, "w") as file:
        json.dump(old_database, file)

format_string = "%Y-%m-%d %H:%M:%S"


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    photo_file = FSInputFile(path=os.path.join(media_dir, 'greeting.png'))
    await message.answer_photo(photo=photo_file)
    await message.answer(
        welcome_message, parse_mode='HTML'
    )
    # Добавление нового пользователя в датабазу, если его там нет

    if message.from_user.id not in list(map(int, database.keys())):
        database[message.from_user.id] = {
            'name': message.from_user.full_name,
            'username': message.from_user.username,
            'step': 0,
            'last message': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'reminder 10': False,
            'last reminder': False,
            'assistant': 0,
            'step_1': 0,
            'step_2': 0,
            'step_3': 0,
            'step_4': 0,
            'step_5': 0,
            'step_6': 0,
            'step_7': 0,
            'revalue_step': 0
        }
    # Сохранение датабазы
    await save_database(database, message)

    builder = welcome_keyboard()

    await message.answer("Выберите опцию:", reply_markup=builder.as_markup(resize_keyboard=True))


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Ну я не знаю, попросите кого-нибудь другого о помощи'
    )


# Этот хэндлер будет срабатывать на "продолжить"
        
@dp.message(F.text.lower().in_(['продолжить']))
async def question_0(message: Message):
        print('Я дошел до "продолжить!"')
        print(type(message.from_user.id))
        if database[message.from_user.id]['step'] == 1:
            builder = assistent_keyboard()
            await message.answer('Расскажите, пожалуйста, ' \
                    'о вашем текущем опыте с ассистентом', reply_markup=builder.as_markup(resize_keyboard=True))
        else:
            keyboard = sub_keyboard()
            await message.answer('Чтобы продолжить, <b>приглашаем подписаться ' \
            'на наш канал</b> — там кейсы подбора ассистентов, инструменты и лучшие практики для работы с помощником.' \
            '\n\nПодписка = доступ к боту + польза в каждом посте.',  reply_markup=keyboard, parse_mode='HTML')
            await save_database(database, message)

async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@dp.callback_query(F.data =='data')
async def process_button_click(callback: CallbackQuery):
    print('я все же добравлся до нажатия кнопки экшуалли')
    if await is_subscribed(callback.from_user.id):
        await callback.message.edit_text("✅ Спасибо! Теперь вы можете использовать бота.")
        database[callback.from_user.id]['step'] = 1
    else:
        await callback.answer("❌ Вы еще не подписались!", show_alert=True)

@dp.callback_query(F.data =='data')
async def process_button_click(callback: CallbackQuery):
    print('я добравлся до нажатия кнопки экшуалли')
    await callback.message.answer('Расскажите, пожалуйста, ' \
    'о вашем текущем опыте с ассистентом')
    await callback.answer()

@dp.message(F.text.in_(assistent_answer)) 
async def main_survey(message: Message):
    database[message.from_user.id][f'assistant'] = message.text
    await save_database(database, message)
    await process_questions(message)
        
async def process_digit_answers_message(message: Message):
    await message.answer('Введите свое число без пробелов и каких-либо других символов:')

@dp.message(F.text.lower().isdigit()) 
async def process_digit_answer(message: Message):
    print('Я застреваю тут')
    match database[message.from_user.id]['step']:
        case 1:
            await counting_digital_answer(message,  1)
        case 2:
            await counting_digital_answer(message,  2)
        case 3:
            await counting_digital_answer(message,  3)
        case 4:
            await counting_digital_answer(message,  4)
        case 5:
            await counting_digital_answer(message,  5)
        case 6:
            await counting_digital_answer(message,  6)
        case 7:
            database[message.from_user.id]['step_7'] = float(message.text)
            database[message.from_user.id]['step'] = 8
            await after_survey(message)
        case 8:
            await recounting_digital_answer(message,  database[message.from_user.id]['revalue_step'])
        
        #await save_database(database, message)

async def question_1(message):
    builder = question_1_keyboard()
    await message.answer("Перейдем к расчету часов и денег, что уходят на рутину." \
    "\n\nУкажите ваш примерный средний доход <b>в месяц</b>. " \
    "Мы используем эту цифру только для <u>одной цели</u> — показать, сколько на самом деле <b>стоит час вашего времени</b>. " \
    "\n\nЕсли вы хотите более точный результат – можете ввести число самостоятельно.", 
    reply_markup=builder.as_markup(resize_keyboard=True), parse_mode='HTML')
    

async def question_2(message: Message):
    builder = question_2_keyboard()
    await message.answer("Идем дальше! " \
    "\nСейчас посчитаем часы, которые вы уделяете рутине.\n\nСколько часов <b>в неделю</b> вы обычно работаете? " \
    "\n\nПолный рабочий день  обычно составляет <b><i>40 часов в неделю</i></b>", 
    reply_markup=builder.as_markup(resize_keyboard=True), parse_mode='HTML')

async def question_3(message: Message):
    builder = question_3_keyboard()
    await message.answer("Сколько времени <b>в неделю</b> уходит на <b>разбор почты и мессенджеров?</b>", 
                         reply_markup=builder.as_markup(resize_keyboard=True), parse_mode='HTML')

async def question_4(message: Message):
    builder = question_3_keyboard()
    await message.answer("Сколько времени <b>в неделю</b> уходит на <b>контроль задач</b> команды"\
    " (напоминания, сбор статусов, контроль выполнения))", reply_markup=builder.as_markup(resize_keyboard=True), parse_mode='HTML')

async def question_5(message: Message):
    builder = question_3_keyboard()
    await message.answer("Сколько времени <b>в неделю</b> уходит на <b>оформление</b>"
    " и отправку <b>типовых документов/писем</b>", reply_markup=builder.as_markup(resize_keyboard=True), parse_mode='HTML')


async def question_6(message: Message):
    builder = question_3_keyboard()
    await message.answer("Сколько времени <b>в неделю</b> уходит на <b>ведение"
                         " деловой переписки</b> с клиентами, партнёрами и подрядчиками?", 
                         reply_markup=builder.as_markup(resize_keyboard=True), parse_mode='HTML')

async def question_7(message: Message):
    builder = question_3_keyboard()
    await message.answer("Сколько времени <b>в неделю</b> уходит на"
                         " подготовку к встречам (сбор информации, презентации)?", 
                         reply_markup=builder.as_markup(resize_keyboard=True), parse_mode='HTML')
    
questions = {1: question_1, 2: question_2,
             3: question_3, 4: question_4,
             5: question_5, 6: question_6,
             7: question_7}


async def process_questions(message: Message):
    print(f"Я очень хочу задать {database[message.from_user.id]['step']} вопрос!")
    await questions[database[message.from_user.id]['step']](message)

async def after_survey(message: Message):
    builder = after_survey_keyboard()
    await save_database(database, message)
    await message.answer('Почти готово! Перепроверим ответы?' \
    '\n\nЕсли что-то хотите изменить — можно легко исправить.', 
    reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard = True))

@dp.message(F.text.in_(after_survey_answers[1]))
async def revalue_answers(message: Message):
    builder = questions_list_keyboard()
    await message.answer('Какой вопрос желаете исправить?', 
                         reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard = True))


@dp.message(F.text.in_(after_survey_answers[0]))
async def final_answer(message: Message):
    builder = howtofix_kyboard()
    final = functions.math(database[message.from_user.id])
    photo_file = FSInputFile(path=os.path.join(media_dir, 'results.png'))
    await message.answer_photo(photo=photo_file)
    await message.answer(f'Результат подсчитан:\n\nВы тратите на рутину около <b>~{final[0]}</b> часов в месяц.'
                         f'\n\nВаш бизнес теряет на этом:\n≈ {final[1]} ₽', 
                         reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard = True), parse_mode='HTML')
    database[message.from_user.id]['step']=10
    await save_database(database, message)

@dp.message(F.text.in_(['Как можно это исправить?']))
async def howtofix(message: Message):
    file = FSInputFile(path=os.path.join(media_dir, 'Как_освободить_часы_и_приумножить_доход.pdf'))
    await message.answer('<b>Каждый час, потраченный на рутину, стоит вашему бизнесу денег.</b>' \
    '\nМы подготовили практический PDF-гайд <b>по работе с ассистентом</b>, который покажет:\n\n' \
    '✅ какие процессы можно делегировать уже завтра;\n' \
    '✅ как освободить десятки часов и перестать тонуть в рутине;\n' \
    '✅ почему ассистент — это не расход, а инвестиция в рост и выручку.\n\n' \
    '⏱ Время прочтения — всего 7 минут ', parse_mode='HTML')
    await message.answer_document(document=file)
    #Здесь он сидит ждет час в самом конце
    await asyncio.sleep(3600)
    photo_file = FSInputFile(path=os.path.join(media_dir, 'last.png'))
    keyboard = manager_keyboard()
    await message.answer_photo(photo=photo_file)
    await message.answer('<b>Специальное предложение  для участников конференции' \
    '\n\nСкидка 10% на индивидуальный подбор ассистента в агентстве A2B '
    '- Assistants to Business</b>.\n\n' \
    'Почему нам доверяют:  \n• Подбор ассистента за ' \
    '2-4 недели под конкретные задачи бизнеса. \n' \
    '• Даём 2 месяца гарантии на бесплатную замену и экономим клиентам 40+ часов на подборе.\n' \
    '• Отбор только A-players - ассистентов топ-уровня, которые берут ответственность, ' \
    'действуют проактивно и помогают руководителю и бизнесу расти быстрее.' \
    '\n• 50+ успешных кейсов: среди наших клиентов CEO Yandex Ultima, CEO Inforce, STUDIO ' \
    '29 и предприниматели из списка Forbes.' \
    '\n• Собственное комьюнити сильных ассистентов и база проверенных подрядчиков '
    '- благодаря этому наши ассистенты быстрее находят решения для сложных и нетривиальных задач.' \
    '\n\nЧтобы получить скидку и обсудить детали, напишите нашему менеджеру.', reply_markup=keyboard, parse_mode='HTML')


@dp.message(F.text.in_(questions_list))
async def new_answers(message: Message):
    database[message.from_user.id]['revalue_step'] = int(message.text.split()[1])
    await questions[int(message.text.split()[1])](message)


async def counting_ansver(message, int):
    database[message.from_user.id][f'step_{int}'] = message.text
    print(f"В датабазу сохранено {database[message.from_user.id]['step_1']}")
    database[message.from_user.id]['step'] = int + 1
    await save_database(database, message)
    await questions[int+1](message)

async def counting_digital_answer(message, int):
    print("Я дошел до обработки своих ответов!")
    database[message.from_user.id][f'step_{int}'] = float(message.text)
    database[message.from_user.id]['step'] = int + 1
    await save_database(database, message)
    await questions[int+1](message)

async def recounting_digital_answer(message, int):
    print("Я дошел до обработки еще одних своих ответов!")
    database[message.from_user.id][f'step_{int}'] = float(message.text)
    await save_database(database, message)
    await after_survey(message)


@dp.message(F.text.in_(answers))
async def process_answers(message: Message):
     print('Я дошел до "процесса обработки сообщений!"')
     print(database[message.from_user.id]['step'])
     print(message.text)
     print(list(answers_variant_1.values()))
     match database[message.from_user.id]['step']:
        case 1:
            if message.text in answers_variant_1.values():
                await counting_ansver(message, 1)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
        case 2:
            if message.text in answers_variant_2.values():
                await counting_ansver(message, 2)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
            elif message.text in answer_back:
                database[message.from_user.id]['step'] = 1
                await process_questions(message)
        case 3:
            if message.text in answers_variant_3.values():
                await counting_ansver(message, 3)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
            elif message.text in answer_back:
                database[message.from_user.id]['step'] = 2
                await process_questions(message)
        case 4:
            if message.text in answers_variant_3.values():
                await counting_ansver(message, 4)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
            elif message.text in answer_back:
                database[message.from_user.id]['step'] = 3
                await process_questions(message)
        case 5:
            if message.text in answers_variant_3.values():
                await counting_ansver(message, 5)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
            elif message.text in answer_back:
                database[message.from_user.id]['step'] = 4
                await process_questions(message)
        case 6:
            if message.text in answers_variant_3.values():
                await counting_ansver(message, 6)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
            elif message.text in answer_back:
                database[message.from_user.id]['step'] = 5
                await process_questions(message)
        case 7:
            if message.text in answers_variant_3.values():
                database[message.from_user.id]['step_7'] = message.text
                database[message.from_user.id]['step'] = 8
                await after_survey(message)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
            elif message.text in answer_back:
                database[message.from_user.id]['step'] = 6
                await process_questions(message)
        case 8:
            if message.text in answers_made_easy:
                database[message.from_user.id][f"step_{database[message.from_user.id]['revalue_step']}"] = message.text
                await after_survey(message)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
        case 9:
            if message.text in answers_variant_1.values():
                database[message.from_user.id]['step_1'] = message.text
                print(f"В датабазу сохранено {database[message.from_user.id]['step_1']}")
                await process_questions(message)
            elif message.text in answer_own:
                await process_digit_answers_message(message)
        case _:
             await process_other_answers(message)


        


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    keyboard = manager_help_keyboard()
    await message.answer(
        'Пожалуйста, перепроверьте ваш ответ. На данный момент он не соответствует инструкции в вопросе.'
        '\n\nЕсли вам необходимо связаться с менеджером — нажмите кнопку ниже⬇️', reply_markup=keyboard)
    
    if database[message.from_user.id]['step'] >= 9:
        return
    await process_questions(message)

@dp.message(F.text.in_(['Как можно это исправить?']))
async def welcome_back(message: Message):
    process_questions(message)

@dp.message(F.text.in_(['Продолжить!']))
async def welcome_back(message: Message):
    process_questions(message)

async def send_reminder(user_id: int):
    builder = reminder_keyboard()
    await bot.send_message(
        user_id,
        "Вы ещё с нами? Не упустите шанс узнать,"\
         " сколько денег вы можете дозаработать!", reply_markup=builder.as_markup(resize_keyboard=True)
        )

async def reminder_worker():
    while True:
        print('я тут работаю вообще-то')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(current_time, format_string)
        print(current_time)
        #datetime.strptime(database[user_id]['last message'], format_string)
        for user_id in database.keys():
            print(type(database[user_id]['last message']))
            time_diff = current_time - datetime.strptime(database[user_id]['last message'], format_string)
            if time_diff >= timedelta(hours=5) and database[user_id]['step'] < 9 \
                    and not database[user_id]['last reminder']:
                
                await send_reminder(user_id)
                database[user_id]['last reminder'] = True
                # Обновляем время последней активности после напоминания
        await asyncio.sleep(360)  # Проверка каждый 6 минут

        


async def main():
    #await dp.run_polling(bot)
    asyncio.create_task(reminder_worker())
    # reminder_worker()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    #asyncio.create_task(reminder_worker())
    asyncio.run(main())
    #dp.run_polling(bot)