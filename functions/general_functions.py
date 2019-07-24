import re
from unicodedata import normalize
from configuration.config_file import (
  db, client, 
  teacher_data,
  is_config_files_set)
from dictionaries import (
  general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang,
  student_dict_lang as stu_lang
)


def basic_setup():
  # Inicializa al docente de la asignatura
  if not db.teachers.find_one():
      db.teachers.insert_one(teacher_data)
  config_file_set = True if (db.students.find_one() and db.activities.find_one()) else False


def strip_accents(string):
  """ Elimina los acentos de una cadena de texto y la devuelve en mayúsculas.

  """
  #print("   ENTRO A STRIP_ACCENTS")
  string = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize("NFD", string), 0, re.I)
  string = normalize('NFC', string)
  return string.upper()


def get_user_data(update, language=""):
  """Obtiene los datos del usuario.
  Devuelve un diccionario con los datos del Usuario:
    id
    telegram_name
    username
    planet
    is_teacher
    language

  """
  # print("CHECK GET USER DATA")
  chat_id = update._effective_chat.id
  user_data = update._effective_user
  if language:
    user_language = language
  else:
    language = db.telegram_users.find_one({'_id':str(user_data['id'])})['language']
  #print("*******",user)
  user = {
    '_id': str(user_data['id']),
    'telegram_name': str(user_data['first_name']),
    'username': "",
    'planet': "",
    'is_teacher': False,
    'language' : language
  }

  if user_data['last_name']:
    user['telegram_name'] += ' '+str(user_data['last_name'])
  if user_data['username']:
    user['username'] = str(user_data['username'])

  if db.teachers.find_one({'_id':user['_id']}):
    user['is_teacher'] = True
  else:
    user['is_teacher']  = False

  if db.students_full.find_one({'_id':user['_id']}):
    user['planet'] = db.students_full.find_one({'_id':user['_id']})['planet']
  if not user['planet'] and chat_id < 0 :
   if update.message.chat['title']:
    user_planet = strip_accents(str(update.message.chat['title']))
  db.telegram_users.save(user)

  #  if db.teachers.find_one(user_data['_id']):
  #    user_data['planet'] = "PRUEBAS_BOT"
  # print("~~~~~ USUARIO NUEVO",user)
  return user


def welcome(context,query, user):
  if user['is_teacher']:
    print("ES DOCENTE",user['language'])
    msg = tea_lang.welcome_text(context,user['language'])
  else:
    msg = stu_lang.welcome_text(context, user['language'])
  query.edit_message_text(
      parse_mode = 'HTML',
      text = msg)


