import inspect
import os
import config.db_sqlite_connection as sqlite
import config.config_file as cfg
from telegram import (
  ReplyKeyboardMarkup,
  ReplyKeyboardRemove,
  InlineKeyboardMarkup as IKMarkup,
)
from functions import general_functions as g_fun, bot_functions as b_fun
from text_language import (
  teacher_lang as t_lang,
  student_lang as s_lang,
  general_lang as g_lang,
)


class User:
  def __init__(self, user_data):
    self._id = user_data["id"]
    self.telegram_name = user_data.full_name
    self.username = user_data["username"].upper()
    self.is_teacher = 0
    self.language = user_data["language_code"]
    self.email = ""

    self.add_telegram_user()
    self.check_language_username()

  def add_telegram_user(self):
    try:
      sql = f"INSERT OR IGNORE INTO telegram_users VALUES ('{self._id}', '{self.telegram_name}','{self.username}','{self.is_teacher}', '{self.language}');"
      if not sqlite.execute_statement(sql):
        return False
      return True
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def check_language_username(self):
    try:
      sql = f"SELECT language, username FROM telegram_users WHERE _id={self._id}"
      language = sqlite.execute_statement(sql, "fetchone")
      if language:
        self.language = language[0]
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False


class Student(User):
  def __init__(self, user_data):
    super().__init__(user_data)
    self.planet = "NULL"

  def check_planet(self):
    sql = f"SELECT planet FROM planet_users WHERE _id={self._id}"
    planet_DB = (sqlite.execute_statement(sql, "fetchone"),)
    if self.planet != planet_DB:
      sql = f"UPDATE planet_users SET planet = {self.planet} WHERE _id={self._id}"
      if not sqlite.execute_statement(sql):
        return False
    return True

  def register_student(self):
    try:
      sql = f"SELECT count(_id) FROM registered_students WHERE _id={self._id}"
      if not sqlite.execute_statement(sql, "fetchone")[0]:
        sql = f"SELECT * FROM students_file WHERE  username = '{self.username}'"
        user_data = sqlite.execute_statement(sql, "fetchone")
        if user_data:
          values = f"{self._id}, '{user_data[2]}, {user_data[1]}', '{user_data[0]}', '{self.username}', "
          sql = f"INSERT INTO registered_students VALUES({values})"
          sqlite.execute_statement(sql)
        else:
          return False
      return True
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def received_message(self, update, context):
    try:
      upm = update.message
      chat_id = upm.chat_id
      if cfg.config_files_set:
        if self.register_student():
          if chat_id < 0:
            self.planet = upm.chat.title
            self.check_planet()
            edu_fun.reg_messages(upm, self)
          else:
            text = s_lang.welcome(self.language, context)
            context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
        else:
          text = s_lang.check_email(self.language, "registration")
          context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
      else:
        if chat_id > 0:
          text = s_lang.not_config_files_set(self.language, context)
          context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def main_menu(self, update, context):
    pass
    # REVISAR SI EL ESTUDIANTE ESTA REGISTRADO

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


