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
    dp.add_handler(Cmd_Hdl("start", cmd.start))
    dp.add_handler(CQ_Hdl(cmd.press_button))
    dp.add_handler(Msg_Hdl(
        (~Filters.command) & (~Filters.status_update),
        g_fun.received_message))
    dp.add_handler(Cmd_Hdl('check_email',cmd.check_email))
    dp.add_handler(Cmd_Hdl("change_language", cmd.change_language))
    dp.add_handler(Cmd_Hdl("menu",cmd.menu))
    dp.add_handler(Cmd_Hdl("grade_students",cmd.grade_students,pass_args=True))
    dp.add_handler(Conv_Hdl(
      entry_points = [Cmd_Hdl('add_activity',add_activity,pass_user_data=True),
                      Cmd_Hdl('add_student', add_student, pass_user_data=True)],

      states={
        NAME: [
          Msg_Hdl(Filters.text, add_activity_name, pass_user_data=True)],
        SECTION: [
          Msg_Hdl(Filters.text, add_activity_section, pass_user_data=True)],
        WEEK: [
          Msg_Hdl(Filters.text, add_activity_week, pass_user_data=True)],
        WEIGHT: [
          Msg_Hdl(Filters.text ,add_activity_weight, pass_user_data=True)],
        SAVE: [
          Msg_Hdl(Filters.text, add_activity_save, pass_user_data=True)],
        
        
        
        STUDENT_NAME: [
          Msg_Hdl(Filters.text, add_student_name, pass_user_data=True)]
      },
      fallbacks=[
        Cmd_Hdl('cancel',cancel)]
    ))

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