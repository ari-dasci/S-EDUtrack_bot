from telegram  import (InlineKeyboardButton as IKButton)

def welcome_text(context, language, start_cmd=False):
  bot_username = context.bot.username
  text = ""
  if language == "ES":
    if not start_cmd:
      text = "Hemos terminado de configurar la asignatura.\n\n"
    return f"{text}Bienvenido al asistente EDUtrack <b>{bot_username}</b>. Te ayudaré en esta asignatura manteniendote informado de los estudiantes que están en riesgo de fracaso escolar de forma semanal.\n\nAdemás de llevar un control sobre los mensajes de los estudiantes, te proporcionaré reportes sobre las evaluaciones que los estudiantes pueden realizar con EDUtrack en la asignatura.\nEstos son los comandos básicos:\n\n/menu\n Te mostraré las opciones con las que podemos trabajar juntos.\n\n/change_language\nTe ayudaré a cambiar el idioma en que te muestro los contenidos. Las opciones actuales son Inglés y Español.\n\n/help\nTe mostraré los comandos que puedes utilizar y la descripción de cada apartado del menú. También podrás acceder al manual de usuario."
  else:
    if not start_cmd:
      text = "We've finished configuring the subject.\n\n"
    return f"{text}Welcome to the assistant EDUtrack <b>{bot_username}</b>. I will help you in this subject by keeping you informed of students who are at risk of school failure on a weekly basis.\n\nIn addition to keeping track of student messages, I will provide you with reports on the assessments that students can make with EDUtrack in the subject. These are the basic commands\n\n/menu\nI'll show you the options we can work with together.\n\n/change_language\nI'll help you to change the language in which I show you the contents. The current options are English and Spanish.\n\n/help\nI'll show you the commands you can use and the description of each menu item. You can also access the user manual."

welcome_short_text ={
  "ES" : "Escribe el comando /menu para ver las opciones con las que podemos trabajar.",
  
  "EN" : "Type the /menu command to see the options we can work with together."
}

not_config_files_set_text = {
  "ES": "La asignatura aún no se ha configurado completamente.",
  
  "EN": "The subject has not yet been fully configured."
}

def error_file_headers_text(language, headers):
  headers = ("\n").join(headers)
  if language == "ES":
    return f"El archivo debe contener las siguientes columnas:\n{headers}\n\nRevisa el formato del archivo."
  else:
    return f"The file must contain the following columns:\n{headers}\n\nCheck the file format."


def config_file_set_text (file_name, language):
  if language == "ES":
    file_name = 'estudiantes' if file_name == 'students' else 'actividades'
    return f"El archivo de configuración <b>{file_name}</b> aún no se ha cargado. Recuerda que lo debes subir con el mismo nombre."
  else:
    return f"The <b>{file_name}</b> configuration file has not yet been uploaded. Remember to upload it with the same name."


download_config_files_text = {
  "ES": "<b>Asistente para la configuración de la asignatura.</b>\n\nAntes de usar EDUtrack debes terminar de configurar la asignatura. Descarga y edita los siguientes archivos. Cuando los tengas listos enviámelos (súbelos) con el mismo nombre para guardarlos en la base de datos.",
  
  "EN": "<b>Subject configuration wizard.</b>\n\nBefore using EDUtrack you must finish configuring the subject. Download and edit the following files. When you have them ready, upload them with the same name to save them in the database."
}

def config_files_set_exist_DB(file_name, language):
  if language == "ES":
    elements = 'estudiantes' if "students" in file_name else 'actividades'
    return f"<b>Ya existe el archivo:</b>\nEl apartado de <b>{elements}</b> ya existe en la base de datos.\nPara agregar más {elements} renombra el archivo como <b>add_{file_name}</b>.\n\nPara reemplazar todo, renombra el archivo como <b>replace_{file_name}</b>.\nSi utilizas está última opción, la sección de calificaciones también se borrará, eliminando todas las calificaciones cargadas previamente."
  
  else:
    elements = 'students' if "students" in file_name  else 'activities'
    return f"<b>The file already exists:</b>\nThe <b>{elements}</b> section already exists in the database.\nTo add more {elements} rename the file as <b>add_{file_name}</b>.\n\nTo replace everything, rename the file as <b>replace_{file_name}</b>.\nIf you use the latter option, the grades section will also be cleared, deleting all previously loaded grades."


