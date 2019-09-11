import inspect
import sys
import configuration.config_file as cfg
from configuration.config_file import (
  db, client,
  teacher_data)
from functions import(
  general_functions as g_fun,
  teacher_functions as tea_fun,
  edutrack_functions as edu_fun,
  commands as cmd
)
from dictionaries import (
  #general_dict_lang as g_lang,
  teacher_dict_lang as tea_lang,
  #student_dict_lang as stu_lang
  )

def create_collections(user):
  """Verifica si el estudiante ya esta identificado pero aún no estaba registrado su planeta, o es un estudiante nuevo y se requieren crear todos los registros de él en la base de datos.
  
  """
  try:
    if user['_id'] not in cfg.identified_students:
      add_student_arf(user)
      add_student_autoevalution(user)
      add_student_eva_resources(user)
      add_student_eva_teacher(user)
      cfg.identified_students.add(user['_id'])
    if user['planet']:
      if user['planet'] not in cfg.created_planets:
        create_planet_collections(user)
      add_student_eva_collaboration(user)
      add_student_eva_virtual_com(user)
      add_student_global_collaboration(user)
      cfg.identified_students.discard(user['_id'])
    return True
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def create_planet_collections(user):
  """Añade un estudiante a las collecciones que no requieren tener el planeta registrado.
  
  """
  try:
    # Collaboration
    user_vc = {
      '_id': user["planet"],
      'members':{},
      'num_members':0
      }
    db.eva_collaboration.insert_one(user_vc)
    db.global_collaboration.insert_one(user_vc)
    
    # Virtual Communication
    user_vc.update({
      'messages': cfg.messages_type
      })  
    db.eva_virtual_com.insert_one(user_vc)

    
    user_vc['messages'] = {'meetings':{}}
    db.eva_vc_meetings.insert_one(user_vc)

    cfg.created_planets.add(user['planet'])
    
    return True
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


## Collections without planet
def add_student_arf(user):
  """ Añade un estudiante a la colección arf (Academic Risk Factor)."""
  try:
    db.arf.insert_one({
      '_id':user['_id'],
      'weeks':dict.fromkeys(cfg.weeks_array,"")
    })
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def add_student_arf_weekly(user):
  """Añade un estudiante a la colección arf semanal."""
  try:
    student = {'_id':user['_id']}
    student.update(dict.fromkeys(cfg.weeks_array))
    db.arf_weekly.insert_one(student)
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def add_student_autoevalution(user):
  """Añade un estudiante a la colección autoevaluación."""
  try:
    db.autoevaluation.insert_one({
      '_id' : user['_id'],
      'ready' : False,
      'questions': dict.fromkeys(cfg.autoeva_questions_list,0),
      'TOTAL' : 0
      })
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def add_student_eva_resources(user):
  """Añade un estudiante a la colección evaluación de recursos."""
  try:
    sections = sorted(list(cfg.activities_sections))
    add_activities = {'_id':user['_id']}
    
    for section in sections:
      resources = dict.fromkeys(db.activities.find({'section':section}).distinct('_id'),"")
      add_activities[section] = resources
    db.eva_resources.replace_one({'_id':user['_id']},add_activities,upsert=True)
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def add_student_eva_teacher(user):
  """Añade un estudiante a la colección evaluación docente."""
  try:
    db.eva_teacher.insert_one({'_id': user['_id']})
    for criterion in cfg.teacher_criteria:
      db.eva_teacher.update_one(
      {'_id': user['_id']},
      {'$set': {
        criterion: dict.fromkeys(cfg.weeks_array,"")
      }})
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False



