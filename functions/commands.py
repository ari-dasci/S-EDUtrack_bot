""" from configuration.DB_connection import db, client
import functions.general_functions as gen_fun
import functions.teacher_commands as tea_cmd
import functions.student_commands as stu_cmd
is_config_files_set = True if (db.students.find_one() and db.activities.find_one()) else False """

def start(update, context, pass_chat_data=True):
  """ Inicializa el bot y saluda."""
  print("START:", context)
  user_first_name = update.message.from_user.first_name
  print(user_first_name)
  chat_id = update.message.chat_id
  context.bot.send_message(
    chat_id = chat_id,
    text = f"Hola {user_first_name}. Soy tu asistente EDUtrack."
  )
  


if __name__ == '__main__':
    pass