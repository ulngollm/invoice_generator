from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from pyrogram.types import Message
from state import ChatState
from commands import CollectUserDataCommand
import os


load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')

app = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)
# типа {chat_id: State}
chat_state = dict()

handlers = {
    ChatState.START: CollectUserDataCommand.start,
    ChatState.WAIT_NUMBER: CollectUserDataCommand.get_invoice_number,
    ChatState.WAIT_NAME: CollectUserDataCommand.get_name,
    ChatState.WAIT_INN: CollectUserDataCommand.get_inn,
    ChatState.WAIT_CLIENT_NAME: CollectUserDataCommand.get_client_name
}


def hello(client: Client, message: Message):
    state = chat_state.get(message.from_user.id, ChatState.START)
    # херово что я императивно вызываю именно эту команду. А если мне уже надо другую?
    command = CollectUserDataCommand(handlers, state, client, message)
    chat_state[message.from_user.id] = command.execute()
    

app.add_handler(MessageHandler(hello, filters.command(['start'])))
app.add_handler(MessageHandler(hello, filters.text))

app.run()