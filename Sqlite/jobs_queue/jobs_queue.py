# from datetime import time, datetime
import telegram.ext
import datetime
from time import localtime


def callback_hour(context):
  context.bot.sendMessage(chat_id=970331050, text=f"Mensaje de cada Hora")


def callback_2_hour(context):
  context.bot.sendMessage(chat_id=970331050, text=f"2 Horas")


def callback_morning(context):
  context.bot.sendMessage(chat_id=970331050, text=f"Buenos días")


def callback_afternoon(context):
  context.bot.sendMessage(chat_id=970331050, text=f"TARRRRRDEEEESSS")


# def send_mesage(context: Cb_context):
def start_job(bot_jobs):
  job_hour = bot_jobs.run_repeating(callback_hour, interval=600, first=0)
  job_2_hour = bot_jobs.run_repeating(callback_2_hour, interval=1200, first=0)
  target_tzinfo = datetime.timezone(datetime.timedelta(hours=-5))
  target_time = datetime.time(hour=10).replace(tzinfo=target_tzinfo)
  job_morning = bot_jobs.run_daily(
    callback_morning, target_time, days=(0, 1, 2, 3, 4, 5, 6,)
  )
  target_time = datetime.time(hour=15).replace(tzinfo=target_tzinfo)
  job_afternoon = bot_jobs.run_daily(
    callback_afternoon, target_time, days=(0, 1, 2, 3, 4, 5, 6)
  )

  print("HORA", job_hour.next_t)
  print("HORA_2", job_2_hour.next_t)
  print("MAÑANA", job_morning.next_t)
  print("TARDE", job_afternoon.next_t)
