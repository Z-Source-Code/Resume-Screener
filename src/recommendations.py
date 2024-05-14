import numpy as np
from scipy.sparse import csr_matrix, issparse
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
from database import fetch_job_descriptions, fetch_user_resume

def compute_similarity_scores(job_descriptions, resume, vectorizer):
  """
  Function to compute the cosine similarity score between the job descriptions and the resume.
  Args:
    job_descriptions (list of strings): job descriptions
    resume (string): resume
  Returns:
        similarity_scores: Cosine similarity scores between job descriptions and the resume
  """
  corpus = job_descriptions + [resume]
  tfidf_matrix = vectorizer.transform(corpus)
  sparse_tfidf_matrix = csr_matrix(tfidf_matrix)
  
  similarity_scores = cosine_similarity(sparse_tfidf_matrix[:-1], sparse_tfidf_matrix[-1])
  
  return similarity_scores

def get_recommendation(n, job_data, job_description_corpus, resume, vectorizer, current_skill_level):
    """
    Function to get the top n job descriptions that are most similar to the resume.
    Args:
        n (int): number of job descriptions to return
        job_data (list of dicts): array of job descriptions
        resume (string): resume
        vectorizer (TfidfVectorizer): TfidfVectorizer object
    Returns:
        top_n_jobs: List of dictionaries containing top n job descriptions and their similarity scores
    """
    similarity_scores = compute_similarity_scores(job_description_corpus, resume, vectorizer)
    top_n_indices = np.argsort(similarity_scores, axis=0)[-n:][::-1].flatten()
    
    top_n_jobs = []
    for index in top_n_indices:
        job_title = job_data[index]['job_title']
        job_description = job_data[index]['job_description_clean']
        similarity_score = similarity_scores[index][0]
        seniority_level = job_data[index]['seniority_level']

        for skill_level in current_skill_level:
          if seniority_level == skill_level:
            top_n_jobs.append({'job_title': job_title, 
                                'job_description_clean': job_description,
                                'similarity_score': similarity_score,
                                'seniority_level': seniority_level})
        
    return top_n_jobs

def main():
  n = 10
  vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 3), preprocessor=None, tokenizer=None)
  jobs_data = fetch_job_descriptions()
  
  job_description_corpus = [job['job_description_clean'] for job in jobs_data]
  vectorizer.fit(job_description_corpus)
  
  user_resume = fetch_user_resume('4fca706a-da00-4ed8-81d0-41af305d8ed7')
  cleaned_resume = user_resume[0]['cleaned_resume']
  
  
  current_skill_level = ['Internship', 'Entry level', 'Mid-Senior level', 'Associate', None]
  top_n_jobs_tfidf = get_recommendation(n, jobs_data, job_description_corpus, cleaned_resume, vectorizer, current_skill_level)
  
  for i, job in enumerate(top_n_jobs_tfidf):
        print(f"Rank {i+1}: {job['job_title']} - Similarity Score: {job['similarity_score']} - {job['seniority_level']}")


if __name__ == '__main__':
  main()