def config_files_send_document(language,elements):
  if language == "ES":
    if elements is 'students':
      return "files/guides/ES/students_format.csv"
    elif elements is 'activities':
      return "files/guides/ES/activities_format.csv"
    else:
      return "files/guides/ES/grades_format.csv" 
  
  else:
    if elements is 'students':
      return "files/guides/EN/students_format.csv"
    elif elements is 'activities':
      return "files/guides/EN/activities_format.csv" 
    else:
      return "files/guides/EN/grades_format.csv"     



config_files_ready_one_text = {
  "ES":"El archivo se ha cargado correctamente.",
  
  "EN": "The file is uploaded correctly."
}
"""
config_files_ready_both_text = {
  "ES" : "Ya he cargado ambos archivos. Espera un momento para crear el apartado de calificaciones.",
  "EN" : "I've already uploaded both files. Wait a moment to create the grades section."
}"""

def add_elements_ready_text (language, elements):
  if language == "ES":
    elements = "los nuevos estudiantes." if elements == 'students' else "las nuevas activiades."
    return f"Se han agregado con éxito {elements}"
  else:
    return f"Successfully added {elements}"


def add_elements_all_exists_text (language, elements):
  if language == "ES":
    elements = "Todos los estudiantes." if elements == 'students' else "Todas las activiades."
    return f"{elements} ya existen en la base  de datos. No se agregó ningún elemento."
  else:
    return f"All {elements} already exist in the database. No item was added."


def add_elements_duplicates (language, elements):
  if language == "ES":
    elements = "Los siguientes estudiantes" if elements == 'students' else "Las siguientes activiades"
    return f"{elements} ya existen en la base de datos:\n"
  else:
    return f"The following {elements} already exist in the database:\n"

add_elements_no_duplicates ={
  "ES" : "\n\nLos demás elementos se agregaron correctamente.",
  
  "EN" : "\n\nThe other elements were added correctly."
}


def teacher_message_registration_error_text(context, language, user):
  bot_username = context.bot.username
  if language == "ES":
    return f"Un usuario ha intentado usar el bot {bot_username} pero no está su username en la base de datos o no esta registrado entre los estudiantes.\n\nID: {user['_id']}\nTelegram_name: {user['telegram_name']}\nNickname: @{user['username']}\n\nSe le solicitó al usuario ingresar su email para el registro o ponerse en contacto con el docente."
    
  else:
    return f"A user has tried to use the bot {bot_username} but his username is not in the database or is not registered among the students.\nID: {user['_id']}\nTelegram_name: {user['telegram_name']}\nNickname: @{user['username']}\n\nThe user was asked to enter his/her email for registration or to contact the teacher."


def meeting(language, action, meeting_num="",active =""):
  if language == "ES":
    if action == "active":
      return f"No se puede iniciar otro meeting, actualmente está activo el meeting {meeting_num} en este planeta. Para iniciar otro primero debes finalizar el actual con el texto:\n == fin de meeting {meeting_num}."
    elif action == "no_number":
      if meeting_num:
        return f"<b>Meeting {meeting_num} activo.</b>\nPara iniciar o finalizar un meeting se debe escribir el número de meeting."
      else:
        return f"Para iniciar o finalizar un meeting se debe escribir el número de meeting."
    elif action == "finish_no_active":
      return f"El meeting actualmente activo es el meeting {meeting_num}. Meeting no finalizado."
    elif action == "none_active":
      return f"No hay ningún meeting activo."
  else:
    if action == "active":
      return f"Cannot start another meeting, currently meeting {meeting_num} is active on this planet. To start another first you must end the current one with the text:\n == end of meeting {meeting_num}."
    elif action == "no_number":
      if meeting_num:
        return f"<b>Meeting {meeting_num} active.</b>\nTo start or finish a meeting you must write the meeting number."
      else:
        return f"To start or finish a meeting you must write the meeting number."
    elif action == "no_active":
      return f"The currently active meeting is the meeting {meeting_num}. Meeting not finished."
    elif action == "none_active":
      return f"There is no active meeting."

