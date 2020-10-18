from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import os, json

bot_token = '1161652378:AAEwBPiWwVTNsv-v_HArYU3NVGhAQAhGXu4'
PORT = int(os.environ.get('PORT', 5000))

# Stages
RESPOND, END= range(2)
ONE, TWO, THREE = range(3)
answer = [0, 1, 2, 0, 2, 0]
curr_question_dict = dict();

# Messages

with open("config.json", "r") as file:
    config = json.load(file)

# evaluate function checks whether the user answered the question correctly
# and stores the result in "context.user_data" dictionary
# (key = update.effective_chat.id)
# (value = score)
def evaluate(update, context, question):
    query = update.callback_query
    query.answer()
    input = query.data
    #print("input:" + input)
    #print("ans: " + str(answer[question]))
    key = update.effective_chat.id
    if (input == str(answer[question])):
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

    return FIRST

# update is the
def respond_to_query(update, context):
    # get curr_question of user
    curr_question = curr_question_dict[update.effective_chat.id]

    # end conversation if no more questions
    if (curr_question >= len(config["questions"])):
        return END

    # Load questions and answer options from json
    question_reference = config["questions"][curr_state]
    answer_options = question_reference["answer_options"]
    question = question_reference["question"]

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
    return RESPOND

def first(update, context):
    query = update.callback_query

    keyboard = [
        [
            InlineKeyboardButton("Hwa Chong", callback_data=str(ONE)),
            InlineKeyboardButton("River Valley", callback_data=str(TWO)),
            InlineKeyboardButton("Dunman High", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text = 'What Secondary School am I from?', reply_markup=reply_markup)
    return SECOND

def second(update, context):
    evaluate(update, context, 1)
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("Black", callback_data=str(ONE)),
            InlineKeyboardButton("Green", callback_data=str(TWO)),
            InlineKeyboardButton("Blue", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text = 'What is my favorite color?', reply_markup=reply_markup)
    return THIRD

def third(update, context):
    evaluate(update, context, 2)
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("15th", callback_data=str(ONE)),
            InlineKeyboardButton("17th", callback_data=str(TWO)),
            InlineKeyboardButton("11th", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text = 'Which floor do I stay on?', reply_markup=reply_markup)
    return FOURTH

def fourth(update, context):
    evaluate(update, context, 3)
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("0", callback_data=str(ONE)),
            InlineKeyboardButton("1", callback_data=str(TWO)),
            InlineKeyboardButton("2", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text = 'How many siblings do I have?', reply_markup=reply_markup)
    return FIFTH

def fifth(update, context):
    evaluate(update, context, 4)
    query = update.callback_query
    keyboard = [
        [
            InlineKeyboardButton("Tchoukball", callback_data=str(ONE)),
            InlineKeyboardButton("Computer Science", callback_data=str(TWO)),
            InlineKeyboardButton("Business Analytics", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text = 'What do I major in?', reply_markup=reply_markup)
    return END

def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""

    evaluate(update, context, 5)
    query = update.callback_query
    score = str(context.user_data[update.effective_chat.id])
    total = str(len(answer) - 1)
    query.edit_message_text(text="You scored " + score + "/" + total + "!!!")
    return ConversationHandler.END


# inline mode -> calling the bot within a chat
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())))
    context.bot.answer_inline_query(update.inline_query.id, results)

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



    # updater.start_polling()

    # link webhook to heroku server
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=bot_token)
    updater.bot.setWebhook('https://stark-mesa-48399.herokuapp.com/' + bot_token)

    updater.idle()


if __name__ == '__main__':
    main()
