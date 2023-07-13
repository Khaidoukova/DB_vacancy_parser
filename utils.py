from pprint import pprint
from config import config

import psycopg2
import requests
#
employer_ids = ['1723062', '3542906', '810277', '4934', '42600']
data = []
def get_vacancies(employer_id, per_page = 100):
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
#for employer_id in employer_ids:
    #n = get_vacancies(employer_id, 100)
   # pprint(n)

def get_company_info(employer_ids):
    comp_list = []

    for employer_id in employer_ids:
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


def create_database(database_name, params):
    conn = psycopg2.connect(host='localhost', user='postgres', password='320670', port=5432)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(host='localhost', database='headhunter', user='postgres', password='320670', port=5432)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company_info (
            company_id int PRIMARY KEY,
            company_name varchar(255),
            number_of_vacancies int                  
        )""")
    conn.commit()
    conn.close()


params = config()
create_database('HeadHunter', params)