### Menu ###
menu = {
  "ES" : {
    "opt" : [
          [IKButton("Opciones academicas",
              callback_data='t_menu-academic')],
          [IKButton("Comunicación virtual",
              callback_data='t_menu-vc')],
          [IKButton("Configurar asignatura",
              callback_data="t_menu-config")],
          [IKButton("Mensajes",
              callback_data='t_menu-msg')]#,
          #[IKButton("Cambiar Docente/Estudiante",
          #callback_data='t_menu-change')]
      ],
    "text" : '<b>MENU DOCENTE</b>\nSelecciona una opción:'
    },
  
  "EN" : {
    "opt" :[
          [IKButton("Academic Options",
              callback_data='t_menu-academic')],
          [IKButton("Virtual Communication",
              callback_data='t_menu-vc')],
          [IKButton("Configure Subject",
              callback_data="t_menu-config")],
          [IKButton("Messages",
              callback_data='t_menu-msg')]#,
          #[IKButton("Cambiar Docente/Estudiante",
          #callback_data='t_menu-change')]
      ],
    "text" : '<b>TEACHER MENU</b>\nSelect an option:'}
}


### Menu: Academic ###
menu_academic = {
  "ES" : {
    "opt" : [
      [IKButton("Actividades",
          callback_data='t_menu-academic-act')],
      [IKButton("Calificaciones y FRA",
          callback_data='t_menu-academic-grades')],
      [IKButton("Estudiantes",
          callback_data='t_menu-academic-stu')],
      [IKButton("Regresar",
          callback_data='t_menu-back')]
    ],
    "text" : '<b>OPCIONES ACADEMICAS</b>\nSelecciona una opción:'
    },
  
  "EN" : {
    "opt" : [
      [IKButton("Activities",
          callback_data='t_menu-academic-act')],
      [IKButton("Grades and ARF",
          callback_data='t_menu-academic-grades')],
      [IKButton("Students",
          callback_data='t_menu-academic-stu')],
      [IKButton("Back",
          callback_data='t_menu-back')]
    ],
    "text" : '<b>ACADEMIC OPTIONS</b>\nSelect an option:'}
}


### Menu: Academic - Activities ###
menu_academic_act = {
  "ES" : {
  "opt" : [
      [IKButton("Ver Lista",
          callback_data='t_menu-academic-act-view'),
      IKButton("Calificar",
          callback_data='t_menu-academic-act-grade')],
      [IKButton("Agregar ",
          callback_data='t_menu-academic-act-add'),
      IKButton("Modificar",
          callback_data='t_menu-academic-act-modify')],
      [IKButton("Eliminar",
          callback_data='t_menu-academic-act-delete'),
      IKButton("Regresar",
          callback_data='t_menu-academic')]
      ],
  "text" : '<b>ACTIVIDADES</b>\nSelecciona una opción:'
  },
  
  "EN" : {
    "opt" : [
      [IKButton("View List",
          callback_data='t_menu-academic-act-view')],
      [IKButton("Grade",
          callback_data='t_menu-academic-act-grade'),
      IKButton("Add",
          callback_data='t_menu-academic-act-add')],
      [IKButton("Modify",
          callback_data='t_menu-academic-act-modify'),
      IKButton("Delete",
          callback_data='t_menu-academic-act-delete')],
      [IKButton("Back",
          callback_data='t_menu-academic')]
      ],
    "text" : '<b>ACTIVITIES</b>\nSelect an option:'}
}



### Menu: Academic - Activities - List###

menu_academic_act_view = {
  "ES" : {
    "opt" : [
        [IKButton("Todas las Actividades",
            callback_data='t_menu-academic-act-view-all')],
        [IKButton("Actividades Calificables",
            callback_data='t_menu-academic-act-view-qualifying')],
        [IKButton("Regresar",
            callback_data='t_menu-academic-act')]
      ],
    "text" : "<b>VER LISTA DE ACTIVIDADES</b>\nSelecciona una opción:",
    "not_file" : "<b>VER LISTA DE ACTIVIDADES</b>\nNo se pudo crear el archivo de actividades."
    },
  
  "EN" : {
    "opt" : [
        [IKButton("All Activities",
            callback_data='t_menu-academic-act-view-all')],
        [IKButton("Qualifying Activities",
            callback_data='t_menu-academic-act-view-qualifying')],
        [IKButton("Back",
            callback_data='t_menu-academic-act')]
      ],
    "text" : "<b>VIEW ACTIVITIES LIST</b>\nSelect an option:",
    "not_file" : "<b>VIEW ACTIVITIES LIST</b>\nThe activities file couldn't be created."
    }
  }


