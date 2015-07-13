from return_relevant_jobs import return_ranked_list_jobs


st_name = 'John Smith'
st_gender = 'Male'
st_major = 'Mechanical Engineering'
st_major_cat = 'Engineering, Science, and Technology'
st_car = 'Yes'
st_lang = 'Yes'
st_gpa = '4.0'
st_class = ''
st_skills = ''

[ranked_students, ranked_jobs] = return_ranked_list_jobs(st_name, st_gender, st_major, st_major_cat, st_car, st_lang, st_gpa, st_class, st_skills)
