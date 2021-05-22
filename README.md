[Spanish Version](#bot-edutrack)

# EDUtrack Bot

EDUtrack es parte de un proyecto de Tesis para evaluar la calidad de la educación superior en un entorno FC-ML de la Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación (ETSIIT) de la Universidad de Granada.

# ¿Qué es EDUtrack?

EDUtrack es un bot para Telegram con una interface en inglés y español. Se emplea principalmente como instrumento de comunicación con el estudiante, pero está preparado para obtener métricas de evaluación de la experiencia docente que ayudan a la evaluación de la calidad de la educación superior en un entorno de metodologías combinadas, "Flipped Classroom" y "M-Learning", denominado entorno FC-ML. Así mismo proporciona un medio de detección temprana del fracaso académico.

## Tabla de contenidos:

---

- [EDUtrack Bot](#edutrack-bot)
- [¿Qué es EDUtrack?](#qué-es-edutrack)
  - [Tabla de contenidos:](#tabla-de-contenidos)
  - [Comenzando 🚀](#comenzando-)
    - [Pre-requisitos 📋](#pre-requisitos-)
    - [Configuración 🔧](#configuración-)
      - [1.- Crea un bot para instanciar EDUtrack](#1--crea-un-bot-para-instanciar-edutrack)
      - [2.- Configurar la instancia de EDUtrack](#2--configurar-la-instancia-de-edutrack)
    - [3. Terminar de configurar su bot EDUtrack](#3-terminar-de-configurar-su-bot-edutrack)
  - [Despliegue en Heroku 📦](#despliegue-en-heroku-)
    - [Antes del despliegue:](#antes-del-despliegue)
      - [1.- Instala los prerequisitos](#1--instala-los-prerequisitos)
      - [2.- Iniciar Sesión en Heroku](#2--iniciar-sesión-en-heroku)
      - [3.- Crear una webapp en Heroku](#3--crear-una-webapp-en-heroku)
      - [4.- Establecer las variables de entorno](#4--establecer-las-variables-de-entorno)
    - [Despliegue con Heroku CLI](#despliegue-con-heroku-cli)
    - [Despliegue con un contenedor Docker y Heroku](#despliegue-con-un-contenedor-docker-y-heroku)
  - [Construido con 🛠️](#construido-con-️)
  - [Autores ✒️](#autores-️)
  - [Contribuyendo 🖇️](#contribuyendo-️)
  - [Wiki 📖](#wiki-)
  - [Versionado 📌](#versionado-)
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

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/Token.png)

```textfile
Ejemplo:
Enlace: t.me/Subject_2021_bot
TOKEN: 1401345537:AAGPGnsIeRROS6500fm2bGPOGqz8kkD9O28
```

#### 2.- Configurar la instancia de EDUtrack

Para configurar los archivos de EDUtrack se puede realizar de 2 formas:

1. A través de <a href="https://t.me/EDUtrack_setup_bot" target="_blank">@EDUtrack_setup</a>, que es un bot que solicita la información general para EDUtrack, por ejemplo nombre del docente y de la asignatura, duración del curso o el Token del bot que nos proporciono BotFather en el paso anterior. Al finalizar EDUtrack_setup_bot nos proporcionara 2 archivos iguales, `edutrack_bot.zip` y `edutrack_bot.tar`, para descargar el que se adecue para nuestras necesidades.

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/edutrack_setup.png)

2. Clonar el repositorio o descargar el zip desde GitHub

```bash
$ git clone https://github.com/jeovani-morales/EDUtrack_bot
```

Presiona **`Enter`** para crear tu clon local.

```bash
> Cloning into 'EDUtrack_bot'...
> remote: Enumerating objects: 868, done.
> remote: Counting objects: 100% (81/81), done.
> remote: Compressing objects: 100% (67/67), done.
> remote: Total 868 (delta 36), reused 52 (delta 14), pack-reused 787
> Receiving objects: 100% (868/868), 5.06 MiB | 7.77 MiB/s, done.
> Resolving deltas: 100% (501/501), done.
```

Antes de editar el archivo de configuración deberá contar con:
 - El TOKEN que le proporciono BotFather
 - El nombre que tiene registrado en la aplicación de Telegram
 - Su usuario de Telegram
 - El ID de Telegram

El nombre y el usuario, se pueden obtener desde el menu Settings de la aplicación de Telegram.

El id se puede obtener utilizando el bot <a href="https://t.me/userinfobot" target="_blank">@UserInfoBot</a>

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ESP/images/userinfobot.png)

Ahora deberás editar manualmente el archivo de configuración `config_file.py` que se encuntra en el direcotorio EDUrack_bot/config.

```bash
# Ubuntu
nano EDUtrack_bot/config/config_file.py

# Windows CMD o Power Shell
notepad EDUtrack_bot/config/config_file.py
```

La información que se debe reemplazar esta indicada con el texto "replace \_element\_", es importante dejar las comillas (""). Por ejemplo

- "replace subject_id" -> "FS_2021"
- "replace subject_name" -> "Fundamentos del Software 2021"

```python
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

Para poner en marcha de forma local se debe tener previamente instalado Python en su version 3.7 o superior y SQLite. Se recomienda crear un **`entorno virtual previamente`** para instalar las librerias requeridas que se encuentran en el archivo **`requirements.txt`**:

- coloroma: Permite mostrar el texto de errores en color para su fácil identificación en las pruebas.
- pandas: Manejo y análisis de estructura de datos
- python-telegram-bot: Interfaz para conectar Python con la API Bot Telegram

Desde la consola en el directorio del EDUtrack_bot ejecutar:

```bash
pip install -r requirements.txt
python3 edutrack.py
```

### 3. Terminar de configurar su bot EDUtrack

Para finalizar la configuración de EDUtrack bot se deberá:

* Crear los planetas (grupos de telegram) y asignar el bot creado como administrador en cada uno de ellos, esto es de suma importancia ya que solo como administrador el bot tendra acceso a contabilizar los mensajes de los estudiantes.

> **NOTA IMPORTANTE:** Al crear los planetas se ofrece la opción  **Historial del chat para nuevos miebros** que por default esta como ***`HIDDEN`*** si se cambia por ***`VISIBLE`***, Telegram modifica el estatus de grupo a supergrupo  por lo que los administradores previamente dados de alta se resetearan, es una cuestion de Telegram, por lo que es necesario volver a dar de alta al bot como administrador.

* Tras crear los planetas y asignar su bot como adminsitrador iniciar una conversación con el bot creado anteriormente, este le enviara 2 archivos, **`students_format.csv`** y **`activities_format.csv`** que son los formatos que se deberán llenar y subir para terminar de configurar la asignatura. Tras subir los archivos los estudiantespodran acceder a su bot instancia de EDUtrack .

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ESP/images/config_files.png)

## Despliegue en Heroku 📦
### Antes del despliegue:
#### 1.- Instala los prerequisitos
1. <a href="https://id.heroku.com/login" target="_blank">Ingresa</a>/<a href="https://signup.heroku.com/" target="_blank">crea</a> una cuenta de Heroku desde su sitio web. Heroku ofrece un plan especial si tienes una cuenta de estudiante/profesor en <a href="https://education.github.com/" target="_blank">GitHub Education</a>. Si cuentas con una cuenta educativa ingresa a <a href="https://www.heroku.com/github-students" target="_blank">Heroku for GitHub Students</a>
2. Instala <a href="https://git-scm.com/book/en/v2/Getting-Started-Installing-Git" target="_blank">Git</a>
3. Instala <a href="https://devcenter.heroku.com/articles/getting-started-with-python#set-up" target="_blank">Heroku CLI</a>

>**NOTA IMPORTANTE:** El plan gratuito en heroku, pone a dormir su bot después de 30 minutos de inactividad (pero no en el plan educativo). Al recibir una solicitud despertará, pero provoca un breve retraso para esta primera solicitud, despúes respondera casi inmediatamente hasta que vuelva a dormir por inactividad. Tambien es importante considerar que el plan gratuito incluye 450 horas de uso mensuales, que se pueden incrementar a 1000 si se añande una tarjeta de credito a su cuenta (mientras no rebase el límite de uso no se realizara ningún cargo). Al dormir un bot (o una heroku app), no gasta horas. Para mas información visite <a href="https://devcenter.heroku.com/articles/free-dyno-hours" target="_blank">Free Dyno Hours</a> <br><br><a href="https://github.com/romainbutteaud" target="_blank">Romain Butteaud</a> desarrollo una app para evitar que tu aplicación gratuita de Heroku vuelva a quedarse dormida. Sólo tienes que añadir la tuya aquí <a href="https://kaffeine.herokuapp.com/" target="_blank">kaffeine.herokuapp.com</a>

Para realizar el despliegue en Heroku se debe de contar con 2 archivos (los cuales ya se encuentran en el repositorio) **`Procfile`** (asegúrarse de que no tiene ninguna extensión de archivo como .txt, porque no funcionará):

```
# Procfile
web: python3 bot.py
```

y **`requirements.txt`**

```textfile
colorama>=0.4.3
pandas>=1.1.2
python-telegram-bot>=12.7
```


#### 2.- Iniciar Sesión en Heroku
Inicie sesión una cuenta en Heroku desde tu terminal/simbolo de Sistema.

```bash
$ heroku login
heroku: Press any key to open up the browser to login or q to exit:
```

 Heroku CLI solicitara presionar una tecla para abrir el navegador y sólo tiene que hacer clic en el botón para iniciar sesión.

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku.png)


#### 3.- Crear una webapp en Heroku
**Si ya cuenta con una web app puede omitir estos pasos. Vaya al punto [4.- Establecer las variables de entorno](#4\--establecer-las-variables-de-entorno).**

Una vez que haya iniciado la sesión, vuelva a la línea de comandos. Para crear una nueva webapp ingrese:

```bash
# Si no se indica <your_app_name> heroku proporcionara un nombre aleatorio

$ heroku create <your_app_name>
Creating ⬢ <your_app_name>... done
https://<your_app_name>.herokuapp.com/ | https://git.heroku.com/<your_app_name>.git
```

#### 4.- Establecer las variables de entorno
1. **HEROKU_APP_NAME**
    ```bash
    $ heroku config:set HEROKU_APP_NAME=<your_app_name> -a <your_app_name>

    Setting HEROKU_APP_NAME and restarting ⬢ <your_app_name>.. done, v3
    !    Warning: The "HEROKU_" namespace is protected and shouldn't be used.
    HEROKU_APP_NAME: <your_app_name>
    ```

2. **TOKEN**
    ```bash
    $ heroku config:set TOKEN=<paste_your_TOKEN_bot> -a <your_app_name>

    Setting TOKEN and restarting ⬢ <your_app_name>.. done, v3
    TOKEN: <your_TOKEN_bot>
    ```

3. **MODE** (debe ser prod)
    ```bash
    $ heroku config:set MODE=prod -a <your_app_name>

    Setting MODE and restarting ⬢ <your_app_name>.. done, v3
    MODE: prod
    ```


### Despliegue con Heroku CLI


### Despliegue con un contenedor Docker y Heroku


## Construido con 🛠️

* [Python](https://www.python.org/)
* [Python Telegram Bot] (https://maven.apache.org/) - Libreria que proporciona la interface con [Telegram API Bot](https://core.telegram.org/bots/api)
* [SQLite](https://www.sqlite.org/index.html) - Motor de Base de Datos

## Autores ✒️

* [<img src="https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ESP/images/ORCID_logo.png" alt="ORCID" width="20"/>](https://orcid.org/0000-0003-4507-3150) [**Jeovani M. Morales Nieto**](https://github.com/jeovani-morales/) - *Doctorando Desarrollador*
* [<img src="https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ESP/images/ORCID_logo.png" alt="ORCID" width="20"/>](https://orcid.org/0000-0002-0183-044X) [**Rosana Montes Soldado**](https://dasci.es/personal/perfil/rosana-montes-soldado/) - *Directora de Tesis y Asesora*
* [<img src="https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ESP/images/ORCID_logo.png" alt="ORCID" width="20"/>](https://orcid.org/0000-0002-7283-312X) [Francisco Herrera Triguero](https://dasci.es/personal/perfil/francisco-herrera-triguero/) - *Director de Tesis*

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