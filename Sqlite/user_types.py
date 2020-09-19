import bisect
import inspect
import os
import re
import threading
from datetime import datetime, timedelta
from time import time
from urllib.request import urlopen

from telegram import InlineKeyboardMarkup as IKMarkup, InlineKeyboardButton as IKButton
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config.config_file as cfg
import config.db_sqlite_connection as sqlite
import numpy as np
import pandas as pd
from functions import bot_functions as b_fun
from functions import general_functions as g_fun
from text_language import general_lang as g_lang
from text_language import student_lang as s_lang
from text_language import teacher_lang as t_lang


class User:
  def __init__(self, user_data, planet=""):
    self._id = user_data["id"]
    self.telegram_name = user_data.full_name
    self.username = user_data["username"].upper()
    self.language = user_data["language_code"]
    self.planet = g_fun.strip_accents(planet)
    self.email = ""

    if self.language != "es":
      self.language = "en"

    self.add_telegram_user()
    self.check_language_username()

  def add_telegram_user(self):
    try:
      sql = f"INSERT OR IGNORE INTO telegram_users VALUES ('{self._id}', '{self.telegram_name}','{self.username}','{self.is_teacher}', '{self.language}');"
      if not sqlite.execute_sql(sql):
        return False
      return True
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def check_language_username(self):
    """It maintains the language selected by the user."""
    try:
      sql = f"SELECT language, username FROM telegram_users WHERE _id={self._id}"
      language = sqlite.execute_sql(sql, "fetchone")
      if language:
        self.language = language[0]
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def reg_messages(self, update):
    def get_message_type():
      try:
        message_type = ""
        if upm.text:
          message_type = "TEXT"
        elif upm.photo:
          message_type = "IMAGE"
        elif upm.video or upm.video_note:
          message_type = "VIDEO"
        elif upm.voice:
          message_type = "VOICE"
        elif upm.sticker:
          message_type = "STICKER"
        elif upm.document:
          type_document = upm.document.mime_type.split("/")
          type_document = type_document[0]
          if type_document == "video":
            message_type = "GIF"
          elif type_document == "image":
            message_type = "IMAGE"
          else:
            message_type = "DOCUMENT"
        return message_type
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    try:
      upm = update.message
      message_type = get_message_type()
      meeting_data = cfg.active_meetings[self.planet]
      meeting = meeting_data["meeting"][-1] if meeting_data["meeting"] else -1

      table = "teacher_messages" if self.is_teacher else "student_messages"

      sql = f"""SELECT COUNT(*) FROM {table}
                WHERE _id = {self._id}
                  and planet = '{self.planet}'
                  and meeting = {meeting} """
      if not sqlite.execute_sql(sql, fetch="fetchone")[0]:
        sql = f"""INSERT OR IGNORE INTO {table} (_id, planet, meeting)
                    VALUES({self._id}, '{self.planet}', {meeting})"""
        sqlite.execute_sql(sql)

      sql = f"""UPDATE {table} SET {message_type} = {message_type} + 1
                WHERE _id = {self._id}
                  and planet = '{self.planet}'
                  and meeting = {meeting} """
      sqlite.execute_sql(sql)
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False


