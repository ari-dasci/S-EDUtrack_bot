from telegram import InlineKeyboardButton as IKButton
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
      return f"Escribe el comando /menu para ver las opciones."

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
    Title = f"<b>VERIFICACIÓN POR EMAIL:</b>\n"
    if action == "registration":
      return f"{Title}Para verificar que eres estudiante de la asignatura <b>{cfg.subject_data['name']}</b> y registrar tu usario de Telegram en la base de datos escribe el comando:\n\n<code>/check_email {lt}correo UGR{gt}</code>\n\nSi no lo sabes/recuerdas, contacta con tu profesor/a.\n\n<b>Ejemplo</b>:\n<code>/check_email nombre@correo.ugr.es</code>"
    elif action == "no_args":
      return f"{Title}Debes escribir tu correo después del comando.\n\n<b>Ejemplo</b>:\n/check_email nombre@correo.ugr.es"
    elif action == "many_args":
      return f"{Title}{email} no es un email correcto, no debe llevar espacios.\n\n<b>Ejemplo:</b>\n<code>/check_email nombre@correo.ugr.espacios</code>"
    elif action == "not_found":
      return f"{Title}El email <b>{email}</b> no se encuentra en la base de datos. Por favor revisa si lo escribiste correctamente o comunícate con tu profesor/a."
    elif action == "exists_email":
      return f"{Title}Ya tengo registrado el email <b>{email}</b> en mi base de datos. No es necesario registrarlo de nuevo. Si el email es el tuyo y no tienes acceso al comando /menu contacta a tu profesor/a."
    elif action == "registered_user":
      return f"Tu usuario ya se encuentra registrado con el email {email}\nSi no es tu correo por favor contacta con tu profesor/a."
    elif action == "success":
      return (
        f"{Title}He registrado con éxito el email {email} a tu usuario de Telegram."
      )

  else:
    Title = f"<b>EMAIL VERIFICATION:</b>\n"
    if action == "registration":
      return f"{Title}To verify that you are a student of <b>{cfg.subject_data['name']}</b> course and to register your Telegram alias in the database, type the command:\n\n<code>/check_email {lt}UGR email{gt}</code>\n\nIf you don't know/remember it, contact with your teacher.\n\n*Example*:\n<code>/check_email nickname@correo.ugr.es</code>"
    elif action == "no_args":
      return f"{Title}You must write your email after the command.\n\n<b>Example</b>:\n/check_email nickname@correo.ugr.es"
    elif action == "many_args":
      return f"{Title}{email} is not a correct email, it must not contain spaces.\n\n<b>Example:</b>\n<code>/check_email nickname@correo.ugr.es</code>"
    elif action == "not_found":
      return f"{Title}The email <b>{email}</b> is not in the database. Please check if you typed it correctly or contact your teacher."
    elif action == "exists_email":
      return f"{Title}I have already registered the email {email} in my database. It is not necessary to register it again. If the email is yours and you do not have access to the /menu command, contact your teacher."
    elif action == "registered_user":
      return f"{Title}Your user is already registered with the email {email}\nIf this is not your email, please contact your teacher."
    elif action == "success":
      return f"{Title}I have successfully registered the email {email} to your Telegram user."


def example_commands(lang, command):
  if lang == "es":
    if command == "check_email":
      return f"\n\n<b>Ejemplo</b>:\n<code>/check_email nombre@correo.ugr.es</code>"


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
      # [IKButton("Cambiar Idioma", callback_data="change_language")],
    ]
  else:
    text = "<b>STUDENT MENU</b>\nSelect an option:"
    opt = [
      [IKButton("My grades", callback_data="s_menu-grade")],
      [
        IKButton("Opinion", callback_data="s_menu-opn"),
        IKButton("Evaluate", callback_data="s_menu-eva"),
      ],
      [IKButton("Suggestion", callback_data="s_menu-suggestion")],
      # [IKButton("Change Language", callback_data="change_language")],
    ]
  return (text, opt)


def my_grade(lang, action, week, stu_data=""):
  if lang == "es":
    Title = f"<b>MI CALIFICACIÓN - SEMANA {week}:</b>\n\n"
    if action == "grades":
      return f"{Title}Tu factor de riesgo académico es: <b>{stu_data['linguistic']}</b>.\nTu calificación actual es: <b>{stu_data['actual_grade']}</b>\nTu calificación máxima posible es: <b>{stu_data['max_possible_grade']}</b> \n\nA continuación te muestro cada actividad que se ha evaluado hasta este momento y su calificación:\n\n{stu_data['activities']}\n\n"
    elif action == "no_active":
      return f"{Title}Actualmente no existen actividades calificadas.\n\nTu factor de riesgo académico es: <b>Ninguno</b>.\nTu máxima calificación posible es: <b>10</b>"
    elif action == "no_email":
      return f"{Title}La base de datos aún no tiene registrado tu email."
  else:
    Title = f"<b>MY GRADE WEEK {week}</b>\n\n"
    if action == "grades":
      return f"{Title}Your academic risk factor is <b>{stu_data['linguistic']}</b>.\nYour actual grade is: <b>{stu_data['actual_grade']}</b>\nYour highest possible grade is: <b>{stu_data['max_possible_grade']}</b>\n\nBelow I show you each activity that has been evaluated so far and its grade:\n{stu_data['activities']}"
    elif action == "no_active":
      return f"{Title}There are currently no qualified activities.\n\nYour academic risk factor is: <b>None</b>.\nYour highest possible grade is: <b>10</b>."
    elif action == "no_email":
      return f"{Title}The database has not yet registered your email."


