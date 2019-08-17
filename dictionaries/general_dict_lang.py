from telegram  import (InlineKeyboardButton as IKButton)


language_opt = [
  [IKButton("ES",callback_data='welcome-ES'),
  IKButton("EN",callback_data='welcome-EN')]
  ]

def choice_language_text (first_name):
  return f'<b>{first_name}</b>!!\n\nSelecciona el botón "ES" para ver el contenido en Español.\n\nSelect the "EN" button to view the content in English.'

wrong_command_group = {
  "ES": "Lo siento este comando no tienen ninguna función en el Grupo.",
  "EN": "Sorry this command has no function in the Group."
}

def email_syntax_error_text(language, email):
  if language == "ES":
    return f'El email "{email}" no tiene la sintaxis correcta, asegurate de haberlo escrito correctamente.\n\nEjemplo:\n/check_email nombre@correo.ugr.es'
  else:
    return f'The email "{email}"" does not have the correct syntax, make sure you typed it correctly.\n\nExample:\n/check_email nombre@correo.ugr.es'


# Estan al revés por el cambio de idioma
cmd_change_language_text={
  "ES": "I changed your language to <b>English.</b>",
  "EN": "He cambiado tu idioma a <b>Español.</b>"  
}






if __name__ == '__main__':
    pass