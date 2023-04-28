from pyrogram import Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from state import ChatState


class Command:
    def __init__(self, handler: callable) -> None:
        self.handler = handler

    def execute(self, **args):
        return self.handler(**args)


class CommandFactory:
    @staticmethod
    def create(state: int, handlers: dict):
        handler = handlers.get(state)
        return Command(handler)


class CollectUserDataCommand:
    def start(client, message) -> int:
        message.reply(
            'привет! Напиши номер счета, пжлст'
        )
        return ChatState.WAIT_NUMBER


    def get_invoice_number(client, message):
        num = message.text
        message.reply(
            'Теперь имя, пжлст'
        )
        return ChatState.WAIT_NAME
    

    def get_name(client, message):
        name = message.text
        message.reply(
            'Имя сохранили. Теперь ИНН'
        )
        return ChatState.WAIT_INN


    def get_inn(client, message):
        inn = message.text
        message.reply(
            'Имя вашего клиента'
        )
        return ChatState.WAIT_CLIENT_NAME


    def get_client_name(client, message):
        client_name = message.text
        message.reply(
            'Ну теперь вроде все'
        )
        return ChatState.COLLECT_COMPLETE
    

class OfferActionCommand:
    def offer_generation(client, message: Message):
        message.reply(
            'Все данные собраны. Сгенерировать счет или изменить данные?',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    'Сгенерировать счет',
                    callback_data='generate:%d' % message.from_user.id
                )
            ],
            [
                InlineKeyboardButton(
                    'Изменить данные',
                    callback_data='change:%d' % message.from_user.id
                )
            ]])
        )