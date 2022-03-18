import vk_captchasolver as vc
from random import randint
import requests
import random
import time
import sys


token_vk = "ТОКЕН ОТ ВК"

message = "text"

while True:
    if True:

        user = input("Введите ссылку: ")

        try:
            messages = input('Сколько сообщений отправить: ')
            messages = int(messages)
            messages += 1
        except:
            print('Количество сообщений должно быть числом')
            sys.exit()

        def deleting_characters(users):
            parts = users.split("/")

            if users.lower().startswith(("https://", "http://")):
                user_name = parts[3]
                get_user_id(user_name)

            elif users.lower().user.startswith("vk.com/"):
                user_name = parts[1]
                get_user_id(user_name)

            else:
                print("❌ Неверная ссылка ❌")
                sys.exit()

        def get_user_id(user_name):

            data_get_user_id = {
                "user_ids": user_name,
                "access_token": token_vk,
                "v": "5.131"
            }

            response = requests.post("https://api.vk.com/method/users.get", data = data_get_user_id)
            data = response.json()

            if not data["response"]:
                print("❌ Неверный ид, проверьте ссылку ❌")
                sys.exit()

            else:
                user_id = data["response"][0]["id"]
                print(f"ID: {user_id}")
                for i in range(1, messages):
                    send_message(user_id)
                    time.sleep(1)


        def send_message(user_id):
            data_send_message = {
                "access_token": token_vk,
                "user_id": user_id,
                "random_id": random.randint(100, 5000),
                "message": message,
                "dont_parse_links": "false",
                "disable_mentions": "false",
                "intent": "default",
                "v": "5.131"
            }

            response = requests.post("https://api.vk.com/method/messages.send", data=data_send_message)
            send_messages = response.json()

            if "response" in send_messages:
                print(f"✅ Отправил сообщение пользователю: {user}")

            elif "error" in send_messages:
                if send_messages["error"]["error_code"] == 14:
                    print("❌ КАПЧА")

                    captcha_img = send_messages["error"]["captcha_img"]
                    img = requests.get(captcha_img)
                    file = open("captcha.png", "wb")
                    file.write(img.content)
                    file.close()
                    captcha_answer = vc.solve(image="captcha.png")

                    captcha_sid = send_messages["error"]["captcha_sid"]
                    data_captcha = {
                        "access_token": token_vk,
                        "user_id": user_id,
                        "random_id": random.randint(1, 100),
                        "message": message,
                        "captcha_sid": captcha_sid,
                        "captcha_key": captcha_answer,
                        "dont_parse_links": "false",
                        "disable_mentions": "false",
                        "intent": "default",
                        "v": "5.131"
                    }
                    requests.post("https://api.vk.com/method/messages.send", data=data_captcha)

                elif send_messages["error"]["error_code"] == 9:
                    print("❌ ФЛУД")

                elif send_messages["error"]["error_code"] == 29:
                    print("Достигнут количественный лимит на вызов метода"
                          "Подробнее об ограничениях на количество вызовов см. на странице "
                          "https://vk.com/dev/data_limits")

                else:
                    print("❌ НЕИЗВЕСТНАЯ ОШИБКА")
                    print(send_messages)

        if __name__ == "__main__":
            deleting_characters(user)
