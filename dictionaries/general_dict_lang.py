from telegram  import (InlineKeyboardButton as IKButton)

autoevaluation_questions_text = {
  "ES": {
    "Q1" : "1.- ¿Tienes un plan de estudio/trabajo habilitado para esta asignatura?",
    "Q2" : "2.- En caso de tener un plan de estudios/trabajo\n¿Lo sigues con constancia?",
    "Q3" : "3.- ¿Esta asignatura te frustra?",
    "Q4" : "4.- ¿Estudias con responsabilidad en esta asignatura?",
    "Q5" : "5.- En todos los temas se ha dado bibliografía asociada. ¿Realizas una lectura comprensiva de dichos textos?"    
  },

  "EN" : {
    "Q1" : "Do you have a study/work plan for this subject?",
    "Q2" : "2.-If you have a plan of study/work, do you follow it consistently?",
    "Q3" : "3.- Does this subject frustrate you?",
    "Q4" : "4.- Do you study responsibly in this subject?",
    "Q5" : "5.- Associated bibliography has been provided on all subjects. Do you make a comprehensive reading of these texts?"
  }
}

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

invalid_user ={
  'ES' : "No tienes permiso para realizar esta acción.",
  'EN' : "You don't have permission to perform this action."
}

def email_syntax_error_text(language, email):
  if language == "ES":
    return f'El email "{email}" no tiene la sintaxis correcta, asegurate de haberlo escrito correctamente.'
  else:
    return f'The email "{email}"" does not have the correct syntax, make sure you typed it correctly.'


# Estan al revés por el cambio de idioma
cmd_change_language_text={
  "ES": "I changed your language to <b>English.</b>",
  "EN": "He cambiado tu idioma a <b>Español.</b>"  
}



file_ready_for_download ={
  'ES' : "Archivo listo para su descarga.",
  'EN' : "File ready for download."
}

files_ready_for_download ={
  'ES' : "Archivos listos para su descarga.",
  'EN' : "Files ready for download."
}


if __name__ == '__main__':
    pass