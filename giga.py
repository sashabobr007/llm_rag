from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import csv
import os
import time
import shutil
import re

def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        print(f"Файл успешно перемещен из {source_path} в {destination_path}")
    except FileNotFoundError:
        print("Указанный файл не найден.")


destination_folder = "done/"
promt = 'ask 5 questions about the text and write the answers to them in English"'
promt_answer = 'answer them in English'


def split_string(text, chunk_size=350):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


files = os.listdir(f'{os.getcwd()}/man')
with open('output.csv', 'a', newline='') as file_write:
    writer = csv.writer(file_write, delimiter=';')
    for filename in files:

        if 'preprocessed' in filename:
            command = filename.split('_')[0]
            print(command)
            with open(f'man/{filename}', 'r') as file:
                text = file.read()
                text = split_string(text)
                for text_small in text:
                    user_input = promt+ text_small + '"'
                    # Авторизация в сервисе GigaChat
                    chat = GigaChat(
                        credentials=os.getenv('CRED'),
                        verify_ssl_certs=False)

                    messages = [
                        SystemMessage(
                            content="Ты бот, который отвечает на вопросы по тексту"
                        )
                    ]
                    messages.append(HumanMessage(content=user_input))
                    res = chat(messages)
                    messages.append(res)
                    answer = res.content
                    print(answer)
                    print(len(answer))
                    if len(answer) < 450:
                        time.sleep(3)

                        splits = re.findall("\d\. ", answer)
                        texts = []
                        for i in range(len(splits)):
                            texts.append(answer)
                        
                        questions =[]

                        for i in range(len(splits)):
                            new = texts[i].split(splits[i])[1]
                            question = new.split('?')[0] + '?'

                            questions.append(question)

                        print('q')
                        print(questions)

                        messages.append(HumanMessage(content=promt_answer))
                        res = chat(messages)
                        messages.append(res)
                        answer = res.content
                        print(answer)

                        splits = re.findall("\d\. ", answer)
                        texts = []
                        for i in range(len(splits)):
                            texts.append(answer)

                        answers = []

                        for i in range(len(splits)):
                            new = texts[i].split(splits[i])[1]
                            answer = new.split('.\n')[0]

                            answers.append(answer)
                        print('a')
                        print(answers)
                        questions_and_answers = dict(zip(questions, answers))
                        for question, answer in questions_and_answers.items():

                            writer.writerow([command, question, answer])
                        #time.sleep(3)
                    else:

                        questions_and_answers = {}
                        splits = re.findall("\d\. ", answer)
                        texts = []
                        for i in range(len(splits)):
                            texts.append(answer)

                        for i in range(len(splits)):
                            new = texts[i].split(splits[i])[1]
                            question = new.split('?')[0]
                            try:
                                answer = new.split(question)[1].split(splits[i + 1])[0]
                                # print(answer)
                            except:
                                answer = new.split(question)[1].split("?")[1]
                            try:
                                answer = answer.split('   Ответ: ')[1]
                            except:
                                try:
                                    answer = answer.split('Answer: ')[1]
                                except:
                                    try:
                                        answer = answer.split('?\n')[1]
                                    except:
                                        pass
                            questions_and_answers[question + '?'] = answer

                        # Перебор словаря и вывод вопросов и ответов
                        for question, answer in questions_and_answers.items():
                            # print(question)
                            # print(answer)
                            writer.writerow([command, question, answer])
                        #time.sleep(1)

            source_file = f"man/{filename}"
            move_file(source_file, os.path.join(destination_folder, filename))
