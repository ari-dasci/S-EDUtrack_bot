import logging
from telegram import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup,
  ChatAction,
)
import config.config_file as cfg
from functions import general_functions as g_fun, bot_functions as b_fun
from text_language import (
  general_lang as g_lang,
  teacher_lang as t_lang,
  student_lang as s_lang,
  bot_lang as b_lang,
)
from classes import Teacher, Student


def start(update, context):
  user_data = update.effective_user
  if user_data.id > 0:
    logging.info(f"User {user_data['id']} {user_data.name}, start a conversation.")
    user = g_fun.get_user_data(user_data)
    if user:
      user.add_telegram_user()
      print(user)
      if cfg.config_files_set:
        if user.is_teacher:
          update.message.reply_text(t_lang.welcome_text(user.language), context, True)
        else:
          update.message.reply_text(s_lang.welcome_text(user.language), context, True)
      else:
        if user.is_teacher:
          b_fun.config_files_set(update, context, user)
        else:
          update.message.reply_text(
            s_lang.not_config_files_set(user.language), context, True
          )
    else:
      text = b_lang.no_username(user_data.language_code)
      update.message.reply_text(text)
      return False


def pressed_button(update, context):
  pass
