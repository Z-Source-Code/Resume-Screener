import os 
from supabase import create_client, Client
from dotenv import load_dotenv 

load_dotenv()

url: str = os.environ.get("SUPABASE_PROJECT_URL")
key: str = os.environ.get("SUPABASE_API_KEY")



supabase: Client = create_client(url, key)
data = supabase.table('Job Postings').select("job_title").execute()

print(data)

# if error:
#     print("Error fetching data:", error)
# else:
#     # Access the retrieved data
#     job_titles = data

#     # Print the retrieved job titles
#     for job_title in job_titles:
#         print(job_title["job title"])