class Teacher(User):
  def __init__(self, user_data):
    super().__init__(user_data)
    self.is_teacher = 1

  def received_message(self, update, context):
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
            edu_fun.meetings(upm, context, self, meeting_indicator)
          elif cfg.active_meetings[planet]["meeting"]:
            self.planet = planet
            edu_fun.reg_messages(upm, self)
        else:
          text = t_lang.welcome_text(self.language, context, "short")
          context.bot.sendMessage(chat_id=self._id, text=text)

      elif upm.document:
        # Check if the document is a configuration document.
        doc = upm.document
        config_file = is_configuration_file(doc)
        if config_file:
          if config_file == "grades":
            activities_grade_file(update, context, self)
          if config_file == "exists":
            text = t_lang.config_files(self.language, "exists_in_DB", doc.file_name)
            context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
          else:
            b_fun.config_files_upload(update, context, self)

      else:
        if upm.chat_id > 0:
          text = t_lang.config_files(self.language, "no_set_up")
          context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
          b_fun.config_files_set(update, context, self)
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)

  def main_menu(self, update, context):
    try:
      text, options = t_lang.main_menu(self.language)
      keyboard = options
      reply_markup = IKMarkup(keyboard)
      update.message.reply_text(
        parse_mode="HTML", text=text, reply_markup=reply_markup,
      )
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def activities_view(self, update, context, option, query=""):
    try:
      if not os.path.exists("files/download"):
        os.makedirs("files/download")
      if option == "all":
        file = "files/download/all_activities"
        sql = "SELECT * FROM activities"
        activities = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.language, "ALL ACTIVITIES")
      elif option == "qualifying":
        file = "files/download/qualifying_activities"
        sql = "SELECT * FROM activities WHERE weight>0"
        activities = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.language, "QUALIFYING ACTIVITIES")
      elif option == "resources":
        file = "files/download/resources_activities"
        sql = "SELECT * FROM activities WHERE name<>''"
        activities = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.language, "RESOURCES ACTIVITIES")
      if g_fun.db_to_csv_html(activities, file, title=title, date=False):
        reply_markup = ""
        text = g_lang.file_ready_for_download(self.language)
        query.edit_message_text(parse_mode="HTML", text=text, reply_markup=reply_markup)
      else:
        text = t_lang.menu_act_view(self.language, "not_file")

      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.csv", "rb"))
      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.html", "rb"))
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def students_view(self, update, context, option, query=""):
    try:
      if not os.path.exists("files/download"):
        os.makedirs("files/download")
      if option == "file":
        file = "files/download/students_format"
        sql = "SELECT * FROM students_file"
        students = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.language, "STUDENTS_FORMAT")
      elif option == "reg":
        file = "files/download/registered_students"
        sql = "SELECT * FROM registered_students"
        students = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.language, "STUDENTS REGISTERED")
      if g_fun.db_to_csv_html(students, file, title=title, date=False):
        reply_markup = ""
        text = g_lang.file_ready_for_download(self.language)
        query.edit_message_text(parse_mode="HTML", text=text, reply_markup=reply_markup)
      else:
        text = t_lang.menu_act_view(self.language, "not_file")

      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.csv", "rb"))
      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.html", "rb"))
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def reports(self, update, context, report_type, query=""):
    def grades():

      return (grades, title)

    def arf():
      pass

    def meetings_participation():
      pass

    def teacher_evaluation():
      pass

    def resources_evaluation():
      pass

    def classmates_in_meetings_eva():
      pass

    def classmates_out_meetings_eva():
      pass

    try:
      folder_path = "files/download/reports"
      if not os.path.exists(folder_path):
        os.makedirs(folder_path)
      file = f"{folder_path}/{report_type}"

      if report_type == "grades":
        sql = "SELECT * FROM grades"
        elements = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.langiage, "GRADE REPORT")
      elif report_type == "ARF":
        sql = "SELECT * FROM academic_risk_factor"
        elements = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.langiage, "ACADEMIC RISK FACTOR REPORT")
      elif report_type == "":
        sql = "SELECT * FROM meetings"
        title = t_lang.title_file(self.langiage, "MEETINGS PARTICIPATION REPORT")
        elements = sqlite.execute_statement(sql, df=True)
      elif report_type == "eva_teacher":
        sql = "SELECT * FROM academic_risk_factor"
        title = t_lang.title_file(self.langiage, "TEACHER EVALUATION REPORT")
        elements = sqlite.execute_statement(sql, df=True)
      elif report_type == "eva_resources":
        sql = "SELECT * FROM eva_classmate_in_meeting"
        elements = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(self.langiage, "RESOURCES EVALUATION REPORT")
      elif report_type == "arf":
        sql = "SELECT * FROM eva_p2p_in_meet"
        elements = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(
          self.langiage, "CLASSMATES EVALUATION\nREPORT IN MEETINGS"
        )
      elif report_type == "arf":
        sql = "SELECT * FROM eva_p2p_out_meet"
        elements = sqlite.execute_statement(sql, df=True)
        title = t_lang.title_file(
          self.langiage, "CLASSMATES EVALUATION\nREPORT OUT MEETINGS"
        )

      elemets = sqlite.execute_statement(sql, df=True)

      if g_fun.db_to_csv_html(elements, file, title=title, date=False):
        reply_markup = ""
        text = g_lang.file_ready_for_download(self.language)
        query.edit_message_text(parse_mode="HTML", text=text, reply_markup=reply_markup)
      else:
        text = t_lang.menu_act_view(self.language, "not_file")
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

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
