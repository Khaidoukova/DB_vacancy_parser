from utils import get_vacancies, get_company_info, create_database, save_data_to_database
#from DBManager import DBManager
from pprint import pprint


employer_ids = ['1723062', '3542906', '810277', '4934', '42600']
emp_data = []
comp_data = []
print("Добрый день, господин проверяющий. Добро пожаловать в мой курсовой проект.")
print("Давайте создадим базу вакансий с сайта HeadHunter у десяти выбранных мной компаний.")
for emp_id in employer_ids:
    data1 = get_vacancies(emp_id)
    emp_data.append(data1)
    data2 = get_company_info(emp_id)
    comp_data.append(data2)

create_database("headhunter")
save_data_to_database(comp_data, emp_data, "headhunter")




