from telegram  import (InlineKeyboardButton as IKButton)
from EDUtrack import my_bot

language_opt = [
  [IKButton("ES",callback_data='welcome-ES'),
  IKButton("EN",callback_data='welcome-EN')]
  ]

def choice_language_text (first_name):
  return f'¡¡Hola <b>{first_name}</b>!! selecciona el botón "ES" para ver el contenido en Español.\n\nHi <b>{first_name}</b>!! select the "EN" button to view the content in English.'

not_config_files_set_text = {
  "ES": f"<b>EDUtrack {my_bot.username}</b> aún no se ha terminado de configurar. Espera instrucciones del docente.",
  "EN": f"<b>EDUtrack {my_bot.username}</b> has not yet finished configuring . Wait for instructions from the teacher."
}



if __name__ == '__main__':
    pass