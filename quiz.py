# A quiz for

from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, PicklePersistence
import os, json

bot_token = '1161652378:AAEwBPiWwVTNsv-v_HArYU3NVGhAQAhGXu4'
PORT = int(os.environ.get('PORT', 5000))

# Setting up variables
RESPOND, END= range(2)
ONE, TWO, THREE = range(3)

# curr_question_dict stores the question progress of the users
# key = update.effective_chat.id
# value = question index (starting from 0)
curr_question_dict = dict()

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
    # print("in evaluate")
    query = update.callback_query
    query.answer()
    input = query.data
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
    if "scores" not in context.bot_data: 
        context.bot_data["scores"] = dict()
    if "old_max_score" in context.bot_data:
        clear_leaderboard_upon_change(update, context, context.bot_data["old_max_score"])
    else: 
        context.bot_data["old_max_score"] = len(config["questions"])

    return RESPOND

def clear_leaderboard_upon_change(update, context, old_max_score):
    if len(context.bot_data["scores"]) != 0 and len(config["questions"]) != old_max_score:
        clear_leaderboard(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text="New quiz found. Clearing old leaderboard.")



# manages most of the quiz response to the users
def respond_to_query(update, context):
    # get curr_question of user
    curr_question = curr_question_dict[update.effective_chat.id]
    
    # print("responding to query number {}".format(curr_question))
    
    # end conversation if no more questions
    if (curr_question >= len(config["questions"])):
        return end(update,context)

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
    username = update.effective_user.username
    context.bot_data["scores"][username] = score
    return ConversationHandler.END


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def leaderboard(update, context):
    output = "*LEADERBOARD* \n"
    list_scores = [(user, score) for user, score in context.bot_data["scores"].items()]
    list_scores.sort(key = lambda x: x[1], reverse = True)
    for i in range(len(list_scores)):
        score = list_scores[i]
        output += "*{}*\. {}: {}/{}\n".format(i + 1, score[0], score[1], len(config["questions"]))
    context.bot.send_message(chat_id=update.effective_chat.id, text=output, parse_mode = ParseMode.MARKDOWN_V2)

def clear_leaderboard_with_password(update, context):
    if len(context.args) == 1 and context.args[0] == "1212":
        clear_leaderboard(update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a password after /leaderboard command")

def clear_leaderboard(update, context):
    context.bot_data["scores"] = dict() 
    context.bot.send_message(chat_id=update.effective_chat.id, text="Leaderboard cleared!")

def main():
    my_persistence = PicklePersistence(filename='my_file')
    updater = Updater(token = bot_token, persistence=my_persistence, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            RESPOND: [
                CallbackQueryHandler(respond_to_query),
            ]
        },
        fallbacks=[CommandHandler('start', start)],
        persistent=True,
        name='conv_handler'
    )

    dispatcher.add_handler(conv_handler)

    leaderboard_handler = CommandHandler('leaderboard', leaderboard)
    dispatcher.add_handler(leaderboard_handler)

    clear_leaderboard_handler = CommandHandler('clearleaderboard', clear_leaderboard_with_password)
    dispatcher.add_handler(clear_leaderboard_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

    # link webhook to heroku server
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=bot_token)
    # updater.bot.setWebhook('https://stark-mesa-48399.herokuapp.com/' + bot_token)

    # updater.idle()


if __name__ == '__main__':
    main()
