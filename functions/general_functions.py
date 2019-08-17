import re
import os
import sys
import inspect
import pandas as pd
from unicodedata import normalize
import configuration.config_file as cfg
from configuration.config_file import (
  db, client,
  teacher_data,
  meeting)
from dictionaries import (
  general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang)
from functions import(
  teacher_functions as tea_fun
)


def basic_setup():
  """Inicializa las configuraciones básicas de EDUtrack.
  - Crea la colección de docente.
  - Crea los directorios necesarios.
  """
  try:
    if not db.teachers.find_one():
      db.teachers.insert_one(teacher_data)

    cfg.is_config_files_set = True if (
      db.students_file.find_one() and db.activities.find_one()) else False
    if db.activities.find_one():
      cfg.uploaded_activities = set(db.activities.find().distinct('_id'))
      cfg.qualifying_activities = set(db.activities.find({'weight':{'$gt':0}}).distinct('_id'))
    if db.students_file.find_one():
      cfg.uploaded_students = set(db.students_file.find().distinct('_id'))
    if db.registered_students.find_one():
      cfg.verified_students = set(db.registered_students.find().distinct('_id'))

    folders = ["./files/download", "./files/config"]
    for directory in folders:
      try:
        os.stat(directory)
      except:
        os.mkdir(directory)
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def send_Msg(context, chat_id, text, parse_mode='HTML'):
  """EDUtrack envía un mensaje al chat especificado.
  chat_id => ID a donde se enviará el mensaje.
  text => Texto del Mensaje.
  parse_monde => Formato del mensaje (HTML ó Markdown).
  
  """ 
  try:
    context.bot.sendMessage(
      chat_id=chat_id,
      parse_mode=parse_mode,
      text=text)
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def strip_accents(string):
  """Recibe un string y elimina los acentos y lo devuelve en mayúsculas."""
  # print("CHECK GFUN ENTRO A STRIP ACCENTS")
  try:
    string = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
            r"\1", normalize("NFD", string), 0, re.I)
    string = normalize('NFC', string)
    return string.upper()
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def get_user_data(update, language=""):
  """Obtiene los datos del usuario.Devuelve un diccionario con los datos del Usuario: {id, telegram_name, username, planet, is_teacher, language}.

  """
  # print("CHECK GFUN GET USER DATA")
  try:
    chat_id = update._effective_chat.id
    user_data = update._effective_user
    if language:
      user_language = language
    elif db.telegram_users.find_one({'_id': str(user_data['id'])}):
      language = db.telegram_users.find_one(
        {'_id': str(user_data['id'])})['language']
    else:
      language = "ES"
    # print("*******",user)
    user = {
      '_id': str(user_data['id']),
      'telegram_name': str(user_data['first_name']),
      'username': "",
      'planet': "",
      'is_teacher': False,
      'language': language
    }

    if user_data['last_name']:
      user['telegram_name'] += ' '+str(user_data['last_name'])
    if user_data['username']:
      user['username'] = str(user_data['username'])

    if db.teachers.find_one({'_id': user['_id']}):
      user['is_teacher'] = True
    else:
      user['is_teacher'] = False

    if db.registered_students.find_one({'_id': user['_id']}):
      user['planet'] = db.registered_students.find_one({'_id': user['_id']})[
        'planet']
    if not user['planet'] and chat_id < 0:
      if update.message.chat['title']:
        user_planet = strip_accents(str(update.message.chat['title']))
    db.telegram_users.save(user)

    #  if db.teachers.find_one(user_data['_id']):
    #    user_data['planet'] = "PRUEBAS_BOT"
    # print("~~~~~ USUARIO NUEVO",user)
    return user
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def welcome(context, query, user):
  """EDUtrack da la bienvenida al usuario dependiendo de su perfil."""
  # print("CHECK GFUN WELCOME")
  try:
    if user['is_teacher']:
      msg = tea_lang.welcome_text(context, user['language'])
    else:
      msg = stu_lang.welcome_text(context, user['language'])
    query.edit_message_text(
      parse_mode='HTML',
      text=msg)
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def is_user_registered(update, context, user):
  """ Revisa si el usuario esta o no registrado en la base de datos de estudiantes o docentes.

  Retorna True si el usuario esta registrado de lo contrario intenta registrarlo.

  """
  #  print("CHECK GFUN   ** ENTRO A IS USER REGISTER **\n")
  try:
    chat_id = update._effective_chat.id

    # Registro del usuario en telegram_users
    user_db = db.telegram_users.find_one({'_id': user['_id']})
    if user != user_db:
      db.telegram_users.save(user)

    if user['is_teacher']:
      return True

    # Revisa si hay cambios en el usuario
    if db.registered_students.find_one({'_id': user['_id']}):
      user_db = db.registered_students.find_one({'_id': user['_id']})
      user['name'] = user_db['name']
      user['email'] = user_db['email']
      difference = set(user.items()) - set(user_db.items())

      if difference:
        #REVISAR SI ESTO ACTUALIZA CORRECTAMENTE 
        db.registered_students.save(user)
        print("   Se actualizo el usuario en students_full")
      return True
    else:
      # Intenta registrar al usuario por su username, o le pide al usuario ingresar su email
      if db.students_file.find_one({"username": {'$exists': True}}):
        if user['username']:
          if user['username'] != context.bot.username:
            if db.students_file.find_one({'username': user['username']}):
              student_data = db.students_file.find_one(
                {'username': user['username']})
              # CAMBIO A A PARTIR DE AQUI
              print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~")
              print("CHECK REVISAR ESTO CUANDO SALGA")
              print("~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
              db.registered_students.save(
                {'_id': user['_id'],
                  'name': student_data['name'],
                  'email': student_data['_id'],
                  'dni': student_data['dni'],
                  'telegram_name': user['telegram_name'],
                  'username': user['username'],
                  'planet': user['planet'],
                  'is_teacher': user['is_teacher']
                })
              ''' 
        #### SE CAMBIO POR LO DE ARRIBA
                if not db.registered_students.find_one({'_id': user['_id']}):
          db.registered_students.insert_one(
                    {'_id': user['_id'],
                    'name': student_data['name'],
                    'email': student_data['_id'],
                    'dni': student_data['dni'],
                    'telegram_name': user['telegram_name'],
                    'username': user['username'],
                    'planet': user['planet'],
                    'is_teacher': user['is_teacher']
                    })
          print("CONTROL Se registro en FULL STUDENTS")
                else:
          db.registered_students.update_one(
                    {'_id': user['_id']},
                    {'$set': {
            'email': student_data['_id'],
            'telegram_name': user['telegram_name'],
            'username': user['username'],
            'planet': user['planet']
                    }})
          #print("Se actualizo en FULL STUDENTS") 
        '''

              """ 
        # ESTO SE COMENTO PARA QUE NO PIDIERA CORREO A LOS ESTUDIANTES PARA EL REGISTRO
          try:
                    bot.sendMessage(parse_mode = 'HTML',# = user['_id'], text= "Bienvenido al asistente EDUtrack +"botname+". Lo primero que tienes que hacer es resgistrarte primero escribiendo el siguiente comando:\n/user_register +e-mail\n\nEjemplo:\n/user_register ejemplo@correo.ugr.es\n\nDeberás utilizar el correo que tienes registrado en Prado.")
          except:
                    print("   No se puedo entregar el mensaje al usuario por que no tiene agregado a EDUTRACK+"botname+")
          if update.message.chat_id < 0 or update.message.new_chat_members:
                    bot.sendMessage(parse_mode = 'HTML',chat_id = update.message.chat_id, text= "Para tener acceso a las opciones de EDUtrack "+botname+", primero  debes registrarte desde una conversación privada. Si aún no me tienes en tus contactos buscame en Telegram como @"+bot_nickname")
                    print("   Se le informa al usuario que primero debe registrarse.")

                # Si es un usuario registrado
                else:
          print("El usuario si esta registrado")
          db.registered_students.update_one(
                    {'_id':user['_id']},
                    {"$set":{
            'planet':user['planet']
                    }}) 
        """
              if user['planet']:
                create_planet_collections(user)
                if not db.eva_virtual_com.find_one({
                  '_id': user['planet'],
                    'members._id': user['_id']}):
                  add_student_eva_virtual_com(user)
                if not db.eva_collaboration.find_one({
                  '_id': user['planet'],
                    'members.student_id': user['_id']}):
                  add_student_eva_collaboration(user)
                if not db.global_collaboration.find_one({
                  '_id': user['planet'],
                    'members.student_id': user['_id']}):
                  add_student_global_collaboration(user)
                  # TODO: Aqui deberia de ir evaluación global para se creada.
              if not db.eva_teacher.find_one({'_id': user['_id']}):
                add_student_eva_teacher(user)
              if db.activities.find_one():
                if not db.eva_resources.find_one({'_id': user['_id']}):
                  add_student_eva_resources(user)
              else:
                print(
                  "Aún no se configura el archivo de actividades. No se registro el estudiante", user['_id'])
              if meeting['active']:
                add_student_vc_meetings(user)
              # TODO: Aqui deberia de ir autoevaluacion para ser creada
              if upm.chat_id < 0:
                reg_messages(bot, upm, user)
              '''  TODO: NO BORRAR REVISAR CUANDO SE MANDA UN TEXTO CUALQUIERA CON EL BOT EN PRIVADO
        else:
                if cfg.is_config_files_set:
          bot.sendMessage(
                    chat_id=user['_id'],
                    parse_mode='HTML',
                    text='Escribe el comando /ayuda para ver la lista de comandos que puedes utilizar.')

                else:
          bot.sendMessage(
                    chat_id=user['_id'],
                    parse_mode='HTML',
                    text='Aún no se ha terminado de configurar la asignatura. Espera a que tu docente te de indicaciones.') '''
              return True
            else:
              send_Msg(
                context, chat_id, stu_lang.check_email_registration_text[user['language']], parse_mode="Markdown")
              teacher_list = db.teachers.find()
              for teacher in teacher_list:
                language = db.telegram_users.find_one(
                  {'_id': teacher['_id']})['language']
                send_Msg(context, teacher['_id'], tea_lang.teacher_message_registration_error_text(
                  teacher['language'], user))
              """ context.bot.sendMessage(
                chat_id = "443344899",
                parse_mode = 'HTML',
                text = "El usuario ha intentado usar el bot pero no esta registrado\n"+
                    "\nID: "+user['_id']+
                    "\nTelegram_name: "+user['telegram_name']+
                    "\nNickname: "+user['username']+
                    "\nPlaneta: "+user['planet']
        ) """
              return False
        else:
          send_Msg(context, chat_id,
                          stu_lang.no_username_text[user['language']])

          print(
            "El usuario", user['_id'], "no tiene un username asociado a su cuenta de Telegram.")
          return False

      else:
        send_Msg(
          context, chat_id, stu_lang.check_email_registration_text[user['language']], parse_mode="Markdown")

      ###################################################
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def received_message(update, context):
  """
  Recibe cada mensaje que se envía en EDUtrack que no sea comando o status_update.

  """
  try:
    print("\nCHECK GFUN ** ENTRO A RECEIVED_MESSAGE **")
    upm = update.message
    if upm.chat_id > 0:
      user = get_user_data(update)
      # Se revisa si se esta subiendo archivos de configuración
      try:
        if user['is_teacher']:
          if cfg.is_config_files_set and not upm.document:
            if upm.chat_id < 0 and upm.text:
              if "== inicio de meeting" in upm.text:
                meeting['active'] = True
                meeting['planet'] = strip_accents(
                  upm.chat['title'])
                meeting['number'] = "meeting_" + \
                  (upm.text).split(' ')[4]
                meetings_array.append(meeting['number'])
                print("______________________ ", upm.text,
                                    "del planeta", upm.chat['title'], "\n\n")
              elif "== fin de meeting" in upm.text:
                meeting['active'] = False
                meeting['planet'] = ""
                print("______________________SE FINALIZO EL MEETING ",
                                    upm.text, "del planeta", upm.chat['title'], "\n\n")
            else:
              print(
                "El docente escribió algo en un grupo fuera del meeting")
          elif upm.document:
            doc = upm.document
            if (doc.file_name == "students_format.csv" or
              doc.file_name == "activities_format.csv" or
              doc.file_name == "add_students_format.csv" or
              doc.file_name == "add_activities_format.csv" or
              doc.file_name == "replace_students_format.csv" or
              doc.file_name == "replace_activities_format.csv" or
                doc.file_name == "grades_format.csv"):

              if doc.file_name == "grades_format.csv":
                edit_grades(bot, update)
              elif (doc.file_name == "students_format.csv" or
                    doc.file_name == "activities_format.csv"):
                if ((doc.file_name == "students_format.csv" and
                    db.students_file.find_one()) or
                    (doc.file_name == "activities_format.csv" and
                    db.activities.find_one())):
                  send_Msg(context, user['_id'], tea_lang.config_files_set_exist_DB(
                    doc.file_name, user['language']))
                else:
                  tea_fun.upload_config_files(
                    update, context, user)
                  print("SALIO")
              else:
                tea_fun.upload_config_files(update, context, user)
                print("SALIO")
            # REVISAR DONDE VA
          else:
            send_Msg(
              context, upm.chat_id, tea_lang.not_config_files_set_text[user['language']], parse_mode="")
            tea_fun.config_files_set(update, context, user)
        else:
          if cfg.is_config_files_set:
            is_user_registered(update, context, user)
          else:
            send_Msg(context, upm.chat_id, stu_lang.not_config_files_set_text(
              context, user['language']))
      except:
        print("****\n*** Error RECEIVED_MESSAGE\n",
                    sys.exc_info()[0], " ***")
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def csv_to_mongodb(update, context, user, collection, file, add_elements=False):
  """Recibe el path de un archivo ".csv" y almacena su contenido en la base de datos.    """
  try:
    print("CHECK GFUN ** CSV TO MONGODB **")
    chat_id = update._effective_chat.id
    delete_blank_lines(file)
    df = pd.read_csv(file, sep=",")
    if not add_elements:
        if collection.find_one():
            collection.drop()
    else:
      elements = 'students' if 'students' in file else 'activities'
      upload_elements = set(df['_id'].tolist())
      db_elements = set(collection.find().distinct('_id'))
      duplicates = upload_elements.intersection(db_elements)
      new_elements = upload_elements.difference(db_elements)

      for element in duplicates:

        df = df.drop(df[df.loc[:, '_id'] == element].index)
      if df.empty:
        send_Msg(context, chat_id, tea_lang.add_elements_ready_text(
          user['language'], elements))
      else:
        duplicates_list = tea_lang.add_elements_duplicates(
          user['language'], elements)
        if duplicates:
          for element in duplicates:
            duplicates_list += "\n"+element
          send_Msg(context, chat_id, duplicates_list)

    collection.insert(df.to_dict('records'))
    if 'students' in file:
      cfg.uploaded_students = set(df['_id'].tolist())
    else:
      cfg.uploaded_activities = set(df['_id'].tolist())
      cfg.qualifying_activities = set(db.activities.find({'weight':{'$gt':0}}).distinct('_id'))
    return True
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def delete_blank_lines(file):
  """Recibe el path de un archivo ".csv" y elimina las líneas en blanco."""
  print("CHECK GFUN DELETE BLANK LINES")
  try:
    df = pd.read_csv(file, sep=",")
    df.dropna(subset=['_id'], inplace=True)
    df.to_csv(file, sep=',', index=False)
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


def remove_file(file):
  """Recibe el path de un archivo y sí existe lo elimina así como su versión html.

  """
  try:
    print("CHECK GFUN REMOVE FILES")
    if os.path.isfile(file):
      os.remove(file)
    file = file[:-4] + ".html"
    if os.path.isfile(file):
      os.remove(file)
  except:
    print(f"*****\nERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n*****")


if __name__ == "__main__":
  pass

# TODO: CHECAR EL REGISTRO DEL ESTUDIANTE
# CHECAR LO DE EL MAIL  Y LO DE SUBIR EL ARCHIVO CON ALIAS
# PERMITIR REGISTRAR ESTUDIANTES SIN CORREO
