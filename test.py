from requests import get, post, delete, patch, put


def test_get_user():
    # User по id 1 и 2 существуют
    print(get('http://127.0.0.1:5050/api/v2/users/1').json())
    print(get('http://127.0.0.1:5050/api/v2/users/2').json())

    # User по id 999 не существует
    print(get('http://127.0.0.1:5050/api/v2/users/999').json())


def test_delete_user():
    print('Before: ')
    test_get_users()

    print('Request:')
    # User по id 1 существует
    print(delete('http://127.0.0.1:5050/api/v2/users/1').json())

    # User по id 999 не существует
    print(delete('http://127.0.0.1:5050/api/v2/users/999').json())

    test_get_users()

    print('After: ')
    test_get_users()


def test_get_users():
    print(get('http://127.0.0.1:5050/api/v2/users/').json())


def test_post_user():
    print('Before: ')
    test_get_users()

    print('Request:')

    # Пользователь добавляется
    print(post('http://127.0.0.1:5050/api/v2/users/',
               json={
                   'name': 'Andrey',
                   'surname': 'Vydra',
                   'age': 17,
                   'position': 'Engineer',
                   'speciality': 'Engineer',
                   'address': 'Address',
                   'email': 'email1@yandex.ru'
               }).json())

    # Не все аргументы
    print(post('http://127.0.0.1:5050/api/v2/users/',
               json={
                   'name': 'Andrey',
                   'surname': 'Vydra'
               }).json())

    # Ошибка с одинаковой почтой
    print(post('http://127.0.0.1:5050/api/v2/users/',
               json={
                   'name': 'Andrey',
                   'surname': 'Vydra',
                   'age': 17,
                   'position': 'Engineer',
                   'speciality': 'Engineer',
                   'address': 'Address',
                   'email': 'email1@yandex.ru'
               }).json())

    print('After: ')
    test_get_users()


test_get_user()
print('--------------------')
test_get_users()
print('--------------------')
test_delete_user()
print('--------------------')
test_post_user()
print('--------------------')
