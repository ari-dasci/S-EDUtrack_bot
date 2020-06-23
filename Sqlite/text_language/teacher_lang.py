def welcome_text(lang, context, action):
  bot_username = context.bot.username
  text = ""
  if lang == "es":
    if action == "short":
      return (
        "Escribe el comando /menu para ver las opciones con las que podemos trabajar."
      )
    if action == "not_start":
      text = "Hemos terminado de configurar la asignatura.\n\n"
    return f"{text}Bienvenido a EDUtrack <b>{bot_username}</b>. Te ayudaré en esta asignatura manteniendote informado de los estudiantes que están en riesgo de fracaso academic de forma semanal.\n\nAdemás de llevar un control de la comunicación en Telegram de los estudiantes, te proporcionaré informes sobre la opinión colectiva sobre la asignatura recogida mediante EDUtrack.\nMis comandos son:\n\n/menu\n Te mostraré las opciones con las que podemos trabajar juntos.\n\n/change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n/help\nTe informaré sobre el menú de opciones. También podrás acceder al manual de usuario."
  else:
    if action == "short":
      return "Type command /menu to see the options with which we can work together."
    if action == "not_start":
      text = "We've finished configuring the subject.\n\n"
    return f"{text}<b>{bot_username}</b>, welcome to EDUtrack. I will help you in this course by keeping you informed of students who are at risk of academic failure on a weekly basis.\n\nIn addition to keeping track of students' Telegram communication, I will provide you with reports on the collective opinion on the course collected through EDUtrack.\nMy commands are:\n\n/menu\n I will show you the options with which we can work together.\n\n/change_language\n I will help you switch the language in which I show you the contents. The current options are English and Spanish.\n\n/help\nI'll inform you about the options menu. You will also be able to access the user manual."


def config_files(lang, action, file_name="", elements="", context=""):
  if lang == "es":
    if action == "download":
      bot_username = context.bot.username
      return f"<b>Asistente para la configuración de la asignatura.</b>\n\nBienvenido a EDUtrack <b>{bot_username}</b>. Antes de usar EDUtrack debes terminar de configurar la asignatura. Descarga y edita estos archivos. Cuando los tengas listos enviámelos con el mismo nombre."
    if action == "ready_one":
      return f"El archivo se ha subido correctamente. Aún falta por subir el archivo <b>{file_name}</b> para finalizar la configuración."
    if action == "replace":
      return f"El archivo se ha subido correctamente."
    if action == "no_set_up":
      return "La asignatura aún no está configurada por completo."
    if action == "header_error":
      return f"El archivo debe contener al menos las siguientes cabeceras de columna:\n{elements}\n\nRevisa el formato del archivo."
    if action == "missing_file":
      file_name = "estudiantes" if file_name == "students" else "actividades"
      return f"El archivo de configuración <b>{file_name}</b> aún no se ha cargado. Recuerda que lo debes subir con el mismo nombre."
    if action == "exists_in_DB":
      if "students" in file_name:
        return f"<b>ARCHIVO EXISTENTE</b>\nLa seccion <b>estudiantes</b> ya existe en la base de datos.\nPara agregar más {elements} renombra el archivo como <b>add_{file_name}</b>.\n\nPara reemplazar todo, renombra el archivo como <b>replace_{file_name}</b>.\nSi utilizas está opción, la sección de calificaciones también se borrará, eliminando todas las calificaciones cargadas previamente."
      else:
        #  The activity file does not allow you to add activities to maintain the correct grading scheme.
        return f"<b>ARCHIVO EXISTENTE</b>\nLa seccion <b>actividades</b> ya existe en la base de datos.\nPara reemplazar las actividades, renombra el archivo como <b>replace_{file_name}</b>.\nSi utilizas está opción, la sección de calificaciones también se borrará, eliminando todas las calificaciones cargadas previamente."
    if action == "add_ready":
      if elements == "students":
        return f"Se han gregado con éxito los estudiantes."
      elif elements == "activities":
        return f"Se han aregado con exito las actividades."
    if action == "add_all_exists":
      return (
        f"Todos los elementos ya existen en la base de datos, no se agrego ninguno."
      )
    if action == "add_duplicates":
      return f"Los siguientes elementos están duplicados:\n{elements}"
    if action == "add_no_duplicates":
      return f"\n\nLos demás elementos se agregaron correctamente."

  else:
    if action == "download":
      bot_username = context.bot.username
      return f"<b>Course setup wizard.</b>\n\nWelcome to EDUtrack {bot_username}. Before using EDUtrack you must finish configuring the course. Download and edit these files. When done, send them to me keeping the file names."
    if action == "ready_one":
      return f"The file uploaded correctly. The {filename} configuration file has yet to be uploaded."
    if action == "replace":
      return f"The file has been uploaded successfully."
    if action == "no_set_up":
      return "The subject is not yet fully configured."
    if action == "header_error":
      return f"The file must contain at least the following headers:\n{elements}\n\nCheck the file format."
    if action == "missing_file":
      return f"Configuration file <b>{file_name}</b> is not uploaded. Remember to keep the file name."
    if action == "exists_in_DB":
      elements = "students" if "students" in file_name else "activities"
      return f"<b>EXISTING FILE</b>\nSection <b>{elements}</b> already exists in the database.\nTo add more {elements} rename the file to <b>add_{file_name}</b>.\n\nTo replace everything, rename the file to <b>replace_{file_name}</b>.\nIf you use the latter option, the grades section will also be cleared, deleting all previously loaded grades."
    if action == "add_elements_ready":
      return f"Successfully added {elements}"
    if action == "add_ready":
      return f"Successfully added {elements}"
    if action == "add_all_exists":
      return f"All the elements already exist in the database, none were added."
    if action == "add_duplicates":
      return f"The following items are duplicated:{elements}"
    if action == "add_no_duplicates":
      return f"\n\nThe other elements were added correctly."


