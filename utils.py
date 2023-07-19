import psycopg2
import requests
from config import config


def get_vacancies(employer_id, per_page=100):
    """Получаем данные по вакансиям работодателей с API сайта """
    v_list = []
    url = "https://api.hh.ru/vacancies"
    params = {'per_page': per_page,
              'employer_id': employer_id}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        vacancies = data.get('items')
        for vacancy in vacancies:
            company_name = vacancy['employer']['name']
            company_id = vacancy['employer']['id']
            vac_name = vacancy['name']
            if vacancy["salary"] is None:
                salary_min = None
                salary_max = None
            elif vacancy["salary"]["from"] == "0" and vacancy["salary"]["to"] != "0":
                salary_min = vacancy["salary"]["to"]
                salary_max = vacancy["salary"]["to"]
            elif vacancy["salary"]["from"] != "0" and vacancy["salary"]["to"] == "0":
                salary_min = vacancy["salary"]["from"]
                salary_max = vacancy["salary"]["from"]
            else:
                salary_min = vacancy["salary"]["from"]
                salary_max = vacancy["salary"]["to"]
            url = vacancy['alternate_url']

            v_dict = {'vac_name': vac_name,
                      'company_name': company_name,
                      'company_id': company_id,
                      'salary_min': salary_min,
                      'salary_max': salary_max,
                      'url': url}

            v_list.append(v_dict)

    return v_list


def get_company_info(employer_id):
    """Получаем данные по работодателям с API сайта """
    comp_list = []

    url = f"https://api.hh.ru/employers/{employer_id}"
    params = {'employer_id': employer_id}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        company_id = data['id']
        company_name = data['name']
        number_of_vacancies = data['open_vacancies']
        comp_dict = {'company_id': company_id,
                     'company_name': company_name,
                     'number_of_vacancies': number_of_vacancies}
        comp_list.append(comp_dict)

    return comp_list


params = config()  # загружаем параметры для подключение к базе данных


def create_database(database_name):
    """Создаем базу данных с заданным именем """
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(database='headhunter', **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company_info (
            company_id int PRIMARY KEY,
            company_name varchar(255),
            number_of_vacancies int                  
        )""")

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE vacancies (
        vacancy_name varchar(255),
        company_id int,
        salary_from int,
        salary_to int,
        url text)""")
    conn.commit()
    conn.close()


def save_data_to_database(data1, data2, database_name):
    """Загружаем данные, полученные по API, в созданную базу данных. """
    conn = psycopg2.connect(dbname=database_name, **params)
    cur = conn.cursor()
    for item in data1:
        for m in item:
            values = (m['company_id'], m['company_name'], m['number_of_vacancies'])
            cur.execute(
                """
                INSERT INTO company_info (company_id, company_name, number_of_vacancies)
                VALUES (%s, %s, %s)
                """, values)

    for vacancy in data2:
        for v in vacancy:
            values = (v['vac_name'], v['company_id'], v['salary_min'], v['salary_max'], v['url'])

            cur.execute(
                """
                INSERT INTO vacancies (vacancy_name, company_id, salary_from, salary_to, url)
                VALUES (%s, %s, %s, %s, %s)""", values)

    conn.commit()
    cur.close()
    conn.close()
