import os
from supabase import create_client, Client
from dotenv import load_dotenv 
import pymupdf

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
      job_description_response = supabase.table('Job Postings') \
      .select('id', 'job_title', 'cleaned_job_description', 'formatted_experience_level') \
      .range(start, start + limit) \
      .execute()
      
      if job_description_response:
        data = job_description_response.data 
        for row in data:
          identifier = row['id']
          job_title = row['job_title']
          job_description = row['cleaned_job_description']
          seniority_level = row['formatted_experience_level']
          all_job_descriptions.append({'id': identifier, 
                                       'job_title': job_title, 
                                       'job_description_clean': job_description, 
                                       'seniority_level': seniority_level})
      
        start += limit 
        if len(data) < limit:
          break
      else:
        print("Error: Empty response from Supabase.")
        break 
      
    return all_job_descriptions
  
  except Exception as e:
    print('An error occurred:', e)

def fetch_raw_resume(user_id: str):
  try:
    supabase = create_sb_client()
    user_resume_response = supabase.table('Resumes').select('resume_raw').eq('id', user_id).limit(1).execute()
    return user_resume_response.data
  except Exception as e:
    print('An error occurred:', e)
    
def fetch_clean_resume(user_id):
  try:
    supabase = create_sb_client()
    user_resume_response = supabase.table('Resumes').select('resume_clean').eq('id', user_id).limit(1).execute()
    return user_resume_response.data
  except Exception as e:
    print('An error occurred:', e)
  
def upload_resume_to_supabase(resume_data: str, user_id: str, column_name: str) -> None:
    """
    Uploads a resume file to Supabase for a specific user. If a row with the given user ID
    already exists in the table, updates the specified column for that row.

    Args:
        resume_data (str): The resume data to upload.
        user_id (str): The ID of the user the resume belongs to.
        column_name (str): The name of the column to update.

    Returns:
        str: The ID of the row in the table.
    """
    try:
        supabase = create_sb_client()
        data, count = supabase.table('Resumes') \
            .upsert({'user_id': user_id, column_name: resume_data}, on_conflict='user_id') \
            .execute()

        print(f"Resume uploaded successfully for user: {user_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


      




