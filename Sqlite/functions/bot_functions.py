import inspect
import os
import pandas as pd
from telegram import ChatAction
from functools import wraps
from urllib.request import urlopen
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from functions import general_functions as g_fun, teacher_functions as t_fun
from text_language import (
  bot_lang as b_lang,
  general_lang as g_lang,
  teacher_lang as t_lang,
  student_lang as s_lang,
)


def send_action(action):
  """Sends 'action' while processing func command."""

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
  try:
    # print("CHECK GFUN ** ENTRO A RECEIVED_MESSAGE **")
    upm = update.message
    user_data = update._effective_user
    chat_id = upm.chat_id
    user = g_fun.get_user_data(user_data)
    # get_user_data returns False if the user does not have the username set up
    if not user and chat_id > 0:
      text = b_lang.no_username(user_data.language_code)
      update.message.reply_text(text)
      return False

    if user.is_teacher:
      t_fun.teacher_received_message(update, context, user)
    else:
      if cfg.config_files_set:
        if user.register_student():
          if chat_id < 0:
            edu_fun.reg_messages(upm, user)
          else:
            text = s_lang.welcome_text(user.language, context)
            context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        else:
          text = s_lang.check_email(user.language, "registration")
          context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
          print()
      else:
        if chat_id > 0:
          text = s_lang.not_config_files_set(user.language, context)
          context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


@send_action(ChatAction.TYPING)
def config_files_set(update, context, user):
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
  try:
    context.bot.sendDocument(
      chat_id=user._id,
      document=open(b_lang.config_files_send_document(user.language, elements), "rb"),
    )
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def activities_grade_files():
  pass


def categories_grade_file():
  pass


@send_action(ChatAction.UPLOAD_DOCUMENT)
def config_files_upload(update, context, user):
  """EDUtrack recibe un documento de configuración:
  students_format, replace_students_format, activities_format o replace_activities_format, lo descarga y lo prepara para subirlo a la base de datos.

  Args:
      update ([type]): [description]
      context ([type]): [description]
      user ([type]): [description]

  Returns:
      bool: Return True if the set up process was completed correctly and False otherwise.
  """
  print("CHECK TEA FUN ** CONFIG FILES UPLOAD **")

  def check_students_file(df_file, elements):
    """Prepara los datos que se insertaran en la tabla students_file y revisa que los nombres de columnas sean correctos.

    Args:
        df_file (DataFrame): DataFrame con los registros de estudiantes que será subidos a la DB.
        elements (str): [description]

    Returns:
        bool: Retorna True si la comprobación es correcto de lo contrario retorna False.
    """
    try:
      df_file = data_preparation(df_file, elements)
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

  def check_activities_file(df_file, elements):
    try:
      df_file = data_preparation(df_file, elements)
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
        file_error = True

      category_data = df_file.loc[df_file["_id"].isin(categories)]
      print(category_data)

      # Check if all categories have parent category
      no_parent_cat = list(category_data.loc[category_data["category"] == ""]["_id"])
      if no_parent_cat:
        no_parent_cat = "\n".join(no_parent_cat)
        text = t_lang.config_files_activities(
          user.language, "no_parent_cat", elements=no_parent_cat
        )
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)

        file_error = True

      # Check if the defined categories have weight.
      weightless_cat = list(category_data.loc[category_data["weight"] == ""]["_id"])
      if weightless_cat:
        weightless_cat = "\n".join(weightless_cat)
        text = t_lang.config_files_activities(
          user.language, "weightless", elements=weightless_cat
        )
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
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
      conn = sqlite.connection(True)
      data_DB = pd.read_sql_query(sql, con=conn)
      conn.close()

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
      if not check_students_file(df_file, elements):
        return False
    elif "activities" in doc.file_name:
      table_name = elements = "activities"
      if not check_activities_file(df_file, elements):
        return False

    if not os.path.exists("files/config"):
      os.makedirs("files/config")

    if add_elements:
      all_elements, duplicate_elements, new_elements = separate_elements(df_file)

      if new_elements.empty:
        text = t_lang.config_files(user.language, "add_all_exists")
        context.bot.sendMessage(chat_id=user._id, parse_mode="HTML", text=text)
        return False

      upload_data = g_fun.save_config_file_DB(new_elements, table_name, "append")
      all_elements.to_csv(f_save_name, index=False)
    else:
      upload_data = g_fun.save_config_file_DB(df_file, table_name, "replace")
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

      cfg.config_files_set = g_fun.are_config_files_set()

      if cfg.config_files_set:
        if add_elements:
          students = list(new_elements["email"])
          if create_grades(update, context, students, add_elements=True):
            if duplicate_elements:
              elements = "\n".join(duplicate_elements)
              print(elements)
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
  try:
    ID = data.columns[0]
    data.columns = data.columns.str.replace(" ", "_")
    data.columns = data.columns.str.replace("-", "_")
    data.dropna(subset=[ID], inplace=True)

    if elements == "activities":
      data.columns = map(str.lower, data.columns)
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
    g_fun.print_except(inspect.stack()[0][3], f"ELEMENTS: {elements}")


def create_grades(update, context, students="", add_elements=False):
  """Crea el apartado de calificaciones en la base de datos a partir deel archivo de estudiantes y actividades subidos por el docente.

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


def menu(update, context):
  pass

