from utils import get_vacancies, get_company_info, create_database, save_data_to_database
from DBManager import DBManager
from config import config


def main():
    params = config()  # загружаем параметры для подключение к базе данных
    employer_ids = ['1723062', '3542906', '810277', '4934', '67611', '65068', '1022259', '27003', '3968', '3672566']
    emp_data = []
    comp_data = []
    print("Добрый день, господин проверяющий. Добро пожаловать в мой курсовой проект.")
    print("Давайте создадим базу вакансий с сайта HeadHunter.")
    create_database("headhunter")  # создаем базу данных с необходимым нам названием
    print("А теперь давайте заполним базу данными десяти выбранных мной компаний.")
    for emp_id in employer_ids:
        data1 = get_vacancies(emp_id)  # получаем данные по вакансиям работодателей
        emp_data.append(data1)
        data2 = get_company_info(emp_id)  # получаем данные по работодателям
        comp_data.append(data2)
    save_data_to_database(comp_data, emp_data, "headhunter")  # загружаем данные по вакансиям и работодателям в базу
    dbase = DBManager('headhunter', **params)  # создаем экземпляр класса DBManager
    while True:
        user_input = input('Какая информация Вас интересует?\n'
                           '1 - список всех компаний и количество вакансий у каждой\n'
                           '2 - список всех вакансий с указанием названия компании, '
                           'названия вакансии и зарплаты и ссылки на вакансию\n'
                           '3 - средняя зарплата по вакансиям\n'
                           '4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                           '5 - показать вакансии по ключевому слову\n'
                           'Для выхода напишите слово "стоп"\n')

        if user_input == "1":
            n = dbase.get_companies_and_vacancies_count()
            for i in n:
                print(f"Название компании {i[0]}, количество вакансий {i[1]}")

        elif user_input == "2":
            n = dbase.get_all_vacancies()
            for i in n:
                print(f'Название вакансии: {i[0]}, '
                      f'Работодатель: {i[1]}, '
                      f'Зарплата от {i[2]} до {i[3]}, '
                      f'Ссылка на вакансию: {i[4]}')

        elif user_input == "3":
            n = dbase.get_avg_salary()
            for i in n:
                print(f'Название вакансии: {i[0]}, '
                      f'Средняя зарплата: {i[1]}')

        elif user_input == "4":
            n = dbase.get_vacancies_with_higher_salary()
            for i in n:
                print(f'Название вакансии: {i[0]}, '
                      f'Зарплата от: {i[1]}, '
                      f'Ссылка на вакансию: {i[2]}')
        elif user_input == "5":
            user_keyword = input("Введите ключевое слово для поиска: ")
            n = dbase.get_vacancies_with_keyword(user_keyword)
            for i in n:
                print(f'Название вакансии: {i[0]}, '
                      f'Работодатель: {i[1]}, '
                      f'Зарплата от {i[2]} до {i[3]}, '
                      f'Ссылка на вакансию: {i[4]}')

        elif user_input.lower() == "cnjg" or user_input.lower() == "стоп":
            quit()

        else:
            print("Команда не распознана. Попробуйте ввести еще раз.")


main()
