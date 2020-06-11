import logging
import inspect
import os
import sys
import telegram
from telegram.ext import (
  Updater,
  CommandHandler,
  MessageHandler,
  Filters,
  CallbackContext,
  CallbackQueryHandler,
)
from classes import User
import config.config_file as cfg
import config.db_sqlite_connection as sqlite
from text_language import general_lang as g_lang
from functions import general_functions as g_fun, commands as cmd
import functions.general_functions as g_fun
import jobs_queue.jobs_queue as jobs_queue


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

    # Connection to the DB
    sqlite.connection()

    # If they do not exist, the tables are created
    sql = 'SELECT count(*) FROM sqlite_master WHERE type = "table"'
    if not sqlite.execute_statement(sql, fetch="fetchone")[0]:
      sqlite.create_db()

    # Link the updater to the bot's Token
    updater = Updater(my_bot.token, use_context=True)

    # JobQueue creation
    bot_jobs = updater.job_queue

    jobs_queue.start_job(bot_jobs)

    # Dispatcher creation
    dp = updater.dispatcher

    # Handlers bot creation
    dp.add_handler(CommandHandler("start", cmd.start))
    dp.add_handler(CallbackQueryHandler(cmd.pressed_button))

    run(updater)

  except:
    error_path = f"{inspect.stack()[0][1]} - {inspect.stack()[0][3]}"
    g_fun.print_except(error_path)


if __name__ == "__main__":
  main()
