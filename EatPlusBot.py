from symbol import if_stmt

import requests
import json
import os
from User import User


class EatPlusBot:

    def __init__(self):

        token = '5700849117:AAGyTAPHlWpF0IoTnogZ8aN-EU0QL_m1zwk'
        self.url = f'https://api.telegram.org/bot{token}/'
        self.user = User

    def Start(self):

        respota2 = ""
        update_id = None

        while True:

            update = self.read_new_messages(update_id)
            data = update["result"]

            if data:

                for info in data:

                    update_id = info['update_id']
                    message = str(info["message"]["text"])
                    chat_id = info["message"]["from"]["id"]
                    print(chat_id)
                    first_message = int(info["message"]["message_id"]) == 1

                    answer = self.create_answer(message, first_message)
                    respota2 = answer

                    if answer == "Qual o seu nome?":
                        respota2 = answer
                        self.response(respota2, chat_id)
                        motor = True
                        while motor:

                            update = self.read_new_messages(update_id)
                            data = update["result"]

                            if data:

                                for info in data:
                                    update_id = info['update_id']
                                    message = str(info["message"]["text"])
                                    chat_id = info["message"]["from"]["id"]
                                    print(chat_id)
                                    first_message = int(info["message"]["message_id"]) == 1

                                    answer = self.metodoDois(message, first_message)
                                    respota2 = answer

                                    if answer == "Cadastro finalizado com sucesso!":
                                        respota2 = answer
                                        self.response(respota2, chat_id)
                                        motor = False

                                    self.response(respota2, chat_id)

                    self.response(respota2, chat_id)

    def read_new_messages(self, update_id):

        link_req = f'{self.url}getUpdates?timeout=5'

        if update_id:
            link_req = f'{link_req}&offset={update_id + 1}'

        result = requests.get(link_req)

        return json.loads(result.content)

    def create_answer(self, message, first_message):

        print('client message: ' + str(message))

        if first_message == True or message.lower() in ('oi', 'Oi', 'oi.', 'Oi.', 'oi!', 'Oi!'):
            return f'Eu me chamo Rafaela.{os.linesep}Vou preencher sua ficha pra você, então preciso que você me fale as informações que te pedir.{os.linesep}Podemos começar, Sim ou não?'

        if message == message in ('sim', 's', 'Sim', 'sim.', 'Sim.'):
            return "Qual o seu nome?"

        if message == message in "1":
            return "Agora qual seu E-mail?"

        if message == message in "2":
            return "Por fim digite sua Senha"

        if message == message in "3":

            return "Cadastro finalizado com sucesso!"

        elif message == message in ('não', 'n', 'Não', 'não.', 'Não.', 'nao', 'Nao', 'Nao.', 'nao.'):
            return 'Quando estiver pronto(a), me diga "oi" que eu venho!'

        else:
            return 'Se quiser falar comigo, só dizer "oi"!'

    def metodoDois(self, message, first_message):
        print('client message: ' + str(message))

        if first_message == True or message.lower() in ('oi', 'Oi', 'oi.', 'Oi.', 'oi!', 'Oi!'):
            return f'Eu me chamo Rafaela.{os.linesep}Vou preencher sua ficha pra você, então preciso que você me fale as informações que te pedir.{os.linesep}Podemos começar, Sim ou não?'

        if message == message in ('sim', 's', 'Sim', 'sim.', 'Sim.'):
            return "Qual o seu nome?"

        if message == message in "1":
            return "Agora qual seu E-mail?"

        if message == message in "2":
            return "Por fim digite sua Senha"

        if message == message in "3":

            return "Cadastro finalizado com sucesso!"

        elif message == message in ('não', 'n', 'Não', 'não.', 'Não.', 'nao', 'Nao', 'Nao.', 'nao.'):
            return 'Quando estiver pronto(a), me diga "oi" que eu venho!'

        else:
            return f'Digite 1 para confirmar seu Nome.{os.linesep}Digite 2 para confirmar seu E-mail.{os.linesep}Digite 3 para confirmar sua Senha.'

    def response(self, answer, chat_id):

        link_req = f'{self.url}sendMessage?chat_id={chat_id}&text={answer}'
        requests.get(link_req)
        print("answer: " + str(answer))
