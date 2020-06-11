import logging
from telegram import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup,
  ChatAction,
)
from functions import general_functions as g_fun
from text_language import general_lang as g_lang
from classes import Teacher, Student


def start(update, context):
  user_data = update.effective_user
  if user_data.id > 0:
    logging.info(f"User {user_data['id']} {user_data.name}, start a conversation.")
    current_user = (
      Teacher(user_data) if g_fun.user_is_teacher(user_data.id) else Student(user_data)
    )

    current_user.add_telegram_user()
    print(current_user)
    update.message.reply_text(g_lang.welcome(current_user))


def pressed_button(update, context):
  pass
