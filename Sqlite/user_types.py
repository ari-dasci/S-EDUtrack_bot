import inspect
import os
import numpy as np
import pandas as pd
import threading
from collections import Counter
from urllib.request import urlopen
from time import time

import config.db_sqlite_connection as sqlite
import config.config_file as cfg
from ordered_set import OrderedSet
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
        if upm.chat_id > 0:
          doc = upm.document
          config_file = is_configuration_file(doc)
          if config_file:
            if config_file == "grades":
              if cfg.config_files_set:
                input_file = context.bot.get_file(doc.file_id)
                f_path = input_file["file_path"]
                df_file = pd.read_csv(urlopen(f_path), encoding="UTF-8-sig")
                df_file = b_fun.data_preparation(df_file, "grades")
                thread_grades = threading.Thread(
                  target=self.thread_grades_activities,
                  args=(update, context, df_file, doc.file_name),
                )
                thread_grades.start()
                # self.__activities_grade_file(update, context, doc)
              else:
                text = t_lang.config_files(self.language, "no_set_up")
                context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
                b_fun.config_files_set(update, context, self)
            elif config_file == "exists":
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

  def thread_grades_activities(self, update, context, df_file, file_name):
    def activities_grade_file(df_file, path_file_name):
      def load_grades(df_file, path_file_name):
        def separate_elements(df_DB, df_file):
          try:
            ## SEPARATE ELEMENTS
            elements = {}
            elements["registered_stu"] = set(df_file["email"]) & set(df_DB["email"])
            elements["unregistered_stu"] = set(df_file["email"]) - set(df_DB["email"])
            elements["duplicated_stu"] = [
              stu for stu, count in Counter(df_file["email"]).items() if count > 1
            ]

            sql = "SELECT _id FROM evaluation_scheme  WHERE active=1"
            activities_active = sqlite.execute_statement(
              sql, fetch="fetchall", as_list=True
            )
            elements["registered_act"] = set(df_file.columns) & set(df_DB.columns)
            elements["registered_act"].remove("email")
            elements["non_active_act"] = elements["registered_act"] - set(
              activities_active
            )

            # TODO: Improve to detect more than one duplicate.
            elements["duplicated_act"] = [
              act[:-2] for act in df_file.columns if ".1" in act
            ]

            unregistered_act = set(df_file.columns) - set(df_DB.columns)

            elements["unregistered_act"] = {
              act for act in unregistered_act if ".1" not in act
            }
            for element in elements:
              elements[element] = sorted(list(elements[element]))

            ## DELETE ELEMENTS

            students = set(elements["unregistered_stu"] + elements["duplicated_stu"])
            for stu in students:
              df_file = df_file.drop(df_file[df_file["email"] == stu].index)

            activities_error = list(unregistered_act) + elements["duplicated_act"]
            df_file = df_file.drop(activities_error, axis=1)

            return (df_file, elements)

          except:
            error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
            g_fun.print_except(error_path)
            return False

        def join_dataframes(df_DB, df_file, students):
          try:
            registered_students = set(df_DB["email"])
            column_names = df_DB.columns

            new_df = pd.merge(df_DB, df_file, on="email", how="left")
            new_df.set_index("email", inplace=True)
            all_columns = list(new_df.columns)
            all_columns.reverse()
            for column in all_columns:
              if "_y" in column:
                column_name = column[:-2]
                column_x = column_name + "_x"

                # for student in registered_students.sorted():
                for student in students:
                  grade = new_df.loc[student, column]
                  new_df.loc[student, column_x] = grade
                new_df.rename(columns={column_x: column_name}, inplace=True)
              else:
                break

            new_df["email"] = new_df.index
            new_df = new_df[column_names]
            new_df.replace({np.nan: 0.0}, inplace=True)
            return new_df
          except:
            error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
            g_fun.print_except(error_path)
            return False

        def show_error_elements(df_file, elements):
          try:
            title = True
            if df_file.shape[0] == 0:
              text = t_lang.menu_act_grade(self.language, "no_students", title=title)
              context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
              title = False
            if elements["unregistered_stu"]:
              students = "\n".join(elements["unregistered_stu"])
              num_stu = len(elements["unregistered_stu"])
              text = t_lang.menu_act_grade(
                self.language, "unregistered_stu", students, num_stu, title=title
              )
              context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
              title = False
            if elements["duplicated_stu"]:
              students = "\n".join(elements["duplicated_stu"])
              num_stu = len(elements["duplicated_stu"])
              text = t_lang.menu_act_grade(
                self.language, "duplicated_stu", students, num_stu, title=title
              )
              context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
              title = False
            if df_file.shape[1] == 1:
              text = t_lang.menu_act_grade(self.language, "no_activities", title=title)
              context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
              title = False
            if elements["unregistered_act"]:
              activities = "\n".join(elements["unregistered_act"])
              num_act = len(elements["unregistered_act"])
              text = t_lang.menu_act_grade(
                self.language, "unregistered_act", activities, num_act, title=title,
              )
              context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
              title = False
            if elements["duplicated_act"]:
              activities = "\n".join(elements["duplicated_act"])
              num_act = len(elements["duplicated_act"])
              text = t_lang.menu_act_grade(
                self.language, "duplicated_act", activities, num_act, title=title
              )
              context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
              print(
                f"Las siguientes {num_act} actividades están duplicadas:\n{activities}"
              )
          except:
            error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
            g_fun.print_except(error_path)
            return False

        try:
          sucess = True
          sql = "SELECT * FROM grades"
          df_DB = sqlite.execute_statement(sql, df=True)
          df_file, elements = separate_elements(df_DB, df_file)

          if df_file.shape[0] == 0 or df_file.shape[1] == 1:
            sucess = False
          else:
            df_grades_to_upload = join_dataframes(
              df_DB, df_file, elements["registered_stu"]
            )
            df_grades_to_upload.to_csv(path_file_name, index=False)
            # sqlite.save_file_in_DB(df_grades_to_upload, "grades")
            sqlite.save_elements_in_DB(df_grades_to_upload, "grades")

          show_error_elements(df_file, elements)
          return elements if sucess else False

        except:
          error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
          g_fun.print_except(error_path)
          return False

      def get_parent_categories(activities):
        try:
          categories = {}
          for activity in activities:
            parent = activity
            categories[activity] = []
            while True:
              sql = f"SELECT category FROM activities WHERE _id = '{parent}'"
              parent_category = sqlite.execute_statement(sql, fetch="fetchone")[0]
              if parent_category == "SUBJECT":
                break
              else:
                parent = parent_category
                categories[activity].append(parent_category)
          return categories

        except:
          error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
          g_fun.print_except(error_path)
          return False

      def activate_activities(activities):
        try:

          for activity in activities:
            categories = tuple(activities[activity]) + ("SUBJECT", activity)
            sql = f"UPDATE evaluation_scheme SET active = 1 WHERE _id IN {categories}"
            sqlite.execute_statement(sql)
        except:
          error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
          g_fun.print_except(error_path)
          return False

      def calculate_evaluation_scheme(new_activities=""):
        # print("CHECK GFUN *** ENTRASTE A CALCULATE EVA SCHEME ***")
        try:
          """ sql = "SELECT * FROM evaluation_scheme"
          df_evaluation_scheme = sqlite.execute_statement(sql, df=True)
          for column in df_evaluation_scheme.columns[1:-1]:
            df_evaluation_scheme[column] = 0.0 """

          sql = "SELECT _id, weight FROM activities WHERE weight > 0"
          activities_weight = dict(
            sqlite.execute_statement(sql, fetch="fetch_all", as_dict=True)
          )

          for activity in new_activities:
            categories = new_activities[activity]
            categories.append("SUBJECT")
            actual_element = activity

            subject_score = activities_weight[activity]
            category_score = activities_weight[activity]

            for category in new_activities[activity]:
              # UPDATE REAL GRADE CATEGORY PARENT
              sql = f"UPDATE evaluation_scheme SET real_weight = real_weight + {category_score} WHERE _id = '{actual_element}'"
              sqlite.execute_statement(sql)

              if category != "SUBJECT":
                category_score *= activities_weight[category]
                subject_score *= activities_weight[category]
              sql = f"UPDATE evaluation_scheme SET category_score = category_score + {category_score} WHERE _id = '{actual_element}'"
              sqlite.execute_statement(sql)

              # category_score = activities_weight[category]

              actual_element = category
            # UPDATE SUBJECT
            sql = f"UPDATE evaluation_scheme SET real_weight = real_weight + {category_score} WHERE _id = '{actual_element}'"
            sqlite.execute_statement(sql)

            sql = f"UPDATE evaluation_scheme SET category_score = category_score + {category_score} WHERE _id = '{actual_element}'"
            sqlite.execute_statement(sql)
            categories = new_activities[activity].copy()
            categories.insert(0, activity)

            sql = f"UPDATE evaluation_scheme SET subject_score = subject_score + {subject_score} WHERE _id in {tuple(categories)}"
            sqlite.execute_statement(sql)
          sql = "SELECT subject_score FROM evaluation_scheme WHERE _id = 'SUBJECT'"
          max_actual_score = sqlite.execute_statement(sql, fetch="fetchone")[0]
          sql = f"UPDATE student_scores SET '_MAX_ACTUAL_SCORE' = {max_actual_score}"
          sqlite.execute_statement(sql)
          # cfg.evaluation_scheme = db.evaluation_scheme.find_one({}, {"_id": 0})
        except:
          error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
          g_fun.print_except(error_path)
          return False

      def calculate_grades(students, activities):
        def set_student_scores(
          student, activities, act_weights, stu_scores, stu_grades
        ):
          """Set the student's scores based on the grades obtained.

          Args:
              student (str): Student ID.
              activities (dict): Dictionary with the activities with their categories.
              act_weights (dict): Dictionary each activity and its weight.
              stu_scores (DataFrame): DataFrame with current student activity scores.
              stu_grades (DataFrame): DataFrame with the student's current activity grades.

          Returns:
              bool: False Returns will be corrected for an error.
          """
          try:
            max_final_grade = float(cfg.subject_data["max_final_grade"])
            for activity in activities:
              weight_activity = act_weights[activity]
              subject_score = score = (
                stu_grades[activity] * weight_activity / max_final_grade
              )
              actual_element = activity

              for category in activities[activity]:
                category_weight = act_weights[category] if category != "SUBJECT" else 1
                subject_score *= category_weight
                category_score = score * category_weight

                if actual_element == activity:
                  stu_scores[actual_element] = category_score
                else:
                  stu_scores[actual_element] += subject_score

                score = stu_scores[actual_element]
                actual_element = category
              stu_scores["SUBJECT"] += subject_score
            subject_score = stu_scores["SUBJECT"]
            max_actual_score = round(stu_scores["_MAX_ACTUAL_SCORE"], 14)
            stu_scores["_PERFORMANCE_SCORE"] = round(
              subject_score / max_actual_score, 14
            )
            stu_scores["_MAX_POSSIBLE_SCORE"] = round(
              1 - max_actual_score + subject_score, 14
            )
          except:
            error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
            g_fun.print_except(error_path)
            return False

        try:
          sql = """SELECT act._id, act.weight
          FROM activities act
          INNER JOIN evaluation_scheme eva
          ON act._id = eva._id
          WHERE eva.active = 1;"""

          activities_weight = dict(
            sqlite.execute_statement(sql, fetch="fetchall", as_dict=True)
          )

          df_grades = sqlite.table_DB_to_df("grades")

          df_scores = sqlite.table_DB_to_df("student_scores")
          for column in df_scores[1:]:
            if column != "_MAX_ACTUAL_SCORE":
              df_scores[column] = 0.0

          for student in students:
            student_grades = df_grades.loc[student]
            student_scores = df_scores.loc[student]

            set_student_scores(
              student, activities, activities_weight, student_scores, student_grades
            )

          df_scores["email"] = df_scores.index
          columns = list(df_scores.columns[:-1])
          columns.insert(0, df_scores.columns[-1])
          df_scores = df_scores[columns]
          sqlite.save_elements_in_DB(df_scores, "student_scores")
        except:
          error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
          g_fun.print_except(error_path)
          return False

      def get_risk_factor(students):
        """Obtains the academic risk factor (arf) of each student and its linguistic representation (linguistic_arf).

        Args:
            students (list): Student list from which the academic risk factor will be obtained.

        Returns:
            [bool]: True if the process is correct False otherwise.
        """
        try:
          max_final_score = float(cfg.subject_data["max_final_grade"])
          min_grade_to_pass = float(cfg.subject_data["min_grade_to_pass"])
          ideal_grading = float(cfg.subject_data["min_ideal_grade"])

          df_scores = sqlite.table_DB_to_df("student_scores")
          df_risk_factor = sqlite.table_DB_to_df("risk_factor")
          df_linguistic_arf = sqlite.table_DB_to_df("linguistic_risk_factor")

          # Rounding off to avoid excessive decimals
          for student in students:
            stu_scores = df_scores.loc[student]
            total_earned_score = round(stu_scores["SUBJECT"], 14)
            max_actual_score = round(stu_scores["_MAX_ACTUAL_SCORE"], 14)

            max_possible_score = round(stu_scores["_MAX_POSSIBLE_SCORE"], 14)
            # remaining_score = max_final_score - max_actual_score
            remaining_score = round(1 - max_actual_score, 14)

            academic_risk_factor = total_earned_score + (
              max_possible_score * remaining_score
            )  # / max_final_score
            academic_risk_factor = round(academic_risk_factor, 14)

            lower_limit = min_grade_to_pass / max_final_score
            increment = ((ideal_grading - min_grade_to_pass) / max_final_score) / 3

            if academic_risk_factor >= lower_limit + (increment * 3):
              linguistic_arf = "none"
            elif academic_risk_factor >= lower_limit + (increment * 2):
              linguistic_arf = "low"
            elif academic_risk_factor >= lower_limit + increment:
              linguistic_arf = "moderate"
            elif academic_risk_factor >= lower_limit:
              linguistic_arf = "critical"
            else:
              linguistic_arf = "very_critical"

            actual_week = g_fun.get_week(action="text")

            df_risk_factor.loc[student][actual_week] = academic_risk_factor
            df_linguistic_arf.loc[student][actual_week] = linguistic_arf

          df_risk_factor["email"] = df_risk_factor.index
          df_linguistic_arf["email"] = df_linguistic_arf.index
          columns = list(df_risk_factor.columns[:-1])
          columns.insert(0, df_risk_factor.columns[-1])
          df_risk_factor = df_risk_factor[columns]
          df_linguistic_arf = df_linguistic_arf[columns]
          sqlite.save_elements_in_DB(df_risk_factor, "risk_factor")
          sqlite.save_elements_in_DB(df_linguistic_arf, "linguistic_risk_factor")
          return True
        except:
          error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
          g_fun.print_except(error_path)
          return False

      try:
        elements = load_grades(df_file, path_file_name)
        if elements:
          # students = elements["registered_stu"]
          sql = "SELECT email FROM risk_factor"
          students = sqlite.execute_statement(sql, fetch="fetchall", as_list=True)
          activities = elements["registered_act"]
          non_active_activities = elements["non_active_act"]
          # sql = "SELECT _id FROM evaluation_scheme WHERE active=1"
          # activities = sqlite.execute_statement(sql, fetch="fetchall", as_list=True)
          activities_with_categories = get_parent_categories(activities)
          non_active_categories = get_parent_categories(non_active_activities)
          if non_active_activities:
            # activate_activities(activities_with_categories)
            # calculate_evaluation_scheme(activities_with_categories)
            activate_activities(non_active_categories)
            calculate_evaluation_scheme(non_active_categories)
          calculate_grades(students, activities_with_categories)
          get_risk_factor(students)
          return True
        else:
          return False
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    ### HASTA AQUI
    try:
      sucess = True
      path_file_name = "files/config/" + file_name
      if activities_grade_file(df_file, path_file_name):
        text = t_lang.menu_act_grade(self.language, "sucess")
      else:
        text = g_lang.error_upload_file(self.language, file_name)
      context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

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
        text = g_lang.file_not_created(self.language)

      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.csv", "rb"))
      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.html", "rb"))
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def grade_activity_cmd(self, update, context):
    try:
      args = context.args
      if len(args) >= 3:
        activity_id = args[0].upper()
        sql = f"SELECT COUNT(_id) FROM activities WHERE _id= '{activity_id}';"
        if sqlite.execute_statement(sql, fetch="fetchone")[0]:
          #  separate_students(args, activity_id)
          students_grades = " ".join(args[1:]).split(";")
          if students_grades[-1] == "":
            students_grades.remove("")

          students = {}
          if students_grades and students_grades != [""]:
            grades_error = ""
            duplicated_students = ""
            for student in students_grades:

              data = (student.strip(" ")).split(" ")
              email = data[0]
              try:
                grade = float(" ".join(data[1:]))
                if email not in students:
                  students[email] = float(grade)
                else:
                  duplicated_students += "\n" + email
                  del students[email]
              except:
                grades_error += "\n" + " ".join(data)

            text = ""
            title = True
            if grades_error:
              text = t_lang.menu_act_grade(self.language, "grades_error", grades_error)
              title = False
            if duplicated_students:
              if not title:
                text += "\n\n"
              text += t_lang.menu_act_grade(
                self.language, "duplicated_stu", duplicated_students, title=title
              )
              context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
            df_grades = pd.DataFrame(
              list(students.items()), columns=["email", activity_id]
            )
            print(df_grades)
            thread_grades = threading.Thread(
              target=self.thread_grades_activities,
              args=(update, context, df_grades, "grades_format.csv"),
            )
            thread_grades.start()

        else:
          text = t_lang.menu_act_grade(
            self.language, "unregistered_act", activity_id, 1
          )
          context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)

      else:
        text = t_lang.menu_act_grade(self.language, "no_arguments")
        context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)

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
        if not students.empty:
          title = t_lang.title_file(self.language, "STUDENTS REGISTERED")
        else:
          text = t_lang.menu_stu_view(self.language, "no_elements_registered")
          query.edit_message_text(parse_mode="HTML", text=text)
          return False
      if g_fun.db_to_csv_html(students, file, title=title, date=False):
        reply_markup = ""
        text = g_lang.file_ready_for_download(self.language)
        query.edit_message_text(parse_mode="HTML", text=text, reply_markup=reply_markup)
      else:
        text = g_lang.file_not_created(self.language)

      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.csv", "rb"))
      context.bot.sendDocument(chat_id=self._id, document=open(f"{file}.html", "rb"))
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def reports(self, update, context, report_type, query=""):
    try:
      folder_path = "files/download/reports"
      if not os.path.exists(folder_path):
        os.makedirs(folder_path)
      file = f"{folder_path}/{report_type}"

      if report_type == "grades":
        sql = "SELECT * FROM grades"
        title = t_lang.title_file(self.language, "GRADE REPORT")
      elif report_type == "ARF":
        sql = "SELECT * FROM academic_risk_factor"
        title = t_lang.title_file(self.language, "ACADEMIC RISK FACTOR REPORT")
      elif report_type == "meetings":
        sql = "SELECT * FROM meetings"
        title = t_lang.title_file(self.language, "MEETINGS PARTICIPATION REPORT")
      elif report_type == "eva_teacher":
        sql = "SELECT * FROM eva_teacher"
        title = t_lang.title_file(self.language, "TEACHER EVALUATION REPORT")
      elif report_type == "eva_resources":
        sql = "SELECT * FROM eva_resources"
        title = t_lang.title_file(self.language, "RESOURCES EVALUATION REPORT")
      elif report_type == "eva_p2p_in_meet":
        sql = "SELECT * FROM eva_p2p_in_meet"
        title = t_lang.title_file(
          self.language, "CLASSMATES EVALUATION\nREPORT IN MEETINGS"
        )
      elif report_type == "eva_p2p_out_meet":
        sql = "SELECT * FROM eva_p2p_out_meet"
        title = t_lang.title_file(
          self.language, "CLASSMATES EVALUATION\nREPORT OUT MEETINGS"
        )

      elements = sqlite.execute_statement(sql, df=True)
      print(type(elements))
      if type(elements) != bool:
        if g_fun.db_to_csv_html(elements, file, title=title, date=False):
          text = g_lang.file_ready_for_download(self.language)
          query.edit_message_text(parse_mode="HTML", text=text)
      else:
        text = "FUNCION EN DESARROLLO\n\n" + g_lang.file_not_created(self.language)
        query.edit_message_text(parse_mode="HTML", text=text)
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
