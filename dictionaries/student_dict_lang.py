from telegram  import (InlineKeyboardButton as IKButton)

def welcome_text(context, language):
  bot_username = context.bot.username
  if language == "ES":
    return f'Bienvenido al asistente  EDUtrack <b>{bot_username}</b>, te acompañare durante el curso para que puedas opinar/evaluar sobre algunos elementos claves en tu aprendizaje.\n\nEscribe el símbolo<b> " / " </b>y te mostrare los comandos que puedes utilizar para que trabajemos juntos. Aquí tienes una breve explicación de cada uno.\n\n\
      /actions\nTe mostraré el menú con las opciones que puedes realizar conmigo.\n\n\
      /change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n\
      /help\nTe mostraré los comandos que puedes utilizar y la descripción de cada apartado del menú. También podrás acceder al manual de usuario.'
  else:
    return f'Welcome to the EDUtrack assistant {bot_username}. I will accompany you during the course so that you can give your opinion/evaluate some key elements in your learning.\n Write the symbol <b> "/" </b> and I will show you the commands you can use to work together. Here'+"'s a brief explanation of each one.\n\n\
      /actions\n I'll show you the menu with the options we can work with.\n\n\
      /change_languageI will help you change the language in which I show you the contents. The current options are English and Spanish.\n\n\
      /help\nI'll show you the commands you can use and the description of each menu item. You will also be able to access the user manual."

def not_config_files_set_text (context, language):
  bot_username = context.bot.username
  if language == "ES":
    return f"<b>EDUtrack {bot_username}</b> aún no se ha terminado de configurar. Espera instrucciones del docente."
  else:
    return f"<b>EDUtrack {bot_username}</b> has not yet finished configuring . Wait for instructions from the teacher."



if __name__ == '__main__':
    pass