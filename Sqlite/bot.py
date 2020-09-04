import logging
import inspect
import os
import sys
import telegram
from time import time
from telegram.ext import (
  Updater,
  CommandHandler as Cmd_Hdl,
  MessageHandler as Msg_Hdl,
  CallbackQueryHandler as CQ_Hdl,
  CallbackContext,
  Filters,
)
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from text_language import general_lang as g_lang
from functions import (
  general_functions as g_fun,
  commands as cmd,
  bot_functions as b_fun,
  jobs_queue,
)


# Configurar logging
logging.basicConfig(
  format="%(asctime)s - %(levelname)s: %(message)s", level=logging.INFO
)

# Obtener el Token y el Modo de trabajo
TOKEN = os.getenv("TOKEN")
mode = os.getenv("MODE")

if not TOKEN or not mode:
  env_var = "TOKEN" if not TOKEN else "MODE"
  sys.exit(logging.info(g_lang.not_env_variable(env_var)))

if mode == "dev":

  def run(updater):
    updater.start_polling()
    logging.info("Bot cargado")
    updater.idle()  # Permite finalizar el bot con Ctrl + C


elif mode == "prod":

  def run(updater):
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")
    logging.info("Bot cargado")


def main():
  try:
    # Bot's conecction
    my_bot = telegram.Bot(token=TOKEN)
    if not my_bot.getMyCommands():
      my_bot.setMyCommands(
        [
          ("start", "Iniciar"),
          ("help", "ayuda"),
          ("change_language", "Cambio de Idioma"),
          ("menu", "Menu de usuario"),
        ]
      )

    # Connection to the DB
    sqlite.connection()

    # Prepare the configuration of the course
    g_fun.config_subject()

    # Link the updater to the bot's Token
    updater = Updater(my_bot.token, use_context=True)

    # JobQueue creation
    bot_jobs = updater.job_queue
    jobs_queue.start_job(bot_jobs)

    # Dispatcher creation
    dp = updater.dispatcher

    # Handlers bot creation
    dp.add_handler(Cmd_Hdl("start", cmd.start))
    dp.add_handler(Cmd_Hdl("change_language", cmd.change_language))
    dp.add_handler(Cmd_Hdl("check_email", cmd.check_email))
    dp.add_handler(Cmd_Hdl("menu", cmd.menu))

    ## Handlers Options Menu
    dp.add_handler(CQ_Hdl(b_fun.options_menu))

    ## Handler who receives messages
    dp.add_handler(
      Msg_Hdl((~Filters.command) & (~Filters.status_update), b_fun.received_message)
    )

    ## Handler Teacher Menu
    dp.add_handler(Cmd_Hdl("grade_activity", cmd.grade_activity))
    run(updater)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


def test():

  ### NO BORRAR HASTA COPIAR A GET week
  from datetime import datetime, timedelta

  def get_weekday_monday(date):
    day = date.strftime("%A")
    if day != "Monday":
      for i in range(1, 8):
        monday_date = date - timedelta(days=i)
        day = monday_date.strftime("%A")
        if day == "Monday":
          return monday_date
    else:
      return date

  today = datetime.today()
  start_date = datetime.strptime(today, "%d/%m/%Y")
  start_monday_date = get_weekday_monday(start_date)
  print(start_monday_date)

  today = datetime.now() + timedelta(days=5)

  difference = today - start_monday_date
  num_week = int(difference.days / 7) + 1

  if num_week > int(cfg.subject_data["num_weeks"]):
    num_week = int(cfg.subject_data["num_weeks"])
  action = "text"
  if not action:
    return num_week
  else:
    text_week = "week_"
    if len(cfg.subject_data["num_weeks"]) != len(str(num_week)):
      text_week += "0" * (len(cfg.subject_data["num_weeks"]) - len(str(num_week)))
    text_week += str(num_week)
    print(text_week)
    return text_week

  """ start = time()
  sql_stu = "SELECT email FROM students_file"
  students = [stu[0] for stu in sqlite.execute_statement(sql_stu, "fetchall")]
  print("\n\n========================\n", students)
  sql_time_1 = time() - start """


if __name__ == "__main__":
  # test()
  #  input("")
  main()