### Menu: Academic - Activities - Grade ###
menu_academic_act_grade = {
  "ES" : {
    "opt" : [
      [IKButton("Subir archivo",
          callback_data='t_menu-academic-act-grade-upload')],
      [IKButton("Utilizar comando",
          callback_data='t_menu-academic-act-grade-cmd')],
      [IKButton("Regresar",
          callback_data='t_menu-academic-act')]
      ],
    "text": "<b>CALIFICAR</b>\nSelecciona una opción:",
    "upload" :  "Descarga este archivo como base para crear el archivo de calificaciones. Subelo con el mismo nombre para cargar las calificaciones.",
    "cmd" : "*CALIFICAR ACTIVIDAD*\nEscribe el comando\n/grade`_`activity <id actividad> <email estudiante> <calificación>;\n\nCada estudiante debe separarse con el signo punto y coma ';'\n\nEjemplo:\n/grade`_`activity Prueba`_`1\nejemplo@correo.ugr.es 8.5;\nejemplo2@gmail.es 9.6;\nejemplo3@hotmail.es 9"
    },
  
  "EN" : {
    "opt" : [
      [IKButton("Upload File",
          callback_data='t_menu-academic-act-grade-upload')],
      [IKButton("Use Command",
          callback_data='t_menu-academic-act-grade-cmd')],
      [IKButton("Regresar",
          callback_data='t_menu-academic-act')]
      ],
    "text" : "<b>GRADE</b>\nSelect an option:",
    "upload" : "Download this file as a basis for creating the grade file. Upload it with the same name to load the grades.",
    "cmd" : "*GRADE ACTIVITY:*\nType the command\n/grade`_`activity <activity> <student email> <grade>;\n\nEach student must separate with the semicolon sign ';'\n\nExample:\n/grade`_`activity Test`_`1\nexample@correo.ugr.es 8.5;\nexample2@gmail.es 9.6;\nexample3@hotmail.es 9"
    }
}




def grade_activity (language, action, students="", activity = "" ):
  if language == "ES":
    if action == "no_arguments":
      return f"El comando no tiene los argumentos necesarios."
    elif action == "no_activities_qualifying":
      return f"Aún no hay actividades calificables en la base de datos."
    elif action == "unregistered_email":
      if len(students.split("\n")) > 2:
        return  f"Los email de los estudiantes: {students}\n\nno se encuentran registrados."
      else:
        return f"El email del estudiante: {students}\n\nno se encuentra registrado."
    elif action == "grading_error":
      if len(students.split("\n")) > 2:
        return  f"La calificación de los estudiantes con el email: {students}\n\ndebe ser un numero entre 0 y 10. Su calificación no ha sido modificada."
      else:
        return f"La calificación del estudiante con el email: {students}\n\ndebe ser un numero entre 0 y 10. Su calificación no ha sido modificada."
    elif action == "no_grade":
      if len(students.split("\n")) > 2:
        return f"Falta la calificación en los estudiantes con el email: {students}\n\nSu calificación no ha sido modificada."
      else:
        return f"Falta la calificación en el estudiante con el email: {students}\n\nSu calificación no ha sido modificada."
    elif action == "no_students":
      return f"Debes agregar por lo menos un estudiante para calificar."
    elif action == "unregistered_activity":
      return f"La actividad con el id <b>{activity}</b> no se encuentra registrada."
    elif action == "no_semicolon":
      return f"Falto el signo punto y coma ';' despues del estudiante {students} por lo que no se registraron los estudiantes a partir de este."
    elif action == "email_syntax_error":
      if len(students.split("\n")) > 2:
        return f"Hay un error de sintaxis en el email de los estudiantes: {students}\n\nSu calificación no ha sido modificada."
      else:
        return f"Hay un error de sintaxis en el email del estudiante: {students}\n\nSu calificación no ha sido modificada."
    elif action == "successful_students":
      if len(students.split("\n")) > 2:
        return f"Se registraron correctamente las calificaciones de la actividad {activity} a los estudiantes:{students}"
      else:
        return f"Se registró correctamente la calificación de la actividad {activity} al estudiante: {students}"

  elif language == "EN":
    if action == "no_arguments":
      return f"The command doesn't have the necessary arguments."
    elif action == "no_activities_qualifying":
      return f"There are still no qualifying activities in the database."
    elif action == "unregistered_email":
      if len(students.split("\n")) > 2:
        return f"The email of the students: {students}\n\nare not registered."
      else:
        return f"The student with the email: {students}\n\nis not registered"
    elif action == "grading_error":
      if len(students.split("\n")) > 2:
        return  f"The grade of the students with the email: {students}\n\nmust be a number between 0 and 10. The grade has not been modified."
      else:
        return f"The grade of the student with the email {students}\n\nmust be a number between 0 and 10. The grade has not been modified."
    elif action == "no_grade":
      if len(students.split("\n")) > 2:
        return f"The grade is missing in the students with the email: {students}\n\nThe grade has not been modified."
      else:  
        return f"Student's grade is missing with email: {students}\n\nYour grade has not been modified."
    elif action == "no_students":
      return f"You must add at least one student to qualify."
    elif action == "unregistered_activity":
      return f"The activity with id <b>{activity}</b> is not registered."
    elif action == "no_semicolon":
      return f"The semicolon sign ';' was missing after the student {students} so we did not register students starting from this."
    elif action == "email_syntax_error":
      if len(students.split("\n")) > 2:
        return f"There is a syntax error in the students' email: {students}\n\nThe grade has not been modified."
      else:  
        return f"There is a syntax error in the student's email: {students}\n\nThe grade has not been modified."
    elif action == "successful_students":
      if len(students.split("\n")) > 2:
        return f"{activity} activity grades were correctly registered for students:{students}."
      else:
        return f"The grade of the activity {activity} was correctly registered to the student:{students}."


