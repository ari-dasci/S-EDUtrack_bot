import logging
from datetime import datetime, timedelta
import inspect
import re
import sys
import os
from colorama import init, Fore, Back
from datetime import datetime, timedelta
from unicodedata import normalize
from config import (
  config_file as cfg,
  db_sqlite_connection as sqlite,
)
from config.create_files_format import create_files
from user_types import Teacher, Student


def config_subject():
  try:
    sql = 'SELECT count(*) FROM sqlite_master WHERE type = "table"'
    if not sqlite.execute_statement(sql, fetch="fetchone")[0]:
      sqlite.create_db()
    cfg.config_files_set = are_config_files_set()

    start_date = cfg.subject_data["start_date"]
    start_date = datetime.strptime(start_date, "%d/%m/%Y")
    cfg.monday_start_week = get_weekday_monday(start_date)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)


def print_except(function, *extra_info):
  try:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    function += f" line:{exc_tb.tb_lineno}"
    error_text = f"""
    ====================
    ERROR IN FUNCTION {function}
    {exc_type}
    {exc_obj}
    """
    if extra_info:
      for element in extra_info:
        error_text += "\n" + element
    error_text += "===================="
    print(Back.RED)
    logging.info(error_text + Back.RESET)
  except:
    error_path = f"{error_text}\n\n{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)


def get_user_data(user_data, planet=""):
  try:
    if user_is_teacher(user_data.id):
      if user_data.username:
        return Teacher(user_data)
    else:
      if user_data.username:
        user = Student(user_data)
        if planet:
          user.planet = planet
        else:
          sql = (
            f"SELECT planet FROM students_file where username= '{user_data.username}'"
          )
          planet = sqlite.execute_statement(sql, "fetchone")
          if planet:
            user.planet = planet[0]
          return user
      # TODO: Saber que se necesita para obtener la información de un estudiante
    return False
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)
    return False


def get_weekday_monday(date):
  try:
    day = date.strftime("%A")
    if day != "Monday":
      for i in range(1, 8):
        monday_date = date - timedelta(days=i)
        day = monday_date.strftime("%A")
        if day == "Monday":
          return monday_date
    else:
      return date
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)
    return False


def get_week(action):
  try:
    today = datetime.now()
    difference = today - cfg.monday_start_week
    num_week = int(difference.days / 7) + 1
    if num_week > int(cfg.course_weeks):
      num_week = int(cfg.course_weeks)
    if action == "num":
      return num_week
    elif action == "text":
      text_week = "week_"
      if len(cfg.subject_data["num_weeks"]) != len(str(num_week)):
        text_week += "0" * (len(cfg.subject_data["num_weeks"]) - len(str(num_week)))
      text_week += str(num_week)
      return text_week
  except:
    print_except(inspect.stack()[0][3])


def user_is_teacher(user_id):
  sql = f"SELECT * FROM teachers WHERE _id={user_id}"
  try:
    return 1 if sqlite.execute_statement(sql, fetch="fetchone") else 0
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)


def are_config_files_set(table_name=""):
  try:
    # TODO: VERIFICAR AQUI SI EXISTE O NO O COMO HACER SIN QUE HAYA TABLAS
    sql_stu = "SELECT count(*) FROM students_file"
    sql_act = "SELECT count(*) FROM activities"
    if (
      sqlite.execute_statement(sql_stu, fetch="fetchone")[0]
      and sqlite.execute_statement(sql_act, fetch="fetchone")[0]
    ):
      return True
    return False
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)


def strip_accents(string):
  """Recibe un string y elimina los acentos y lo devuelve en mayúsculas."""
  # print("CHECK GFUN *** ENTRO A STRIP ACCENTS ***")
  try:
    string = re.sub(
      r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
      r"\1",
      normalize("NFD", string),
      0,
      re.I,
    )
    string = normalize("NFC", string)
    return string.upper()
  except:
    print_except(inspect.stack()[0][3], string)


def remove_file(file):
  """Recibe el path de un archivo y sí existe lo elimina así como su versión html.

  """
  try:
    if os.path.isfile(file):
      os.remove(file)
    file = file[:-4] + ".html"
    if os.path.isfile(file):
      os.remove(file)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)


def dataframes_comparison(df1, df2, which="all"):
  """Find rows which are different between two DataFrames.
    all - Shows the union between the dataframes.
    no_repeat - Shows only the elements that are not repeated.
    both - Shows only the repeated elements.
    only_left - Shows only the elements on the left that are not on the right.
    only_right - Shows only the elements on the right that are not on the left.

    """
  comparison_df = df1.merge(df2, indicator=True, how="outer")
  if which == "all":
    diff_df = comparison_df
  elif which == "no_repeat":
    diff_df = comparison_df[comparison_df["_merge"] != "both"]
  else:
    diff_df = comparison_df[comparison_df["_merge"] == which]
  return diff_df


def db_to_csv_html(df, file, headers=[], title="", date=True):
  """Guarda la información del cursor almacenado en 'elements' de la base de datos en un archivo 'csv' y 'html' en el path almacenado en 'file'.

  Arguments:
      elements {pymongo.cursor.Cursor} -- Resgistros a guardar en los archivos.
      file {str} -- Path y nombre del archivo sin extensión donde se almacenan los archivos.
      headers {list} -- Lista con el orden de los encabezados para un archivo
      title {str} -- Título que llevara el archivo HTML.
      date {bool} -- Si es True agregara la fecha al final del archivo.

  Returns:
      [bool] -- 'True' si se crean correctamente los archivos 'False' si se genera una excepción.
  """
  try:
    # df = pd.DataFrame(list(elements))
    # TODO: Verificar si no afecta a textos
    if "activities" in file:
      df.sort_values(by=["_id"], inplace=True)
    elif "students" in file:
      df.sort_values(by=["email"], inplace=True)
      for element in ["_jeovani@correo.ugr.es", "_burrita@correo.ugr.es"]:
        df = df.drop(df[df.loc[:, "email"] == element].index)
    if headers:
      df = df[headers]
    if "grades" in file:
      df2 = df.mean()
      df2["_id"] = "PROMEDIOS"
      df = df.append(df2, ignore_index=True)
    df = df.round(2)
    create_files(file, df, title, date, mode="w+")
    return True
    """
    ## Esto estaba antes
    df = pd.DataFrame(list(elements))
    print(df)
    df.to_csv(file, index=False)
    file = file[:-4]
    df.index = range(1, df.shape[0] + 1)
    with open(file + ".html", "w") as html_file:
      html_file.write(df.to_html(justify="center"))
    return True """
  except:
    print_except(inspect.stack()[0][3])
    return False
