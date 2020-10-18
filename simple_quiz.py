from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import dispatcher
import telegram

bot_token = '1161652378:AAEwBPiWwVTNsv-v_HArYU3NVGhAQAhGXu4'

start_message = '''
Start the quiz by entering the command /quiz
To answer a question, answer "/next <YOUR ANSWER>" e.g. "/next A"
'''

question_1 = '''
**What secondary school am I from?**
A: Hwa Chong
B: River Valley
C: Dunman High
'''

question_2 = '''
**What is my favorite color?**
A: Black
B: Green
C: Blue
'''

question_3 = '''
**Which floor do I stay on?**
A: 15th
B: 17th
C: 11th
'''

answer = [0, "B", "C", "A"]

curr_question_reference = dict()

def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = start_message)

# Starts a quiz, initializes the player in the reference dictionary
def quiz(update, context):
    user_id = update.effective_chat.id
    curr_question_reference[user_id] = 1 # initialize
    context.user_data[user_id] = 0 # store the user's score here
    context.bot.send_message(chat_id = user_id, text = question_1, parse_mode = telegram.ParseMode.MARKDOWN_V2)

# evaluate function checks whether the user answered the question correctly
# and stores the result in "context.user_data" dictionary
# Note: evaluate() is called after a callback
# (key = update.effective_chat.id)
# (value = score)
def evaluate(update, context, question):
    input = context.args[0]
    user_id = update.effective_chat.id
    if (input == answer[question]):
        context.user_data[user_id] += 1  # store the score here

def next(update, context):
    # Check the current_question
    user_id = update.effective_chat.id
    last_question = curr_question_reference[user_id]

    # Evaluate previous response
    evaluate(update, context, last_question)

    curr_question = last_question + 1
    print(curr_question)
    if curr_question == 2:
        context.bot.send_message(chat_id = update.effective_chat.id, text = question_2, parse_mode = telegram.ParseMode.MARKDOWN_V2)
    elif curr_question == 3:
        context.bot.send_message(chat_id = update.effective_chat.id, text = question_3, parse_mode = telegram.ParseMode.MARKDOWN_V2)
    else:
        score = str(context.user_data[user_id])
        total = str(3)
        context.bot.send_message(chat_id = update.effective_chat.id, text="You scored " + score + "/" + total + "!!!")

    curr_question_reference[user_id] = curr_question

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    quiz_handler = CommandHandler('quiz', quiz)
    question_handler = CommandHandler('next', next)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(quiz_handler)
    dispatcher.add_handler(question_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
