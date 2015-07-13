# Match-My-Students

Match-My-Students is product that takes in information about a student and returns a ranked list of relevant jobs available in the database of a student-employment facilitating company. In the case that no relevant jobs can be found, the model outputs a message stating that our robot, Job-roid, has embarked on a mission to get the student the best jobs that match their profile and will return shortly. A demo of Match-My-Students can be found at www.matchmystudents.com

main.py - main file that takes in the information about a student and returns a ranked list of jobs relevant to the student's profile. It calls the function get_ranked_list_jobs in return_relevant_jobs.py.

return_relevant_jobs.py - a file that contains the function get_ranked_list_jobs. It imports the required modules and functions and implements the following algorithm:
  - First, processes the given student's text data and all the text data of the other students in the database.
  - Tokenizes the text data, filters stop words, and then calculates term-frequences to compute the cosine similarity between the given student and the other students in the database.
  - Identifies the top 10 most similar students in the database.
  - Then, looks for the clusters of job listings that contain the jobs that these similar students applied to.
  - Finally, returns a ranked list of the active jobs in these clusters to the given student.

demo_functions.py - a file that contains a number of functions that get called by return_ranked_list_jobs.
