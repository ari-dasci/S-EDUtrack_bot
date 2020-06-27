import inspect
import os
import pandas as pd
from telegram import ChatAction, InlineKeyboardMarkup as IKMarkup
from functools import wraps
from urllib.request import urlopen
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from functions import general_functions as g_fun
from text_language import (
  bot_lang as b_lang,
  general_lang as g_lang,
  teacher_lang as t_lang,
  student_lang as s_lang,
)

# Function Decorator
def send_action(action):
  """Decorator that sends 'action' while processing func command.

  Args:
      action (str): String with the action displayed by the bot
  """

  def decorator(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
      context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=action
      )
      return func(update, context, *args, **kwargs)

    return command_func

  return decorator


def received_message(update, context):
  """Receives a message from the user that is not a command. Identifies whether the user is a student or a teacher and redirects to the corresponding function.

  Args:
      update (:class:'telegram-Update'): Current request received by the bot
      context (:class:'telegram.ext-CallbackContext'): Context of the current request
  """
  try:
    chat_id = update.message.chat_id
    user = g_fun.get_user_data(update._effective_user)
    # get_user_data returns False if the user does not have the username set up
    if chat_id > 0:
      if user:
        user.received_message(update, context)
      else:
        text = b_lang.no_username(update._effective_user.language_code)
        update.message.reply_text(text)
        return False
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


