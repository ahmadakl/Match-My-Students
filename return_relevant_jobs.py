from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import preprocessing, metrics, cross_validation
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.metrics import jaccard_similarity_score
from sklearn.datasets.samples_generator import make_blobs
import pandas as pd
import numpy as np
import itertools
from itertools import chain
import scipy
from scipy import spatial
from scipy.spatial import distance
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from pandas import DataFrame
from demo_functions import map_to
from demo_functions import map_back
from demo_functions import exists_in_list
import pymysql as mdb


def return_ranked_list_jobs(st_name, st_gender, st_major, st_major_cat, st_car, st_lang, st_gpa, st_class, st_skills):

	con = mdb.connect('localhost', 'root', '', 'demodb')

	students_database = pd.read_sql(sql="SELECT * FROM Student_Sum", con=con)
 	jobs_database = pd.read_sql(sql="SELECT * FROM Jobs", con=con)

	[mod_car, mod_lang, mod_gpa] = map_to(st_car, st_lang, st_gpa)

	student_description = st_gender + "," + st_major + "," + st_major_cat + "," + mod_car + "," + mod_lang + "," + mod_gpa + "," + st_class + "," + st_skills
	s1 = pd.Series(0, name='id')
	s2 = pd.Series(student_description, name='description')
	student_db = pd.concat([s1, s2], axis=1)

	database_cols = students_database.iloc[:,1:]
	database_clean = database_cols.iloc[:,0:len(database_cols.columns)-1]
	database_clean.loc[database_clean['gpa'] <= 1, 'gpa'] = 'very_poor_average'
	database_clean.loc[(database_clean['gpa'] > 1) & (database_clean['gpa'] <= 2), 'gpa'] = 'poor_average'
	database_clean.loc[(database_clean['gpa'] > 2) & (database_clean['gpa'] <= 3), 'gpa'] = 'good_average'
	database_clean.loc[(database_clean['gpa'] > 3) & (database_clean['gpa'] <= 3.5), 'gpa'] = 'very_good_average'
	database_clean.loc[(database_clean['gpa'] > 3.5) & (database_clean['gpa'] <= 4), 'gpa'] = 'excellent_average'

	# return ranked list of students based on cosine similarity

	students_description = database_clean.gender.map(str) + "," + database_clean.major_title + "," + database_clean.major_category + "," + database_clean.own_car + "," + database_clean.speaks_foreign_languages + "," + database_clean.gpa + "," + database_clean.favorite_class + "," + database_clean.skills

	students_ids = database_clean.loc[:,'student_id']
	s1 = pd.Series(students_ids, name='id')
	s2 = pd.Series(students_description, name='description')
	students_db = pd.concat([s1, s2], axis=1)
	students_db = student_db.append(students_db)

	count_vect = CountVectorizer()
	students_counts = count_vect.fit_transform(students_db.description)
	students_tf_transformer = TfidfTransformer(use_idf=False).fit(students_counts)
	students_tf = students_tf_transformer.transform(students_counts)
	similarity_matrix = metrics.pairwise.linear_kernel(students_tf[1:,:], students_tf[0,:])

	similarity_col = list(itertools.chain.from_iterable(similarity_matrix))
	sorted_sim_indices = np.argsort(similarity_col)
	top_indices = np.fliplr([sorted_sim_indices[-10:]])[0]
	top_sim_costs = similarity_matrix[top_indices]
	similar_students = database_cols.iloc[top_indices,:]

	top_sim_costs_mapped = list(itertools.chain.from_iterable(top_sim_costs))
	similar_students.loc[:,'similarity_cost'] = pd.Series(top_sim_costs_mapped, index=similar_students.index)

	ranked_students = []
	[result_car, result_lang] = map_back(mod_car, mod_lang)
	new_student = dict(id=st_name, gender=st_gender, m_title=st_major, car=result_car, lang=result_lang, gpa=st_gpa, skills=st_skills)
	ranked_students.append(new_student)
	for std in range(len(similar_students)):
    		result = similar_students.iloc[std,:]
    		[result_car, result_lang] = map_back(result[4], result[5])
    		ranked_students.append(dict(id=result[0], gender=result[1], m_title=result[2], car=result_car, lang=result_lang, gpa=result[6], skills=result[8]))

    # return the list of jobs that similar students applied to

	similar_students.loc[:,'jobs_unique'] = similar_students['job_listing_id'].map(lambda x: map(int, x.split(",")))
  	jobs_listings = similar_students.loc[:,'jobs_unique']
  	
  	listings = list(itertools.chain.from_iterable(jobs_listings.tolist()))
  	jobs_database = jobs_database.iloc[:,1:]
  	relevant_jobs = jobs_database.loc[jobs_database['job_id'].isin(listings)]
  	relevant_jobs_active = relevant_jobs.loc[relevant_jobs['status'] == 'active', :]
  	relevant_jobs_active.sort(['when_active'], ascending=[False], inplace=True)
  	
    # Get the jobs that are relevant to the new student
	
	labels = jobs_database['cluster_label']
	relevant_jobs_ind = map(int, jobs_database.loc[jobs_database['job_id'].isin(listings)].index)
	clusters = labels[relevant_jobs_ind[:]]
	cluster_jobs = jobs_database.loc[jobs_database['cluster_label'].isin(clusters)]
	cluster_jobs_active = cluster_jobs.loc[cluster_jobs['status'] == 'active',:]

	jobs_active_id = cluster_jobs_active.loc[:,'job_id']
	jobs_active_description = cluster_jobs_active.job_title.map(str) + "," + cluster_jobs_active.responsibilities + "," + cluster_jobs_active.skills + "," + cluster_jobs_active.qualifications

	s1 = pd.Series(jobs_active_id, name='id')
	s2 = pd.Series(jobs_active_description, name='description')
	jobs_active_db = pd.concat([s1, s2], axis=1)
	student_job_comp = student_db.append(jobs_active_db)
	
	count_vect = CountVectorizer()
	st_jobs_counts = count_vect.fit_transform(student_job_comp.description)
	tf_transformer = TfidfTransformer(use_idf=False).fit(st_jobs_counts)
	st_job_tf = tf_transformer.transform(st_jobs_counts)
	
	st_job_sim_matrix = metrics.pairwise.linear_kernel(st_job_tf[1:,:], st_job_tf[0,:])
	st_job_sim_col = list(itertools.chain.from_iterable(st_job_sim_matrix))
	st_job_sim_col_array = np.array(st_job_sim_col)
	top_indices_thresh = np.where(st_job_sim_col_array >= 0.25)[0]
	top_costs = st_job_sim_col_array[top_indices_thresh]

	similar_jobs = cluster_jobs_active.iloc[top_indices_thresh,:]
	similar_jobs.drop('cluster_label', axis=1, inplace=True)
	similar_jobs['similarity_cost'] = pd.Series(top_costs, index=similar_jobs.index)
	similar_jobs.sort(['when_active'], ascending=[False], inplace=True)

	ranked_jobs = []
	for job in range(len(similar_jobs)):
    		jlist = similar_jobs.iloc[job,:]
    		ranked_jobs.append(dict(id=jlist[0], title=jlist[1], name=jlist[2], status=jlist[5], created_at=jlist[3]))
	
	for job in range(len(relevant_jobs_active)):
    		jlist = relevant_jobs_active.iloc[job,:]
    		if(not exists_in_list(jlist, ranked_jobs)):
    			ranked_jobs.append(dict(id=jlist[0], title=jlist[1], name=jlist[2], status=jlist[5], created_at=jlist[3]))

	return ranked_students, ranked_jobs
