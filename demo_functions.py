import pymysql as mdb
import pandas as pd
import string
import numpy as np

def map_to(st_car, st_lang, st_gpa):

	if st_car == 'Yes':
		mod_car = 'own_car'
	else:
		mod_car = 'does_not_own_car'

	if st_lang == 'Yes':
		mod_lang = 'speaks_other_languages'
	else:
		mod_lang = 'does_not_speak_other_languages'
	
	st_gpa = float(st_gpa)
	if st_gpa <= 1:
		mod_gpa = 'very_poor_average'
	else:
		if (st_gpa > 1) & (st_gpa <= 2): 
			mod_gpa= 'poor_average'
		else:
			if (st_gpa > 2) & (st_gpa <= 3):
				mod_gpa = 'good_average'
			else:
				if (st_gpa > 3) & (st_gpa <= 3.5):
					mod_gpa = 'very_good_average'
				else:
					mod_gpa = 'excellent_average'

	return mod_car, mod_lang, mod_gpa



def map_back(result_car, result_lang):

	if result_car == 'own_car':
		result_car = 'Yes'
	else:
		if result_car == 'does_not_own_car':
			result_car = 'No'

	if result_lang == 'speaks_other_languages':
		result_lang = 'Yes'
	else:
		if result_lang == 'does_not_speak_other_languages':
			result_lang = 'No'

	return result_car, result_lang

def exists_in_list(jlist, ranked_jobs):
	job_test_id = jlist.job_id
	for item in ranked_jobs:
		if item['id'] == job_test_id:
			return True
	return False


def get_databases():
	con = mdb.connect('localhost', 'root', '', 'demodb')
	students_database = pd.read_sql(sql="SELECT * FROM Student_Sum", con=con)
	jobs_database = pd.read_sql(sql="SELECT * FROM Jobs", con=con)
	return students_database, jobs_database








