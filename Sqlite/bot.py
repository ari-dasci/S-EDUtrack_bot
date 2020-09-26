import inspect
import logging
import os
import sys
from time import time

import telegram

# from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler as CQ_Hdl
from telegram.ext import CommandHandler as Cmd_Hdl
from telegram.ext import Filters
from telegram.ext import MessageHandler as Msg_Hdl
from telegram.ext import Updater


import config.db_sqlite_connection as sqlite
from functions import bot_functions as b_fun
from functions import commands as cmd
from functions import general_functions as g_fun
from functions import jobs_queue
from text_language import general_lang as g_lang

# Configurar logging
logging.basicConfig(
  format="%(asctime)s - %(levelname)s: %(message)s", level=logging.INFO
)

# Get the token and the working mode
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
    jobs_queue.start_jobs(bot_jobs)

    # Dispatcher creation
    dp = updater.dispatcher

    # General Handlers
    dp.add_handler(Cmd_Hdl("start", cmd.start))
    dp.add_handler(Cmd_Hdl("change_language", cmd.change_language))
    dp.add_handler(Cmd_Hdl("menu", cmd.menu))
    dp.add_handler(Cmd_Hdl("help", cmd.help))

    ## Handlers Options Menu
    dp.add_handler(CQ_Hdl(b_fun.options_menu))

    ## Handler receiving messages
    dp.add_handler(
      Msg_Hdl((~Filters.command) & (~Filters.status_update), b_fun.received_message)
    )
    dp.add_handler(Msg_Hdl(Filters.status_update, b_fun.status_update))

    ## Handlers Teacher
    dp.add_handler(Cmd_Hdl("grade_activity", cmd.grade_activity))
    dp.add_handler(Cmd_Hdl("add_teacher", cmd.add_teacher))
    dp.add_handler(Cmd_Hdl("start_meeting", cmd.set_meeting))
    dp.add_handler(Cmd_Hdl("end_meeting", cmd.set_meeting))
    dp.add_handler(Cmd_Hdl("modify_student", cmd.modify_student))

    ## Handlers Students
    dp.add_handler(Cmd_Hdl("check_email", cmd.check_email))
    dp.add_handler(Cmd_Hdl("suggestion", cmd.suggestion))

    # Start to receive updates
    run(updater)
  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)
    return False


def test():
  import config.config_file as cfg
  from datetime import datetime
  from functions.jobs_queue import calculate_weekly_grades as calc

  start_date = cfg.subject_data["start_date"]
  start_date = datetime.strptime(start_date, "%d/%m/%Y")
  cfg.monday_start_week = g_fun.get_weekday_monday(start_date)
  cfg.config_files_set = True
  calc("")

  input("PRESIONA UNA TECLA PARA CONTIUAR")


if __name__ == "__main__":
  # test()
  main()