class Student(User):
  def __init__(self, user_data, planet):
    self.is_teacher = 0
    super().__init__(user_data, planet)

  def register_student(self, from_planet=False):
    def register():
      try:
        sql = f"SELECT * FROM students_file WHERE username = '{self.username}'"
        user_data = sqlite.execute_sql(sql, fetch="fetchone", as_dict=True)
        planet = self.planet

        if user_data:
          if not planet:
            planet = user_data["planet"]
          user_data = dict(user_data)
          values = f"""{self._id}, '{user_data["last_name"]}, {user_data["first_name"]}', '{user_data["email"]}', '{self.username}', '{planet}'"""
          sql = f"INSERT INTO registered_students VALUES({values})"
          sqlite.execute_sql(sql)
        elif from_planet:
          values = f"""{self._id}, "", "", '{self.username}', '{planet}'"""
          sql = f"INSERT INTO registered_students VALUES({values})"
          sqlite.execute_sql(sql)

        else:
          return False
        return True
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    def check_if_change(registered_user):
      try:
        changes = []
        if self.planet and self.planet != registered_user["planet"]:
          planet = self.planet.upper()
          changes.append(f"planet = '{planet}'")
        if self.username and self.username != registered_user["username"]:
          changes.append(f"username = '{self.username}'")

        if not registered_user["full_name"]:
          sql = f"SELECT last_name, first_name FROM students_file where username='{self.username}'"
          name = sqlite.execute_sql(sql, fetch="fetchone")
          if name:
            full_name = name[0], name[1]
            changes.append(f"full_name = '{full_name}'")
        if not registered_user["email"]:
          sql = f"SELECT email FROM students_file where username = '{self.username}'"
          email = sqlite.execute_sql(sql, fetch="fetchone")
          if email:
            changes.append(f"email = '{email}'")
        changes = ",".join(changes)
        if changes:
          sql = f"UPDATE registered_students SET {changes} WHERE _id = {self._id}"
          sqlite.execute_sql(sql)
        return True
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    try:
      sql = f"SELECT * FROM registered_students WHERE _id={self._id}"
      registered_user = sqlite.execute_sql(sql, fetch="fetchone", as_dict=True)
      if not registered_user:
        if register():
          return True
      else:
        if check_if_change(dict(registered_user)):
          return True
      return False
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def received_message(self, update, context):
    try:
      upm = update.message
      chat_id = upm.chat_id
      from_planet = False
      if cfg.config_files_set:
        if chat_id < 0:
          from_planet = True

        if self.register_student(from_planet):
          if chat_id < 0:
            self.reg_messages(update)
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
    try:
      sql = f"SELECT COUNT(*) FROM registered_students WHERE _id = {self._id}"
      if sqlite.execute_sql(sql, fetch="fetchone")[0]:
        text, options = s_lang.main_menu(self.language)
        keyboard = options
        reply_markup = IKMarkup(keyboard)
        update.message.reply_text(
          parse_mode="HTML",
          text=text,
          reply_markup=reply_markup,
        )
      else:
        text = s_lang.check_email(self.language, "registration")
        context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def my_grade(self, update, context, query):
    def get_activities_list(eva_scheme, def_grades, text="", level=1):
      try:
        for element in eva_scheme:
          act_name = df_act_names.loc[element]["name"]
          act_name = act_name if act_name else element
          grade = str(round(def_grades.loc[element]["grade"], 3))
          if eva_scheme[element]:
            if df_act_names.loc[element]["visible"]:
              spaces = " " if level == 1 else "  " * level
              text += f"\n\n{spaces}* {act_name} = {grade}"
            text = get_activities_list(eva_scheme[element], def_grades, text, level + 1)
          else:
            if df_act_names.loc[element]["visible"]:
              text += f"\n{'  '*level}   -{act_name} = {grade}"
        return text
      except:
        error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
        g_fun.print_except(error_path)
        return False

    try:
      actual_week = g_fun.get_week("text")
      num_week = g_fun.get_week("num")
      sql = "SELECT COUNT(*) FROM evaluation_scheme WHERE active = 1"
      if sqlite.execute_sql(sql, fetch="fetchone")[0]:
        if self._id in cfg.registered_emails:
          if cfg.registered_emails[self._id]:
            email = cfg.registered_emails[self._id]
            columns = "_id, name, visible"
            df_act_names = sqlite.table_DB_to_df(
              "activities", columns=columns, set_index=True
            )
            sql = f"""SELECT l.{actual_week}, a.SUBJECT, g._MAX_POSSIBLE_GRADE
                      FROM  linguistic_risk_factor l
                      INNER JOIN grades g
                      ON l.email = g.email
                      INNER JOIN actual_grades a
                      ON l.email = a.email
                      WHERE l.email = '{email}'"""
            data = sqlite.execute_sql(sql, fetch="fetchone")
            sql = f"SELECT {actual_week} FROM risk_factor Where email = '{email}'"
            stu_risk_factor = sqlite.execute_sql(sql, fetch="fetchone")[0]

            sql = "SELECT category FROM activities WHERE category <> ''"
            categories = sqlite.execute_sql(sql, fetch="fetchall", as_list=True)
            sql = """SELECT _id FROM activities WHERE weight >0
                  and _id not in (SELECT category FROM activities WHERE category <> '')"""
            activities = sqlite.execute_sql(sql, fetch="fetchall", as_list=True)

            sql = f"SELECT * FROM grades WHERE email = '{email}'"
            df_grades_activities = sqlite.execute_sql(sql, df=True)
            sql = f"SELECT * FROM actual_grades WHERE email = '{email}'"
            df_grades_categories = sqlite.execute_sql(sql, df=True)
            df_grades = pd.concat(
              [df_grades_activities[activities], df_grades_categories],
              axis=1,
            )
            df_grades = df_grades[sorted(df_grades.columns)].T
            df_grades.columns = ["grade"]

            linguistic_arf = g_lang.linguistic_arf(self.language, data[0])
            max_activity_grade = float(cfg.subject_data["max_activity_grade"])
            student_data = {}
            if data:
              student_data["linguistic"] = linguistic_arf
              student_data["actual_grade"] = round(data[1] * max_activity_grade, 3)
              student_data["max_possible_grade"] = round(data[2], 3)

            # GET ACTIVITIES LIST
            student_data["activities"] = get_activities_list(
              cfg.evaluation_scheme["SUBJECT"], df_grades
            )
            text = s_lang.my_grade(self.language, "grades", num_week, student_data)
            #### REVISAR ESTE SI ES CONTEXT
            query.edit_message_text(parse_mode="HTML", text=text)
          else:
            text = s_lang.my_grade(self.language, "no_email", num_week)
            query.edit_message_text(chat_id=self._id, parse_mode="HTML", text=text)
            text = s_lang.check_email(self.language, "registration")
            #### REVISAR ESTE SI ES CONTEXT
            context.bot.sendMessage(parse_mode="HTML", text=text)

          # GET ACTUAL_GRADE

          # GET MAX_POSSIBLE_GRADE

          # GET ACTIVITIES LIST
          sql = "SELECT _id FROM activities WHERE visible =1"
          visible_activities = sqlite.execute_sql(sql, fetch="fetchall", as_list=True)

      else:
        text = s_lang.my_grade(self.language, "no_active", num_week)
        query.edit_message_text(parse_mode="HTML", text=text)

    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def opn_tea_practice(self, context, query, selections):
    try:
      actual_week = g_fun.get_week("text")
      num_week = g_fun.get_week("num")
      email = cfg.registered_emails[self._id]
      criterion = value = ""
      category = selections[3]
      if len(selections) > 4:
        criterion = selections[4]
        if len(selections) > 5:
          value = selections[5]

      if not value:
        if not criterion:
          if category == "teacher":
            criteria = {
              criterion for criterion in cfg.teacher_criteria if "T_" in criterion
            }
          else:
            criteria = {
              criterion for criterion in cfg.teacher_criteria if "C_" in criterion
            }

          if email:
            sql = f"""SELECT CRITERION FROM opn_teacher_practice
            WHERE email = '{email}' and week = {num_week}"""
            evaluated_criteria = sqlite.execute_sql(sql, fetch="fetchall", as_list=True)
            if evaluated_criteria:
              criteria = criteria - set(evaluated_criteria)

            criteria_dict = {}
            for criterion in criteria:
              criterion_name = g_lang.teacher_criteria(self.language, criterion)
              criteria_dict[criterion_name] = criterion
            criteria = sorted(criteria_dict.items()) if criteria_dict else []

            keyboard = []
            for criterion in criteria:
              keyboard.append(
                [
                  IKButton(
                    criterion[0], callback_data=f"s_menu-opn-tp-{category}-{criterion[1]}"
                  )
                ]
              )
            keyboard.append(
              [
                IKButton(
                  g_lang.back_text[self.language], callback_data=f"s_menu-opn-tp"
                )
              ]
            )

          if len(keyboard) == 1:
            text = s_lang.opn_tea_practice(self.language, "no_criteria", week=num_week)
            b_fun.show_menu(query, text, keyboard)

          else:
            text = s_lang.opn_tea_practice(self.language, "choice_criterion", num_week)
            b_fun.show_menu(query, text, keyboard)

        else:
          criterion_name = g_lang.teacher_criteria(self.language, criterion)
          options = g_lang.scale_7(self.language, query.data)
          text = s_lang.opn_tea_practice(self.language, "criterion", num_week, criterion_name)
          b_fun.show_menu(query, text, options)

      else:
        sql = f"""INSERT OR IGNORE INTO opn_teacher_practice
              VALUES('{email}', {num_week}, '{criterion}', '{value}')"""
        sqlite.execute_sql(sql)
        # g_fun.show_menu(query,stu_lang.opn_tea_practice_menu[user['language']]['opt'],stu_lang.opn_tea_practice(user['language'],'text_after_save'))
        print(selections[:-3])

        self.opn_tea_practice(context, query, selections[:-2])
    except:
      error_path = f'{inspect.stack()[0][1]} - {inspect.stack()[0][3]}'
      g_fun.print_except(error_path)
      return False

  def opn_collaboration(self, context, query, selections):
    try:
      if (
        user["_id"] in cfg.registered_students
        and user["_id"] not in cfg.identified_students
      ):
        actual_week = g_fun.get_week("text")
        num_week = g_fun.get_week()
        classmate = value = ""

        if len(selections) > 3:
          classmate = selections[3]
          if len(selections) > 4:
            value = selections[4]

        if not value:
          if not classmate:
            classmates = db.opn_collaboration.find_one(
              {"_id": user["planet"]}, {"_id": 0}
            )["members"][user["_id"]]["classmates"]

            keyboard = []
            for classmate in classmates:
              if not classmates[classmate]["values"][actual_week]:
                if db.registered_students.find_one({"_id": classmate}):
                  name = db.registered_students.find_one({"_id": classmate})["name"]
                  keyboard.append(
                    [IKButton(name, callback_data=f"s_menu-opn-coll-{classmate}")]
                  )
            keyboard.append(
              [
                IKButton(
                  g_lang.back_text[user["language"]], callback_data=f"s_menu-opn"
                )
              ]
            )
            if len(keyboard) == 1:
              g_fun.show_menu(
                query,
                keyboard,
                stu_lang.opn_collaboration(
                  user["language"], "no_classmates", week=num_week
                ),
              )
            else:
              g_fun.show_menu(
                query, keyboard, stu_lang.opn_collaboration(user["language"], "text")
              )
          else:
            name = db.registered_students.find_one({"_id": classmate})["name"]
            g_fun.show_menu(
              query,
              g_lang.scale_7(user["language"], query.data),
              stu_lang.opn_collaboration(user["language"], "scale", name, num_week),
            )
        else:
          db.opn_collaboration.update_one(
            {"_id": user["planet"]},
            {
              "$set": {
                f"members.{user['_id']}.classmates.{classmate}.values.{actual_week}": value
              },
              "$push": {
                f"members.{classmate}.weekly_values.{actual_week}.values": value,
                f"members.{classmate}.general_values": value,
                f"weekly_values.{actual_week}.values": value,
                f"planet_values": value,
              },
            },
          )

          t = threading.Thread(
            target=edu_fun.student_tupla, args=(classmate, user["planet"], actual_week)
          )
          t.start()

          opn_collaboration(context, query, user, selections[:-2])
      else:
        g_fun.send_Msg(
          context,
          user["_id"],
          stu_lang.opn_collaboration(user["language"], "no_planet"),
          query=query,
        )
    except:
      g_fun.print_except(inspect.stack()[0][3], user, selections)

  def opn_rsrcs(self, context, query, selections):
    try:
      # actual_week = g_fun.get_week("text")
      num_week = g_fun.get_week()
      if cfg.resources["week"] < num_week:
        g_fun.get_resources()
      section = resource = value = ""

      if len(selections) > 3:
        section = selections[3]
        if len(selections) > 4:
          resource = selections[4]
          if len(selections) > 5:
            value = selections[5]
      student_resources = db.opn_resources.find_one({"_id": user["_id"]}, {"_id": 0})
      keyboard = []
      if not value:
        if not resource:
          if not section:
            sections = sorted(cfg.resources)
            sections.remove("week")
            for section in sections:
              for resource in cfg.resources[section]:
                if not student_resources[section][resource]:
                  # bisect.insort(keyboard, [IKButton(section, callback_data=f"s_menu-opn-rsrcs-{section}")])
                  keyboard.append(
                    [IKButton(section, callback_data=f"s_menu-opn-rsrcs-{section}")]
                  )
                  break
            keyboard.append(
              [
                IKButton(
                  g_lang.back_text[user["language"]], callback_data=f"s_menu-opn"
                )
              ]
            )

            if len(keyboard) == 1:
              g_fun.show_menu(
                query, keyboard, stu_lang.opn_resources(user["language"], "no_section")
              )
            else:
              g_fun.show_menu(
                query,
                keyboard,
                stu_lang.opn_resources(user["language"], "text_section"),
              )
          else:
            for resource in sorted(cfg.resources[section]):
              if not student_resources[section][resource]:
                resource_name = db.activities.find_one({"_id": resource})["name"]

                keyboard.append(
                  [
                    IKButton(
                      resource_name,
                      callback_data=f"s_menu-opn-rsrcs-{section}-{resource}",
                    )
                  ]
                )
            keyboard.append(
              [
                IKButton(
                  g_lang.back_text[user["language"]], callback_data=f"s_menu-opn"
                )
              ]
            )
            g_fun.show_menu(
              query, keyboard, stu_lang.opn_resources(user["language"], "text_rsrc")
            )
        else:
          resource_name = db.activities.find_one({"_id": resource})["name"]
          g_fun.show_menu(
            query,
            g_lang.scale_7(user["language"], query.data),
            stu_lang.opn_resources(user["language"], "scale", resource_name),
          )

      else:
        db.opn_resources.update_one(
          {"_id": user["_id"]}, {"$set": {f"{section}.{resource}": value}}
        )

        opn_rsrcs(context, query, user, selections[:-3])
    except:
      g_fun.print_except(inspect.stack()[0][3], user, selections)

  def opn_tea_meetings(self, context, query, selections):
    try:
      if db.opn_teacher_meetings.find_one():
        meeting = value = ""
        if len(selections) > 4:
          meeting = selections[4]
          if len(selections) > 5:
            value = selections[5]

        keyboard = []
        if not value:
          if not meeting:
            meetings = db.opn_teacher_meetings.find().distinct("_id")
            for meeting in meetings:
              meeting_data = meeting.split("_")
              meeting_num = meeting_data[1]
              if (
                user["_id"]
                not in db.opn_teacher_meetings.find_one({"_id": meeting})["students"]
              ):
                keyboard.append(
                  [
                    IKButton(
                      f"Meeting {meeting_num}",
                      callback_data=f"s_menu-opn-tp-vc-{meeting}",
                    )
                  ]
                )
            keyboard.append(
              [
                IKButton(
                  g_lang.back_text[user["language"]], callback_data=f"s_menu-opn"
                )
              ]
            )
            if len(keyboard) == 1:
              g_fun.show_menu(
                query,
                keyboard,
                stu_lang.opn_tea_meet(user["language"], "all_meetings_evaluated"),
              )
            else:
              g_fun.show_menu(
                query, keyboard, stu_lang.opn_tea_meet(user["language"], "text_meeting")
              )
          else:
            meeting_data = meeting.split("_")
            meeting_num = meeting_data[1]
            g_fun.show_menu(
              query,
              g_lang.scale_7(user["language"], query.data),
              stu_lang.opn_tea_meet(user["language"], "scale", meeting_num),
            )
        else:
          db.opn_teacher_meetings.update_one(
            {"_id": meeting}, {"$push": {"students": user["_id"], "values": value}}
          )
          opn_tea_meetings(context, query, user, selections[:-3])
      else:
        g_fun.show_menu(
          query, keyboard, stu_lang.opn_tea_meet(user["language"], "no_meetings")
        )

    except:
      g_fun.print_except(inspect.stack()[0][3], user, selections)

  def suggestion(self, update, context):
    try:
      if context.args:

        message = " ".join(context.args)
        email = cfg.registered_emails[self._id]
        today = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        sql = f"INSERT INTO suggestions VALUES({self._id}, '{email}', '{today}', '{message}')"
        sqlite.execute_sql(sql)
        text = s_lang.suggestion(self.language, "save")
        context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
      else:
        text = s_lang.suggestion(self.language, "empty")
        context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)

    except:
      error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
      g_fun.print_except(error_path)
      return False

  def check_email(self, update, context):
    try:
      if not self.register_student():
        if len(context.args) == 1:
          email = context.args[0].lower()
          if re.match(
            "^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$", email.lower()
          ):
            sql = f"SELECT COUNT(*) FROM registered_students WHERE email='{email}'"
            if sqlite.execute_sql(sql, "fetchone")[0]:
              # Tenia registration como accion
              text = s_lang.check_email(self.language, "exists_email")
              context.bot.sendMessage(
                chat_id=self._id, parse_mode="HTML", text=text
              )
              return True
            else:
              sql = f"SELECT * FROM students_file WHERE email='{email}'"
              student = sqlite.execute_sql(sql, fetch="fetchone", as_dict=True)
              if student:
                student = dict(student)
                values = f"{self._id}, '{student['last_name']}, {student['first_name']}', '{email}', '{self.username}','{student['planet']}'"
                sql = f"INSERT INTO registered_students VALUES({values})"
                sqlite.execute_sql(sql)
                cfg.registered_emails[self._id] = email
                if student["planet"]:
                  cfg.active_meetings.update(
                    {student["planet"]: {"users": {}, "meeting": ""}}
                  )
                text = s_lang.check_email(self.language, "success", email)
                context.bot.sendMessage(
                  chat_id=self._id, parse_mode="HTML", text=text
                )
                text = s_lang.welcome(self.language, context, "long")
                context.bot.sendMessage(
                  chat_id=self._id, parse_mode="HTML", text=text
                )
                # cfg.registered_students.add(self["_id"])
                # cfg.registered_stu_emails.add(self["email"])
                return True

              else:
                text = s_lang.check_email(self.language, "not_found")
                context.bot.sendMessage(
                  chat_id=self._id, parse_mode="HTML", text=text
                )
          else:
            text = g_lang.email_syntax_error(self.language, email)
            context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
        elif len(context.args) < 1:
          text = s_lang.check_email(self.language, "no_args")
          context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
        else:
          text = s_lang.check_email(
            self.language, "many_args", " ".join(context.args)
          )
          context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
      else:
        sql = f"SELECT email FROM registered_students WHERE _id={self._id}"
        email_DB = sqlite.execute_sql(sql, "fetchone")
        if email_DB:
          text = s_lang.check_email(self.language, "registered_user", email_DB[0])
          context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
    except:
      error_path = f'{inspect.stack()[0][1]} - {inspect.stack()[0][3]}'
      g_fun.print_except(error_path)
      return False

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
  def __init__(self, user_data, planet):
    self.is_teacher = 1
    super().__init__(user_data, planet)

  def received_message(self, update, context):
    def is_configuration_file(doc):
      try:
        if doc.file_name == "grades_format.csv":
          return "grades"
        elif doc.file_name in cfg.list_config_files:
          sql_stu = f"SELECT count(*) FROM students_file"
          sql_act = f"SELECT count(*) FROM activities"
          if (
            doc.file_name == "students_format.csv"
            and sqlite.execute_sql(sql_stu, "fetchone")[0]
          ) or (
            doc.file_name == "activities_format.csv"
            and sqlite.execute_sql(sql_act, "fetchone")[0]
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
          self.reg_messages(update)
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
                df_grades = pd.read_csv(urlopen(f_path), encoding="UTF-8-sig")
                df_grades = b_fun.data_preparation(df_grades, "grades")
                thread_grades = threading.Thread(
                  target=b_fun.thread_grade_activities,
                  args=(
                    update,
                    context,
                    df_grades,
                    self,
                  ),
                )
                thread_grades.start()
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

  def main_menu(self, update, context):
    try:
      text, options = t_lang.main_menu(self.language)
      keyboard = options
      reply_markup = IKMarkup(keyboard)
      update.message.reply_text(
        parse_mode="HTML",
        text=text,
        reply_markup=reply_markup,
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
        activities = sqlite.table_DB_to_df("activities")
        title = t_lang.title_file(self.language, "ALL ACTIVITIES")
      elif option == "qualifying":
        file = "files/download/qualifying_activities"
        sql = f"SELECT * FROM activities WHERE weight>0"
        activities = sqlite.execute_sql(sql, df=True)
        title = t_lang.title_file(self.language, "QUALIFYING ACTIVITIES")
      elif option == "resources":
        file = "files/download/resources_activities"
        sql = f"SELECT * FROM activities WHERE name<>''"
        activities = sqlite.execute_sql(sql, df=True)
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
        if sqlite.execute_sql(sql, fetch="fetchone")[0]:
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
            thread_grades = threading.Thread(
              target=b_fun.thread_grade_activities,
              args=(
                update,
                context,
                df_grades,
                self,
              ),
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
        students = sqlite.table_DB_to_df("students_file")
        title = t_lang.title_file(self.language, "STUDENTS_FORMAT")
      elif option == "reg":
        file = "files/download/registered_students"
        students = sqlite.table_DB_to_df("registered_students")
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
        sql = f"SELECT * FROM grades"
        title = t_lang.title_file(self.language, "GRADE REPORT")
      elif report_type == "ARF":
        sql = f"SELECT * FROM academic_risk_factor"
        title = t_lang.title_file(self.language, "ACADEMIC RISK FACTOR REPORT")
      elif report_type == "meetings":
        sql = f"SELECT * FROM meetings"
        title = t_lang.title_file(self.language, "MEETINGS PARTICIPATION REPORT")
      elif report_type == "eva_teacher":
        sql = f"SELECT * FROM eva_teacher"
        title = t_lang.title_file(self.language, "TEACHER EVALUATION REPORT")
      elif report_type == "eva_resources":
        sql = f"SELECT * FROM eva_resources"
        title = t_lang.title_file(self.language, "RESOURCES EVALUATION REPORT")
      elif report_type == "eva_p2p_in_meet":
        sql = f"SELECT * FROM eva_p2p_in_meet"
        title = t_lang.title_file(
          self.language, "CLASSMATES EVALUATION\nREPORT IN MEETINGS"
        )
      elif report_type == "eva_p2p_out_meet":
        sql = f"SELECT * FROM eva_p2p_out_meet"
        title = t_lang.title_file(
          self.language, "CLASSMATES EVALUATION\nREPORT OUT MEETINGS"
        )

      elements = sqlite.execute_sql(sql, df=True)
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

  def activate_eva(self, update, context):
    try:
      chat_id = update.callback_query.message.chat_id
      flag = 0
      if chat_id > 0:
        flag = 1 if cfg.subject_data["activate_evaluations"] == 0 else 0
        sql = f"UPDATE subject_data SET activate_evaluations={flag}"
        sqlite.execute_sql(sql)
        cfg.subject_data["activate_evaluations"] = 0
        text = t_lang.menu_activate_eva(self.language, flag)
        context.bot.sendMessage(chat_id=self._id, parse_mode="HTML", text=text)
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
      Planet: {self.planet}
    ==============================="""