# Functions for configuring the course
@send_action(ChatAction.TYPING)
def config_files_set(update, context, user):
  """Sends the student and activity configuration files for the teacher to configure the course.

    Args:
        context (:class:'telegram.ext-CallbackContext'): Context of the current request.
        user (:class:'user_types.Teacher'): General teacher information.
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
      text = t_lang.config_files(user.language, "download", context=context)
      context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
      config_files_send_document(context, user, "students")
      config_files_send_document(context, user, "activities")
    else:
      text = t_lang.config_files(user.language, "missing_file", not_set[0])
      context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
      config_files_send_document(context, user, not_set[0])
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def config_files_send_document(context, user, elements):
  """Sends the 'user' the requested document in 'elements'.

  Args:
      context (:class:'telegram.ext-CallbackContext'): Context of the current request.
      user (:class:'user_types.Teacher'): General teacher information.
      elements (str): Indicator of the document that will be sent to the user 'students' or 'activities'.
  """
  try:
    context.bot.sendDocument(
      chat_id=user._id,
      document=open(b_lang.config_files_send_document(user.language, elements), "rb"),
    )
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


@send_action(ChatAction.UPLOAD_DOCUMENT)
def config_files_upload(update, context, user):
  """EDUtrack receives a configuration document:
  students_format, add_stundents_format, replace_students_format, activities_format or replace_activities_format. To upload it to the DB.

  Args:
      update (:class:'telegram-Update'): Current request received by the bot.
      context (:class:'telegram.ext-CallbackContext'): Context of the current request.
      user (:class:'user_types.Teacher'): General teacher information.

  Returns:
      bool: Return True if the set up process was completed correctly and False otherwise.
  """

  def check_students_file(df_file):
    """Prepara los datos que se insertaran en la tabla students_file y revisa que los nombres de columnas sean correctos.

    Args:
        df_file (:class:'pandas-DataFrame'): DataFrame with the student records that will be uploaded to the DB.
    Returns:
        bool: Returns True if the check is correct otherwise returns False.
    """
    try:
      df_file = data_preparation(df_file, "students")
      # Elimina los archivos generados al solicitar el reporte de estudiantes.
      g_fun.remove_file("files/download/students_full.csv")
      g_fun.remove_file("files/downlad/students.csv")

      if not set(cfg.students_headers_file).issubset(file_headers):
        headers = ("\n").join(cfg.students_headers_file)
        text = t_lang.config_files(user.language, "header_error", elements=headers)
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        config_files_send_document(context, user, "students")
        return False
      return True
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)

  def check_activities_file(df_file):
    """Check that the activities_format file meets the necessary requirements before it is uploaded to the DB.

    Args:
        df_file (:class:'pandas-DataFrame'): DataFrame with the activity records that will be uploaded to the DB.
        elements (str): elements (str): Indicator that you are working with activities.
    """

    def are_categories_defined(root_category):
      try:
        # Check if all categories are defined
        if root_category != {"SUBJECT"}:
          if "SUBJECT" not in root_category:
            text = t_lang.config_files_activities(user.language, "no_main_category")
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          else:
            root_category.remove("SUBJECT")

          undefined_categories = "\n".join(root_category)
          if undefined_categories:
            text = t_lang.config_files_activities(
              user.language, "undefined_category", elements=undefined_categories
            )
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          return False
        return True
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    def categories_have_parent(category_data):
      try:
        # Check if all categories have parent category
        no_parent_cat = list(category_data.loc[category_data["category"] == ""]["_id"])
        if no_parent_cat:
          no_parent_cat = "\n".join(no_parent_cat)
          text = t_lang.config_files_activities(
            user.language, "no_parent_cat", elements=no_parent_cat
          )
          context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          return False
        return True
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    def categories_have_weight(category_data):
      try:
        # Check if the defined categories have weight.
        weightless_cat = list(category_data.loc[category_data["weight"] == ""]["_id"])
        if weightless_cat:
          weightless_cat = "\n".join(weightless_cat)
          text = t_lang.config_files_activities(
            user.language, "weightless", elements=weightless_cat
          )
          context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          return False
        return True
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    try:
      df_file = data_preparation(df_file, "activities")
      # Elimina los archivos generados al solicitar el reporte de actividades.
      g_fun.remove_file("files/download/all_activities.csv")
      g_fun.remove_file("files/download/qualifying_activities.csv")
      # Revisa los encabezados del archivo

      if not set(cfg.activities_headers_file).issubset(file_headers):
        headers = ("\n").join(cfg.students_headers_file)
        text = t_lang.config_files(user.language, "header_error", elements=headers)
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        config_files_send_document(context, user, "activities")
        return False

      # Get the categories file
      file_error = False
      categories = set(filter(None, df_file["category"].unique()))
      root_category = categories - set(df_file["_id"].dropna())
      category_data = df_file.loc[df_file["_id"].isin(categories)]

      if not are_categories_defined(root_category):
        file_error = True

      if not categories_have_parent(category_data):
        file_error = True

      if not categories_have_weight(category_data):
        file_error = True

      if file_error:
        return False
      return True
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)

  def separate_elements(df_file):
    try:
      sql = "SELECT * FROM students_file"
      data_DB = sqlite.execute_statement(sql, df=True)

      all_elements = g_fun.dataframes_comparison(data_DB, df_file).drop(
        ["_merge"], axis=1
      )
      duplicate_elements = list(
        g_fun.dataframes_comparison(data_DB, df_file, which="both")["email"]
      )
      new_elements = g_fun.dataframes_comparison(
        data_DB, df_file, which="right_only"
      ).drop(["_merge"], axis=1)
      return (all_elements, duplicate_elements, new_elements)
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return Exception

  try:
    doc = update.message.document
    add_elements = True if "add" in doc.file_name else False

    # Get File from Telegram
    input_file = context.bot.get_file(doc.file_id)
    f_path = input_file["file_path"]  # Se obtiene la ruta de descarga
    f_save_name = f"files/config/{doc.file_name}"  # Ruta donde se guardara el archivo
    temp = urlopen(f_path)
    df_file = pd.read_csv(urlopen(f_path), encoding="UTF-8-sig")

    file_headers = temp.readline().decode("UTF-8-sig")
    file_headers = set(file_headers[:-2].split(","))

    # Revisa que los archivos y nombres de columnas sean correctos
    if "students" in doc.file_name:
      table_name = "students_file"
      elements = "students"
      if not check_students_file(df_file):
        return False
    elif "activities" in doc.file_name:
      table_name = elements = "activities"
      if not check_activities_file(df_file):
        return False

    if not os.path.exists("files/config"):
      os.makedirs("files/config")

    if add_elements:
      all_elements, duplicate_elements, new_elements = separate_elements(df_file)

      if new_elements.empty:
        text = t_lang.config_files(user.language, "add_all_exists")
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        return False

      upload_data = sqlite.save_config_file_DB(new_elements, table_name, "append")
      all_elements.to_csv(f_save_name, index=False)
    else:
      upload_data = sqlite.save_config_file_DB(df_file, table_name, "replace")
      df_file.to_csv(f_save_name, index=False)

    # Set the global variables for activities, sections and categories. Creates the evaluation schema.

    if upload_data:
      # TODO: REVISAR ESTE APARTADO SI ES FUNCIONAL
      """ if "activities" in doc.file_name:
        # if collection.name == "activities":
        cfg.activities_sections = set(db.activities.find().distinct("section"))
        cfg.categories_evaluation = set(
          db.activities.find({"category": {"$ne": ""}}).distinct("category")
        )
        g_fun.create_evaluation_scheme() """

      if g_fun.are_config_files_set():
        cfg.config_files_set = True
        if add_elements:
          students = list(new_elements["email"])
          if create_grades(update, context, students, add_elements=True):
            if duplicate_elements:
              elements = "\n".join(duplicate_elements)
              text = t_lang.config_files(
                user.language, "add_duplicates", elements=elements
              )
              text += t_lang.config_files(user.language, "add_no_duplicates")
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            else:
              text = t_lang.config_files(user.language, "add_ready", elements=elements)
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        else:
          if elements == "students":
            students = list(df_file["email"])
          else:
            sql = "SELECT DISTINCT email FROM  students_file"
            students = [stu[0] for stu in sqlite.execute_statement(sql, "fetchall")]
          if create_grades(update, context, students):
            text = t_lang.welcome_text(user.language, context, "not_start")
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          else:
            text = t_lang.config_files(user.language, "ready_one")
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
            config_files_set(context, user)
      else:
        if "students" in doc.file_name:
          missing_file = "activities_format.csv"
        else:
          missing_file = "students_format.csv"

        text = t_lang.config_files(user.language, "ready_one", missing_file)
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
    else:
      text = t_lang.config_files(user.language, "no_loaded", doc.file_name)
      context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
      return False
  except:
    g_fun.print_except(inspect.stack()[0][3], user)
    file = update.message.document.file_name
    text = g_lang.error_upload_file(user.language, file)
    context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)


def data_preparation(data, elements):
  """Clean and prepare the dataframe 'data' to be uploaded to the database.

  Args:
      data (:class:'pandas.DataFrame'): Records of the file to be uploaded to the DB.
      elements (str): Indicator of the type of document you want to upload, 'students' or 'activities'.
  Returns:
      [pandas-DataFrame]: DataFrame clean.
  """
  try:
    ID = data.columns[0]
    data.columns = data.columns.str.replace(" ", "_")
    data.columns = data.columns.str.replace("-", "_")
    data.dropna(subset=[ID], inplace=True)

    if elements == "activities":
      data.columns = map(str.lower, data.columns)
      data.replace({"true": 1, "false": 0}, inplace=True)
      data["week"].fillna(0, inplace=True)
      data["visible"].fillna(0, inplace=True)
      data["weight"].fillna(0.0, inplace=True)
      data["active"] = 0
      data.fillna("", inplace=True)
      for col in ["_id", "section", "category"]:
        data[col] = data[col].str.upper()

    elif elements == "students":
      data.columns = map(str.lower, data.columns)
      data.fillna("", inplace=True)
      for col in ["first_name", "last_name", "username", "planet"]:
        data[col] = data[col].str.upper()
      # VER SI HACE FALTA PARA ALGO
      # data["name"] = data[ID].str.lower()
    elif elements == "grades":
      data.fillna(0, inplace=True)
      data.replace({"-": 0}, inplace=True)
      grades_cols = list(data.columns[1:])
      data[grades_cols] = data[grades_cols].astype(float)
    return data
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def create_grades(update, context, students, add_elements=False):
  """Creates the table 'grades' in the database from the file of students and activities uploaded by the teacher.

  Args:
      update (:class:'telegram-Update'): Current request received by the bot.
      context (:class:'telegram.ext-CallbackContext'): Context of the current request.
      students (list): List of students to be saved in the 'grades' table
      add_elements (bool, optional): Indicates if new elements will be added or if the table will be created. Defaults to False.

  Returns:
      bool: Returns True if the process is correct otherwise returns False
  """
  print("CHECK TEAFUN ** CREATE GRADES **")
  try:
    sql_act = "SELECT DISTINCT _id FROM activities WHERE weight>0"
    activities = [act[0] for act in sqlite.execute_statement(sql_act, "fetchall")]

    if not add_elements:
      sql = "DROP TABLE IF EXISTS grades"
      print(sqlite.execute_statement(sql))
      fields = """email TEXT NOT NULL PRIMARY KEY,
                  SUBJECT REAL DEFAULT 0,
                  _PERFORMANCE_SCORE REAL DEFAULT 0,
                  _MAX_ACTUAL_SCORE REAL DEFAULT 0,
                  _MAX_POSSIBLE_SCORE REAL DEFAULT 10
                  """
      for act in activities:
        fields += f", {act} REAL NOT NULL DEFAULT 0"
      fields += ", FOREIGN KEY(email) REFERENCES students_file(email)"
      sql = f"CREATE TABLE grades ({fields})"
      sqlite.execute_statement(sql)

    for student in students:
      sql = f"INSERT INTO grades (email) VALUES('{student}')"
      sqlite.execute_statement(sql)

    return True

    """ activities_list = dict.fromkeys(activities, 0)

    for student in new_elements:
      student.update(
        {
          "SUBJECT": 0,
          "_PERFORMANCE_SCORE": 0,
          "_MAX_ACTUAL_SCORE": 0,
          "_MAX_POSSIBLE_SCORE": 10,
        }
      )
      student.update(activities_list)
    db.grades.insert_many(new_elements)
    return True """
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def options_menu(update, context):
  try:
    query = update.callback_query
    selections = (query.data).split("-")
    choice = selections[-1]
    user = g_fun.get_user_data(update._effective_user)
    if user:
      if len(selections) > 1:
        # STUDENT MENU
        if selections[0] == "s_menu":
          if selections[1] == "back":
            pass
        # TEACHER MENU
        elif selections[0] == "t_menu":
          print(selections)
          if selections[1] == "back":
            text, options = t_lang.main_menu(user.language)
            show_menu(query, text, options)

          elif selections[1] == "act":
            if len(selections) == 2:
              text, options = t_lang.menu_act(user.language)
              show_menu(query, text, options)
            elif selections[2] == "view":
              if len(selections) == 3:
                text, options = t_lang.menu_act_view(user.language, "menu")
                show_menu(query, text, options)
              else:
                user.activities_view(update, context, selections[3], query)
            elif selections[2] == "grade":
              if len(selections) == 3:
                text, options = t_lang.menu_act_grade(user.language, "menu")
                show_menu(query, text, options)
              elif selections[3] == "upload":
                text = t_lang.menu_act_grade(user.language, "upload")
                query.edit_message_text(parse_mode="HTML", text=text)
                config_files_send_document(context, user, "grades")
              elif selections[3] == "cmd":
                text = t_lang.menu_act_grade(user.language, "cmd")
                query.edit_message_text(parse_mode="HTML", text=text)
            elif selections[2] == "replace":
              text = t_lang.menu_act_replace(user.language)
              query.edit_message_text(parse_mode="HTML", text=text)
              config_files_send_document(context, user, "activities")
            elif selections[2] == "modify":
              headers = "name\nsection\nweek\n"
              text = t_lang.menu_act_modify(user.language)
              query.edit_message_text(parse_mode="HTML", text=text)
            elif selections[2] == "delete":
              text = t_lang.menu_act_delete(user.language)
              query.edit_message_text(parse_mode="HTML", text=text)
            elif selections[2] == "active":
              sql = "SELECT DISTINCT _id FROM activities WHERE weight>0 AND active <> 1"
              inactive_act = [
                act[0] for act in sqlite.execute_statement(sql, "fetchall")
              ]
              inactive_act = "\n".join(sorted(inactive_act))
              text = t_lang.menu_act_active(user.language, "text")
              query.edit_message_text(parse_mode="HTML", text=text)
              text = t_lang.menu_act_active(user.language, "activities", inactive_act)
              context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          elif selections[1] == "stu":
            if len(selections) == 2:
              text, options = t_lang.menu_stu(user.language)
              show_menu(query, text, options)
            elif selections[2] == "view":
              if len(selections) == 3:
                text, options = t_lang.menu_stu_view(user.language, "menu")
                show_menu(query, text, options)
              else:
                user.students_view(update, context, selections[3], query)
            elif selections[2] == "add":
              text = t_lang.menu_stu_add(user.language)
              query.edit_message_text(parse_mode="HTML", text=text)
              config_files_send_document(context, user, "students")
            elif selections[2] == "modify":
              headers = "email\nfirst_name\nlast_name"
              text = t_lang.menu_stu_modify(user.language, headers)
              query.edit_message_text(parse_mode="HTML", text=text)
            elif selections[2] == "delete":
              text = t_lang.menu_stu_delete(user.language)
              query.edit_message_text(parse_mode="HTML", text=text)
          elif selections[1] == "reports":
            if len(selections) == 2:
              text, options = t_lang.menu_reports(user.language)
              show_menu(query, text, options)
            elif selections[2] == "grades":
              user.reports(update, context, selections[2], query)
            elif selections[2] == "ARF":
              print("ENTRO A ARF")
            elif selections[2] == "meetings":
              print("ENTRO A meetings")
            elif selections[2] == "eva_teacher":
              print("ENTRO A eva_teacher")
            elif selections[2] == "eva_contents":
              print("ENTRO A eva_contents")
            elif selections[2] == "eva_classmate":
              print("ENTRO A eva_classmate")

    else:
      text = b_lang.no_username(update._effective_user.language_code)
      update.message.reply_text(text)
      return False

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def show_menu(query, menu_text, menu_opt, context=""):
  try:
    keyboard = menu_opt
    reply_markup = IKMarkup(keyboard)
    if query:
      query.edit_message_text(
        parse_mode="HTML", text=menu_text, reply_markup=reply_markup
      )
    else:
      context.bot.sendMessage(
        chat_id="443344899", text=menu_text, reply_markup=reply_markup
      )
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False
