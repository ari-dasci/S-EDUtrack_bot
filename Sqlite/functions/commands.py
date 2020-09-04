import inspect
import logging
import re
from telegram import (
  InlineKeyboardButton as IKButton,
  InlineKeyboardMarkup as IKMarkup,
  ChatAction,
)
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from functions import general_functions as g_fun, bot_functions as b_fun
from text_language import (
  general_lang as g_lang,
  teacher_lang as t_lang,
  student_lang as s_lang,
  bot_lang as b_lang,
)
from user_types import Teacher, Student


def start(update, context):
  """Start a conversation with the user. Register the user in the database and check if the subject is configured to welcome the user.

  Args:
      update (:class:'telegram.update.Update'): Current request received by the bot
      context (:class:'telegram.ext.callbackcontext.CallbackContext'): Context of the current request

  Returns:
      bool: Returns True if the process is performed correctly or False if an error is generated.
  """
  try:
    chat_id = update.message.chat_id
    if chat_id > 0:
      user = g_fun.get_user_data(update._effective_user)
      logging.info(f"User {user._id} {user.telegram_name}, start a conversation.")
      if user:
        print(user)
        if user.is_teacher:
          if cfg.config_files_set:
            text = t_lang.welcome_text(user.language, context, "start")
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          else:
            b_fun.config_files_set(update, context, user)
        else:
          if cfg.config_files_set:
            if user.register_student():
              text = s_lang.welcome_text(user.language, context, "long")
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            else:
              pass
              # TODO: Enviar el mensaje de escriibe tu mail para registrarte o contacta con tu profesor.
          else:
            text = s_lang.not_config_files_set(user.language, context)
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
      else:
        text = b_lang.no_username(update._effective_user.language_code)
        update.message.reply_text(text)
        return False
    else:
      text = g_lang.wrong_command_group(user_data.language, context)
      context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def change_language(update, context):
  """Change the language in which the contents are displayed.

  Args:
      update (:class:'telegram.update.Update'): Current request received by the bot
      context (:class:'telegram.ext.callbackcontext.CallbackContext'): Context of the current request

  Returns:
      bool: Returns True if the process is performed correctly or False if an error is generated.
  """

  try:
    chat_id = update.message.chat_id
    user_data = update.effective_user
    if chat_id > 0:
      sql = f"SELECT language FROM telegram_users WHERE _id={user_data.id}"
      language = sqlite.execute_statement(sql, "fetchone")[0]
      new_lang = "es" if language is "en" else "en"
      return True
    else:
      text = g_lang.wrong_command_group(user_data.language, context)
      context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def check_email(update, context):
  try:
    print("CHECK CMD *** CHECK EMAIL ***")
    chat_id = update._effective_chat.id
    if chat_id > 0:
      if cfg.config_files_set:
        user = g_fun.get_user_data(update._effective_user)
        if user:
          if not user.register_student():
            if len(context.args) == 1:
              email = context.args[0].lower()
              if re.match(
                "^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$", email.lower()
              ):
                sql = "SELECT count(email_students_file) FROM registered_students"
                if sqlite.execute_statement(sql, "fetchone")[0]:
                  # Tenia registration como accion
                  text = s_lang.check_email(user.language, "exists_email")
                  context.bot.sendMessage(
                    chat_id=user._id, parse_mode="HTML", text=text
                  )
                  return True
                else:
                  sql = f"SELECT * FROM students_file WHERE email='{email}'"
                  student = sqlite.execute_statement(sql, "fetchone")
                  if student:
                    values = f"{user._id}, '{student[2]} , {student[1]}', '{email}'"
                    sql = f"INSERT INTO registered_students VALUES({values})"
                    sqlite.execute_statement(sql)
                    text = s_lang.check_email(user.language, "success", email)
                    context.bot.sendMessage(
                      chat_id=user._id, parse_mode="HTML", text=text
                    )
                    text = s_lang.welcome(user.language, context, "long")
                    # cfg.registered_students.add(user["_id"])
                    # cfg.registered_stu_emails.add(user["email"])
                    return True

                  else:
                    text = s_lang.check_email(user.language, "not_found")
                    context.bot.sendMessage(
                      chat_id=user._id, parse_mode="HTML", text=text
                    )
              else:
                text = g_lang.email_syntax_error(user.language, email)
                context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            elif len(context.args) < 1:
              text = s_lang.check_email(user.language, "no_args")
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            else:
              text = s_lang.check_email(
                user.language, "many_args", " ".join(context.args)
              )
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          else:
            sql = f"SELECT email FROM registered_students WHERE _id={user._id}"
            email_DB = sqlite.execute_statement(sql, "fetchone")
            if email_DB:
              text = s_lang.check_email(user.language, "registered_user", email_DB[0])
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        else:
          text = b_lang.no_username(update._effective_user.language_code)
          update.message.reply_text(text)
          return False
      else:
        text = s_lang.not_config_files_set(user.language, context)
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def add_teacher(update, context):
  try:
    chat_id = update.message.chat_id
    if chat_id > 0:
      if len(context.args) == 2:
        username = context.args[0]
        email = context.args[1]
        sql = "SELECT * FROM telegram_users WHERE username={username}"
        teacher_data = sqlite.execute_statement(sql, "fetchone")
        if teacher_data:
          values = (
            f"{teacher_data[0]}, '{teacher_data[1]}','{teacher_data[2]}', {email}"
          )
          sql = f"INSERT INTO teachers VALUES({values})"
        else:
          sql = "CREATE TABLE IF NOT EXISTS teachers_temp (username TEXT, email TEXT)"
          sqlite.execute_statement(sql)
          sql = f"INSERT INTO teachers_temp VALUES('{username}', '{email}')"
          cfg.standby_teachers = True
      else:
        pass
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def menu(update, context):
  """[summary]

  Args:
      update ([type]): [description]
      context ([type]): [description]

  Returns:
      [type]: [description]
  """
  try:
    chat_id = update.message.chat_id
    if chat_id > 0:
      user = g_fun.get_user_data(update._effective_user)
      if user:
        if user.is_teacher:
          if cfg.config_files_set:
            user.main_menu(update, context)
          else:
            text = t_lang.config_files(user.language, "no_set_up")
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            b_fun.config_files_set(update, context, user)
        else:
          if cfg.config_files_set:
            if user.register_student():
              user.main_menu(update, context)
          else:
            text = s_lang.not_config_files_set(user.language, context)
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
      else:
        text = b_lang.no_username(update._effective_user.language_code)
        update.message.reply_text(text)
        return False
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def grade_activity(update, context):
  try:
    chat_id = update.message.chat_id
    if chat_id > 0:
      user = g_fun.get_user_data(update._effective_user)
      if user:
        if user.is_teacher:
          user.grade_activity_cmd(update, context)
        print()

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False