## Collectons with planet
def add_student_eva_collaboration(user):
  """Añade un estudiante a la colección evaluación de la colboración entre compañeros.
  
  """
  #print("CHECK EDUFUN *** ENTRA A ADD STUDENT EVA COLLABORATION ***")
  try:
    if not db.eva_collaboration.find_one({'_id':user['planet'], f"members.{user['_id']}": {"$exists":True} }):
      members = db.eva_collaboration.find({'_id':user['planet']}).distinct('members')[0]
    db.eva_collaboration.update_one({'_id':user['planet']},
      {'$set':{
        f"members.{user['_id']}":{
          "classmates" : {},
          "valuations" : dict.fromkeys(cfg.weeks_array,[]),
          "tupla" : {
            'label':"",
            'alpha' : 0.0
            }}},
        '$inc': {'num_members':+1}})


    for member in members:
      db.eva_collaboration.update_one({'_id':user['planet']},{
        '$set':{
          f"members.{user['_id']}.classmates.{member}":{
            'weeks':dict.fromkeys(cfg.weeks_array,"")}}})
      db.eva_collaboration.update_one({'_id':user['planet']},{
        '$set':{
          f"members.{member}.classmates.{user['_id']}":{
            'weeks':dict.fromkeys(cfg.weeks_array,"")}}})

  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def add_student_global_collaboration(user):
  #print("CHECK EDUFUN *** ENTRA A ADD STUDENT GLOBAL COLLABORATION ***")
  try:

    if not db.global_collaboration.find_one({'_id':user['planet'], f"members.{user['_id']}": {"$exists":True} }):
      members = db.global_collaboration.find({'_id':user['planet']}).distinct('members')[0]

    db.global_collaboration.update_one({'_id':user['planet']},
      {'$set':{
        f"members.{user['_id']}":{
          "classmates" : {},
          "valuations" : [],
          "tupla" : {
            'label':"",
            'alpha' : 0.0
            }}},
        '$inc':{'num_members':+1} })


    for member in members:
      db.global_collaboration.update_one({'_id':user['planet']},{
        '$set':{
          f"members.{user['_id']}.classmates.{member}":{
            'value':""}}})
      db.global_collaboration.update_one({'_id':user['planet']},{
        '$set':{
          f"members.{member}.classmates.{user['_id']}":{
            'value':""}}})
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def add_student_eva_virtual_com (user):
  """Añade un estudiante a la colección evaluación de la comunicación virtual.
  
  """
  #print("CHECK EDU FUN ** ENTRO EN ADD_STUDENT_VIRTUAL_COM **")
  try:
    member = {user['_id']:cfg.messages_type}
    members = db.eva_virtual_com.find_one(
      {'_id': user['planet']})['members']
    members.update(member)
    db.eva_virtual_com.update_one(
      {'_id': user['planet']}, {
        "$set": {'members': members},
        "$inc":{'num_members':+1}
      })
  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False



##########################

def reg_messages(upm, user):
  try:
    #print("CHECK EDUFUN   ** ENTRO EN REG MESSAGES **")
    # Si no existe el estudiante crea el espacio para capturar sus mensajes
    message_type = ""
    if upm.text:
      message_type = 'TEXT'
    elif upm.photo:
      message_type = 'IMAGE'
    elif upm.video:
      message_type = 'VIDEO'
    elif upm.voice:
      message_type = 'VOICE'
    elif upm.sticker:
      message_type = 'STICKER'
    elif upm.document:
      type_document = upm.document.mime_type.split('/')
      type_document = type_document[0]
      if type_document == "video":
        message_type = 'GIF'
      elif type_document == "image":
        message_type = 'IMAGE'
      else:
        message_type = 'DOCUMENT'

    db.eva_virtual_com.update_one({'_id': user['planet']},{
      '$inc':{
        f"members.{user['_id']}.{message_type}":+1,
        f"members.{user['_id']}._TOTAL":+1,
        f"messages.{message_type}":+1,
        f"messages._TOTAL":+1,
      }})

    if cfg.active_meetings[user['planet']]:
      if cfg.active_meetings[user['planet']]['meeting']:
        reg_meeting_messages(upm, user, message_type)  
  except:
    g_fun.print_except(inspect.stack()[0][3])


def reg_meeting_messages (upm, user, message_type):
  meeting_data = cfg.active_meetings[user['planet']]
  
  meeting = meeting_data['meeting']

  ## Incrementar si existe un meeting activo.
  if not user['_id'] in cfg.active_meetings[user['planet']]['users']:
      add_student_eva_vc_meetings(user)

  if meeting in cfg.active_meetings[user['planet']]['meeting']:
        db.eva_vc_meetings.update_one({'_id': user['planet']},{
          '$inc':{
            f"members.{user['_id']}.meetings.{meeting}.{message_type}":+1,
            f"members.{user['_id']}.meetings.{meeting}._TOTAL":+1,
            f"messages.meetings.{meeting}.{message_type}":+1,
            f"messages.meetings.{meeting}._TOTAL":+1,
          }})
  else:
    add_meeting(user, meeting)



