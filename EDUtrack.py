import telegram
from telegram.ext import CommandHandler, Updater
import logging
from configuration.configuration_file import token_bot
from functions import commands as cmd

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
    mi_bot = telegram.Bot(token = token_bot)
    updater = Updater(mi_bot.token, use_context = True)

    # Despachador que registra los handlers
    dp = updater.dispatcher

    # Comandos
    dp.add_handler(CommandHandler("start", cmd.start))

    updater.start_polling()

    logging.basicConfig(
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO)
    print("Bot Cargado")
    # Bloquear para que se ejecute hasta que pulse Ctrl-C o error
    updater.idle()

if __name__ == '__main__':
    main()