import requests
from telegram import update
from telegram.ext import Updater, CommandHandler
import os
import pyunsplash


api_key = "wDfhBnhVLYdyz-mNkbegoqH4Zy5TNcskBNZFeb6vfeo"
pu = pyunsplash.PyUnsplash(api_key=api_key)


PORT = int(os.environ.get('PORT', 5000))
mytoken = '1161652378:AAEwBPiWwVTNsv-v_HArYU3NVGhAQAhGXu4'

startMessage = ''' 
    Get a random photo of a dog according to breed!
    List of Commands is as follows:
    /pug
    /shiba
    /bulldog
    /maltese
    /goldenretriever
    /chowchow
    /samoyed
    /husky
    /pomeranian
    /labrador
'''
aboutMessage = '''This bot sends random photos of dogs according to breed created as an example for Tembusu Tech Week 2020.
Dog breeds chosen are dedicated to my friends :)
Pug- Ariel
French Bulldog- Tasha
Maltese- Jamie
Golden Retriever- Zhan Wei
Chow Chow- Bao
Samoyed- Yik Heng
Husky- Sabrina
Pomeranian- Park (best year 1 in tchouk)
Labrador- Htet'''


def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = startMessage)

def send_photo(update, context):
    context.bot.send_photo(chat_id = update.effective_chat.id, photo = open('photo.jpg', 'rb'))

def about(update, context):
    update.message.reply_text(aboutMessage)

def feet(update, context):
    img = pu.photos(type_='random', count=1, featured=True,query="feet")
    for photos in img.entries:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo = photos.link_download)

def pug(update, context):
    # retrieves the json file from the dog.ceo api
    contents = requests.get('https://dog.ceo/api/breed/pug/images/random').json()
    # message field of the json file retrieved contains the random photo
    url = contents['message']
    # sends photo back to user who requested
    update.message.reply_photo(photo = url)

def shiba(update, context):
    contents = requests.get('https://dog.ceo/api/breed/shiba/images/random').json()
    url = contents['message']
    # update.message.reply_photo(photo = url)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def bulldog(update, context):
    contents = requests.get('https://dog.ceo/api/breed/bulldog/french/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def maltese(update, context):
    contents = requests.get('https://dog.ceo/api/breed/maltese/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def goldenRetriever(update, context):
    contents = requests.get('https://dog.ceo/api/breed/retriever/golden/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def chowchow(update, context):
    contents = requests.get('https://dog.ceo/api/breed/chow/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def samoyed(update, context):
    contents = requests.get('https://dog.ceo/api/breed/samoyed/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def husky(update, context):
    contents = requests.get('https://dog.ceo/api/breed/husky/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def pomeranian(update, context):
    contents = requests.get('https://dog.ceo/api/breed/pomeranian/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def labrador(update, context):
    contents = requests.get('https://dog.ceo/api/breed/labrador/images/random').json()
    url = contents['message']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = url)

def main():
    updater = Updater(token = mytoken)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    send_photo_handler = CommandHandler('photo', send_photo)
    about_handler = CommandHandler('about', about)
    pug_handler = CommandHandler('pug', pug)
    shiba_handler = CommandHandler('shiba', shiba)
    bulldog_handler = CommandHandler('bulldog', bulldog)
    maltese_handler = CommandHandler('maltese', maltese)
    goldenRetriever_handler = CommandHandler('goldenretriever', goldenRetriever)
    chowchow_handler = CommandHandler('chowchow', chowchow)
    samoyed_handler = CommandHandler('samoyed', samoyed)
    husky_handler = CommandHandler('husky', husky)
    pomeranian_handler = CommandHandler('pomeranian', pomeranian)
    labrador_handler = CommandHandler('labrador', labrador)
    feet_handler = CommandHandler('feet', feet)


    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(send_photo_handler)
    dispatcher.add_handler(about_handler)
    dispatcher.add_handler(pug_handler)
    dispatcher.add_handler(shiba_handler)
    dispatcher.add_handler(bulldog_handler)
    dispatcher.add_handler(maltese_handler)
    dispatcher.add_handler(goldenRetriever_handler)
    dispatcher.add_handler(chowchow_handler)
    dispatcher.add_handler(samoyed_handler)
    dispatcher.add_handler(husky_handler)
    dispatcher.add_handler(pomeranian_handler)
    dispatcher.add_handler(labrador_handler)
    dispatcher.add_handler(feet_handler)

    updater.start_polling()
    # link webhook to heroku server
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=mytoken)
    # updater.bot.setWebhook('https://mysterious-castle-06984.herokuapp.com/' + mytoken)

    updater.idle()

if __name__ == '__main__':
    main()