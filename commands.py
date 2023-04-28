from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from state import ChatState


class Command:
    def __init__(self, handlers: map, state: int, client: Client, message: Message = None, callback_query: CallbackQuery = None) -> None:
        self.handlers = handlers
        self.state = state
        self.client = client
        self.message = message
        self.callback_query = callback_query


    def execute(self):
        handler = self.handlers.get(self.state)
        if handler == None:
            return None
        return handler(self)


class CollectUserDataCommand(Command):
    def start(self) -> int:
        # todo предложить заполнить имя
        self.message.reply(
            'привет! Напиши номер счета, пжлст'
        )
        return ChatState.WAIT_NUMBER


    def get_invoice_number(self):
        num = self.message.text
        self.message.reply(
            'Теперь имя, пжлст'
        )
        return ChatState.WAIT_NAME
    

    def get_name(self):
        name = self.message.text
        self.message.reply(
            'Имя сохранили. Теперь ИНН'
        )
        return ChatState.WAIT_INN


    def get_inn(self):
        # todo получить номер клиента из вывода
        inn = self.message.text
        self.message.reply(
            'Имя вашего клиента'
        )
        return ChatState.WAIT_CLIENT_NAME


    def get_client_name(self):
        client_name = self.message.text
        self.message.reply(
            'Ну теперь вроде все'
        )
        return ChatState.COLLECT_COMPLETE