# coding: latin-1
# -*- coding: utf-8 -*-
import telebot
import pyautogui
import datetime






def telegram(mensaje):
    TELEGRAM_BOT_TOKEN = '6232135002:AAGPl356BEAbpzSQlgomBQi45YBUZJk136Q' #TOKEN CHAT TELEGRAM DE REPORTE DE ALARMAS
    TELEGRAM_CHAT_ID = '7411433556'
    hora_actual = datetime.datetime.now().strftime("%I:%M:%p")
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    contenido_mensaje = hora_actual
    pantallazo = pyautogui.screenshot('abrir_navegador.png')
    if mensaje == 'Se abrio el navegador correctamente:':
        contenido_mensaje += ( 
            f"Se valido el navegador correctamente"
        )
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=pantallazo, caption=contenido_mensaje)


telegram('Se abrio el navegador correctamente:')
