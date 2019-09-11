from telegram  import (InlineKeyboardButton as IKButton)
import configuration.config_file as cfg

def welcome_text(context, language):
  bot_username = context.bot.username
  if language == "ES":
    return f'Bienvenido al asistente EDUtrack <b>{bot_username}</b>, te acompañare durante el curso para que puedas opinar/evaluar sobre algunos elementos claves en tu aprendizaje.\n\nEscribe el símbolo <b>" / "</b> y te mostrare los comandos que puedes utilizar para que trabajemos juntos. Aquí tienes una breve explicación de cada uno.\n\n/menu\nTe mostraré el menú con las opciones que puedes realizar conmigo.\n\n/change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n/help\nTe mostraré los comandos que puedes utilizar y la descripción de cada apartado del menú. También podrás acceder al manual de usuario.'
  else:
    return f'Welcome to the EDUtrack assistant{bot_username}. I will accompany you during the course so that you can give your opinion/evaluate some key elements in your learning.\nWrite the symbol <b> "/" </b> and I will show you the commands you can use to work together. Here'+"'s a brief explanation of each one.\n\n/menu\nI'll show you the menu with the options we can work with.\n\n/change_language\nI will help you change the language in which I show you the contents. The current options are English and Spanish.\n\n/help\nI'll show you the commands you can use and the description of each menu item. You will also be able to access the user manual."


welcome_short_text ={
  'ES' : "Escribe el comando /menu para ver las opciones con las que podemos trabajar.",
  'EN' : "Type the /menu command to see the options we can work with together."
}

def not_config_files_set_text (context, language):
  bot_name = context.bot.first_name
  if language == "ES":
    return f"<b>EDUtrack {bot_name}</b> aún no se ha terminado de configurar. Espera instrucciones del docente."
  else:
    return f"<b>EDUtrack {bot_name}</b> has not yet finished configuring. Wait for instructions from the teacher."


def check_email(language, action, email=""):
  if language == "ES":
    if action == "registration":
      return f"*Verificación por email:*\nPara verificar que eres estudiante de la asignatura *{cfg.subject_name}* y registrar tu usario de Telegram en la base de datos escribe el comando:\n\n/check`_`email <Tu email PRADO>\n\nSi no lo sabes o no lo recuerdas, contacta a tu docente.\n\n*Ejemplo*:\n/check`_`email nombre@correo.ugr.es"
    elif action == "no_args":
      return f"Debes escribir tu correo después del comando.\n\n<b>Ejemplo</b>:\n/check_email nombre@correo.ugr.es"
    elif action == "many_args":
      return f"{email} no es un email correcto, no debe llevar espacios.\n\n<b>Ejemplo:</b>\n/check_email nombre@correo.ugr.espacios"
    elif action == "not_found":
      return f"El email <b>{email}</b> no se encuentra en la base de datos. Por favor revisa si lo escribiste correctamente o comunícate con tu docente."
    elif action == "existing email":
      return f"Ya tengo registrado el email {email} en mi base de datos. No es necesario registrarlo de nuevo."
    elif action == "success":
      return f"He registrado con éxito el email {email} a tu usuario de Telegram."

  elif language == "EN":
    if action == "registration":
      return f"*Email verification:*\nTo verify that you are a student of this subject and register your Telegram user in the database, type the command:\n\n/check`_`email <your email PRADO>\n\nIf you don't know it or don't remember it, contact your teacher.\n\n*Example*:\n/check`_`email nombre@correo.ugr.es"
    elif action == "no_args":
      return f"You must write your email after the command.\n\n<b>Example</b>:\n/check_email name@correo.ugr.es"
    elif action == "many_args":
      return f"{email} is not a correct email, it must not contain spaces.\n\n<b>Example:</b>\n/check_email name@correo.ugr.es"
    elif action == "not_found":
      return f"The email <b>{email}</b> is not in the database. Please check if you typed it correctly or contact your teacher."
    elif action == "existing email":
      return f"I have already registered the email {email} in my database. It is not necessary to register it again."
    elif action == "success":
      return f"I have successfully registered the email {email} to your Telegram user."





## WARNINGS
no_username_text = {
  "ES" : "Me di cuenta que no tienes un username/alias registrado en tu cuenta de Telegram. Para utilizar EDUtrack debes configurar un username/alias. Ve a ajustes en tu cuenta de Telegram y edita tu perfil para asignar un username/alias.",
  "EN" : "I noticed that you don't have a username registered in your Telegram account. To use EDUtrack you must set up a username. Go to settings in your Telegram account and edit your profile to assign a username."
}


