import logging
import inspect
import sys
import os
from colorama import init, Fore, Back
import config.db_sqlite_connection as sqlite
import config.config_file as cfg

from classes import Teacher, Student


def config_subject():
  try:
    sql = 'SELECT count(*) FROM sqlite_master WHERE type = "table"'
    if not sqlite.execute_statement(sql, fetch="fetchone")[0]:
      sqlite.create_db()
    cfg.config_files_set = are_config_files_set()
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
          user.add_telegram_user()
          return user
      # TODO: Saber que se necesita para obtener la información de un estudiante
    return False
  except:
    pass

    # current_user.add_telegram_user()
    # print(current_user)


def user_is_teacher(user_id):
  sql = f"SELECT * FROM teachers WHERE id_telegram={user_id}"
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


def save_config_file_DB(df, table_name, action="replace"):
  try:
    conn = sqlite.connection(True)
    df.to_sql(table_name, con=conn, index=False, if_exists=action)
    conn.close()
    return True
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)
    return False


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
