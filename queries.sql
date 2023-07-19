1. INSERT INTO company_info (company_id, company_name, number_of_vacancies) VALUES (%s, %s, %s)
2. INSERT INTO vacancies (vacancy_name, company_id, salary_from, salary_to, url) VALUES (%s, %s, %s, %s, %s)
3. SELECT company_name, number_of_vacancies FROM company_info
4. SELECT vacancy_name, company_name, salary_from, salary_to, url FROM vacancies JOIN company_info USING (company_id)
5. SELECT vacancy_name, (salary_from + salary_to) / 2 AS avg_salary FROM vacancies
6. SELECT vacancy_name, salary_from, url FROM vacancies WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)
7. SELECT vacancy_name, company_name, salary_from, salary_to, url FROM vacancies INNER JOIN company_info USING (company_id) WHERE vacancy_name LIKE '%{the_word}%'
