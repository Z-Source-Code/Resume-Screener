from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
from database import create_sb_client

def compute_similarity_score(job_descriptions, resume, vectorizer):
  """
  Function to compute the cosine similarity score between the job descriptions and the resume.
  Args:
    job_descriptions (series): job descriptions
    resume (string): resume
  """
  text_list = job_descriptions.values.tolist() + [resume]
  tfidf_matrix = vectorizer.fit_transform(text_list)
  similarity_scores = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])
  return similarity_scores


def get_recommendation(n, data_jobs, resume, vectorizer):
  """
  Function to get the top n job descriptions that are most similar to the resume.
  Args:
    n (int): number of job descriptions to return
    data_jobs (dataframe): dataframe of job descriptions
  """
  similarity_scores = compute_similarity_score(data_jobs['job_description_clean'], resume, vectorizer)
  top_n_indices = np.argsort(similarity_scores, axis=0)[-n:].flatten()
  
  top_n_jobs = []
  for index in top_n_indices[::-1]:
      job_title = data_jobs.iloc[index]['job_title']
      job_descriptions = data_jobs.iloc[index]['job_description_clean']
      similarity_score = similarity_scores[index][0]
      top_n_jobs.append({'job_title': job_title, 'job_description_clean': job_descriptions, 'similarity_scores': similarity_score})

  return pd.DataFrame(top_n_jobs)


def main():
  n = 10
  vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
  top_n_jobs_tfidf = get_recommendation(n, data_jobs, lemmatized_resume, vectorizer)
  

if __name__ == '__main__':
  main()