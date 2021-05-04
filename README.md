[Spanish Version](#bot-edutrack)

# EDUtrack Bot 
EDUtrack es parte de un proyecto de Tesis para evaluar la calidad de la educación superior en un entorno FC-ML de la Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación (ETSIIT) de la Universidad de Granada.

# ¿Qué es EDUtrack?
EDUtrack es un bot para Telegram con una interface en inglés y español. Se emplea principalmente como instrumento de comunicación con el estudiante, pero está preparado para obtener métricas de evaluación de la experiencia docente que ayudan a la evaluación de la calidad de la educación superior en un entorno de metodologías combinadas, "Flipped Classroom" y "M-Learning", denominado entorno FC-ML. Así mismo proporciona un medio de detección temprana del fracaso académico. 

## Tabla de contenidos:
---

- [Comenzando 🚀](#comenzando-)
- [Pre-requisitos :wrench:](#pre-requisitos-)
- [Configuración :gear:](#configuración-)
- [Despliegue 📦](#despliegue-)
- [Construido con 🛠️](#construido-con-)
- [Contribuyendo 🖇️](#contribuyendo-)
- [Wiki 📖](#wiki_)
- [Versionado 📌](#versionado-)
- [Autores ✒️](#autores-)
- [Licencia 📄](#licencia-)
- [Expresiones de Gratitud 🎁](#expresiones-de-gratitud-)

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **- [Despliegue](#despliegue-)** para conocer como desplegar el proyecto.

### Pre-requisitos 📋

Para configurar una instancia de EDUtrack se requiere
- Python 3.7 o superior
- SQLite
- Una cuenta de Telegram

### Configuración 🔧
La configuración de EDUtrack se puede desarrollar en 3 pasos

#### 1.- Crea un bot para instanciar EDUtrack
Primero se debe crear un bot desde <a href="https://t.me/Botfather" target="_blank">@BotFather</a>. Al finalizar te proporcionara un enlace que podras compartir a otros usuarios para que interactuen con el bot. Y por otra parte te proporcionara el _**TOKEN**_ de tu bot, que es la clave con la cual se realizara la conexión entre el bot que acabas de crear y EDUtrack.

![](Versiones_overleaf/Token.png)
   
```
Ejemplo:
Enlace: t.me/Subject_2021_bot
TOKEN: 1401345537:AAGPGnsIeRROS6500fm2bGPOGqz8kkD9O28
```

#### 2.- Configurar la instancia de EDUtrack
Para configurar los archivos de EDUtrack se puede realizar de 2 formas:
1. A través de <a href="https://t.me/EDUtrack_setup_bot" target="_blank">@EDUtrack_setup</a>, que es un bot que solicita la información general para EDUtrack, por ejemplo nombre del docente y de la asignatura, duración del curso o el Token del bot que nos proporciono BotFather en el paso anterior. Al finalizar EDUtrack_setup_bot nos proporcionara 2 archivos iguales, `edutrack_bot.zip` y `edutrack_bot.tar`, para descargar el que se adecue para nuestras necesidades.
    
2. Clonar el repositorio o descargar el zip desde GitHub

```
# Clonar GitHub CLI
gh repo clone jeovani-morales/EDUtrack_bot

# Clonar HTTPS
$ git clone https://github.com/jeovani-morales/EDUtrack_bot

```
Presiona **`Enter`** para crear tu clon local.
```
> Cloning into 'EDUtrack_bot'...
> remote: Enumerating objects: 868, done.
> remote: Counting objects: 100% (81/81), done.
> remote: Compressing objects: 100% (67/67), done.
> remote: Total 868 (delta 36), reused 52 (delta 14), pack-reused 787
> Receiving objects: 100% (868/868), 5.06 MiB | 7.77 MiB/s, done.
> Resolving deltas: 100% (501/501), done.
```

Ahora deberás editar manualmente el archivo de configuración `config_file.py` que se encuntra en el direcotorio EDUrack_bot/config.
```
# Ubuntu 
nano EDUtrack_bot/config/config_file.py

# Windows CMD o Power Shell
notepad EDUtrack_bot/config/config_file.py
```
```
# config_file.py
#===========================================
# Data to modify
#=========================================

subject_data = {
  "_id": "replace subject_id", # Database name
  "name": "replace subject_name",
  "start_date": "replace start_date", # format dd/mm/yyyy
  "course_weeks": "replace num_weeks", # Number of weeks of the course excluding vacation weeks
  "start_vacations" : "replace start_vacations", # format dd/mm/yyyy
  "end_vacations": "replace end_vacations", # format dd/mm/yyyy
  "max_final_grade": "replace max_final_grade", # Highest grade a student can get
  "max_activity_grade": "replace max_activity_grade", # Maximum qualification that an activity can get
  "min_grade_to_pass": "replace min_grade_to_pass", # Minimum grade a student must get in order not to fail
  "min_ideal_grade": "replace min_ideal_grade", # A student's ideal grade should be a value between max_final_grade and min_grade_to_pass+1. See the manual for more information on this note.
  "activate_evaluations:": "0", # Don´t modify
  "active_planet_registry": "1", # Don´t modify
  "maintenance": "0", # Don´t modify
  "ignore_categories": set(), # Don´t modify
}

teacher_data = {
  "email": "replace email", # teacher email
  "name": "replace teacher_name", 
  "telegram_name": "replace telegram_name", 
  "username": "replace username",
  "telegram_id": "replace _id", # To know the teacher's id visit @userinfobot on Telegram from the teacher's account.
  "language": "replace language", # es for Spanish, en for english
  "is_teacher": 1, # Don´t modify
}
```
Para poner en marcha de forma local se debe tener previamente instalado Python en su version 3.7 o superior y SQLite. Se recomienda crear un entorno virtual previamente para instalar las librerias requeridas que se encuentran en el archivo `requirements.txt`:
- coloroma: Permite mostrar el texto de errores en color para su fácil identificación en las pruebas.
- pandas: Manejo y análisis de estructura de datos
- python-telegram-bot: Interfaz para conectar Python con la API Bot Telegram

Desde la consola en el directorio del EDUtrack_bot ejecutar:

```
pip install -r requirements.txt
python3 edutrack.py

```

### 3. Terminar de configurar su bot EDUtrack
Para finalizar la configuración de EDUtrack bot se deberá:
* Crear los planetas (grupos de telegram) y asignar el bot creado como administrador en cada uno de ellos, esto es de suma importancia ya que solo como administrador el bot tendra acceso a contabilizar los mensajes de los estudiantes.

><span style="color:red"> **NOTA IMPORTANTE:** Al crear los planetas se ofrece la opción  **Historial del chat para nuevos miebros** que por default esta como `**HIDDEN**` si se cambia por `**VISIBLE**`, Telegram modifica el estatus de grupo a supergrupo  por lo que los administradores previamente dados de alta se resetearan, es una cuestion de Telegram, por lo que es necesario volver a dar de alta al bot como administrador.

* Tras crear los planetas y asignar su bot como adminsitrador iniciar una conversación con el bot creado anteriormente, este le enviara 2 archivos, **`students_format.csv`** y **`activities_format.csv`** que son los formatos que se deberán llenar y subir para terminar de configurar la asignatura. Tras subir los archivos los estudiantespodran acceder a su bot instancia de EDUtrack .

## Despliegue en Heroku 📦
Para realizar el despliegue en Heroku se debe de contar con 2 archivos (los cuales ya se encuentran en el repositorio) Procfile (asegúrarse de que no tiene ninguna extensión de archivo como .txt detrás, porque no funcionará):
```
web: python3 bot.py

requirements.txt
```
y `**requirements.txt**`
```
colorama==0.4.3
pandas==1.1.2
python-telegram-bot==12.7
```

### Crear una webapp en Heroku
1. Inicie sesión/cree una cuenta en Heroku.
2. Instala la CLI de Heroku. Si no tienes Git instalado, primero instala Git antes de proceder con la CLI de Heroku.

3. Una vez instalado, puedes utilizar el comando heroku en tu terminal/símbolo del sistema. Ve al mismo directorio que tus archivos de EDUtrack bot, y escribe:

```heroku login```



### 1. Despligue con Heroku CLI
### 2. Despliegue con un contenedor Docker y Heroku 


## Construido con 🛠️

* [Python](https://www.python.org/)
* [Python Telegram Bot] (https://maven.apache.org/) - Libreria que proporciona la interface con [Telegram API Bot](https://core.telegram.org/bots/api)
* [SQLite](https://www.sqlite.org/index.html) - Motor de Base de Datos

## Autores ✒️

* [<img src="Versiones_overleaf/ORCID_logo.png" alt="ORCID" width="20"/>](https://orcid.org/0000-0003-4507-3150) [**Jeovani M. Morales Nieto**](https://github.com/jeovani-morales/) - *Doctorando Desarrollador*
* [<img src="Versiones_overleaf/ORCID_logo.png" alt="ORCID" width="20"/>](https://orcid.org/0000-0002-0183-044X) [**Rosana Montes Soldado**](https://dasci.es/personal/perfil/rosana-montes-soldado/) - *Directora de Tesis y Asesora*  
* [<img src="Versiones_overleaf/ORCID_logo.png" alt="ORCID" width="20"/>](https://orcid.org/0000-0002-7283-312X) [Francisco Herrera Triguero](https://dasci.es/personal/perfil/francisco-herrera-triguero/) - *Director de Tesis*

También puedes mirar la lista de todos los [contribuyentes](https://github.com/your/project/contributors) quíenes han participado en este proyecto.



## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

 

## Licencia 📄
Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* etc.



---
⌨️ con ❤️ por [Villanuevand](https://github.com/Villanuevand) 😊