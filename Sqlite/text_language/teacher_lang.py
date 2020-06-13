def welcome_text(lang, context, start_cmd=False):
  bot_username = context.bot.username
  text = ""
  if lang == "es":
    if not start_cmd:
      text = "Hemos terminado de configurar la asignatura.\n\n"
    return f"{text}Bienvenido a EDUtrack <b>{bot_username}</b>. Te ayudaré en esta asignatura manteniendote informado de los estudiantes que están en riesgo de fracaso escolar de forma semanal.\n\nAdemás de llevar un control de la comunicación en Telegram de los estudiantes, te proporcionaré informes sobre la opinión colectiva sobre la asignatura recogida mediante EDUtrack.\nMis comandos son:\n\n/menu\n Te mostraré las opciones con las que podemos trabajar juntos.\n\n/change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n/help\nTe informaré sobre el menú de opciones. También podrás acceder al manual de usuario."
  else:
    if not start_cmd:
      text = "We've finished configuring the subject.\n\n"
    return f"{text}<b>{bot_username}</b>, welcome to EDUtrack. I will help you in this course by keeping you informed of students who are at risk of academic failure on a weekly basis.\n\nIn addition to keeping track of students' Telegram communication, I will provide you with reports on the collective opinion on the course collected through EDUtrack.\nMy commands are:\n\n/menu\n I will show you the options with which we can work together.\n\n/change_language\n I will help you switch the language in which I show you the contents. The current options are English and Spanish.\n\n/help\nI'll inform you about the options menu. You will also be able to access the user manual."


def config_files(lang, action, file_name="", elements=""):
  if lang == "es":
    if action == "download":
      return "<b>Asistente para la configuración de la asignatura.</b>\n\nAntes de usar EDUtrack debes terminar de configurar la asignatura. Descarga y edita estos archivos. Cuando los tengas listos enviámelos con el mismo nombre."
    if action == "ready_one":
      return "El archivo se ha cargado correctamente."
    if action == "no_set_up":
      return "La asignatura aún no está configurada por completo."
    if action == "header_error":
      return f"El archivo debe contener al menos las siguientes cabeceras de columna:\n{elements}\n\nRevisa el formato del archivo."
    if action == "missing_file":
      file_name = "estudiantes" if file_name == "students" else "actividades"
      return f"El archivo de configuración <b>{file_name}</b> aún no se ha cargado. Recuerda que lo debes subir con el mismo nombre."
    if action == "exists_in_DB":
      elements = "estudiantes" if "students" in file_name else "actividades"
      return f"<b>ARCHIVO EXISTENTE</b>\nLa seccion <b>{elements}</b> ya existe en  la base de datos.\nPara agregar más {elements} renombra el archivo como <b>add_{file_name}</b>.\n\nPara reemplazar todo, renombra el archivo como <b>replace_{file_name}</b>.\nSi utilizas está última opción, la sección de calificaciones también se borrará, eliminando todas las calificaciones cargadas previamente."

  else:
    if action == "download":
      return "<b>Course setup wizard.</b>\n\nBefore using EDUtrack you must finish configuring the course. Download and edit these files. When done, send them to me keeping the file names."
    if action == "ready_one":
      return "The file uploaded correctly."
    if action == "no_set_up":
      return "The subject is not yet fully configured."
    if action == "header_error":
      return f"The file must contain at least the following headers:\n{elements}\n\nCheck the file format."
    if action == "missing_file":
      return f"Configuration file <b>{file_name}</b> is not uploaded. Remember to keep the file name."
    if action == "exists_in_DB":
      elements = "students" if "students" in file_name else "activities"
      return f"<b>EXISTING FILE</b>\nSection <b>{elements}</b> already exists in the database.\nTo add more {elements} rename the file to <b>add_{file_name}</b>.\n\nTo replace everything, rename the file to <b>replace_{file_name}</b>.\nIf you use the latter option, the grades section will also be cleared, deleting all previously loaded grades."
