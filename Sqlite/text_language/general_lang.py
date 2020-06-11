def not_env_variable(var):
  return f"Environment variable {var} is not set. The boot was not initialized."


def welcome(user):
  if user.lang == "es":
    return f"Hola {user.telegram_name}, yo soy tu bot."
  else:
    return f"Hello {user.telegram_name}, I am your bot."
