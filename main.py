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


def greeting(client: Client, message: Message):
    state = chat_state.get(message.from_user.id, ChatState.START)

    if state != ChatState.COLLECT_COMPLETE:
        OfferActionCommand.retry(client, message)
        return
    
    OfferActionCommand.offer_collect_data(client, message)


def collect_data(client: Client, message: Message):
    state = chat_state.get(message.from_user.id, ChatState.START)
    saved_invoice = cache.get_item(message.from_user.id)
    if not saved_invoice:
        saved_invoice = Invoice()
        cache.save_item(message.from_user.id, saved_invoice)

    command = CommandFactory.create(state, handlers)
    chat_state[message.from_user.id] = command.execute(client=client, message=message, invoice=saved_invoice)


def generate(client: Client, message: Message):
    state = chat_state.get(message.from_user.id, ChatState.START)
    if state != ChatState.COLLECT_COMPLETE:
        message.reply(
            'Не заполнены данные, из которых генерировать отчет. Чтобы заполнить, выберите команду /collect'
        )

app.add_handler(MessageHandler(greeting, filters.command(['start'])))
app.add_handler(MessageHandler(collect_data, filters.command(['collect'])))
app.add_handler(MessageHandler(generate, filters.command(['generate'])))
app.add_handler(MessageHandler(collect_data, filters.text))

app.run()