def menu_opinion(lang):
  if lang == "es":
    text = f"<b>OPINAR</b>\nSelecciona una opción:"
    opt = [
      [IKButton("Práctica Docente", callback_data="s_menu-opn-tp")],
      [IKButton("Colaboración entre compañeros", callback_data="s_menu-opn-coll")],
      [IKButton("Recursos/materiales", callback_data="s_menu-opn-rsrcs")],
      [IKButton("Regresar", callback_data="s_menu-back")],
    ]
  else:
    text = "<b>OPINION</b>\nSelect an option:"
    opt = [
      [IKButton("Teaching Practice", callback_data="s_menu-opn-tp")],
      [IKButton("Peer Collaboration", callback_data="s_menu-opn-coll")],
      [IKButton("Resources/materials", callback_data="s_menu-opn-rsrcs")],
      [IKButton("Back", callback_data="s_menu-back")],
    ]
  return (text, opt)


def menu_opn_tea_practice(lang):
  if lang == "es":
    text = "<b>OPINION DE LA PRACTICA DOCENTE</b>\nSelecciona una categoría para ver los criterios:"
    opt = [
      [IKButton("Docente", callback_data="s_menu-opn-tp-teacher")],
      [IKButton("Contenidos", callback_data="s_menu-opn-tp-content")],
      [IKButton("Comunicación Virtual", callback_data="s_menu-opn-tp-vc")],
      [IKButton("Regresar", callback_data="s_menu-opn")],
    ]
  else:
    text = "<b>TEACHING PRACTICE OPINION</b>\nSelect a category to see the criteria:"
    opt = [
      [IKButton("Teacher", callback_data="s_menu-opn-tp-teacher")],
      [IKButton("Contents", callback_data="s_menu-opn-tp-content")],
      [IKButton("Virtual Comunication", callback_data="s_menu-opn-tp-vc")],
      [IKButton("Back", callback_data="s_menu-opn")],
    ]
  return (text, opt)


def opn_tea_practice(lang, action, week, criterion=""):
  if lang == "es":
    Title = f"<b>OPINION SOBRE LA PRACTICA DOCENTE\nSEMANA {week}</b>\n\n"
    if action == "criterion":
      return f"{Title}¿Cuál es tu opinión sobre el criterio <b>{criterion}</b> en la práctica docente según tu experiencia de esta semana en la asignatura?"
    elif action == "text_after_save":
      return (
        f"{Title}Se ha guardado correctamente tu opinión.\n\nSelecciona una opción."
      )
    elif action == "no_criteria":
      return f"{Title}No hay criterios que evaluar o ya los has evaluado todos esta semana. Regresa en otro momento o la siguiente semana."
    elif action == "choice_criterion":
      return f"{Title}Selecciona un criterio para evaluarlo."
  else:
    Title = f"<b>TEACHING PRACTICE OPINION\nWEEK {week}</b>\n\n"
    if action == "criterion":
      return f"{Title}What is your opinion about criterion <b>{criterion}</b> in the teaching practice according to your experience of this week in the subject?"
    elif action == "text_after_save":
      return f"{Title}Your opinion has been saved correctly.\n\nSelect an option:"
    elif action == "no_criteria":
      return f"{Title}There are no criteria to evaluate or you've already evaluated them all this week. Come back at another time or the next week."
    elif action == "choice_criterion":
      return f"{Title}Selecciona un criterio para evaluarlo."


def opn_collaboration(lang, action, classmate="", week=""):
  if lang == "es":
    Title = f"<b>OPINION SOBRE LA COLABORACION ENTRE COMPAÑEROS\nSEMANA {week}</b>\n\n"
    if action == "text":
      return f"Selecciona una opción."
    if action == "no_planet":
      return f"{Title}Aún no estás registrado en ningún planeta."
    elif action == "scale":
      return f"{Title}¿Cómo consideras que ha sido la colaboración de tu compañero/a <b>{classmate}</b> en las tareas de tu planeta durante esta semana?."
    elif action == "no_classmates":
      return f"{Title}No hay compañeros de equipo que evaluar o ya has evaluado a todos en esta semana. Regresa en otro momento o la siguiente semana."
    elif action == "text_after_save":
      return (
        f"{Title}Se ha guardado correctamente tu evaluación.\n\nSelecciona una opción."
      )

  else:
    Title = f"<b>PEER COLLABORATION OPINION\nWEEK {week}</b>\n\n"
    if action == "text":
      return f"{Title}Select an option:"
    if action == "no_planet":
      return (
        f"<b>PEER COLLABORATION OPINION</b>\nYou're not registered in any planet yet."
      )
    elif action == "scale":
      return f"{Title}How do you think your team-mate <b>{classmate}</b> collaborated in your planet's tasks this week?."
    elif action == "no_classmates":
      return f"{Title}There are no teammates to evaluate or you have already evaluated everyone this week. Come back at another time or the next week."
    elif action == "text_after_save":
      return f"{Title}Your evaluation has been saved correctly.\n\nSelect an option:"


