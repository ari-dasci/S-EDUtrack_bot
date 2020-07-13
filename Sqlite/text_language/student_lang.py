import config.config_file as cfg

lt = "&lt;"
gt = "&gt;"


def welcome(lang, context, action="short"):
  bot_username = context.bot.username
  if lang == "es":
    if action == "long":
      return f"Bienvenido a EDUtrack <b>{bot_username}</b>, te acompañare durante el curso para hacerte más participe en la asignatura.\n\nEscribe el símbolo <b>'/'</b> y te mostrare los comandos que puedes utilizar para que trabajemos juntos. Aquí tienes una breve explicación de cada uno.\n\n/menu\nTe mostraré el menú con las opciones activas que pordrás utilizar.\n\n/change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n/help\nPodrás descargar el manual de usuario."
      # Te mostraré los comandos que puedes utilizar y la descripción de cada apartado del menú. También podrás acceder al manual de usuario.'
    if action == "short":
      return "Escribe el comando /menu para ver las opciones."

  else:
    if action == "long":
      return f"Welcome to EDUtrack {bot_username}. I will guide you during the course so that you can be more active in this subject.\nType character <b> '/' </b> and I will show you the commands you can use to work together. Here's a brief explanation of each one.\n\n/menu\nI'll show you the menu with the active options you can use.\n\n/change_language\nI will help you change the language in which I show you the contents. The current options are English and Spanish.\n\n/help\nYou can download the user manual."
    if action == "short":
      return ("Type /menu command to see active conversations.",)

    # I'll show you the commands you can use and the description of each menu item. You will also be able to access the user manual."


def not_config_files_set(lang, context):
  bot_name = context.bot.first_name
  if lang == "es":
    return f"<b>EDUtrack {bot_name}</b> está en modo configuración y por ello aún no está activo. Espera instrucciones de tu profesor/a."
  else:
    return f"<b>EDUtrack {bot_name}</b> is in configuration mode and therefore is not active yet. Wait for instructions of your teacher."


def check_email(lang, action, email=""):
  if lang == "es":
    if action == "registration":
      return f"<b>Verificación por email:</b>\nPara verificar que eres estudiante de la asignatura <b>{cfg.subject_data['name']}</b> y registrar tu usario de Telegram en la base de datos escribe el comando:\n\n<code>/check_email {lt}correo UGR{gt}</code>\n\nSi no lo sabes/recuerdas, contacta con tu profesor/a.\n\n<b>Ejemplo</b>:\n<code>/check_email nombre@correo.ugr.es</code>"
    elif action == "no_args":
      return f"<b>Verificación por email:</b>\nDebes escribir tu correo después del comando.\n\n<b>Ejemplo</b>:\n/check_email nombre@correo.ugr.es"
    elif action == "many_args":
      return f"<b>Verificación por email:</b>\n{email} no es un email correcto, no debe llevar espacios.\n\n<b>Ejemplo:</b>\n<code>/check_email nombre@correo.ugr.espacios</code>"
    elif action == "not_found":
      return f"<b>Verificación por email:</b>\nEl email <b>{email}</b> no se encuentra en la base de datos. Por favor revisa si lo escribiste correctamente o comunícate con tu docente."
    elif action == "exists_email":
      return f"<b>Verificación por email:</b>\nYa tengo registrado el email <b>{email}</b> en mi base de datos. No es necesario registrarlo de nuevo. Si el email es el tuyo y no tienes acceso al comando /menu contacta a tu profesor/a."
    elif action == "registered_user":
      return f"Tu usuario ya se encuentra registrado con el email {email}\nSi no es tu correo por favor contacta con tu profesor/a."
    elif action == "success":
      return f"<b>Verificación por email:</b>\nHe registrado con éxito el email {email} a tu usuario de Telegram."

  else:
    if action == "registration":
      return f"<b>Email verification:</b>\nTo verify that you are a student of *{cfg.subject_data['name']}* course and to register your Telegram alias in the database, type the command:\n\n<code>/check_email {lt}UGR email{gt}</code>\n\nIf you don't know/remember it, contact with your teacher.\n\n*Example*:\n<code>/check_email nickname@correo.ugr.es</code>"
    elif action == "no_args":
      return f"<b>Email verification:</b>\nYou must write your email after the command.\n\n<b>Example</b>:\n/check_email nickname@correo.ugr.es"
    elif action == "many_args":
      return f"<b>Email verification:</b>\n{email} is not a correct email, it must not contain spaces.\n\n<b>Example:</b>\n<code>/check_email nickname@correo.ugr.es</code>"
    elif action == "not_found":
      return f"<b>Email verification:</b>\nThe email <b>{email}</b> is not in the database. Please check if you typed it correctly or contact your teacher."
    elif action == "exists_email":
      return f"<b>Email verification:</b>\nI have already registered the email {email} in my database. It is not necessary to register it again. If the email is yours and you do not have access to the /menu command, contact your teacher."
    elif action == "registered_user":
      return f"Your user is already registered with the email {email}\nIf this is not your email, please contact your teacher."
    elif action == "success":
      return f"<b>Email verification:</b>\nI have successfully registered the email {email} to your Telegram user."


def example_commands(lang, command):
  if lang == "es":
    if command == "check_email":
      return "\n\n<b>Ejemplo</b>:\n<code>/check_email nombre@correo.ugr.es</code>"


## MENUS ####################
def main_menu(lang):
  if lang == "es":
    text = "<b>MENU ESTUDIANTE</b>\nSelecciona una opción:"
    opt = [
      [IKButton("Mi Calificación", callback_data="s_menu-grade")],
      [
        IKButton("Opinar", callback_data="s_menu-opn"),
        IKButton("Evaluar", callback_data="s_menu-eva"),
      ],
      [IKButton("Sugerencia", callback_data="s_menu-suggestion")],
      [IKButton("Cambiar Idioma", callback_data="change_language")],
    ]
  else:
    text = "<b>STUDENT MENU</b>\nSelect an option:"
    opt = [
      [IKButton("My grades", callback_data="s_menu-grade")],
      [
        IKButton("Opinion", callback_data="s_menu-opn"),
        IKButton("Evaluate", callback_data="s_menu-eva"),
      ],
      [IKButton("Sugerencia", callback_data="s_menu-suggestion")],
      [IKButton("Change Language", callback_data="change_language")],
    ]
  return (text, opt)


def my_grade(lang, action, week, *data):
  if lang == "es":
    if action == "grades":
      return f"<b>MI CALIFICACIÓN\nSEMANA {week}</b>:\nTu factor de riesgo académico es: <b>{data[0]}</b>.\nTu calificación actual es: <b>{data[1]}</b>\nTu calificación máxima posible es: <b>{data[2]}</b> \n\nA continuación te muestro cada actividad que se ha evaluado hasta este momento y su calificación:\n{data[3]}\n\n"
    elif action == "no_active":
      return f"<b>SEMANA {week}</b>\nActualmente no existen actividades calificadas.\n\nTu factor de riesgo académico es: <b>Ninguno</b>.\nTu máxima calificación posible es: <b>10</b>"
  else:
    if action == "grades":
      return f"<b>MY GRADES\nWEEK {week}</b>:\nYour academic risk factor is <b>{data[0]}</b>.\nYour actual grade is: <b>{data[1]}</b>\nYour highest possible grade is: <b>{data[2]}</b>\n\nBelow I show you each activity that has been evaluated so far and its grade:\n{data[3]}"
    elif action == "no_active":
      return f"<b>WEEK {week}</b>\nThere are currently no qualified activities.\n\nYour academic risk factor is: <b>None</b>.\nYour highest possible grade is: <b>10</b>."
