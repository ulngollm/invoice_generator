from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from pyrogram.types import Message
from state import ChatState
from commands import CommandFactory, CollectUserDataCommand, OfferActionCommand
import os
from storage import Cache
from model.invoice import Invoice

load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')

app = Client('bot', API_ID, API_HASH, bot_token=BOT_API_TOKEN)
chat_state = dict()
cache = Cache()

handlers = {
    ChatState.START: CollectUserDataCommand.start,
    ChatState.WAIT_NUMBER: CollectUserDataCommand.get_invoice_number,
    ChatState.WAIT_NAME: CollectUserDataCommand.get_name,
    ChatState.WAIT_INN: CollectUserDataCommand.get_inn,
    ChatState.WAIT_CLIENT_NAME: CollectUserDataCommand.get_client_name,
    ChatState.COLLECT_COMPLETE: OfferActionCommand.offer_generation
}


def hello(client: Client, message: Message):
    state = chat_state.get(message.from_user.id, ChatState.START)
    saved_invoice = cache.get_item(message.from_user.id)
    if not saved_invoice:
        saved_invoice = Invoice()
        cache.save_item(message.from_user.id, saved_invoice)

    command = CommandFactory.create(state, handlers)
    chat_state[message.from_user.id] = command.execute(client=client, message=message, invoice=saved_invoice)



app.add_handler(MessageHandler(hello, filters.command(['start'])))
app.add_handler(MessageHandler(hello, filters.text))

app.run()