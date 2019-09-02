import inspect
import sys
import configuration.config_file as cfg
from configuration.config_file import (
  db, client,
  teacher_data,
  meeting)
from functions import(
  teacher_functions as tea_fun,
  edutrack_functions as edu_fun,
  commands as cmd
)


def create_collections(user):
  """Verifica si el estudiante ya esta identificado pero aún no estaba registrado su planeta, o es un estudiante nuevo y se requieren crear todos los registros de él en la base de datos.
  
  """
  try:
    if user['_id'] not in cfg.identified_students:
      add_student_arf(user)
      add_student_arf_weekly(user)
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
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


def create_planet_collections(user):
  """Añade un estudiante a las collecciones que no requieren tener el planeta registrado.
  
  """
  try:
    #student = {'_id':user['_id'], 'planet':user['planet']}
    #student.update(cfg.messages_type)
    #db.eva_collaboration.insert_one(student)
    if user['planet'] not in cfg.created_planets:
      
      # Evaluating Collaboration 
      db.eva_collaboration.insert_one({
      '_id':user['planet'],
      'members':[]})

      # Virtual Communication
      # db.eva_virtual_com.insert_one(student)
      db.eva_virtual_com.insert_one({
      '_id': user["planet"],
      'members':[],
      'num_members':0,
      'messages': cfg.messages_type,
      'TOTAL':0})
      print("   Se creo el planeta",user['planet'],"en eva_virtual_com")

    
      # Global collaboration
      #db.global_collaboration.insert_one(student)
      db.global_collaboration.insert_one({
      '_id':user['planet'],
      'members':[]})
    
      cfg.created_planets.add(user['planet'])
    
    return True
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


## Collections without planet
def add_student_arf(user):
  """ Añade un estudiante a la colección arf (Academic Risk Factor)."""
  try:
    db.arf.insert_one({
      '_id':user['_id'],
      'risk_factor':0,
      'risk_factor_linguistic':'',
      'potencial_recovery_score':0
    })
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


def add_student_arf_weekly(user):
  """Añade un estudiante a la colección arf semanal."""
  try:
    student = {'_id':user['_id']}
    student.update(dict.fromkeys(cfg.weeks_array))
    db.arf_weekly.insert_one(student)
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
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
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


def add_student_eva_resources(user):
  """Añade un estudiante a la colección evaluación de recursos."""
  try:
    sections = sorted(list(cfg.activities_sections))
    add_activities = {'_id':user['_id']}
    #db.eva_resources.insert_one({'_id': user['_id']})
    #print("ACTIVITIES SECTION", cfg.activities_sections)
    
    for section in sections:
      resources = dict.fromkeys(db.activities.find({'section':section}).distinct('_id'),"")
      add_activities[section] = resources
    db.eva_resources.replace_one({'_id':user['_id']},add_activities,upsert=True)
    
    """ for section in cfg.activities_sections:
      resources = db.activities.find({'section': section}, {'_id': 1})
      section_resources = {}
      for resource in resources:
        section_resources[resource['_id']] = ""
        print("      CONTROL R",resource['_id'])
      print("CONTROL section_resources",section_resources)
      db.eva_resources.update_one(
        {'_id': user['_id']},
        {'$set': {
          section: section_resources
        }}) """
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
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
    print("Se agrego el estudiante " +
      user['_id']+" a la base de datos eva_teacher")
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False



## Collectons with planet
def add_student_eva_collaboration(user):
  """Añade un estudiante a la colección evaluación de la colboración entre compañeros.
  
  """
  #print("CONTROL ENTRA A ADD STUDENT EVA COLLABORATION",user)
  try:
    members = db.eva_collaboration.find({'_id':user['planet']}).distinct('members.student_id')
    print("MEMBERS1", members)
    """  members = db.eva_collaboration.find_one(
        {'_id':user['planet']},
        {'_id':0, 'members.student_id':1})
    print("MEMBERS2", members) """
    db.eva_collaboration.update_one(
      {'_id':user['planet']},
      {'$push':{
        'members' : {
          'student_id' : user['_id'],
          'classmates' : [],
          'valuations' : dict.fromkeys(cfg.weeks_array,[]),
          'tupla' : {
            'label' : "",
            'alpha' : 0.0
          }}}})
    for member in members:
      db.eva_collaboration.update_one({'_id':user['planet'], 'members.student_id':user['_id']},{
      '$push':{
        'members.$.classmates':{
          'classmate_id':member,
          'weeks':dict.fromkeys(cfg.weeks_array,"")
          }}})
      db.eva_collaboration.update_one({'_id':user['planet'], 'members.student_id':member},{
        '$push':{
          'members.$.classmates':{
            'classmate_id': user['_id'],
            'weeks': dict.fromkeys(cfg.weeks_array, "")
          }}})    
    """ for member in members['members']:
      db.eva_collaboration.update_one({'_id':user['planet'], 'members.student_id':user['_id']},{
      '$push':{
        'members.$.classmates':{
          'classmate_id':member['student_id'],
          'weeks':dict.fromkeys(cfg.weeks_array,"")
          }}})
      db.eva_collaboration.update_one({'_id':user['planet'], 'members.student_id':member['student_id']},{
        '$push':{
          'members.$.classmates':{
            'classmate_id': user['_id'],
            'weeks': dict.fromkeys(cfg.weeks_array, "")
          }}}) """
    print("Se ha registrado el usuario", user['_id'], "en eva_collaboration")
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False


