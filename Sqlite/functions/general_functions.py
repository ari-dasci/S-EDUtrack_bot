import logging
import inspect
import sys
from colorama import init, Fore, Back
import config.db_sqlite_connection as sqlite


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
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)


def user_is_teacher(user_id):
  sql = f"SELECT * FROM teachers WHERE id_telegram={user_id}"
  try:
    return 1 if sqlite.execute_statement(sql, fetch="fetchone") else 0
  except Exception as e:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    print_except(error_path)