## STUDENT MENU
menu = {
  'ES' : {
    "opt" : [
      [IKButton("Mi Calificación",
          callback_data='s_menu-grade')],
      [IKButton("Opinar",
          callback_data='s_menu-opn'),
      IKButton("Evaluar",
          callback_data='s_menu-eval')],
      [IKButton("Sugerencia",
          callback_data='s_menu-suggestion')],
      [IKButton("Cambiar Idioma",
          callback_data='change_language')]
      ],

    "text" : "<b>MENU ESTUDIANTE</b>\nSelecciona una opción:"
  },

  'EN' : {
    "opt" : [
      [IKButton("My score",
          callback_data='s_menu-grade')],
      [IKButton("Opinion",
          callback_data='s_menu-opn'),
      IKButton("Evaluate",
          callback_data='s_menu-eval')],
      [IKButton("Sugerencia",
          callback_data='s_menu-suggestion')],
      [IKButton("Change Language",
          callback_data='change_language')]
      ],
    "text": "<b>STUDENT MENU</b>\nSelect an option:"}
}


linguistic_arf = {
  'ES' : {
    "irrecoverable": "Irrecuperable",
    "very_critical": "Muy Crítico",
    "critical": "Crítico",
    "moderate": "Moderado",
    "low": "Bajo",
    "none": "Ninguno"
  },
  'EN' : {
    "irrecoverable": "Irrecoverable",
    "very_critical": "Very Critical",
    "critical": "Critical",
    "moderate": "Moderate",
    "low": "Low",
    "none": "None"
  }
}

## MENU - MY GRADE
def my_grade (language, action, week, *data):
  print(data)
  if language == "ES":
    if action == "grades":
      return f"<b>SEMANA {week}</b>:\nTu factor de riesgo académico es: <b>{data[0]}</b>.\nActualmente tu calificación es: <b>{data[1]}</b>\nTu máxima calificación posible es: <b>{data[2]}</b>\n\nA continuación te muestro cada actividad que se ha evaluado hasta este momento y su calificación:\n{data[3]}\n\n"
    elif action == "no_active":
      return f"<b>SEMANA {week}</b>:\nActualmente no existen actividades calificadas.\n\nTu factor de riesgo académico es: <b>Ninguno</b>.\nTu máxima calificación posible es: <b>10</b>"
  else:
    if action == "grades":
      return f"<b>WEEK {week}</b>:\nYour academic risk factor is <b>{data[0]}</b>.\nYour actual grade is: <b>{data[1]}</b>\nYour highest grade possible is: <b>{data[2]}</b>\n\nBelow I show you each activity that has been evaluated so far and its grade:\n{[3]}"
    elif action == "no_active":
      return f"<b>WEEK {week}</b>:\nThere are currently no qualified activities.\n\nYour academic risk factor is: <b>None</b>.\nYour highest possible rating is: <b>10</b>."



## MENU - OPINION
menu_opinion = {
  'ES' : {
    "opt" : [
      [IKButton("Práctica Docente",
          callback_data='s_menu-opn-tp')],
      [IKButton("Colaboración de compañeros",
          callback_data='s_menu-opn-coll')],
      [IKButton("Recursos/materiales",
          callback_data='s_menu-opn-rsrcs')],
      [IKButton("Regresar",
          callback_data='s_menu-back')]
      ],
    "text" : "<b>OPINAR</b>\nSelecciona una opción:"
  },

  'EN' : {
    "opt" : [
      [IKButton("Teaching Practice",
          callback_data='s_menu-opn-tp')],
      [IKButton("Peer Collaboration",
          callback_data='s_menu-opn-coll')],
      [IKButton("Resources/materials",
          callback_data='s_menu-opn-rsrcs')],
      [IKButton("Back",
          callback_data='s_menu-back')]
      ],
    "text" : "<b>OPINION</b>\nSelect an option:"
  }
}


## MENU - OPINION - TEACHER PRACTICE
opn_tea_practice_menu = {
  'ES' : {
    "opt" : [
      [IKButton("Docente",
          callback_data='s_menu-opn-tp-teacher')],
      [IKButton("Contenidos",
          callback_data='s_menu-opn-tp-content')],
      [IKButton("Regresar",
          callback_data='s_menu-opn')]
      ],
    "text" : "<b>EVALUACIÓN DE LA PRACTICA DOCENTE</b>\nSelecciona una opción:"
  },

  'EN' : {
    "opt" : [
      [IKButton("Teacher",
          callback_data='s_menu-opn-tp-criteria-teacher')],
      [IKButton("Contents",
          callback_data='s_menu-opn-tp-criteria-content')],
      [IKButton("Back",
          callback_data='s_menu-opn')]
      ],
    "text" : "<b>TEACHING PRACTICE EVALUATION</b>\nSelect an option:"
  }}


