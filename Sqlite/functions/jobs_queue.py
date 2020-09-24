# from datetime import time, datetime
import inspect
import telegram.ext
import datetime
from time import localtime
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from user_types import Student
from functions import general_functions as g_fun


def weekly_arf(context):
  if cfg.config_files_set:
    if cfg.active_activities:
      user_data = {}

      df_students_data = sqlite.table_DB_to_df("telegram_users", index=True)

      for student in cfg.registered_stu:
        email = cfg.registered_stu[student]
        if cfg.registered_stu[student]:

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
    print("LISTOO", cfg.resources)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


# def send_mesage(context: Cb_context):
def start_jobs(bot_jobs):
  # Set the time zone
  target_tzinfo = datetime.timezone(datetime.timedelta(hours=+2))

  target_time = datetime.time(hour=20, minute=42).replace(tzinfo=target_tzinfo)
  job_weekly_arf = bot_jobs.run_daily(weekly_arf, target_time, days=(6,))

  target_time = datetime.time(hour=16, minute=19).replace(tzinfo=target_tzinfo)
  job_set_resources_week = bot_jobs.run_daily(
    set_resources_week, target_time, days=(2,)
  )

  # job_minute = bot_jobs.run_repeating(weekly_arf, interval=300, first=0,)


"""   target_time = datetime.time(hour=16).replace(tzinfo=target_tzinfo)
  job_afternoon = bot_jobs.run_daily(
    callback_afternoon, target_time, days=(6)
  )
  print("MAÑANA", job_morning.next_t)
  print("TARDE", job_afternoon.next_t)
 """