def config_files_activities(language, action, elements=""):
  if language == "es":
    print(len(elements.split("\n")))
    if action == "no_main_category":
      return "<b>FALTA LA CATEGORÍA SUBJECT</b>\n\nTodos los <b>'_id' calificables</b> deben tener una categoría. Si el <b>'_id'</b> es una categoría superior (no tiene categoría padre), su categoría debe ser <b>'SUBJECT'</b>."
    elif action == "undefined_category":
      msg = "Todas las categorías deben estar definidas en la columna <b>'_id'</b> y tener un peso y categoría establecidos."
      if len(elements.split("\n")) == 1:
        return f"<b>CATEGORÍA NO DEFINIDA</b>\n\nLa categoría {elements} no está definida.\n\n{msg}"
      elif len(elements.split("\n")) > 1:
        return f"<b>CATEGORÍAS NO DEFINIDAS</b>\n\nLas siguientes categorías no están definidas:\n\n{elements}\n\n{msg}"
    elif action == "weightless":
      if len(elements.split("\n")) == 1:
        return f"<b>CATEGORIA SIN PESO</b>\n\nLa categoría <b>{elements}</b> no tiene definido el peso."
      elif len(elements.split("\n")) > 1:
        return f"<b>CATEGORIAS SIN PESO</b>\n\nLas siguientes categorías no tienen definido el peso:\n\n<b>{elements}</b>"
    elif action == "no_parent_cat":
      if len(elements.split("\n")) == 1:
        return f"<b>SIN CATEGORIA PADRE</b>\n\nLa categoría <b>{elements}</b> no tiene definida su categoria padre."
      elif len(elements.split("\n")) > 1:
        return f"<b>CATEGORIAS SIN PESO</b>\n\nLas siguientes categorías no tienen definida la categoria padre:\n\n</b>{elements}</b>"

  else:
    if action == "no_main_category":
      return "<b>SUBJECT CATEGORY MISSING</b>\n\nAll <b>qualifying '_id'</b> must have a category. If <b>'_id'</b> is a higher category (doesn't have a parent category) its category must be <b>'SUBJECT'</b>."
    elif action == "undefined_category":
      msg = "All categories must be defined in column <b>'_id'</b> and have an established weight and category."
      if len(elements.split("\n")) == 1:
        return f"<b>UNDEFINED CATEGORY</b>\n\nThe {elements} category is not defined.\n\n{msg}"
      elif len(elements.split("\n")) > 1:
        return f"<b>UNDEFINED CATEGORIES</b>\\nnThe following categories are not defined:\n\n{elements}\n\n{msg}"
    elif action == "weightless":
      if len(elements.split("\n")) == 1:
        return f"<b>WEIGHTLESS CATEGORY</b>\n\nThe <b>{elements}</b> category has no defined weight."
      elif len(elements.split("\n")) > 1:
        return f"<b>WEIGHTLESS CATEGORIES</b>\n\nThe following categories have no defined weight:\n\n<b>{elements}</b>"
    elif action == "no_parent_cat":
      if len(elements.split("\n")) == 1:
        return f"<b>NO PARENT CATEGORY</b>\n\nThe <b>{elements}</b> category has not defined its parent category."
      elif len(elements.split("\n")) > 1:
        return f"<b>NO PARENT CATEGORY</b>\n\nThe following categories don't have the parent category defined:\n\n<b>{elements}</b>"