def is_user_registered(update, context, user):
  """ Revisa si el estudiantes esta o no registrado en la base de datos.

  Regresa True si el estudiante esta registrado de lo contrario intenta registrarlo.
  """
  print("CHECK   ** ENTRO A IS STUDENT REGISTER **\n",user)
  chat_id = update._effective_chat.id
  
  ''' # No se en que momento utilizao esto
  if update.callback_query:
    data = update.callback_query.message
  else: 
    data = update.message '''
    
  # Registro del usuario en telegram_users
  user_db = db.telegram_users.find_one({'_id': user['_id']})
  if user != user_db:
    db.telegram_users.save(user)
    print("CHECK   Se actualizo el usuario en telegram_users")
    
  if user['is_teacher'] or chat_id <0:
    return True

  # Registro del estudiante en las demas colecciones
  if not db.students_full.find_one({'_id':user['_id']}):
    if db.students.find_one():
      if user['username']:
        if user['username'] != context.bot.username and not user['is_teacher']:
          print("AQUI")
          if db.students.find_one({'username': user['username']}):
            student_data = db.students.find_one({'username': user['username']})
            if not db.students_full.find_one({'_id': user['_id']}):
              db.students_full.insert_one(
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
              db.students_full.update_one(
                {'_id': user['_id']},
                {'$set': {
                  'email': student_data['_id'],
                  'telegram_name': user['telegram_name'],
                  'username': user['username'],
                  'planet': user['planet']
                }})
              #print("Se actualizo en FULL STUDENTS")

              """
              # ESTO SE COMENTO PARA QUE NO PIDIERA CORREO A LOS ESTUDIANTES PARA EL REGISTRO
              try:
                bot.sendMessage(parse_mode = 'HTML',chat_id = user['_id'], text= "Bienvenido al asistente EDUtrack +"botname+". Lo primero que tienes que hacer es resgistrarte primero escribiendo el siguiente comando:\n/user_register +e-mail\n\nEjemplo:\n/user_register ejemplo@correo.ugr.es\n\nDeberás utilizar el correo que tienes registrado en Prado.")
              except:
                print("   No se puedo entregar el mensaje al usuario por que no tiene agregado a EDUTRACK+"botname+")
              if update.message.chat_id < 0 or update.message.new_chat_members:
                bot.sendMessage(parse_mode = 'HTML',chat_id = update.message.chat_id, text= "Para tener acceso a las opciones de EDUtrack "+botname+", primero  debes registrarte desde una conversación privada. Si aún no me tienes en tus contactos buscame en Telegram como @"+bot_nickname")
                print("   Se le informa al usuario que primero debe registrarse.")

            # Si es un usuario registrado
            else:
              print("El usuario si esta registrado")
              db.students_full.update_one(
                {'_id':user['_id']},
                {"$set":{
                  'planet':user['planet']
                }}) """
            if user['planet']:
              create_planet_collections(user)
              if not db.eva_virtual_com.find_one({
                '_id': user['planet'],
                'members._id': user['_id']}):
                add_student_eva_virtual_com(user)
              if not db.eva_collaboration.find_one({
                '_id':user['planet'],
                'members.student_id':user['_id']}):
                add_student_eva_collaboration(user)
              if not db.global_collaboration.find_one({
                '_id':user['planet'],
                'members.student_id':user['_id']}):
                add_student_global_collaboration(user)
                #TODO: Aqui deberia de ir evaluación global para se creada.
            if not db.eva_teacher.find_one({'_id': user['_id']}):
              add_student_eva_teacher(user)
            if db.activities.find_one():
              if not db.eva_resources.find_one({'_id': user['_id']}):
                add_student_eva_resources(user)
            else:
              print("Aún no se configura el archivo de actividades. No se registro el estudiante", user['_id'])
            if meeting['active']:
              add_student_vc_meetings(user)
            #TODO: Aqui deberia de ir autoevaluacion para ser creada
            if upm.chat_id < 0:
              reg_messages(bot, upm, user)
            '''  TODO: NO BORRAR REVISAR CUANDO SE MANDA UN TEXTO CUALQUIERA CON EL BOT EN PRIVADO
            else:
              if is_config_files_set:
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
            print("Existe la db STUDENTS pero no esta el estudiante", user['_id'], "con el username",user['username'])
            context.bot.sendMessage(
              chat_id = user['_id'],
              parse_mode = 'HTML',
              text = "No te encuentras registrado como estudiante de la asignatura. Comunicate con tu docente.")
            print(user)
            context.bot.sendMessage(
              chat_id = "443344899",
              parse_mode = 'HTML',
              text = "El usuario ha intentado usar el bot pero no esta registrado\n"+
                  "\nID: "+user['_id']+
                  "\nTelegram_name: "+user['telegram_name']+
                  "\nNickname: "+user['username']+
                  "\nPlaneta: "+user['planet']
            )
            return False

      else:
        context.bot.sendMessage(
          chat_id=upm.chat_id,
          text = "Para utilizar el bot debes configurar un username/alias en tu cuenta de Telegram. Ve a ajustes en tu cuenta de Telegram y edita tu perfil para asignar un username/alias.")
        print("El usuario",user['_id'],"no tiene un username asociado a su cuenta de Telegram.")
        return False
    else:
      context.bot.send_message(
        chat_id=chat_id,
        text="Aún no se ha terminado de configurar la asignatura. Espera las indicaciones de tu docente.")
      print("Aún no existe la base de datos de estudiantes.")
      return False
  else:
    if db.students_full.update_one():
      user_db = db.students_full.update_one({'_id': user['_id']})
      if user_db != user:
        db.students_full.save(user)
        print("   Se actualizo el usuario en students_full")
      return True
    else:
      print("No existe la coleccion students_full")


def msg_wrong_command_group(update, context, user):
  print("CHECK WRONG COMMAND")
  chat_id = update._effective_chat.id
  context.bot.send_message(
        parse_mode = 'HTML',
        chat_id = chat_id,
        text = g_lang.wrong_command_group[user['language']])




if __name__ == '__main__':
    pass