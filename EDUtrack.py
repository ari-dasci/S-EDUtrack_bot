import telegram
from telegram.ext import (
    Updater,
    CommandHandler as CmdHandler,
    CallbackQueryHandler as CQHandler,
    MessageHandler as MsgHandler,
    Filters)
import logging
import configuration.config_file as cfg
from configuration.config_file import (
    token_bot)
from functions import (
    commands as cmd,
    general_functions as g_fun)


# if (db.students_file.find_one() and db.activities.find_one()) else False

def main():
    """ Inicializa el bot.

        Se solicita la identificación del bot mediante el Token que proporciona BotFather.

        mi_bot => Token proporcionado por BotFather.
        updater => Recibe las actualizaciones del bot.
        dp => Despachador que administrar los manejadores.
        updater.start_polling() => Inicia la recepción de mensajes.
        updater.idle() => Permite finalizar el bot con Ctrl+C.

    """
    # Identificar el bot
    my_bot = telegram.Bot(token = token_bot)
    # Obtiene las actualizaciones de EDUtrack 
    updater = Updater(my_bot.token, use_context = True)

    # Despachador que registra los handlers
    dp = updater.dispatcher

    # Comandos
    dp.add_handler(CmdHandler("start", cmd.start))
    dp.add_handler(CQHandler(cmd.press_button))
    dp.add_handler(MsgHandler(
        (~Filters.command) & (~Filters.status_update),
        g_fun.received_message))
    dp.add_handler(CmdHandler('check_email',cmd.check_email))
    dp.add_handler(CmdHandler("change_language", cmd.change_language))

    # Carga la configuración inicial
    g_fun.basic_setup()

    updater.start_polling()

    logging.basicConfig(
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO)
    print("Bot Cargado")
    updater.idle()

if __name__ == '__main__':
    main()