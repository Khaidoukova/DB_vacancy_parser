import psycopg2
import requests


class DBManager:
    employer_ids = ['1723062', '3542906', '810277', '4934', '42600']

    def get_companies_and_vacancies_count(self, employer_id, per_page=100):

        url = "https://api.hh.ru/vacancies"
        params = {'per_page': per_page,
                  'employer_id': employer_id}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
