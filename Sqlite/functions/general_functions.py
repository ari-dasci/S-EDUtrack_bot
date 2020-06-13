import logging
import inspect
import sys
from colorama import init, Fore, Back
import config.db_sqlite_connection as sqlite
import config.config_file as cfg

from classes import Teacher, Student


def config_subject():
  sql = 'SELECT count(*) FROM sqlite_master WHERE type = "table"'
  if not sqlite.execute_statement(sql, fetch="fetchone")[0]:
    sqlite.create_db()
  cfg.config_files_set = are_config_files_set()


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


def get_user_data(user_data):
  try:
    if user_is_teacher(user_data.id):
      if user_data.username:
        return Teacher(user_data)
    else:
      pass
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
    sql_stu = f"SELECT count(*) FROM students_file"
    sql_act = f"SELECT count(*) FROM activities"
    if (
      sqlite.execute_statement(sql_stu, fetch="fetchone")[0]
      and sqlite.execute_statement(sql_act, fetch="fetchone")[0]
    ):
      return True
    return False
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)
