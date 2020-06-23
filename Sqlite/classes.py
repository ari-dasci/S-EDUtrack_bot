import inspect
import config.db_sqlite_connection as sqlite
import config.config_file as cfg
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from functions import general_functions as g_fun
from text_language import teacher_lang as t_lang, student_lang as s_lang


class User:
  def __init__(self, user_data):
    self._id = user_data["id"]
    self.telegram_name = user_data.full_name
    self.username = user_data["username"].upper()
    self.is_teacher = 0
    self.language = user_data["language_code"]
    self.email = ""

  def add_telegram_user(self):
    try:
      sql = f"SELECT count(_id) FROM telegram_users WHERE _id={self._id}"
      if not sqlite.execute_statement(sql, fetch="fetchone")[0]:
        sql = f"""INSERT INTO telegram_users VALUES ("{self._id}", "{self.telegram_name}","{self.username}","{self.is_teacher}", "{self.language}");"""
        if not sqlite.execute_statement(sql):
          print("Hubo un error al guardar al usuario en telegram_users")
          return False
      return True
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False


class Student(User):
  def __init__(self, user_data):
    super().__init__(user_data)
    self.planet = 0

  def __str__(self):
    return f"""
    ===============================
      STUDENT
      ID: {self._id}
      Telegram_name: {self.telegram_name}
      Username: {self.username}
      Is_teacher : {self.is_teacher}
      Language: {self.language}
      Planet: {self.planet}
    ==============================="""

  def register_student(self):
    try:
      sql = f"SELECT count(id_telegram) FROM registered_students WHERE id_telegram={self._id}"
      if not sqlite.execute_statement(sql, "fetchone")[0]:
        sql = f"SELECT * FROM students_file WHERE  username = '{self.username}'"
        user_data = sqlite.execute_statement(sql, "fetchone")
        if user_data:
          values = f"{self._id}, '{user_data[2]}, {user_data[1]}', '{user_data[0]}'"
          print(values)
          sql = f"INSERT INTO registered_students VALUES({values})"
          sqlite.execute_statement(sql)
        else:
          return False
      return True
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False


class Teacher(User):
  def __init__(self, user_data):
    super().__init__(user_data)
    self.is_teacher = 1

  def __str__(self):
    return f"""
    ===============================
      TEACHER
      ID: {self._id}
      Telegram_name: {self.telegram_name}
      Username: {self.username}
      Is_teacher : {self.is_teacher}
      Language: {self.language}
    ==============================="""
