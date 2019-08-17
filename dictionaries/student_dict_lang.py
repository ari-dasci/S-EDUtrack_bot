from telegram  import (InlineKeyboardButton as IKButton)

def welcome_text(context, language):
  bot_username = context.bot.username
  if language == "ES":
    return
    f'Bienvenido al asistente EDUtrack <b>{bot_username}</b>, te acompañare durante el curso para que puedas opinar/evaluar sobre algunos elementos claves en tu aprendizaje.\n\nEscribe el símbolo <b>" / "</b> y te mostrare los comandos que puedes utilizar para que trabajemos juntos. Aquí tienes una breve explicación de cada uno.\n\n/actions\nTe mostraré el menú con las opciones que puedes realizar conmigo.\n\n/change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n/help\nTe mostraré los comandos que puedes utilizar y la descripción de cada apartado del menú. También podrás acceder al manual de usuario.'
  else:
    return 
    f'Welcome to the EDUtrack assistant{bot_username}. I will accompany you during the course so that you can give your opinion/evaluate some key elements in your learning.\nWrite the symbol <b> "/" </b> and I will show you the commands you can use to work together. Here'+"'s a brief explanation of each one.\n\n/actions\nI'll show you the menu with the options we can work with.\n\n/change_language\nI will help you change the language in which I show you the contents. The current options are English and Spanish.\n\n/help\nI'll show you the commands you can use and the description of each menu item. You will also be able to access the user manual."


def not_config_files_set_text (context, language):
  bot_name = context.bot.first_name
  if language == "ES":
    return f"<b>EDUtrack {bot_name}</b> aún no se ha terminado de configurar. Espera instrucciones del docente."
  else:
    return f"<b>EDUtrack {bot_name}</b> has not yet finished configuring. Wait for instructions from the teacher."


check_email_registration_text = {
  "ES" : f"*Verificación por email:*\nPara verificar que eres estudiante de esta asignatura y registrar tu usario de Telegram en la base de datos escribe el comando:\n\n/check`_`email <Tu email PRADO>\n\nSi no lo sabes o no lo recuerdas, contacta a tu docente.\n\n*Ejemplo*:\n/check`_`email nombre@correo.ugr.es",
  
  "EN" : f"*Email verification:*\nTo verify that you are a student of this subject and register your Telegram user in the database, type the command:\n\n/check`_`email <your email PRADO>\n\nIf you don't know it or don't remember it, contact your teacher.\n\n*Example*:\n/check`_`email nombre@correo.ugr.es"
}


check_email_no_args_text = {
  "ES" : "Debes escribir tu correo después del comando.\n\n<b>Ejemplo</b>:\n/check_email nombre@correo.ugr.es",
  "EN" : "You must write your email after the command.\n\n<b>Example</b>:\n/check_email name@correo.ugr.es"
}


def check_email_many_args_text (email, language):
  if language == "ES":
    return f'"{email}" no es un email correcto, no debe llevar espacios.\n\n<b>Ejemplo:</b>\n/check_email nombre@correo.ugr.espacios'
  else: 
    return f'"{email}" is not a correct email, it must not contain spaces.\n\n<b>Example:</b>\n/check_email name@correo.ugr.es'


def email_not_found_text (email, language):
  if language == "ES":
    return f"El email <b>{email}</b> no se encuentra en la base de datos. Por favor revisa si lo escribiste correctamente o comunícate con tu docente."
  else:
    return f"The email <b>{email}</b> is not in the database. Please check if you typed it correctly or contact your teacher."


def email_is_registered_text(email, language):
  if language == "ES":
    return f'Ya tengo registrado el email "{email}" en mi base de datos. No es necesario registrarlo de nuevo.'
  else:
    return f'I have already registered the email "{email}" in my database. It is not necessary to register it again.'


## WARNINGS
no_username_text = {
  "ES" : "Me di cuenta que no tienes un username/alias registrado en tu cuenta de Telegram. Para utilizar EDUtrack debes configurar un username/alias. Ve a ajustes en tu cuenta de Telegram y edita tu perfil para asignar un username/alias.",
  "EN" : "I noticed that you don't have a username registered in your Telegram account. To use EDUtrack you must set up a username. Go to settings in your Telegram account and edit your profile to assign a username."
}








if __name__ == '__main__':
    pass