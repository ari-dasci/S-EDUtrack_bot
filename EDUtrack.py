import telegram
from telegram.ext import (
    Updater,
    CommandHandler as Cmd_Hdl,
    CallbackQueryHandler as CQ_Hdl,
    MessageHandler as Msg_Hdl,
    ConversationHandler as Conv_Hdl,
    Filters)
import logging
import configuration.config_file as cfg
from configuration.config_file import (
    token_bot)
from functions import (
    commands as cmd,
    general_functions as g_fun,
    teacher_functions as tea_fun)
from dictionaries import (
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang,
  general_dict_lang as g_lang
)


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
    dp.add_handler(Cmd_Hdl("start", cmd.start))
    dp.add_handler(Cmd_Hdl('check_email',cmd.check_email))
    dp.add_handler(Cmd_Hdl("change_language", cmd.change_language))
    dp.add_handler(Cmd_Hdl("menu",cmd.menu))
    dp.add_handler(Cmd_Hdl("grade_activity", tea_fun.grade_activity))
    dp.add_handler(CQ_Hdl(cmd.press_button))
    dp.add_handler(Msg_Hdl(
        (~Filters.command) & (~Filters.status_update),
        g_fun.received_message))
    
    
    

    # Carga la configuración inicial
    g_fun.basic_setup(my_bot)

    updater.start_polling()

    logging.basicConfig(
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.INFO)
    print("Bot Cargado")
    updater.idle()

if __name__ == '__main__':
    main()