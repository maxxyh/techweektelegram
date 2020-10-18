# A quiz for

from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import os, json

bot_token = '1161652378:AAEwBPiWwVTNsv-v_HArYU3NVGhAQAhGXu4'
PORT = int(os.environ.get('PORT', 5000))

# Setting up variables
RESPOND, END= range(2)
ONE, TWO, THREE = range(3)

# curr_question_dict stores the question progress of the users
# key = update.effective_chat.id
# value = question index (starting from 0)
curr_question_dict = dict();

# Messages
with open("config.json", "r") as file:
    config = json.load(file)
question_bank = config["questions"]

# evaluate function checks whether the user answered the question correctly
# and stores the result in "context.user_data" dictionary
# Note: evaluate() is called after a callback
# (key = update.effective_chat.id)
# (value = score)
def evaluate(update, context, question):
    query = update.callback_query
    query.answer()
    input = query.data
    #print("input:" + input)
    #print("ans: " + str(answer[question]))
    key = update.effective_chat.id
    if (question > 0 and input == str(question_bank[question-1]["correct_answer"])):  # have to minus 1 because of 0-indexing
        context.user_data[key] += 1

def start(update, context):
    key = update.effective_chat.id
    context.user_data[key] = 0
    curr_question_dict[key] = 0
    keyboard = [
            [
                InlineKeyboardButton("I am ready!", callback_data=str(ONE)),
            ]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(config["start_message"], reply_markup=reply_markup)

    return RESPOND

# manages most of the quiz response to the users
def respond_to_query(update, context):
    # get curr_question of user
    curr_question = curr_question_dict[update.effective_chat.id]
    # end conversation if no more questions
    if (curr_question >= len(config["questions"])):
        return END

    evaluate(update, context, curr_question)
    # Load questions and answer options from json
    answer_options = question_bank[curr_question]["answer_options"]
    question = question_bank[curr_question]["question"]

    keyboard = [
        [
            InlineKeyboardButton(answer_options[0], callback_data=str(ONE)),
            InlineKeyboardButton(answer_options[1], callback_data=str(TWO)),
            InlineKeyboardButton(answer_options[2], callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.edit_message_text(text = question, reply_markup=reply_markup)
    curr_question_dict[update.effective_chat.id] += 1
    return RESPOND

def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""

    num_questions = len(question_bank)
    evaluate(update, context, num_questions)
    query = update.callback_query
    score = str(context.user_data[update.effective_chat.id])
    total = str(num_questions)
    query.edit_message_text(text="You scored " + score + "/" + total + "!!!")
    return ConversationHandler.END


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    updater = Updater(token = bot_token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            RESPOND: [
                CallbackQueryHandler(respond_to_query),
            ],
            END: [
                CallbackQueryHandler(end),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)



    #updater.start_polling()

    # link webhook to heroku server
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=bot_token)
    updater.bot.setWebhook('https://stark-mesa-48399.herokuapp.com/' + bot_token)

    updater.idle()


if __name__ == '__main__':
    main()
