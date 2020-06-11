from telegram import InlineKeyboardButton as IKButton


def not_env_variable(var):
  return f"Environment variable {var} is not set. The boot was not initialized."


def set_language(user, opt="opt"):
  if opt == "opt":
    return [
      [
        IKButton("ES", callback_data="welcome-ES"),
        IKButton("EN", callback_data="welcome-EN"),
      ]
    ]
  else:
    return f"<b>{user['first_name']}</b>!!\n\nPara cambiar el idioma del contenido, usa el botón ES-español o EN-inglés.\n\nTo switch content language, press the ES-Spanish or EN-English button."


def welcome(user):
  if user.language == "es":
    return f"Hola {user.telegram_name}, yo soy tu bot."
  else:
    return f"Hello {user.telegram_name}, I am your bot."
