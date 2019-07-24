from telegram  import (InlineKeyboardButton as IKButton)

def welcome_text(context, language):
  print("LNAGUAGE",language)
  bot_username = context.bot.username
  print(context.bot)
  if language == "ES":
    return f"Bienvenido al asistente EDUtrack <b>{bot_username}</b>"
  else:
    return f"Welcome Teacher."

not_config_files_set_text = {
  "ES": "<b> A",
  "EN":""
}

def config_file_set_text (file_name, user):
  if user['language'] == "ES":
    file_name = 'estudiantes' if file_name == 'students' else 'actividades'
    return f"Aún no se ha subido el archivo de configuración de <b>{file_name}</b>. Recuerda que lo debes subir con el mismo nombre",
  else:
    
     f"The <b>{file_name}</b> configuration file has not yet been uploaded. Remember to upload it with the same name"


activities_file_set_text = {
  "ES": "Aún no se ha subido el archivo de configuración de actividades. Recuerda que lo debes subir con el mismo nombre",
  "EN": "The student configuration file has not yet been uploaded. Remember to upload it with the same name"
}

download_config_files_text = {
  "ES": "<b>Asistente para la configuración de la asignatura</b>.\n\nDescarga y edita los siguientes archivos. Cuando los tengas listos enviámelos (súbelos) con el mismo nombre para guardarlos en la base de datos.",
  "EN": "<b>Assistant for the configuration of the subject </b>.\nDownload and edit the following files. When you have them ready, upload them with the same name to save them in the database."

}