def opn_tea_practice(language, action, criterion="", week=""):
  if language == "ES":
    if action == "criterion":
      return f"<b>OPINION DE LA PRACTICA DOCENTE\nSEMANA {week}</b>\n¿Cómo evalúas el criterio <b>{criterion[2:]}</b> en la práctica docente según tu experiencia de esta semana en la asignatura?"
    elif action == "text_after_save":
      return f"<b>OPINION DE LA PRACTICA DOCENTE</b>\nSe ha guardado correctamente tu opinión.\n\nSelecciona una opción."
    elif action == "no_criteria":
      return f"<b>OPINION DE LA PRACTICA DOCENTE\nSEMANA {week}</b>\n\nNo hay criterios que evaluar o ya has evaluado a todos. Regresa la siguiente semana."
  
  elif language == "EN":
    if action == "criterion":
      return f"<b>TEACHING PRACTICE OPINION\nWEEK {week}</b>\nHow do you evaluate the criterion <b>{criterion[2:]}</b> in teaching practice based on your experience this week in the subject?"
    elif action == "text_after_save":
      return f"<b>TEACHING PRACTICE OPINION</b>\nYour opinion has been saved correctly.\n\nSelect an option:"
    elif action == "no_criteria":
      return f"<b>TEACHING PRACTICE OPINION\nWEEK {week}</b>\n\nThere are no criteria to evaluate or you have already evaluated everyone. Come back next week."


## MENU - OPINION - COLLABORATION
def opn_collaboration(language, action, classmate="", week=""):
  if language == "ES":
    if action == "text":  
      return f"<b>OPINION DE LA COLABORACION DE COMPAÑEROS</b>\n\nSelecciona una opción."
    elif action == "scale":
      return f"<b>OPINION DE LA COLABORACION DE COMPAÑEROS\nSEMANA {week}</b>\n\n¿Cómo consideras que ha sido la colaboración de tu compañero(a) <b>{classmate}</b> en el chat de tu planeta durante esta semana?."
    elif action == "no_classmates":
      return f"<b>OPINION DE LA COLABORACION DE COMPAÑEROS:\nSEMANA {week}</b>\n\nNo hay compañeros de equipo que evaluar o ya has evaluado a todos. Regresa la siguiente semana."
    elif action == "text_after_save":
      return f"<b>OPINION DE LA COLABORACION DE COMPAÑEROS:</b>\nSe ha guardado correctamente tu evaluación.\n\nSelecciona una opción."
  
  elif language == "EN":
    if action == "text":  
      return f"<b>PEER COLLABORATION OPINION</b>\n\nSelect an option:"
    elif action == "scale":
      return f"<b>PEER COLLABORATION OPINION\nSEMANA {week}</b>\n\nHow do you think your teammate <b>{classmate}</b> collaborated in your planet's chat this week?."
    elif action == "no_classmates":
      return f"<b>PEER COLLABORATION OPINION\nSEMANA {week}</b>\n\nThere are no teammates to evaluate or you have already evaluated everyone. Come back next week."
    elif action == "text_after_save":
      return f"<b>PEER COLLABORATION OPINION</b>\nYour evaluation has been saved correctly.\n\nSelect an option:"

## MENU - OPINION - RESOURCES
def opn_resources(language, action, resource=""):
  if language == "ES":
    if action == "text_section":
      return f"<b>OPINION DE LOS RECURSOS</b>\nSelecciona una sección para ver sus recursos."
    elif action == "text_rsrc":
      return f"<b>OPINION DE LOS RECURSOS</b>\nSelecciona una opción:"
    elif action == "scale":
      return f"<b>OPINION DE LOS RECURSOS</b>\n¿Como consideras el recurso/material <b>{resource}</b>?."
    elif action == "no_section":
      return f"<b>OPINION DE LOS RECURSOS</b>\nActualmente no hay más recursos que evaluar, regresa la siguiente semana."
    elif action == "text_after_save":
      return f"<b>OPINION DE LOS RECURSOS</b>\nSe ha guardado correctamente tu opinión.\n\nSelecciona una opción."

  elif language == "EN":
    if action == "text_section":
      return f"<b>RESOURCE OPINION/b>\nSelect a section to view its resources."
    elif action == "text_rsrc":
      return f"<b>RESOURCE OPINION/b>\nSelect an option:?"
    elif action == "scale":
      return f"<b>RESOURCE OPINION/b>\nHow do you consider the resource/material <b>{resource}</b>?"
    elif action == "no_section":
      return f"<b>RESOURCE OPINION/b>\nCurrently there are no more resources to evaluate, come back next week."
    elif action == "text_after_save":
      return f"<b>RESOURCE OPINION/b>\nYour opinion has been saved correctly.\n\nSelect an option:"





if __name__ == '__main__':
    pass