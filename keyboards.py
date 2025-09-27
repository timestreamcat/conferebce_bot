from aiogram.types import Message, FSInputFile, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data import *


# Первые кнопочки


def welcome_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Продолжить")
    builder.adjust(1)

    return builder

# Кнопки к первому вопросу
def question_1_keyboard():
    print('Я дошел до кнопок первого вопроса!')
    builder = ReplyKeyboardBuilder()

    buttons = [KeyboardButton(text=i) for i in answers_variant_1.values()]
    buttons.append(KeyboardButton(text=answer_own))

    builder.row(*buttons, width=2)

    print('Я сделал кнопки первого вопроса!')
    return builder

# Кнопки к второму вопросу
def question_2_keyboard():
    builder = ReplyKeyboardBuilder()

    buttons = [KeyboardButton(text=i) for i in answers_variant_2.values()]
    buttons.append(KeyboardButton(text=answer_own))
    buttons.append(KeyboardButton(text=answer_back))

    builder.row(*buttons, width=2)

    return builder

# Кнопки к третьему, четвертому, пятому, шестому и седьмому вопросу
def question_3_keyboard():
    builder = ReplyKeyboardBuilder()

    buttons = [KeyboardButton(text=i) for i in answers_variant_3.values()]
    buttons.append(KeyboardButton(text=answer_own))
    buttons.append(KeyboardButton(text=answer_back))

    builder.row(*buttons, width=2)

    return builder

def after_survey_keyboard():
    builder = ReplyKeyboardBuilder()

    buttons = [KeyboardButton(text=i) for i in after_survey_answers]

    builder.row(*buttons, width=1)

    return builder

def sub_keyboard():
    button_1 = InlineKeyboardButton(
            text="Подписаться!", callback_data="data", url="https://t.me/a2b_agency"
                )
    button_2 = InlineKeyboardButton(
            text="Я подписался!", callback_data="data"
                )
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_1], [button_2]]
            )
    return keyboard

def assistent_keyboard():
    builder = ReplyKeyboardBuilder()

    buttons = [KeyboardButton(text=i) for i in assistent_answer]

    builder.row(*buttons, width=1)

    return builder

def questions_list_keyboard():
    builder = ReplyKeyboardBuilder()

    buttons = [KeyboardButton(text=i) for i in questions_list]

    builder.row(*buttons, width=1)

    return builder

def reminder_keyboard():
    builder = ReplyKeyboardBuilder()

    buttons = KeyboardButton(text='Продолжаем!') 

    builder.row(buttons, width=1)

    return builder

def howtofix_kyboard():
    builder = ReplyKeyboardBuilder()

    buttons = KeyboardButton(text='Как можно это исправить?') 

    builder.row(buttons, width=1)

    return builder

def manager_keyboard():
    button_1 = InlineKeyboardButton(
            text="Написать менеджеру", callback_data="data", url="https://t.me/A2bagency?text=%D0%94%D0%BE%D0%B1%D1%80%D1%8B%D0%B9%20%D0%B4%D0%B5%D0%BD%D1%8C!%20%D0%AF%20%D1%81%20%D0%BA%D0%BE%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%86%D0%B8%D0%B8%20%C2%AB%D0%92%D1%80%D0%B5%D0%BC%D1%8F%20%D0%BB%D0%B8%D0%B4%D0%B5%D1%80%D0%BE%D0%B2%C2%BB.%20%D0%A5%D0%BE%D1%87%D1%83%20%D0%BF%D0%BE%D0%B4%D0%BE%D0%B1%D1%80%D0%B0%D1%82%D1%8C%20%D0%B0%D1%81%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BD%D1%82%D0%B0"
                )
    button_2 = InlineKeyboardButton(
            text="Подписаться!", callback_data="data"
                )
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_1]]
            )
    return keyboard

def manager_help_keyboard():
    button_1 = InlineKeyboardButton(
            text="Написать менеджеру", callback_data="data", url="https://t.me/A2bagency?text=%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D1%81%D1%82%D0%B2%D1%83%D0%B9%D1%82%D0%B5!%20%D0%A3%20%D0%BC%D0%B5%D0%BD%D1%8F%20%D0%B2%D0%BE%D0%BF%D1%80%D0%BE%D1%81%20%D0%BF%D0%BE%20%D0%B1%D0%BE%D1%82%D1%83"
                )
    button_2 = InlineKeyboardButton(
            text="Подписаться!", callback_data="data"
                )
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_1]]
            )
    return keyboard