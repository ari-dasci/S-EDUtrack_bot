import inspect
import config.db_sqlite_connection as sqlite
from functions import general_functions as g_fun, bot_functions as b_fun
from text_language import teacher_lang as t_lang
import config.config_file as cfg


def teacher_received_message(update, context, user):
  def start_end_meeting(upm):
    try:
      planet = strip_accents(upm.chat.title)
      if upm.text:
        text = upm.text.strip(" ").upper()
        if text.startswith("=== INICIO DE MEETING") or text.startswith(
          "=== START MEETING"
        ):
          return "start"
        elif text.startswith("=== FIN DE MEETING") or text.startswith(
          "=== END MEETING"
        ):
          return "end"
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)

  def is_configuration_file(doc):
    try:
      if doc.file_name == "grades_format.csv":
        return "grades"
      elif doc.file_name in cfg.list_config_files:
        sql_stu = f"SELECT count(*) FROM students_file"
        sql_act = f"SELECT count(*) FROM activities"
        if (
          doc.file_name == "students_format.csv"
          and sqlite.execute_statement(sql_stu, "fetchone")[0]
        ) or (
          doc.file_name == "activities_format.csv"
          and sqlite.execute_statement(sql_act, "fetchone")[0]
        ):
          return "exists"
        else:
          return True
      else:
        return False
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)

  try:
    upm = update.message
    if cfg.config_files_set and not upm.document:
      if upm.chat_id < 0:
        meeting_indicator = start_end_meeting(upm)
        if meeting_indicator:
          edu_fun.meetings(upm, context, user, meeting_indicator)
        elif cfg.active_meetings[planet]["meeting"]:
          user.planet = planet
          edu_fun.reg_messages(upm, user)
      else:
        text = t_lang.welcome_text(user.language, context, "short")
        context.bot.sendMessage(chat_id=user._id, text=text)

    elif upm.document:
      # Check if the document is a configuration document.
      doc = upm.document
      config_file = is_configuration_file(doc)
      if config_file:
        if config_file == "grades":
          activities_grade_file(update, context, user)
        if config_file == "exists":
          text = t_lang.config_files(user.language, "exists_in_DB", doc.file_name)
          context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        else:
          b_fun.config_files_upload(update, context, user)

    else:
      if upm.chat_id > 0:
        text = t_lang.config_files(user.language, "no_set_up")
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        tea_fun.config_files_set(context, user)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
