import inspect
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from functions import general_functions as g_fun
from text_language import teacher_lang as t_lang, bot_lang as b_lang


def received_message(update, context):
  try:
    # print("CHECK GFUN ** ENTRO A RECEIVED_MESSAGE **")
    upm = update.message
    user_data = update._effective_user
    chat_id = upm.chat_id
    user = g_fun.get_user_data(user_data)
    if not user and chat_id > 0:
      text = b_lang.no_username(user_data.language_code)
      update.message.reply_text(text)
      return False
    # Se revisa si se esta subiendo archivos de configuración
    if user["is_teacher"]:
      if cfg.is_config_files_set and not upm.document:
        if upm.chat_id < 0:
          planet = strip_accents(upm.chat.title)
          if upm.text:
            text = upm.text.strip(" ").upper()
            if text.startswith("=== INICIO DE MEETING") or text.startswith(
              "=== START MEETING"
            ):
              edu_fun.meetings(upm, context, user)
            elif text.startswith("=== FIN DE MEETING") or text.startswith(
              "=== END MEETING"
            ):
              edu_fun.meetings(upm, context, user, "end")
            elif cfg.active_meetings[planet]["meeting"]:
              user["planet"] = planet
              edu_fun.reg_messages(upm, user)
        else:
          send_Msg(context, user["_id"], tea_lang.welcome_short_text[user["language"]])
      elif upm.document:

        doc = upm.document
        if doc.file_name == "grades_format.csv":
          tea_fun.activities_grade_file(update, context, user)
        elif doc.file_name == "categories_grades_format.csv":
          tea_fun.categories_grade_file(update, context, user)
        elif (
          doc.file_name == "students_format.csv"
          or doc.file_name == "activities_format.csv"
          or doc.file_name == "add_students_format.csv"
          or doc.file_name == "add_activities_format.csv"
          or doc.file_name == "replace_students_format.csv"
          or doc.file_name == "replace_activities_format.csv"
        ):
          if (doc.file_name == "students_format.csv" and cfg.uploaded_students) or (
            doc.file_name == "activities_format.csv" and cfg.uploaded_activities
          ):
            send_Msg(
              context,
              user["_id"],
              tea_lang.config_files(user["language"], "exists_in_DB", doc.file_name),
            )
          else:
            tea_fun.config_files_upload(update, context, user)
      else:
        if upm.chat_id > 0:
          send_Msg(
            context, upm.chat_id, tea_lang.config_files(user["language"], "no_set_up")
          )
          tea_fun.config_files_set(context, user)
    else:
      if cfg.is_config_files_set:
        if is_user_registered(update, context, user):
          if chat_id < 0:
            edu_fun.reg_messages(upm, user)
          else:
            send_Msg(
              context, user["_id"], stu_lang.welcome_short_text[user["language"]]
            )
        else:
          if chat_id > 0:
            send_Msg(
              context,
              chat_id,
              stu_lang.not_config_files_set_text(context, user["language"]),
            )
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def config_files_set(context, user):
  """Sends the student and activity configuration files for the teacher to configure the course.

    Args:
        context ([type]): [description]
        user (dict): General user information.
    """
  try:
    not_set = []
    sql_stu = f"SELECT count(*) FROM students_file"
    sql_act = f"SELECT count(*) FROM activities"

    if not sqlite.execute_statement(sql_stu, "fetchone")[0]:
      not_set.append("students")
    if not sqlite.execute_statement(sql_act, "fetchone")[0]:
      not_set.append("activities")

    if len(not_set) == 2:
      text = t_lang.config_files(user.language, "download")
      context.bot.sendMessage(chat_id=user.id, parse_mode="HTML", text=text)
      config_files_send_document(context, user, "students")
      config_files_send_document(context, user, "activities")
    else:
      text = t_lang.config_files(user.language, "missing_file", not_set[0])
      context.bot.sendMessage(chat_id=user.id, parse_mode="HTML", text=text)
      config_files_send_document(context, user, not_set[0])

      """g_fun.send_Msg(
          context, user["_id"], tea_lang.config_files(user["language"], "download")
        )
        config_files_send_document(context, user, "students")
        config_files_send_document(context, user, "activities")
      else:
        if not db.students_file.find_one():
          g_fun.send_Msg(
            context,
            user["_id"],
            tea_lang.config_files(
              user["language"], "missing_file", file_name="students"
            ),
          )
          config_files_send_document(context, user, "students")
        elif not db.activities.find_one():
          g_fun.send_Msg(
            context,
            user["_id"],
            tea_lang.config_files(
              user["language"], "missing_file", file_name="activities"
            ),
          )
          config_files_send_document(context, user, "activities")"""
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def config_files_send_document(context, user, elements):
  try:
    context.bot.sendDocument(
      chat_id=user.id,
      document=open(b_lang.config_files_send_document(user.language, elements), "rb"),
    )
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