def add_student_eva_vc_meetings (user):
  """Añade un estudiante a la colección evaluación de la comunicación virtual.
  
  """
  try:
    meeting = cfg.active_meetings[user['planet']]['meeting']
    members = cfg.active_meetings[user['planet']]['users'].copy()
    db.eva_vc_meetings.update_one({'_id':user["planet"]},
    {
      '$set':{ f"members.{user['_id']}.meetings":{meeting:cfg.messages_type}},
      '$inc':{'num_members':+1}
    })
    cfg.active_meetings[user['planet']]['users'].add(user['_id'])
    if not db.eva_vc_meetings.find_one({'_id': user['planet'],f"messages.meetings.{meeting}":{'$exists':True}}):
      db.eva_vc_meetings.update_one({'_id':user["planet"]},
        {'$set':{
          f"messages.meetings.{meeting}":cfg.messages_type
        }})
      
      for member in members:
        ###### AQUI TENGO QUE REVISAR QUE SHOW CON LOS MEMBERS SI LLEGAN EN DICCIONARIO O QUE SHOW PARA ELEMINAR EL QUE ACABO DE AGREGAR Y METER EL MEETNG EN LOS DEMAS ESTUDIANTES.
        if meeting not in members[member]['meetings']:
          db.eva_vc_meetings.update_one({'_id':user["planet"]},
            {'$set':{
              f"members.{member}.meetings.{meetings_data['meeting']}":cfg.messages_type
            }})
      

  except:
    g_fun.print_except(inspect.stack()[0][3])
    return False


def add_meeting(user, meeting_data ):
  #if not db.eva_vc_meetings.find_one({'_id': user['planet'],f"messages.meetings.{meetings_data['meeting']}":{'$exists':True}}):
    if user['planet'] not in cfg.planet_meetings():
      db.eva_vc_meetings.update_one({'_id':user["planet"]},
        {'$set':{
          f"messages.meetings.{meetings_data['meeting']}":cfg.messages_type
        }})
      cfg.planet_meetings.update({user['planet']:{}})

    #if not db.eva_vc_meetings.find_one({'_id': user['planet'], f"members.{user['_id']}":{'$exists':True}}):


    if not db.eva_vc_meetings.find_one({'_id': user['planet'], 'members.'+user['_id']+'.meetings.'+meetings_data['meeting']:{'$exists':True}}):
  
      members = db.eva_vc_meetings.find({'_id': user['planet']}).distinct('members')[0]
      for member in members:
        if meetings_data['meeting'] not in members[member]['meetings']:
          db.eva_vc_meetings.update_one({'_id':user["planet"]},
            {'$set':{
              f"members.{member}.meetings.{meetings_data['meeting']}":cfg.messages_type
            }})



def meetings(upm, context, user, action = "start"):
  try:
    planet = g_fun.strip_accents(upm.chat['title'])
    chat_id = upm.chat_id
    meeting_text = (upm.text).split(' ')
    if len(meeting_text)==5:
      meeting_num = (upm.text).split(' ')[4]
      meeting = "meeting_" + meeting_num
      if action == "start":
        if planet not in cfg.active_meetings: 
          cfg.active_meetings.update({planet:{'users':{}, 'meeting':meeting}})
        elif meeting not in cfg.active_meetings[planet]['meeting']:
          cfg.active_meetings[planet].update({'meeting':meeting})
        else:
          g_fun.send_Msg(context, chat_id, tea_lang.meeting(user['language'],"active",meeting_num))

      elif action == "end":
        if cfg.active_meetings[planet]['meeting']:
          if meeting in cfg.active_meetings[planet]['meeting']:
            cfg.active_meetings[planet]['meeting'] = ""
          else:
            meeting_num = cfg.active_meetings[planet]['meeting'][-1]
            g_fun.send_Msg(context, chat_id, tea_lang.meeting(user['language'],"finish_no_active",meeting_num))
        else:
          g_fun.send_Msg(context, chat_id, tea_lang.meeting(user['language'],"none_active",meeting_num))
    else:
      if cfg.active_meetings[planet]['meeting']:
        meeting_num = cfg.active_meetings[planet]['meeting'][-1]
        g_fun.send_Msg(context, chat_id,
          tea_lang.meeting(user['language'], action ="no_number", meeting_num = meeting_num))
      else:
        g_fun.send_Msg(context, chat_id, tea_lang.meeting(user['language'],action ="no_number"))
  except:
    g_fun.print_except(inspect.stack()[0][3])