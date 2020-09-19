import inspect
import logging
import threading

import pandas as pd
from telegram import ChatAction
from telegram import InlineKeyboardButton as IKButton
from telegram import InlineKeyboardMarkup as IKMarkup

import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from functions import bot_functions as b_fun
from functions import general_functions as g_fun
from text_language import bot_lang as b_lang
from text_language import general_lang as g_lang
from text_language import student_lang as s_lang
from text_language import teacher_lang as t_lang
from user_types import Student, Teacher


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
    user = g_fun.get_user_data(update._effective_user)
    if chat_id > 0:
      if user:
        logging.info(f"User {user._id} {user.telegram_name}, start a conversation.")
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
              text = s_lang.welcome(user.language, context, "long")
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            else:
              text = s_lang.check_email(user.language, "registration")
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          else:
            text = s_lang.not_config_files_set(user.language, context)
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
      else:
        text = b_lang.no_username(update._effective_user.language_code)
        update.message.reply_text(text)
        return False
    else:
      text = g_lang.wrong_command_group(user.language, context)
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
      language = sqlite.execute_sql(sql, "fetchone")[0]
      print(language)
      new_lang = "es" if language == "en" else "en"
      print(new_lang)
      sql = (
        f"UPDATE telegram_users SET language = '{new_lang}' WHERE _id={user_data.id}"
      )
      sqlite.execute_sql(sql)
      text = g_lang.change_language(new_lang)
      context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
    else:
      text = g_lang.wrong_command_group(user_data.language, context)
      context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def check_email(update, context):
  try:
    chat_id = update._effective_chat.id
    if chat_id > 0:
      if cfg.config_files_set:
        user = g_fun.get_user_data(update._effective_user)
        if user:
          user.check_email(update, context)
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
    user = g_fun.get_user_data(update._effective_user)
    if chat_id > 0:
      if len(context.args) == 2:
        username_teacher = context.args[0].upper()
        email_teacher = context.args[1].lower()
        sql = f"SELECT COUNT(*) FROM teachers WHERE username = '{username_teacher}'"
        if not sqlite.execute_sql(sql, fetch="fetchone")[0]:
          sql = f"SELECT * FROM telegram_users WHERE username='{username_teacher}'"
          teacher_data = sqlite.execute_sql(sql, "fetchone", as_dict=True)

          if teacher_data:
            teacher_data = dict(teacher_data)
            values = f"""
            '{email_teacher}', '{teacher_data["telegram_name"]}', '{username_teacher}',{teacher_data["_id"]}
            """
            sql = f"INSERT INTO teachers VALUES({values})"
            sqlite.execute_sql(sql)
            text = t_lang.add_teacher(user.language, "sucess", username_teacher)
          else:
            text = t_lang.add_teacher(
              user.language, "not_found", user.username, context.bot.username
            )

        else:
          text = t_lang.add_teacher(user.language, "already")
      else:
        text = g_lang.wrong_num_arguments(user.language) + t_lang.add_teacher(
          user.language, "text", bot_username=context.bot.username, title=False
        )
      context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
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
        if cfg.config_files_set:
          user.main_menu(update, context)
        else:
          if user.is_teacher:
            text = t_lang.config_files(user.language, "no_set_up")
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            b_fun.config_files_set(update, context, user)
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


