# from datetime import time, datetime
import inspect
import telegram.ext
import datetime
import sys
import pandas as pd
from time import time, localtime, sleep
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from user_types import Student
from functions import general_functions as g_fun, bot_functions as b_fun
from tqdm import trange


def weekly_arf(context):
  if cfg.config_files_set:
    if cfg.active_activities:
      user_data = {}
      df_students_data = sqlite.table_DB_to_df("telegram_users", index=True)

      for student in cfg.registered_stu["_id"]:  # students.index:
        data = df_students_data.loc[student]
        user_data["id"] = data.name
        user_data["full_name"] = data.telegram_name
        user_data["username"] = data.username
        user_data["language_code"] = data.language
        user = Student(user_data, "")
        user.my_grade(context)


def set_resources_week(context):
  try:
    cfg.resources["week"] = g_fun.get_week("num")
    g_fun.get_resources()
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def calculate_weekly_grades(context):
  try:
    if cfg.config_files_set:
      sql = "SELECT DISTINCT email FROM students_file"
      students = sqlite.execute_sql(sql, fetch="fetchall", as_list=True)
      b_fun.get_risk_factor(students)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def start_jobs(bot_jobs):
  # Set the time zone
  target_tzinfo = datetime.timezone(datetime.timedelta(hours=+2))

  target_time = datetime.time(hour=12, minute=30).replace(tzinfo=target_tzinfo)
  job_weekly_arf = bot_jobs.run_daily(weekly_arf, target_time, days=(0, 4))

  target_time = datetime.time(hour=1, minute=30).replace(tzinfo=target_tzinfo)
  job_set_calculate_grades = bot_jobs.run_daily(
    calculate_weekly_grades, target_time, days=(0, 4, 5)
  )

  target_time = datetime.time(hour=2).replace(tzinfo=target_tzinfo)
  job_set_resources_week = bot_jobs.run_daily(
    set_resources_week, target_time, days=(0,)
  )

  # job_minute = bot_jobs.run_repeating(weekly_arf, interval=300, first=0)


"""   target_time = datetime.time(hour=16).replace(tzinfo=target_tzinfo)
  job_afternoon = bot_jobs.run_daily(
    callback_afternoon, target_time, days=(6)
  )
  print("MAÑANA", job_morning.next_t)
  print("TARDE", job_afternoon.next_t)
 """

