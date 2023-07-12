from pprint import pprint

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
        return data

for employer_id in employer_ids:
    emp_data = get_vacancies(employer_id, keyword='python')
    data.append(emp_data)

pprint(data)