def set_meeting(update, context):
  def set_meeting_attendance():
    try:
      sql = f"SELECT DISTINCT _id FROM student_messages WHERE meeting = {meeting_num} and planet = '{planet}'"
      students = sqlite.execute_sql(sql, fetch="fetchall", as_list=True)
      df_students = pd.DataFrame(students, columns=["_id"])
      df_students["meeting"] = meeting_num

      df_students_DB = sqlite.table_DB_to_df("meetings_attendance")
      df_attendance = pd.concat([df_students_DB, df_students])
      df_attendance = df_attendance.drop_duplicates()
      sqlite.save_elements_in_DB(df_attendance, "meetings_attendance")

    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def get_score_meetings():
    """Guarda la calificación de cada estudiante que ha participado en el meeting especificado.

        Arguments:
            planet {str} -- Nombre del planeta
            meeting {[type]} -- ID del meeting
        """
    try:
      meeting_id = f"ML_{meeting.upper()}"
      sql = f"""SELECT email FROM registered_students WHERE _id in
              (SELECT _id FROM meetings_attendance WHERE meeting = '{meeting_num}')"""
      students_email = sqlite.execute_sql(sql, fetch="fetchall", as_list=True)
      # if len(students_email) == 1:
      emails = "','".join(students_email)
      df_grades = sqlite.table_DB_to_df(
        "grades", fields="email, {meeting_id}", set_index=True
      )

      for student in students_email:
        # TODO: REVISAR LA CALIFICACION SOBRE 10 ó SOBRE 1
        df_grades.loc[student][meeting_id] = 10

      df_grades["email"] = df_grades.index
      df_grades.reset_index(drop=True, inplace=True)
      meeting_data = [meeting_num, planet]
      thread_grade_meeting = threading.Thread(
        target=b_fun.thread_grade_activities(
          update, context, df_grades, user, meeting=meeting_data
        )
      )
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  try:
    """cfg.active_meetings["GRUPO_A"]["meeting"] = "meeting_1"
        print(cfg.active_meetings)"""

    upm = update.message
    chat_id = upm.chat_id
    user = g_fun.get_user_data(update._effective_user)
    if chat_id < 0:
      planet = g_fun.strip_accents(upm.chat.title)
      args = context.args
      if len(args) == 1:
        try:
          meeting_num = int(args[0])
        except:
          text = t_lang.meeting(user.language, "is_not_a_number", args[0])
          context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
          return False
        else:
          meeting = f"meeting_{meeting_num}"
          # VER COMO SABER SI EL COMANDO ES START O END
          if upm.text.startswith("/start_meeting"):
            if planet not in cfg.active_meetings:
              cfg.active_meetings.update({planet: {"users": {}, "meeting": meeting}})
            elif meeting not in cfg.active_meetings[planet]["meeting"]:
              cfg.active_meetings[planet].update({"meeting": meeting})
              text = t_lang.meeting(user.language, "start", meeting_num)
              context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
            else:
              text = t_lang.meeting(user.language, "active", meeting_num)
              context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)

          elif upm.text.startswith("/end_meeting"):
            if cfg.active_meetings[planet]["meeting"]:
              if meeting in cfg.active_meetings[planet]["meeting"]:
                cfg.active_meetings[planet]["meeting"] = ""
                # cfg.closed_meetings.add(meeting)
                text = t_lang.meeting(user.language, "end", meeting_num)
                context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
                # Guarda en la base de datos la asisencia a meetings
                set_meeting_attendance()
                get_score_meetings()

              else:
                meeting_num = cfg.active_meetings[planet]["meeting"][-1]
                text = t_lang.meeting(user.language, "finish_no_active", meeting_num)
                context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
            else:
              text = t_lang.meeting(user.language, "none_active", meeting_num)
              context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
      else:
        if not args:
          if cfg.active_meetings:
            if cfg.active_meetings[planet]:
              if cfg.active_meetings[planet]["meeting"]:
                meeting_num = cfg.active_meetings[planet]["meeting"][-1]
                text = t_lang.meeting(user.language, "no_number", meeting_num)
                context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
                return False

          text = t_lang.meeting(user.language, "no_number")
          context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
          return False
        else:
          text = t_lang.meeting(user.language, "error_args")
          context.bot.sendMessage(chat_id=chat_id, parse_mode="HTML", text=text)
        return False

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


# STUDENTS COMMAND


def suggestion(update, context):
  try:
    chat_id = update.message.chat_id
    if chat_id > 0:
      user = g_fun.get_user_data(update._effective_user)
      if user:
        user.suggestion(update, context)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False
