from telegram  import (InlineKeyboardButton as IKButton)


language_opt = [
  [IKButton("ES",callback_data='welcome-ES'),
  IKButton("EN",callback_data='welcome-EN')]
  ]

def choice_language_text (first_name):
  return f'¡¡Hola <b>{first_name}</b>!! selecciona el botón "ES" para ver el contenido en Español.\n\nHi <b>{first_name}</b>!! select the "EN" button to view the content in English.'




wrong_command_group = {
  "ES": "Lo siento este comando no tienen ninguna función en el Grupo.",
  "EN": "Sorry this command has no function in the Group.",
  "": "Lo siento este comando no tienen ninguna función en el Grupo.\nSorry this command has no function in the Group."
}


if __name__ == '__main__':
    pass