### Menu: Academic - Activities - Add ###
menu_academic_act_add_text ={
  "ES" : f"<b>AGREGAR ACTIVIDADES:</b>\nPara agregar actividades sube un archivo con el nombre <b>add_activities_format.csv</b> con el mismo formato de /activities_format.\n\nPara reemplazar el archivo de configuración de actividades, sube un archivo con el nombre <b>replace_activities_format.csv</b> con el formato /activities_format. <b>Ten en cuenta que hacer esto reemplazara la base de datos de calificaciones también</b>.",
  
  "EN" : f"<b>ADD ACTIVITIES:</b>\nTo add activities upload a file with the name <b>add_activities_format.csv</b> with the same format as /activities_format.\n\nTo replace the activity configuration file, upload a file named <b>replace_activities_format.csv</b> with the format /activities_format. <b>Note that doing this will replace the ratings database <also></also></b>."
}

### Menu: Academic - Activities - Modify ###

def menu_academic_act_modify_text (language, headers='\nAQUI LAS CABECERAS'):
  if language == 'ES':
    return f"*MODIFICAR ACTIVIDAD:*\nPara modificar una actividad escribe el comando /modify`_`activity <id actividad> <campo a modificar> <nuevo contenido>\n\nLos campos que puedes modificar son:{headers}\n\n<b>Ejemplos:</b>\n/modify_activity GLOSARIO weight .03 (Modifica el peso de la actividad)\n/modify`_`activity GLOSARIO week 4 (Modifica la semana de la actividad)"
  else:
    return f"*MODIFY ACTIVITY:*\nTo modify an activity type the command /modify`_`activity <id activity> <field to modify> <new content>\n\nThe fields you can modify are:{headers}\n\n<b>Example:</b>\n/modify`_`activity GLOSSARY weight .03 (modifies the activity weight)\n/modify_activity GLOSSARY week 4 (modify the activity week)."

### Menu: Academic - Activities - Delete ###
menu_academic_act_delete_text ={
  "ES" : f"*ELIMINAR ACTIVIDAD:*\nPara eliminar un a actividad escribe el comando /del`_`activity <id actividad>\n\n<b>Ejemplo:</b>\n/del_activity T1_GLOSARIO",
  
  "EN" : f"*DELETE ACTIVITY:*\nTo delete an activity type the command /del`_`activity <id activity>\n\n<b>Example:</b>\n/del_activity T1_GLOSSARY"
}

### Menu: Academic - Grades ###
menu_academic_grades_opt ={
  "ES" : [
    [IKButton("Ver calificaciones",
      callback_data='t_menu-academic-grades-view')],
    [IKButton("Factor de Riesgo",
      callback_data='t_menu-academic-grades-srf')],
    [IKButton("Regresar",
      callback_data='t_menu-academic')]
  ],
  
  "EN" : [
    [IKButton("View Grades",
      callback_data='t_menu-academic-grades-view')],
    [IKButton("Risk Factor",
      callback_data='t_menu-academic-grades-arf')],
    [IKButton("Back",
      callback_data='t_menu-academic')]
    ]
}

