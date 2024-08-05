# RobotCenselMichael

Este repositorio tiene el codigo del robot encargado de automatizar el proceso de ingreso a la pagina de Censel y descargar los reportes web de baterias, intrusion, fallo de test y panico y guardarlos en la base de datos.

# Configuracion 

1. Clonar el repositorio.
2. Instalar las dependencias usando 'pip install -r requirements.txt'.  pip freeze > "requirements.txt"
3. Crear el bot de telegram 

## Como crear el bot de telegram

1. Descargar Telegram desktop
2. Buscar el bot llamado "BotFather" este bot nos guiará paso a paso para crear nuestro bot (Debemos asegurarnos de hacer el proceso con el Bot verificado)
3. Este bot nos dará el token de el bot que acabamos de crear, est token debemos guardarlo en la variabe llamada TELEGRAM_BOT_TOKEN
4. luego debemos obtener nuestro chat id, este lo obtenemos con el bot Get My ID, este automaticamente nos dara el id que necesitamos y lo debemos guardarla en la variable TELEGRAM_CHAT_ID.

Con estos cambios ya deberiamos tener nuestro bot parametrizado para que nos lleguen todos los mensajes, a continuacion dejare una imagen de los chats de los bots que tenemos que buscar, para asegurarnos de no hacer el proceso en el bot que no debemos.

![bot: Get My ID](image.png)
![bot: BotFather](image.png)