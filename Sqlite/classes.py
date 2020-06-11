import config.db_sqlite_connection as sqlite
import config.config_file as cfg
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


class User:
  def __init__(self, user_data):
    self.id = user_data["id"]
    self.telegram_name = user_data.full_name
    self.username = user_data["username"]
    self.is_teacher = 0
    self.language = user_data["language_code"]
    self.planet = 0

  def change_language(self, update):
    reply_keyboard = [["EN", "ES"]]
    update.message.reply_text(
      "Selecciona un idioma",
      # g_lang.welcome(user.full_name),
      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

  def add_telegram_user(self, user):
    self.is_teacher = self.user_is_teacher(self.id)
    sql = f"""INSERT INTO telegram_users VALUES ("{self.id}", "{self.telegram_name}","{self.username}","{self.is_teacher}", "{self.language}");"""
    try:
      sqlite.execute_statement(sql)
      print(f"Se ha agregado el usuario {user.full_name}, en telegram_users")
      return self
    except Exception as e:
      print(e)
      print()

  def is_in_DB(self):
    # TODO: dos funciones una para telegram_users y otra para registered_users
    # tal vez sea bueno crear una variable global con telegram_users y registered_users

    sql = f"SELECT * FROM telegram_users WHERE id={self.id}"
    try:
      if sqlite.execute_statement(sql, fetch="fetchone"):
        return self

      else:
        print("SE DEBE REGISTRAR")
        return False

    except Exception as e:
      print(e)
      print()

  def user_is_teacher(self, user_id):
    sql = f"SELECT * FROM teachers WHERE id_telegram={user_id}"
    try:
      user = sqlite.execute_statement(sql, fetch="fetchone")
      return 1 if user else 0
    except Exception as e:
      print(e)
      print(e)

  def __str__(self):
    return f"""
    ===============================
      ID: {self.id}
      Telegram_name: {self.telegram_name}
      Username: {self.username}
      Is_teacher : {self.is_teacher}
      Language: {self.language}
      Planet: {self.planet}
    ==============================="""


class Student(User):
  pass


class Teacher(User):
  pass
