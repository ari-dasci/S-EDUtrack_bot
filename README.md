[Spanish Version](#bot-edutrack)

# EDUtrack Bot

EDUtrack es parte de un proyecto de Tesis para evaluar la calidad de la educación superior en un entorno FC-ML de la Escuela Técnica Superior de Ingenierías Informática y de Telecomunicación (ETSIIT) de la Universidad de Granada.

# ¿Qué es EDUtrack?

EDUtrack es un bot para Telegram con una interface en inglés y español. Se emplea principalmente como instrumento de comunicación con el estudiante, pero está preparado para obtener métricas de evaluación de la experiencia docente que ayudan a la evaluación de la calidad de la educación superior en un entorno de metodologías combinadas, "Flipped Classroom" y "M-Learning", denominado entorno FC-ML. Así mismo proporciona un medio de detección temprana del fracaso académico.


---
<details> <summary> Tabla de Contenidos</summary>

- [EDUtrack Bot](#edutrack-bot)
- [¿Qué es EDUtrack?](#qué-es-edutrack)
- [Comenzando 🚀](#comenzando-)
- [Configuración 🔧](#configuración-)
  - [1.- Crea un bot para instanciar EDUtrack](#1--crea-un-bot-para-instanciar-edutrack)
  - [2.- Configurar la instancia de EDUtrack](#2--configurar-la-instancia-de-edutrack)
    - [2.1. A través de EDUtrack_Setup](#21-a-través-de-edutrack_setup)
    - [2.2 Clonar el repositorio y realizar la configuración manual](#22-clonar-el-repositorio-y-realizar-la-configuración-manual)
  - [3. Terminar de configurar su bot EDUtrack](#3-terminar-de-configurar-su-bot-edutrack)
- [Despliegue](#despliegue)
  - [Despliegue en un servidor local](#despliegue-en-un-servidor-local)
    - [Instalación de librerias](#instalación-de-librerias)
    - [Establecer variables de entorno](#establecer-variables-de-entorno)
    - [Ejecución del script](#ejecución-del-script)
  - [Despliegue en Heroku 📦](#despliegue-en-heroku-)
    - [Antes del despliegue:](#antes-del-despliegue)
    - [1. Metodo GUI - Conexión a Github](#1-metodo-gui---conexión-a-github)
    - [2. Heroku Git usando Heroku CLI](#2-heroku-git-usando-heroku-cli)
      - [1. Inicio de sesión](#1-inicio-de-sesión)
      - [2.- Crear una webapp en Heroku](#2--crear-una-webapp-en-heroku)
      - [3.- Establecer las variables de entorno](#3--establecer-las-variables-de-entorno)
      - [4. Desplegar la instancia de EDUtrack](#4-desplegar-la-instancia-de-edutrack)
    - [Despliegue con un contenedor Docker y Heroku](#despliegue-con-un-contenedor-docker-y-heroku)
    - [Ver el Status de nuestra app](#ver-el-status-de-nuestra-app)
  - [Construido con 🛠️](#construido-con-️)
  - [Autores ✒️](#autores-️)
  - [Contribuyendo 🖇️](#contribuyendo-️)
  - [Wiki 📖](#wiki-)
  - [Versionado 📌](#versionado-)
  - [Licencia 📄](#licencia-)
  - [Expresiones de Gratitud 🎁](#expresiones-de-gratitud-)

</details>
# Comenzando 🚀
Para configurar una instancia de EDUtrack se requiere

- Python 3.7 o superior
- SQLite
- Una cuenta de Telegram

# Configuración 🔧

La configuración de EDUtrack se puede desarrollar en 3 pasos:

## 1.- Crea un bot para instanciar EDUtrack

Primero se debe crear un bot desde <a href="https://t.me/Botfather" target="_blank">@BotFather</a>. Al finalizar te proporcionara un enlace que podras compartir a otros usuarios para que interactuen con el bot. Y por otra parte te proporcionara el _**TOKEN**_ de tu bot, que es la clave con la cual se realizara la conexión entre el bot que acabas de crear y EDUtrack.

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/Token.png)

```textfile
En el ejemplo de la imágen:
Enlace: t.me/Subject_2021_bot
TOKEN: 1401345537:AAGPGnsIeRROS6500fm2bGPOGqz8kkD9O28
```

## 2.- Configurar la instancia de EDUtrack

Para configurar los archivos de EDUtrack se puede realizar de 2 formas:

### 2.1. A través de EDUtrack_Setup

<a href="https://t.me/EDUtrack_setup_bot" target="_blank">@EDUtrack_setup</a>, es un bot que solicita la información general para EDUtrack, por ejemplo nombre del docente y de la asignatura, duración del curso, entre otros.

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/edutrack_setup.png)

Al finalizar <a href="https://t.me/EDUtrack_setup_bot" target="_blank">@EDUtrack_setup</a> nos proporcionara 2 archivos comprimidos iguales, `edutrack_bot.zip` y `edutrack_bot.tar`, se procederá a descargar el que se adecue a nuestras necesidades y se descomprime el archivo en la ubicación deseada. Para continuar vamos a la sección [3. Terminar de configurar su bot EDUtrack](#3-terminar-de-configurar-su-bot-edutrack)

### 2.2 Clonar el repositorio y realizar la configuración manual

1. Clonar repositorio
En la terminal de nuestro sistema, accederemos al directorio donde se alojara la instancia de EDUtrack y se escribira el siguiente comando:

    ```bash
    git clone https://github.com/jeovani-morales/EDUtrack_bot
    ```

    Presiona **`Enter`** para crear tu clon local y se mostraraun mensaje similar a este:

    ```bash
    > Cloning into 'EDUtrack_bot'...
    > remote: Enumerating objects: 868, done.
    > remote: Counting objects: 100% (81/81), done.
    > remote: Compressing objects: 100% (67/67), done.
    > remote: Total 868 (delta 36), reused 52 (delta 14), pack-reused 787
    > Receiving objects: 100% (868/868), 5.06 MiB | 7.77 MiB/s, done.
    > Resolving deltas: 100% (501/501), done.
    ```
2. Configuración manual

    Para realizar la configuración manual, se debe contar con:

    - El nombre que tiene registrado en la aplicación de Telegram
    - Su usuario de Telegram
    - El ID de Telegram

    El nombre y el usuario, se pueden obtener desde el menu Settings de la aplicación de Telegram.

    El id se puede obtener utilizando el bot <a href="https://t.me/userinfobot" target="_blank">@UserInfoBot</a>

    ![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ESP/images/userinfobot.png)


    Accedemos al directorio del reposirtorio EDUtrack_bot
    ```bash
    # change into the `repo` directory
    cd EDUtrack_bot
    ```
    Ahora deberás editar manualmente el archivo de configuración **`config_file.py`** que se encuntra en el direcotorio EDUrack_bot/config.

    ```bash
    # Linux
    nano config/config_file.py

    # Windows CMD o Power Shell
    notepad config/config_file.py
    ```

    La información que se debe reemplazar esta indicada con el texto "replace `<element>`", donde `<element>` es la variable a sustituir. Es importante dejar las comillas (""). Por ejemplo

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

## 3. Terminar de configurar su bot EDUtrack

Para finalizar la configuración de EDUtrack bot se deberá crear los grupos de telegram y asignar el bot creado como **ADMINISTRADOR** en cada uno de ellos.

> ***NOTA IMPORTANTE:*** Es muy importante que el bot se encuentre como administrador en cada grupo de Telegram, ya que solo como administrador tendra acceso a la  información necesaria para realizar sun funciones.

> ***NOTA IMPORTANTE:*** Al crear los planetas se ofrece la opción  **Historial del chat para nuevos miebros** que por default esta como ***`HIDDEN`*** si se cambia por ***`VISIBLE`***, Telegram modifica el estatus de grupo a supergrupo  por lo que los administradores previamente dados de alta se resetearan, es una cuestion de Telegram, por lo que es necesario volver a dar de alta al bot como administrador.

Para finalizar la configuración se deben subir a nuestro bot 2 archivos ***`students_format.csv`*** y ***`activities_format.csv`***. La plantilla de estos archivos nos la entregara nuestro bot EDUtrak al iniciar una conversación con el después de realizar el [despligue](#despliegue). El despliegue se explica en la siguiente sección.

# Despliegue
El despliegue de EDUtrack nos permitirá entablar una conversación con nuestro bot. Se puede realizar en un servidor local, o en un servidor en Internet a través de un webhook, para este último se explicará como hacerlo dentro de HEROKU.


## Despliegue en un servidor local
Es importante recordar que para poner en marcha EDUtrack de forma local, se debe tener previamente instalado Python en su version 3.7 o superior y SQLite.


### Instalación de librerias
Se recomienda crear un **`entorno virtual previamente`** para instalar las librerias requeridas que se encuentran en el archivo **`requirements.txt`**:

```textfile
colorama>=0.4.3
pandas>=1.1.2
python-telegram-bot>=12.7
```

- coloroma: Permite en un entorno local, mostrar los errores en color para identificarlos con facílidad.
- pandas: Manejo y análisis de estructura de datos
- python-telegram-bot: Interfaz para conectar Python con la API Bot Telegram

Desde la terminal de tu sistema, ya en el entorno virtual, nos aseguramos de estar en el directorio de EDUtrack_bot y ejecutamos:

```bash
pip install -r requirements.txt
```


### Establecer variables de entorno
Se debe establecer la variable de entorno TOKEN, la cual contendrá el TOKEN proporcionado por BotFather para nuestro bot. Esto se realiza por seguridad para que el TOKEN no se encuentre alojado directamente en los archivos.

> **NOTA IMPORTANTE** esta forma de configurar las variables de entorno son temporales, es decir, se deben de establecer las variables de entorno cada vez que se abre una nueva terminal.

```bash
#Linux
export TOKEN="<TOKEN_proporcionado_por_BotFather>"
export MODE="dev"

# Windows Powershell
$env TOKEN="<TOKEN_proporcionado_por_BotFather>"
$env MODE="dev"

# Windows CMD
set TOKEN="<TOKEN_proporcionado_por_BotFather>"
set MODE="dev"
```


### Ejecución del script
Si todo ha salido correctamente hasta este momento solo nos queda ejecutar el script de python:
```bash
  python edutrack.py
```
Al ejecutar nuestro script se mostrara el siguiente mensaje, el cuál indicará que el bot se ha cargado correctamente.

```
 ====================================================
| EDUtrack_bot  Copyright (C) 2021  Jeovani Morales
| This program comes with ABSOLUTELY NO WARRANTY.
| This is free software, and you are welcome
| to redistribute it under certain conditions see
| https://github.com/jeovani-morales/EDUtrack_bot
=====================================================

Loaded Bot
```

## Despliegue en Heroku 📦
### Antes del despliegue:
1. <a href="https://id.heroku.com/login" target="_blank">Ingresa</a>/<a href="https://signup.heroku.com/" target="_blank">crea</a> una cuenta de Heroku desde su sitio web. Heroku ofrece un plan especial si tienes una cuenta de estudiante/profesor en <a href="https://education.github.com/" target="_blank">GitHub Education</a>. Si cuentas con una cuenta educativa ingresa a <a href="https://www.heroku.com/github-students" target="_blank">Heroku for GitHub Students</a>
2. Instala <a href="https://git-scm.com/book/en/v2/Getting-Started-Installing-Git" target="_blank">Git</a> (Para despliegue en terminal)
3. Instala <a href="https://devcenter.heroku.com/articles/getting-started-with-python#set-up" target="_blank">Heroku CLI</a> (Para despliegue en terminal)

<!-- En caso de tener problemas con  las instalación de Heroku CLI en linux se pueden utilizar los
siguientes comandos
```bash
wget https://cli-assets.heroku.com/heroku-cli/channels/stable/heroku-cli-linux-x64.tar.gz -O heroku.tar.gz

tar -xvzf heroku.tar.gz

sudo mkdir -p /usr/local/lib /usr/local/bin

# listar los archivos y guardar la version de heroku
ls

#Sustituir la version de heroku
sudo mv heroku-cli-HEROKU_VERSION-linux-x64 /usr/local/lib/heroku

sudo ln -s /usr/local/lib/heroku/bin/heroku /usr/local/bin/heroku

```
 -->

>***NOTA IMPORTANTE:*** El plan gratuito en heroku, pone a dormir su bot después de 30 minutos de inactividad. Al recibir una solicitud despertará, pero provoca un breve retraso para esta primera solicitud, despúes respondera casi inmediatamente hasta que vuelva a dormir por inactividad. Tambien es importante considerar que el plan gratuito incluye 450 horas de uso mensuales, que se pueden incrementar a 1000 si se añande una tarjeta de credito a su cuenta (mientras no rebase el límite de uso no se realizara ningún cargo). Al dormir un bot (o una heroku app), no gasta horas. Para mas información visite <a href="https://devcenter.heroku.com/articles/free-dyno-hours" target="_blank">Free Dyno Hours</a>.<br><br><a href="https://github.com/romainbutteaud" target="_blank">Romain Butteaud</a> desarrollo una app para evitar que tu aplicación gratuita de Heroku vuelva a quedarse dormida. Sólo tienes que añadir la tuya aquí <a href="https://kaffeine.herokuapp.com/" target="_blank">kaffeine.herokuapp.com</a>.</div>

Para realizar el despliegue en Heroku se debe de haber modificado el archivo **`config_file`** del directorio **`config`** (Si se utilizo el boto EDUtrack_setup ya está configurado). Además se debe contar con 2 archivos (los cuales ya se encuentran en el repositorio), **`requirements.txt`** que ya se ha utilizado previamente y **`Procfile`** (este archivo no debe tener ninguna extensión de archivo como .txt, porque no funcionará), el cual debe contener el siguiente texto:

```textfile
web: python3 edutrack.py
```
### 1. Metodo GUI - Conexión a Github

- Antes de realizar el despligue con este método debes crear una copia del repositorio [EDUtrack_bot]("https://github.com/jeovani-morales/EDUtrack_bot) en tu propia cuenta de GitHub.

- <a href="https://id.heroku.com/login" target="_blank">Ingresa</a>/<a href="https://signup.heroku.com/" target="_blank">crea</a> tu cuenta en el sitio web de Heroku y crea una nueva app donde alojaras tu instancia de EDUtrack_bot.

- Crea una nueva app desde el botón **`New`**
![Botón New para crear una nueva app](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku_btn_new.png)

- Selecciona la app que acabas de crear y en el menú selecciona la opción de Settings.
![Opción Settings del menu de la app](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku_settings.png)

- En la sección **`Confif Vars`** presiona el botón **`Reveal Config Vars`** y añade las variables:
  - HEROKU_APP_NAME: como valor escribe el nombre de la app actual
  - TOKEN: Escribe el TOKEN que te proporciono BotFather anteriormente
  - MODE: Escribe prod (tiene que ser así para que busque las variables dentro de Heroku)
![Configuración de las variables](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku_config_vars.png)

- En el menu de la aplicación selecciona la opción Deploy y en el apartado **`Deployment method`** selecciona la opción **`Github Connect to GitHub`**.

![Metodo Deployment](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku_deploy_method.png)

- Te pedirá iniciar sesión en tu cuenta de GitHUb y te permitirá buscar entre tus repositorios, busca aquél donde alojaste EDUtrack_bot. Presiona el botón Connect.

![Selección del repositorio EDUtrack_bot](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku_connect_github.png)

- Heroku nos presetnara dos opciones para realziar el despliegue, de forma manual y de forma automática. La forma automática reiniciara el despligue cada que se realice un cambio en el repositorio. En ambas nos pedirá que seleccionemos la rama que desplegaremos, seleccionamos **`Main`** y presionamos el botón **`Deploy Branch`** para la forma manual o **`Enabled Automatic Deploys`**.


### 2. Heroku Git usando Heroku CLI
#### 1. Inicio de sesión

Inicie sesión una cuenta en Heroku desde la terminal de tu sistema.

```bash
heroku login
heroku: Press any key to open up the browser to login or q to exit:
```

 Heroku CLI solicitara presionar una tecla para abrir el navegador y sólo tiene que hacer clic en el botón para iniciar sesión.

![](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku.png)


#### 2.- Crear una webapp en Heroku
**Si ya cuenta con una web app puede omitir estos pasos. Vaya al punto [4.- Establecer las variables de entorno](#4\--establecer-las-variables-de-entorno).**

Una vez que haya iniciado la sesión, vuelva a la línea de comandos. Para crear una nueva webapp ingrese:

```bash
# Si no se indica <your_app_name> heroku proporcionara un nombre aleatorio

$ heroku create <your_app_name>
Creating ⬢ <your_app_name>... done
https://<your_app_name>.herokuapp.com/ | https://git.heroku.com/<your_app_name>.git
```

#### 3.- Establecer las variables de entorno
Las varaibles de entorno se pueden establecer directamente desde el sitio web de Heroku en la sección de **`Settings`**. Tambien se puede establcer utilizando la terminal con Heroku CLI como se describe a continuación:

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

#### 4. Desplegar la instancia de EDUtrack

1. Crear un nuevo respositorio de Git:
    ```bash
    git init
    ```
2. Indicar a Git los archivos que se van a actualizar en el siguiente commit. Con el punto "." indicamos que queremos actualizar todos los archivos:
    ```bash
    git add .
    ```
3. Realizam:os el commit especificando una descripción
    ```bash
    git commit -m "update files"
    ```
4. Asignamos un control remoto al repositorio local:
    ```bash
    heroku git:remote -a <your_app_name>
    ```
5. Se envia todo al servidor heroku:
    ```bash
    git push heroku main
    ```
Al finalizar se mostrará un mensaje similar a este:

```bash
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 347 bytes | 347.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Building on the Heroku-20 stack
remote: -----> Using buildpack: heroku/python
remote: -----> Python app detected
remote: -----> No Python version was specified. Using the same version as the last build: python-3.9.5
remote:        To use a different version, see: https://devcenter.heroku.com/articles/python-runtimes
remote: -----> No change in requirements detected, installing from cache
remote: -----> Using cached install of python-3.9.5
remote: -----> Installing pip 20.2.4, setuptools 47.1.1 and wheel 0.36.2
remote: -----> Installing SQLite3
remote: -----> Installing requirements with pip
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote:
remote: -----> Compressing...
remote:        Done: 85.9M
remote: -----> Launching...
remote:        Released v18
remote:        https://<your_app_name>.herokuapp.com/ deployed to Heroku
remote:
remote: Verifying deploy... done.
To https://git.heroku.com/<your_app_name>.git
   c705235..9154a1d  main -> main
```






### Despliegue con un contenedor Docker y Heroku

### Ver el Status de nuestra app
Para ver el estatus de nuestra aplicaciónpresionamos el botón **`More`** que se encuentra en la parte superior derecha del sitio web de la app y seleccinamos la opción View Logs

![Opción View Logs desde el botón More](https://raw.githubusercontent.com/jeovani-morales/EDUtrack_bot/EDUtrack_files/ENG/images/heroku_logs_gui.png)


Desde la terminal podemos también podemos mostrar los logs:
```bash
heroku logs -t -a <your_app_name>
```
Y nos mostrará un mensaje similar a este
```bash
2021-05-25T17:11:25.000000+00:00 app[api]: Build started by user **********
2021-05-25T17:12:01.937808+00:00 app[api]: Deploy 9154a1d2 by user **********
2021-05-25T17:12:01.937808+00:00 app[api]: Release v18 created by user **********
2021-05-25T17:12:02.209351+00:00 heroku[web.1]: State changed from down to starting
2021-05-25T17:12:11.086495+00:00 heroku[web.1]: Starting process with command `python3 edutrack.py`
2021-05-25T17:12:16.000000+00:00 app[api]: Build succeeded
2021-05-25T17:12:20.650217+00:00 app[web.1]: Conexión exitosa
2021-05-25T17:12:21.374078+00:00 app[web.1]:
2021-05-25T17:12:21.374117+00:00 app[web.1]: ====================================================
2021-05-25T17:12:21.374118+00:00 app[web.1]: | EDUtrack_bot  Copyright (C) 2021  Jeovani Morales
2021-05-25T17:12:21.374118+00:00 app[web.1]: | This program comes with ABSOLUTELY NO WARRANTY.
2021-05-25T17:12:21.374118+00:00 app[web.1]: | This is free software, and you are welcome
2021-05-25T17:12:21.374119+00:00 app[web.1]: | to redistribute it under certain conditions see
2021-05-25T17:12:21.374119+00:00 app[web.1]: | https://github.com/jeovani-morales/EDUtrack_bot
2021-05-25T17:12:21.374119+00:00 app[web.1]: ====================================================
2021-05-25T17:12:21.374120+00:00 app[web.1]:
2021-05-25T17:12:21.374188+00:00 app[web.1]: Loaded Bot
```

Y listo ya podemos ir a la app de Telegram e iniciar un conversación con nuestro bot para terminar de configurar nuestra asignatura: .


## Construido con 🛠️

* [Python](https://www.python.org/)
* [Python Telegram Bot] (https://github.com/python-telegram-bot/python-telegram-bot) - Libreria que proporciona la interface con [Telegram API Bot](https://core.telegram.org/bots/api)
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
Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](https://github.com/jeovani-morales/EDUtrack_bot/blob/main/License.md) para detalles

## Expresiones de Gratitud 🎁

* En la elaboración de un proyecto como este es imposible reinvertar la rueda, por lo que agradezco a:
  * [Artem Rys](https://medium.com/@rysartem) y su artículo [Creating Telegram Bot and Deploying it to Heroku](https://medium.com/python4you/creating-telegram-bot-and-deploying-it-on-heroku-471de1d96554)
  * [HOUI](https://medium.com/@liuhh02) y su artículo [How to Deploy a Telegram Bot using Heroku for FREE](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2)
  quienes facilitaron la compresión del despligue de nuestro bot.
  * [Villanuevand](https://github.com/Villanuevand) quien proporciono la plantilla para la realización de este [Readme](https://gist.github.com/Villanuevand/6386899f70346d4580c723232524d35a)



---
