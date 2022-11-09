import requests
import json
import os
from User import User
import re

class EatPlusBot:

    def __init__(self):

        token = '5700849117:AAGyTAPHlWpF0IoTnogZ8aN-EU0QL_m1zwk'
        self.url = f'https://api.telegram.org/bot{token}/'
        self.user = User()

    def Start(self):

        update_id = None

        while True:

            update = self.read_new_messages(update_id)
            data = update["result"]

            if data:

                for info in data:

                    update_id = info['update_id']
                    message = str(info["message"]["text"])
                    chat_id = info["message"]["from"]["id"]
                    first_message = int(info["message"]["message_id"]) == 1

                    update = self.read_new_messages(update_id)
                    answer = self.create_answer(message, first_message,chat_id)
                    self.response(answer, chat_id)

    def read_new_messages(self, update_id):

        link_req = f'{self.url}getUpdates?timeout=1'

        if update_id:
            link_req = f'{link_req}&offset={update_id + 1}'
        result = requests.get(link_req)

        return json.loads(result.content)

    def create_answer(self, message, first_message, chat_id):

        print('client message: ' + str(message))

        condition_no = message == message in ('não', 'n', 'Não', 'não.', 'Não.', 'nao', 'Nao', 'Nao.', 'nao.')
        condition_yes = message == message in ('sim', 's', 'Sim', 'sim.', 'Sim.')
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if self.user.id == '':
            if first_message == True or message in ('oi', 'Oi', 'oi.', 'Oi.', 'oi!', 'Oi!') or '/start':
                self.user.id = 'placeholder'
                return f'Eu me chamo Rafaela.{os.linesep}Vou preencher sua ficha pra você, então preciso que você me fale as informações que te pedir.{os.linesep}Podemos começar?{os.linesep}Sim ou não?'
            else:
                return 'Se quiser falar comigo, só dizer "oi"!'
        elif self.user.id == chat_id:
                return f"Olá {self.user.name}. Seu cadastro já foi realizado!"

        if self.user.name == '':
            if message == message in ('sim', 's', 'Sim', 'sim.', 'Sim.','continuar','Continuar'):
                self.user.name = 'placeholder'
                return "Qual o seu nome?"
            elif condition_no:
                return 'Me avise quando estiver pronto(a)! Só dizer "continuar".'
            else:
                return f"Poderia verificar sua resposta?"

        if self.user.name == 'placeholder' and self.user.email == '':
            self.user.name = message
            return f"Seu nome será {self.user.name}. Tem certeza? sim, ou não?"

        if self.user.name != 'placeholder' and self.user.email == '':
            if condition_yes:
                self.user.email = 'place@holder.com'
                return "Qual o seu email?"
            elif condition_no:
                self.user.name = 'placeholder'
                return "Reescreva seu nome"
            else:
                return f"Seu nome será {self.user.name}. Tem certeza? sim, ou não?"

        if self.user.email == 'place@holder.com' and self.user.name != 'placeholder':
            if re.fullmatch(regex, message):
                self.user.email = message
                return f"Seu email será {self.user.email}. Tem certeza? sim ou não?"
            else:
                return "Escreva um email válido"

        if self.user.email != 'place@holder.com' and self.user.password == '':
            if condition_yes:
                self.user.password = 'placeholder'
                return "Qual será sua senha? (mínimo de 6 caractéres)"
            elif condition_no:
                self.user.email = 'place@holder.com'
                return "Reescreva seu email"
            else:
                return f"Seu email será {self.user.email}. Tem certeza? sim ou não?"

        if self.user.email != 'place@holder.com' and self.user.name != 'placeholder' and self.user.password == 'placeholder':
            if len(message) >= 6:
                self.user.password = message
                return f"Sua senha será {self.user.password}. Tem certeza?{os.linesep}Sim ou não?"
            else:
                return "Escreva uma senha válida"

        if self.user.password != 'placeholder':
            if condition_yes:
                self.user.id = chat_id
                return f"Cadastro finalizado!{os.linesep}Nome: {self.user.name}{os.linesep}Email: {self.user.email}{os.linesep}Senha: {self.user.password}{os.linesep}"
            elif condition_no:
                self.user.password = 'placeholder'
                return "Reescreva sua senha"
            else:
                return f"Sua senha será {self.user.password}. Tem certeza?{os.linesep}Sim ou não?"

    def response(self, answer, chat_id):

        link_req = f'{self.url}sendMessage?chat_id={chat_id}&text={answer}'
        requests.get(link_req)
        print("answer: " + str(answer))
