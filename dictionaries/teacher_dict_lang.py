from telegram  import (InlineKeyboardButton as IKButton)

def welcome_text(context, language):
  bot_username = context.bot.username
  if language == "ES":
    return f"Bienvenido al asistente EDUtrack <b>{bot_username}</b>"
  else:
    return f"Welcome to the assistant EDUtrack <b>{bot_username}</b>"


not_config_files_set_text = {
  "ES": "La asignatura aún no se ha configurado completamente.",
  "EN": "The subject has not yet been fully configured."
}

def config_file_set_text (file_name, language):
  if language == "ES":
    file_name = 'estudiantes' if file_name == 'students' else 'actividades'
    return f"El archivo de configuración <b>{file_name}</b> aún no se ha cargado. Recuerda que lo debes subir con el mismo nombre."
  else:
    return f"The <b>{file_name}</b> configuration file has not yet been uploaded. Remember to upload it with the same name."


download_config_files_text = {
  "ES": "<b>Asistente para la configuración de la asignatura.</b>\n\nAntes de usar EDUtrack debes terminar de configurar la asignatura. Descarga y edita los siguientes archivos. Cuando los tengas listos enviámelos (súbelos) con el mismo nombre para guardarlos en la base de datos.",
  "EN": "<b>Subject configuration wizard.</b>\n\nBefore using EDUtrack you must finish configuring the subject. Download and edit the following files. When you have them ready, upload them with the same name to save them in the database."
}

def config_files_set_exist_DB(file_name, language):
  if language == "ES":
    elements = 'estudiantes' if "students" in file_name else 'actividades'
    return f"<b>Ya existe el archivo:</b>\nEl apartado de <b>{elements}</b> ya existe en la base de datos.\nPara agregar más {elements} renombra el archivo como <b>add_{file_name}</b>.\n\nPara reemplazar todo, renombra el archivo como <b>replace_{file_name}</b>.\nSi utilizas está última opción, la sección de calificaciones también se borrará, eliminando todas las calificaciones cargadas previamente."
  else:
    elements = 'students' if "students" in file_name  else 'activities'
    return f"<b>The file already exists:</b>\nThe <b>{elements}</b> section already exists in the database.\nTo add more {elements} rename the file as <b>add_{file_name}</b>.\n\nTo replace everything, rename the file as <b>replace_{file_name}</b>.\nIf you use the latter option, the grades section will also be cleared, deleting all previously loaded grades."

config_files_ready_one_text = {
  "ES":"El archivo se ha cargado correctamente.",
  "EN": "The file is uploaded correctly."
}

config_files_ready_both_text = {
  "ES" : "Ya he cargado ambos archivos. Espera un momento para crear el apartado de calificaciones.",
  "EN" : "I've already uploaded both files. Wait a moment to create the grades section."
}

def add_elements_ready_text (language, elements):
  if language == "ES":
    elements = "los nuevos estudiantes." if elements == 'students' else "las nuevas activiades."
    return f"Se han agregado con éxito {elements}"
  else:
    return f"Successfully added {elements}"

def add_elements_all_exists_text (language, elements):
  if language == "ES":
    elements = "Todos los estudiantes." if elements == 'students' else "Todas las activiades."
    return f"{elements} ya existen en la base  de datos. No se agregó ningún elemento."
  else:
    return f"All {elements} already exist in the database. No item was added."

def add_elements_duplicates (language, elements):
  if language == "ES":
    elements = "Los siguientes estudiantes" if elements == 'students' else "Las siguientes activiades"
    return f"{elements} ya existen en la base de datos:\n"
  else:
    return f"The following {elements} already exist in the database:\n"

add_elements_no_duplicates ={
  'ES' : "\n\nLos demás elementos se agregaron correctamente.",
  'EN' : "\n\nThe other elements were added correctly."
}

grades_section_ready_text = {
  "ES" : "Hemos terminado de configurar la asignatura. Escribe el comando /menu para mostrarte el menú de acciones que puedes realizar. O escribe el comando /help para ver la ayuda de EDUtrack.",
  "EN" : "We've finished configuring the subject. Type the command /menu to show you the menu of actions you can do. Or type the /help command to see EDUtrack's help."
  }


def teacher_message_registration_error_text(language, user):
  if language == "ES":
    return f"Un usuario ha intentado usar el bot pero no esta registrado entre los estudiantes.\nID: {user['_id']}\nTelegram_name: {user['telegram_name']}\nNickname: {user['username']}"
    
  else:
    return f"The user has tried to use the bot but is not registered.\nID: {user['_id']}\nTelegram_name: {user['telegram_name']}\nNickname: {user['username']}"          