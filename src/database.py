import os
from supabase import create_client, Client
from dotenv import load_dotenv 

load_dotenv()

def create_sb_client():
  url: str = os.environ.get("SUPABASE_PROJECT_URL")
  key: str = os.environ.get("SUPABASE_API_KEY")
  supabase: Client = create_client(url, key)
  return supabase

def fetch_job_descriptions():
  try: 
    supabase = create_sb_client()
    start = 0
    limit = 1000
    all_job_descriptions = []
    
    while True:
      job_description_response = supabase.table('Job Postings').select('id', 'job_title', 'cleaned_job_description').range(start, start + limit).execute()
      if job_description_response:
        data = job_description_response.data 
        for row in data:
          identifier = row['id']
          job_title = row['job_title']
          job_description = row['cleaned_job_description']
          all_job_descriptions.append({'id': identifier, 'job_title': job_title, 'job_description_clean': job_description})
      
        start += limit 
        if len(data) < limit:
          break
      else:
        print("Error: Empty response from Supabase.")
        break 
      
    return all_job_descriptions
  
  except Exception as e:
    print('An error occurred:', e)

def fetch_user_resume(user_id):
    supabase = create_sb_client()
    user_resume_response = supabase.table('User').select('cleaned_resume').eq('id', user_id).limit(1).execute()
    return user_resume_response.data



