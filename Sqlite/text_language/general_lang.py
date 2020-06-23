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


def error_upload_file(language, file=""):
  if language == "es":
    return f"Hubo un error al subir el archivo {file}. Por favor inténtalo de nuevo."
  else:
    return f"There was an error uploading the file {file}. Please try again."


def email_syntax_error(language, email):
  if language == "es":
    return f'El email "{email}" no tiene la sintaxis correcta, asegurate de haberlo escrito correctamente.'
  else:
    return f'The email "{email}" does not have the correct syntax, make sure you typed it correctly.'
