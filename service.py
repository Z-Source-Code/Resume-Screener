import bentoml
from pathlib import Path
from src.database import upload_resume_to_supabase
from src.resume_processing import clean_and_lemmatize_resume
import pymupdf
import threading

@bentoml.service
class JobRecommender:
  @bentoml.api
  def recommendations(self, input: Path) -> str:
    user_id = '4fca706a-da00-4ed8-81d0-41af305d8ed7'
    
    with pymupdf.open(input) as doc:
        raw_resume_text = chr(12).join([page.get_text() for page in doc])
        
    def upload_raw_resume():
      upload_resume_to_supabase(raw_resume_text, user_id, "resume_raw")
      
    def clean_and_store_resume():
      cleaned_resume_text = clean_and_lemmatize_resume(raw_resume_text)
      upload_resume_to_supabase(cleaned_resume_text, user_id, "resume_clean")
      
    upload_thread = threading.Thread(target=upload_raw_resume)
    clean_thread = threading.Thread(target=clean_and_store_resume)
        
    upload_thread.start()
    clean_thread.start()
    
    upload_thread.join()
    clean_thread.join()

    return 'Recommendation generation and resume processing in progress...'
