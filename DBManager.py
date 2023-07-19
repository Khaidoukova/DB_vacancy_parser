import psycopg2


class DBManager:

    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """ Получаем список всех компаний и количество вакансий у каждой компании."""
        with self.conn:
            self.cur.execute(f'SELECT company_name, number_of_vacancies FROM company_info')
            data = self.cur.fetchall()

        return data

    def get_all_vacancies(self):
        """ Получаем список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn:
            self.cur.execute("""
            SELECT vacancy_name, company_name, salary_from, salary_to, url
            FROM vacancies
            JOIN company_info USING (company_id)
            """)
            data = self.cur.fetchall()

        return data

    def get_avg_salary(self):
        """ Получаем среднюю зарплату по вакансиям."""
        with self.conn:
            self.cur.execute("""SELECT vacancy_name, (salary_from + salary_to) / 2 AS avg_salary
            FROM vacancies """)
            data = self.cur.fetchall()
        return data

    def get_vacancies_with_higher_salary(self):
        """ Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn:
            self.cur.execute("""SELECT vacancy_name, salary_from, url 
            FROM vacancies 
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)""")
            data = self.cur.fetchall()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """ Получаем список всех вакансий, в названии которых содержатся переданные в метод слова"""
        the_word = keyword[1:]
        with self.conn:
            self.cur.execute(f"""SELECT vacancy_name, company_name, salary_from, salary_to, url
            FROM vacancies
            INNER JOIN company_info USING (company_id)
            WHERE vacancy_name LIKE '%{the_word}%' """)
            data = self.cur.fetchall()
        return data
