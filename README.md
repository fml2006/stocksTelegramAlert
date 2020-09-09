#BOT DE ALERTAS EN TELEGRAM

#FUNCIONMIENTO
 1- Crea Base de Datos y tablas automaticamente
 2- Obtiene de Yfinance los datos
 3- Calcula y guarda el indicador CCI y volumen promedio en timeframe de 1hora
 4- Desde telegram con enviar /start inicia, con /alert envia los tickers que cumplan la condicion de CCI ( debajo de la linea de 0 ) y si se envia el ticker devuelve el precio de cierre. 
 Solo tiene seteadas un puñado de tickers se puden sumar mas en screener.py


#Librerias usadas
pandas
numpy
yfinance
pymysql
sqlalchemy
datetime

#Comando de instalacion
pip install SQLAlchemy
pip install PyMySQL
pip install yfinance
pip install numpy
pip install pandas

#Instalacion de Libreria Telegam
pip install python-telegram-bot

#Iniciar BotFather en Telegram para obtener TOKEN e ingresarlo en el file echobot.py

#Base de datos en MySQL se crea al hacer correr el desarrollo, es necesario iniciar el servidor ( XAMPP o el que usen )
#Chequear la funcion connectDB() en functions.py es donde crea la Base de datos. 

#El proyecto fue desarrollado de forma dinamica para que sea facilmente escalarlo o modificarlo.

#PARA INICIAR EL PROYECTO EN CONSOLA SE DEBERA CORRER EL SIGUIENTE COMANDO ( siempre estando dentro de la carpeta del proyecto )
python echobot.py

#Caulquier duda estoy a disposición ya sea para cualquier duda o iniciar algun proyecto en conjunto. 

#FACUNDO MATIAS LEMOS 