menu_academic_grades_text ={
  "ES" : "<b>CALIFICACIONES:</b>\nSelecciona una opción:",
  "EN" : "<b>GRADES:</b>\nSelect an option:"
}

### Menu: Academic - Grades - View List ###
menu_academic_act_grades_view_text ={
  "ES" : f"",
  "EN" : f""
}

### Menu: Academic - Grades - ARF ###
menu_academic_act_grades_arf_text ={
  "ES" : f"",
  "EN" : f""
}


### Menu: Academic - Students ###
menu_academic_stu_opt ={
  "ES" : [
    [IKButton("Ver lista",
        callback_data='t_menu-academic-stu-view'),
    IKButton("Agregar",
        callback_data='t_menu-academic-stu-add')],
    [IKButton("Modificar",
        callback_data='t_menu-academic-stu-modify'),
    IKButton("Eliminar",
        callback_data='t_menu-academic-stu-delete')],
    [IKButton("Regresar",
        callback_data='t_menu-academic')]
  ],
  
  "EN" : [
    [IKButton("View List",
        callback_data='t_menu-academic-stu-view'),
    IKButton("Add",
        callback_data='t_menu-academic-stu-add')],
    [IKButton("Modify",
        callback_data='t_menu-academic-stu-modify'),
    IKButton("Delete",
        callback_data='t_menu-academic-stu-delete')],
    [IKButton("Back",
        callback_data='t_menu-academic')]
  ]
}

menu_academic_stu_text ={
  "ES" : "<b>ESTUDIANTES:</b>\nSelecciona una opción:",
  "EN" : "<b>STUDENTS:</b>\nSelect an option:"
}

### Menu: Academic - Students - View List ###
menu_academic_stu_view_opt ={
  "ES" : [
    [IKButton("Ver archivo de estudiantes",
        callback_data='t_menu-academic-stu-view-file')],
    [IKButton("Ver estudiantes registrados",
        callback_data='t_menu-academic-stu-view-reg')],
    [IKButton("Regresar",
        callback_data='t_menu-academic-stu')]
  ],
  
  "EN" : [
    [IKButton("View students file",
        callback_data='t_menu-academic-stu-view-file')],
    [IKButton("View registered students",
        callback_data='t_menu-academic-stu-view-reg')],
    [IKButton("Back",
        callback_data='t_menu-academic-stu')]
  ]
}

menu_academic_stu_view_text ={
  "ES" : "<b>VER LISTA DE ESTUDIANTES:</b>\nSelecciona una opción:",
  "EN" : "<b>VIEW STUDENTS LIST:</b>\nSelect an option:"
}


### Menu: Academic - Students - View List - File ###
menu_academic_act_stu_view_file_text ={
  "ES" : f"",
  "EN" : f""
}

### Menu: Academic - Students - View List - Registered ###
menu_academic_act_stu_view_reg_text ={
  "ES" : f"",
  "EN" : f""
}

### Menu: Academic - Students - Add ###
menu_academic_act_stu_add_text ={
  "ES" : f"<b>AGREGAR ESTUDIANTES:</b>\nPara agregar estudiantes sube un archivo con el nombre <b>add_students_format.csv</b> con el mismo formato de /students_format.\n\nPara reemplazar el archivo de configuración de estudiantes sube un archivo con el nombre <b>replace_students_format.csv</b> con el formato /students_format. <b>Ten en cuenta que hacer esto reemplazara la base de datos de calificaciones tambien</b>.",
  
  "EN" : f"<b>ADD STUDENTS:</b>\nTo add students upload a file named <b>add_students_format.csv</b> with the same format as /students_format.\n\nTo replace the student configuration file upload a file named <b>replace_students_format.csv</b> with the format /students_format. <b>Note that doing this will replace the ratings database also </b>."
}

### Menu: Academic - Students - Modify ###
menu_academic_act_stu_modify_text ={
  "ES" : f"*MODIFICAR ESTUDIANTE:*\nPara modificar el nombre de un estudiante escribe el comando /modify_student <email del estudiante> <nuevo nombre completo> \n\n<b>Ejemplo:</b>\n/modify_student ejemplo@correo.ugr.es Fernando García Fernandez",
  
  "EN" : f"<b>MODIFY STUDENT:</b>\nTo modify a student's name type the command /modify_student <email of the student> <new full name> \n\n<b>Example:</b>\n/modify_student example@correo.ugr.es Jhon Smith"
}