def add_student_eva_virtual_com (user):
  """Añade un estudiante a la colección evaluación de la comunicación virtual.
  
  """
  #print("CONTROL ** ENTRO EN ADD_STUDENT_VIRTUAL_COM")
  if not db.teachers.find_one(user['_id']):
    try:
      member = {'_id': user['_id']}
      member.update(cfg.messages_type)
      #print("CONTROL MEMBER", member)
      members = db.eva_virtual_com.find_one(
        {'_id': user['planet']})['members']
      members.append(member)
      #print("CONTROL MEMBERSSSS",members)
      num_members = db.eva_virtual_com.find_one(
        {'_id': user['planet']})['num_members']+1
      db.eva_virtual_com.update_one(
        {'_id': user['planet']}, {
          "$set": {
            'members': members,
            'num_members': num_members
          }})
      print("   Se agrego el estudiante ", user['_id'],"en el planeta",user['planet'],"en eva_virtual_com")
    except:
      print(f"\n**********\n\
        ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
        {sys.exc_info()[0]}\n\
        {sys.exc_info()[1]}\n**********\n")
      return False


def add_student_global_collaboration(user):
  #print("CONTROL ENTRA A ADD STUDENT GLOBAL COLLABORATION")
  try:
    members = db.global_collaboration.find_one(
        {'_id':user['planet']},
        {'_id':0, 'members.student_id':1})
    db.global_collaboration.update_one(
      {'_id':user['planet']},
      {'$push':{
        'members' : {
          'student_id' : user['_id'],
          'classmates' : [],
          'valuations' : [],
          'tupla' : {
            'label' : "",
            'alpha' : 0.0
          }}}})
    for member in members['members']:
      db.global_collaboration.update_one({'_id':user['planet'], 'members.student_id':user['_id']},{
      '$push':{
        'members.$.classmates':{
          'classmate_id':member['student_id'],
          'value':""
          #'weeks':dict.fromkeys(cfg.weeks_array,"")
          }}})
      db.global_collaboration.update_one({'_id':user['planet'], 'members.student_id':member['student_id']},{
        '$push':{
          'members.$.classmates':{
            'classmate_id': user['_id'],
            'value' : ""
            #'weeks': dict.fromkeys(cfg.weeks_array, "")
          }}})
    print("Se ha registrado el usuario", user['_id'], "en global_collaboration")
  except:
    print(f"\n**********\n\
      ERROR IN FUNCTION {inspect.stack()[0][3]}\n\
      {sys.exc_info()[0]}\n\
      {sys.exc_info()[1]}\n**********\n")
    return False

##########################

def reg_messages(upm, context, user):
  print("\n   ** ENTRO EN REG_MESSAGES **")
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
    print("DOCUMENT")
    type_document = upm.document.mime_type.split('/')
    type_document = type_document[0]
    if type_document == "video":
      message_type = 'GIF'
    elif type_document == "image":
      message_type = 'IMAGE'
    else:
      message_type = 'DOCUMENT'

  inc_message_type(user, message_type)


def inc_message_type(user, message_type):
  members = db.eva_virtual_com.find_one(
  {'_id': user['planet'], 'members._id': user['_id']})['members']
  count = 0
  for member in members:
    if member['_id'] == user['_id']:
      db.eva_virtual_com.update_one(
        {
          '_id': user['planet'],
          'members._id': user['_id']
        },
        {
          '$inc': {'members.'+str(count)+'.'+message_type: +1, 'members.'+str(count)+'.'+'_TOTAL': +1}
        })
      break
    count += 1
  # Aumenta el contador para el total del planeta
  db.eva_virtual_com.update_one(
    {'_id': user['planet']}, {
      '$inc': {message_type: +1, '_TOTAL': +1}
    })


