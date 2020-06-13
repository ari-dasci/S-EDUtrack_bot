def welcome_text(lang, context):
  bot_username = context.bot.username
  if lang == "ES":
    return f"Bienvenido a EDUtrack <b>{bot_username}</b>, te acompañare durante el curso para hacerte más participe en la asignatura.\n\nEscribe el símbolo <b>'/'</b> y te mostrare los comandos que puedes utilizar para que trabajemos juntos. Aquí tienes una breve explicación de cada uno.\n\n/menu\nTe mostraré el menú con las conversaciones activas.\n\n/change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n/help\nPodrás descargar el manual de usuario."
    # Te mostraré los comandos que puedes utilizar y la descripción de cada apartado del menú. También podrás acceder al manual de usuario.'

  else:
    return f"Welcome to EDUtrack {bot_username}. I will guide you during the semester so that you can be more active in this course.\nType character <b> '/' </b> and I will show you the commands you can use to work together. Here's a brief explanation of each one.\n\n/menu\nI'll show you the menu with my active conversations.\n\n/change_language\nI will help you change the language in which I show you the contents. The current options are English and Spanish.\n\n/help\nYou can download the user manual."
    # I'll show you the commands you can use and the description of each menu item. You will also be able to access the user manual."


def not_config_files_set(language, context):
  bot_name = context.bot.first_name
  if language == "ES":
    return f"<b>EDUtrack {bot_name}</b> está en modo configuración y por ello aún no está activo. Espera instrucciones de tu profesor/a."
  else:
    return f"<b>EDUtrack {bot_name}</b> is in configuration mode and therefore is not active yet. Wait for instructions of your teacher."
