import folium
import webbrowser
from dadata import Dadata
from art import tprint

import database as db


def make_map(lat, lon, full_address):
    map = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker(location=[lat, lon], popup=full_address).add_to(map)
    map.save('map.html')
    webbrowser.open('map.html')


def dadata_menu(token, secret):
    while True:
        tprint('-- Dadata menu --', font='small', chr_ignore=True)
        print('Доступные действия:')
        print('\n1. Поиск координат по адресу')
        print('\n2. Вернуться в главное меню')
        choice = input('\nВыберите действие: ')
        if choice == '1':
            query = input('\nВведите адрес: ')
            dadata = Dadata(token, secret)
            result = dadata.suggest(name="address", query=query)
            if result:
                for count, item in enumerate(result, start=1):
                    print(f'{count}) - {item["value"]}')
                choice = input('\nВыберите нужный адрес: ')
                finanal_result = dadata.clean(
                    name="address", source=result[int(choice) - 1]["value"])
                full_address = finanal_result["result"]
                lat = finanal_result["geo_lat"]
                lon = finanal_result["geo_lon"]
                tprint('-- Result --', font='small', chr_ignore=True)
                print(
                    f'\nКоординаты {full_address}: Широта - {lat}, Долгота - {lon}')
                print('\n1. Показать на карте (Будет открыта веб-страница)')
                print('\n2. Вернуться в dadata menu')
                choice = input('\nВыберите действие: ')
                if choice == '1':
                    make_map(lat, lon, full_address)
                elif choice == '2':
                    continue
            else:
                print('\n-- Ошибка--\nНе удалось найти адрес')
        elif choice == '2':
            break
        else:
            print(f'\n-- Ошибка--\nНеверный ввод\nУкажите номер действия цифрой')


def main_menu():
    while True:
        tprint('-- Main menu --', font='small', chr_ignore=True)
        print('Доступные действия:')
        print('1. Регистрация')
        print('2. Вход')
        print('3. Выход')
        choice = input('\nВыберите действие: ')
        if choice == '1':
            username = input('\nВведите имя пользователя: ')
            if db.check_user(username):
                print(f'\n-- Ошибка--\nПользователь с таким именем уже существует\nВыберите уникальное имя\n')
                continue
            password = input('Введите пароль: ')
            token = input('Введите токен (API-ключ): ')
            secret = input('Введите секрет (Секретный ключ): ')
            db.create_user(username, password, token, secret)
            print('\nПользователь успешно зарегистрирован\nМожете авторизоваться\n')
        elif choice == '2':
            username = input('\nВведите имя пользователя: ')
            password = input('\nВведите пароль: ')
            if db.login_user(username, password):
                print('\nВход выполнен')
                user = db.get_token_and_secret(username)
                dadata_menu(user[0], user[1])
            else:
                print(f'\n-- Ошибка--\nНеверный логин или пароль')
        elif choice == '3':
            break
        else:
            print(f'\n-- Ошибка--\nНеверный ввод\nУкажите номер действия цифрой')


if __name__ == '__main__':
    main_menu()
    input('Нажмите Enter для выхода')
    exit()
