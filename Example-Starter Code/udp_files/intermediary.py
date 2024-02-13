from supabase import create_client, Client

url: str = "https://blzwcpdxyfmqngexhskf.supabase.co" 
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJsendjcGR4eWZtcW5nZXhoc2tmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDcyNTEyMTMsImV4cCI6MjAyMjgyNzIxM30.Y78DCDzwlRNW8MVQiVJ4itxl9NdjV99PPa7Q9hh_daI"  
supabase: Client = create_client(url, key)


new_record = {"id": "123", "codename": "test"}
inserted_data = supabase.table("player").insert(new_record).execute()
print(inserted_data.data)  # Prints the inserted data