## MENU - OPINION - RESOURCES
def opn_resources(lang, action, resource=""):
  if lang == "es":
    Title = f"<b>OPINION SOBRE LOS RECURSOS</b>\n"
    if action == "text_section":
      return f"{Title}Selecciona una sección para ver sus recursos."
    elif action == "text_rsrc":
      return f"{Title}Selecciona una opción:"
    elif action == "scale":
      return f"{Title}¿Como consideras el recurso/material <b>{resource}</b>?."
    elif action == "no_section":
      return f"{Title}Actualmente no hay más recursos que evaluar. Regresa en otro momento o la siguiente semana."
    elif action == "text_after_save":
      return (
        f"{title}Se ha guardado correctamente tu opinión.\n\nSelecciona una opción."
      )

  else:
    Title = f"<b>RESOURCES OPINION</b>\n"
    if action == "text_section":
      return f"{Title}Select a section to view its resources."
    elif action == "text_rsrc":
      return f"{Title}Select an option:"
    elif action == "scale":
      return f"{Title}How do you consider the resource/material <b>{resource}</b>?"
    elif action == "no_section":
      return f"{Title}Currently there are no more resources to evaluate. Come back at another time or the next week."
    elif action == "text_after_save":
      return f"{Title}Your opinion has been saved correctly.\n\nSelect an option:"


## MENU - OPINION - TEACHER - MEETINGS
def opn_tea_meet(lang, action, meeting=""):
  if lang == "es":
    Title = f"<b>OPINIÓN SOBRE LA COMUNICACIÓN VIRTUAL CON EL DOCENTE</b>\n"
    if action == "text_meeting":
      return f"{Title}Selecciona una meeting."
    elif action == "no_meetings":
      return f"{Title}Aún no se ha realizado ningún meeting. Regresa después."
    elif action == "all_meetings_evaluated":
      return f"{Title}Ya has evaluado las meetings hasta la fecha. Regresa después."
    elif action == "scale":
      return f"{Title}¿Como consideras que fue la actuación del docente en la <b>meeting {meeting}</b>?."

  else:
    Title = f"<b>OPINION OF THE VIRTUAL COMMUNICATION WITH THE TEACHER</b>\n"
    if action == "text_meeting":
      return f"{Title}Select a meeting."
    elif action == "no_meetings":
      return f"{Title}No meeting has yet taken place. Come back later."
    elif action == "all_meetings_evaluated":
      return (
        f"{Title}You've already evaluated the meetings to <date class="
        "></date> Come back later."
      )
    elif action == "scale":
      return f"{Title}How do you think the teacher's performance was in the <b>meeting {meeting}</b>?"


def evaluate(lang, action):
  if lang == "es":
    if action == "not_available":
      return f"<b>EVALUAR</b>\nPor el momento esta función no se encuentra disponible. Solicita información a tu profesor/a."
  else:
    if action == "not_available":
      return f"<b>EVALUATE</b>\nAt the moment this function is not available. Ask your teacher for information."


def suggestion(lang, action):
  if lang == "es":
    if action == "text":
      return f"<b>SUGERENCIA:</b>\nEn esta sección podras sugerir ideas que mejoren este bot o también que quieras proponer para la asignatura. Puede ser integrar alguna funcionalidad o proponer alguna mejora de mi funcionamiento.\n\nEscribe el comando /suggestion {lt}tu sugerencia{gt}\n\nEjemplo:\n/suggestion Creo que se podría mejorar el funcionamieno si..."
    elif action == "empty":
      return f"<b>SUGERENCIA:</b>\nLo siento la sugerencia no puede estar vacía.\n\nEscribe el comando /suggestion {lt}tu sugerencia{gt}\n\nEjemplo:\n/suggestion Creo que se podría mejorar el funcionamieno si..."
    elif action == "save":
      return f"<b>SUGERENCIA:</b>\nSe ha guardado tu dugerencia con exito."
  else:
    if action == "text":
      return f"<b>SUGGESTION:</b>\nIn this section you can suggest ideas that improve this bot or also that you want to propose for the course. It can be to integrate some functionality or to propose some improvement of my operation\n\nType the command /suggestion {lt}your suggestion{gt}\n\nExample:\n/suggestion I think that this course could be improved if..."
    elif action == "empty":
      return f"<b>SUGGESTION:</b>\nI'm sorry the suggestion can't be empty.\n\nType the command /suggestion {lt}your suggestion{gt}\n\nExample:\n/suggestion I think that this course could be improved if..."
    elif action == "save":
      return f"<b>SUGGESTION:</b>\nYour suggestion has been successfully saved."
