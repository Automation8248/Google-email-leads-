import requests
import re
import json
import time
import random
import os
from datetime import datetime

# ==========================================
# 1. 50+ USER AGENTS LIST
# ==========================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_8) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_9 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 OPR/104.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
]

# ==========================================
# 2. LISTS (Topics & Locations)
# ==========================================
TOPICS = [
    "Dentists", "Orthodontists", "Chiropractors", "Veterinary Clinics", "Pet Groomers", 
    "Pet Boarding/Hotels", "Dog Trainers", "Plumbers", "Electricians", "HVAC", 
    "Roofers", "Landscapers", "Painters", "Locksmiths", "Pest Control Services", 
    "Divorce Lawyers", "Personal Injury Lawyers", "Criminal Defense Lawyers", "Accountants/CPAs", 
    "Real Estate Agents", "Property Managers", "Financial Advisors", "Insurance Agents", 
    "Gyms & Fitness Centers", "Yoga Studios", "Pilates Studios", "Personal Trainers", 
    "Martial Arts Schools", "Dance Schools", "Swimming Instructors", "Spas & Massage Centers", 
    "Hair Salons", "Nail Salons", "Barber Shops", "Tattoo Parlors", "Skin Care Clinics", 
    "Dietitians & Nutritionists", "Mental Health Counselors", "Pharmacies", "Medical Laboratories", 
    "Optometrists", "Audiologists", "Coffee Shops", "Bakeries", "Italian Restaurants", 
    "Seafood Restaurants", "Catering Services", "Food Trucks", "Bars & Pubs", "Event Planners", 
    "Wedding Photographers", "Videographers", "DJs & Music Services", "Car Rentals", 
    "Car Mechanics", "Towing Services", "Car Wash", "Driving Schools", "Solar Panel Installers", 
    "Pool Cleaning Services", "House Cleaning Services", "Interior Designers", "Florists", 
    "Gift Shops", "Jewelry Stores", "Toy Stores", "Bookstore Owners", "Hardware Stores", 
    "Dry Cleaners", "Tailors", "Carpet Cleaners", "Window Cleaning Services", "Junk Removal", 
    "Home Staging", "Architects", "Land Surveyors", "General Contractors", "Home Inspection", 
    "Tutoring Centers", "Music Teachers", "Language Schools", "Preschools", "After-school Programs", 
    "Travel Agencies", "Boutique Hotels", "Bed and Breakfasts", "Tour Guides", "Boat Chartering", 
    "Adventure Sports", "Art Galleries", "Pottery Studios", "Graphic Designers", "Web Development Agencies", 
    "Recruiting Agencies", "Waste Management", "Security Guard Services", "Storage Facilities", 
    "Moving Companies", "Notary Public Services", "Bike Repair Shops"
]

LOCATIONS = [
    # USA States
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
    "Wisconsin", "Wyoming",
    # UK Countries
    "England", "Northern Ireland", "Scotland", "Wales"
]

# ==========================================
# 3. FILE MANAGEMENT SETUP
# ==========================================
EMAIL_DIR = "emails"
PROGRESS_FILE = "progress.json"

if not os.path.exists(EMAIL_DIR):
    os.makedirs(EMAIL_DIR)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(progress_data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress_data, f, indent=4)

# ==========================================
# 4. CORE SCRAPING LOGIC
# ==========================================
def scrape_google_emails(topic, location, start_page, end_page):
    query = f'"{topic}" "{location}" "contact us" "@gmail.com"'
    extracted_emails = set()
    
    start_index = (start_page - 1) * 10
    end_index = end_page * 10  # Upto page 30

    print(f"--> Scraping '{topic}' in '{location}' (Pages {start_page} to {end_page})...")

    for start in range(start_index, end_index, 10):
        current_page = (start // 10) + 1
        url = f"https://www.google.com/search?q={query}&start={start}"
        
        # Random User-Agent selection
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        try:
            response = requests.get(url, headers=headers)
            # Find all emails
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@gmail\.com', response.text)
            
            for email in emails:
                extracted_emails.add(email.lower())
                
            print(f"Page {current_page} scanned. Found {len(emails)} emails.")
            
            # Anti-block random delay (4 to 8 seconds)
            time.sleep(random.uniform(4, 8)) 
        except Exception as e:
            print(f"Error on Page {current_page}: {e}")
            
    return list(extracted_emails)

# ==========================================
# 5. SINGLE RUN MANAGER
# ==========================================
def run_scraper(target_topic):
    progress = load_progress()
    
    if target_topic not in progress:
        progress[target_topic] = []
        
    completed_locations = progress[target_topic]
    pending_locations = [loc for loc in LOCATIONS if loc not in completed_locations]
    
    if not pending_locations:
        print(f"✅ Sabhi 54 locations '{target_topic}' ke liye poori ho chuki hain!")
        return False # False means job is done

    # Sirf 1 location uthana hai jaisa aapne kaha
    loc_to_scrape = pending_locations[0]
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Run Started!")
    print(f"Topic: {target_topic} | Target Location: {loc_to_scrape}\n")

    topic_file_path = os.path.join(EMAIL_DIR, f"{target_topic.lower().replace(' ', '_').replace('/', '_')}.json")
    
    # Purana data load karna
    existing_emails = set()
    if os.path.exists(topic_file_path):
        with open(topic_file_path, "r") as f:
            existing_emails = set(json.load(f))

    # Page 7 se 30 tak scrape karna
    new_emails = scrape_google_emails(topic=target_topic, location=loc_to_scrape, start_page=7, end_page=30)
    existing_emails.update(new_emails)
    
    # Progress save karna
    progress[target_topic].append(loc_to_scrape)
    save_progress(progress)

    # Emails save karna
    with open(topic_file_path, "w") as f:
        json.dump(list(existing_emails), f, indent=4)

    print(f"\n✅ {loc_to_scrape} Done! New emails found: {len(new_emails)}")
    print(f"📂 Total unique emails for {target_topic}: {len(existing_emails)}")
    print(f"Saved in -> {topic_file_path}\n")
    return True # True means it ran successfully

# ==========================================
# 6. 24-HOUR AUTOMATION LOOP
# ==========================================
if __name__ == "__main__":
    # Aap is variable ko change karke apna topic select kar sakte hain
    CURRENT_TOPIC = "Dentists" 
    
    print(f"🟢 Automation Started for '{CURRENT_TOPIC}'...")
    print("Script will run 2 times in 24 hours (Every 12 Hours).")
    
    while True:
        # Run the scraper
        has_more_locations = run_scraper(target_topic=CURRENT_TOPIC)
        
        if not has_more_locations:
            print(f"No more locations left for {CURRENT_TOPIC}. Exiting automation.")
            break
            
        print("\n⏳ Next run will be exactly after 12 hours. Do not close this window...")
        
        # 12 ghante (43200 seconds) tak wait karega agle run ke liye
        # (12 hours * 60 minutes * 60 seconds = 43200)
        time.sleep(43200)
