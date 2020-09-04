from telegram import InlineKeyboardButton as IKButton


def not_env_variable(var):
  return f"Environment variable {var} is not set. The boot was not initialized."


def set_language(user, opt="opt"):
  if opt == "opt":
    return [
      [
        IKButton("ES", callback_data="welcome-es"),
        IKButton("EN", callback_data="welcome-en"),
      ]
    ]
  else:
    return f"<b>{user['first_name']}</b>!!\n\nPara cambiar el idioma del contenido, usa el botón ES-español o EN-inglés.\n\nTo switch content language, press the ES-Spanish or EN-English button."


def welcome(user):
  if user.language == "es":
    return f"Hola {user.telegram_name}, yo soy tu bot."
  else:
    return f"Hello {user.telegram_name}, I am your bot."


def file_ready_for_download(lang):
  if lang == "es":
    return "Archivo listo para su descarga."
  else:
    return "File ready for download."


def error_upload_file(lang, file=""):
  if lang == "es":
    return f"Hubo un error al subir el archivo {file}\nPor favor reviselo e inténtalo de nuevo."
  else:
    return (
      f"There was an error uploading the file {file}\nPlease check it and try again."
    )


def ok_upload_file(lang, file=""):
  if lang == "es":
    return f"El archivo {file} se subio correctamente."
  else:
    return f"The file {file} was uploaded correctly"


def email_syntax_error(lang, email):
  if lang == "es":
    return f'El email "{email}" no tiene la sintaxis correcta, asegurate de haberlo escrito correctamente.'
  else:
    return f'The email "{email}" does not have the correct syntax, make sure you typed it correctly.'


def wrong_command_group(lang, context):
  bot_username = context.bot.username
  if lang == "es":
    return f"Lo siento este comando no tiene ninguna función en el Grupo. Hablame en chat privado. @{bot_username}"

  else:
    return (
      f"Sorry this command has no function in the Group. Talk to me on a private chat. @{bot_username}",
    )


def wrong_num_arguments(lang, context):
  if lang == "es":
    return "La cantidad de argumentos para el comando es incorrecta.\n"
  else:
    return "The number of arguments for the command is incorrect.\n"


def file_not_created(lang):
  if lang == "es":
    return "Lo siento el archivo no pudo ser creado."
  else:
    return "I'm sorry the file couldn't be created."


def linguistic_arf(lang, arf_text):
  if lang == "es":
    if arf_text == "irrecoverable":
      return "Irrecuperable"
    if arf_text == "very_critical":
      return "Muy Crítico"
    if arf_text == "critical":
      return "Crítico"
    if arf_text == "moderate":
      return "Moderado"
    if arf_text == "low":
      return "Bajo"
    if arf_text == "none":
      return "Ninguno"
  else:
    return arf_text.replace("_", " ").capitalize()
