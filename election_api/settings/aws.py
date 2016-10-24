import os
from datetime import date, timedelta


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID') 
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY') 
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME') 
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True
AWS_S3_CUSTOM_DOMAIN = 'election_api.overcastcdn.com'

future = date.today() + timedelta(days=365)
# Expires 1 years in the future at 8PM GMT
AWS_HEADERS = {
    'Expires': future.strftime('%a, %d %b %Y 20:00:00 GMT')
}