### Menu: Academic - Students - Delete ###
menu_academic_act_stu_delete_text ={
  "ES" : f"*ELIMINAR ESTUDIANTE:*\nPara eliminar un estudiante escribe el comando /del`_`student  <email>\n\n<b>Ejemplo:</b>\n/del`_`student ejemplo@correo.ugr.es",
  
  "EN" : f"*DELETE STUDENT:*\nTo delete a student type the command /del`_`student <email>\n\n<b>Example:</b>\n/del`_`student example@correo.ugr.es"
}
### Menu: Virtual Com ###
menu_academic_vc_opt = {
  "ES" : [
    [IKButton("Ver miembros por planeta",
        callback_data='t_menu-vc-members')],
    [IKButton("Analítica por planeta",
        callback_data='t_menu-vc-planet')],
    [IKButton("Analítica para la asignatura",
        callback_data='t_menu-vc-subject')],
    #[IKButton("C.V. Por Meeting",
    #callback_data = 'vc-t_menu-meeting')],
    [IKButton("Regresar",
        callback_data='t_menu-back')]
  ],
  
  "EN" : [
    [IKButton("See Planet Members",
        callback_data='t_menu-vc-members')],
    [IKButton("Planet Analytics",
        callback_data='t_menu-vc-planet')],
    [IKButton("Subject Analytics",
        callback_data='t_menu-vc-subject')],
    #[IKButton("Meeting Analytics",
    #callback_data = 'vc-t_menu-meeting')],
    [IKButton("Regresar",
        callback_data='t_menu-back')]
  ]
}

menu_academic_vc_text ={
  "ES" : "<b>COMUNICACION VIRTUAL:</b>\nSelecciona una opción:",
  
  "EN" : "<b>VIRTUAL COMMUNICATION:</b>\nSelect an option:"
}


### Menu: Virtual Com - Planet Members ###
menu_academic_vc_planet_members_text ={
  "ES" : f"<b>VER MIEMBROS POR PLANETA:</b>\nSelecciona una opción:",
  
  "EN" : f"<b>VIEW PLANET MEMBERS:</b>\nSelect an option:"
}

menu_academic_vc_not_planet_text ={
  "ES" : f"<b>VER MIEMBROS POR PLANETA:</b>\nAún no se ha registrado ningún planeta.",
  "EN" : f"<b>VIEW PLANET MEMBERS:</b>\nNo planet has been registered yet."
}

### Menu: Virtual Com - Planet Analytics ###
menu_academic_vc_planet_analytics_text ={
  "ES" : f"<b>ANALITICA POR PLANETA:</b>\nSelecciona una opción:",
  "EN" : f"<b>PLANET ANALYTICS:</b>\nSelect an option:"
}

### Menu: Virtual Com - Subject Analytics ###
menu_academic_vc_subject_analytics_text ={
  "ES" : f"",
  "EN" : f""
}

### Menu: Virtual Com - Meeting Analytics ###
menu_academic_vc_meeting_analytics_text ={
  "ES" : f"",
  "EN" : f""
}


### Menu: Subject Config ###
menu_config_subject_text ={
  "ES" : f"",
  "EN" : f""
}

### Menu: Messages ###
menu_messages_text ={
  "ES" : f"",
  "EN" : f""
}


add_activity ={
  'ES' : {
    "_id" : "AGREGAR ACTIVIDAD:\n\nA continuación deberás escribir la siguiente información de la actividad:\n\nID\nNombre\nSección\nSemana\nPeso\n\nPuedes cancelar este proceso escribiendo el comando /cancel en cualquier momento.\n\nIniciemos escribiendo el Id de la actividad:",
    
    "name": "Escribe el nombre de la actividad:",

    "section" : "Muy bien, ahora escribe la sección:",

    "week" : "¿A que semana pertenece la actividad?\n(Debe ser un número entero)",

    "weight" : "¿Cuál es el peso de esta actividad?",

    "save" : "Se agregó la actividad con éxito."
  },

  'EN' : {
    '_id' : "ADD ACTIVITY:\n\nNext, you must write the following information about the activity:\n\nID\nName\nSection\nWeek\nWeight\n\nYou can cancel this process by typing the /cancel command at any time.\n\nLet's start by typing the activity ID :",

    "name": "Enter the activity name:",

    "section" : "All right, now write the section:",

    "week" : "What week does the activity belong to? (Must be a whole number)",

    "weight" : "What is the weight of this activity?",

    "save" : "Successful activity was added."
  }
}