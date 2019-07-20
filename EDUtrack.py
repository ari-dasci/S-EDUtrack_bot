import telegram
from telegram.ext import (
    Updater,
    CommandHandler as CmdHandler,
    CallbackQueryHandler as CQHandler)
import logging
from configuration.config_file import token_bot
from functions import (
    commands as cmd,
    general_functions as g_fun)

# Identificar el bot
my_bot = telegram.Bot(token = token_bot)

def main():
    """ Inicializa el bot.

        Se solicita la identificación del bot mediante el Token que proporciona BotFather.

        mi_bot => Token proporcionado por BotFather.
        updater => Recibe las actualizaciones del bot.
        dp => Despachador que administrar los manejadores.
        updater.start_polling() => Inicia la recepción de mensajes.
        updater.idle() => Permite finalizar el bot con Ctrl+C.

    """
    # Obtiene las actualizaciones de EDUtrack 
    updater = Updater(my_bot.token, use_context = True)

    # Despachador que registra los handlers
    dp = updater.dispatcher

    # Comandos
    dp.add_handler(CmdHandler("start", cmd.start))
    dp.add_handler(CQHandler(cmd.press_button))

    # Carga la configuración inicial
    g_fun.basic_setup()

    updater.start_polling()

    logging.basicConfig(
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO)
    print("Bot Cargado")
    # Bloquear para que se ejecute hasta que pulse Ctrl-C o error
    updater.idle()

if __name__ == '__main__':
    main()