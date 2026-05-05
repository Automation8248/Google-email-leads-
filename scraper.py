import requests
import re
import json
import csv
import os
import time
from datetime import datetime

# ==========================================
# 1. API KEYS (Google Custom Search)
# ==========================================
API_KEY = "YOUR_GOOGLE_API_KEY"
CX_ID = "YOUR_SEARCH_ENGINE_ID"

# ==========================================
# 2. FULL LISTS (100 Topics & 54 Locations)
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
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
    "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
    "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
    "Wisconsin", "Wyoming", "England", "Northern Ireland", "Scotland", "Wales"
]

DOMAINS = ["@gmail.com", "@yahoo.com", "@outlook.com"]

# ==========================================
# 3. DIRECTORY & PROGRESS SETUP
# ==========================================
OUTPUT_DIR = "leads_output"
PROGRESS_FILE = "progress.json"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(progress_data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress_data, f, indent=4)

# ==========================================
# 4. GOOGLE API SCRAPING LOGIC
# ==========================================
def extract_emails_via_cse(topic, location, pages=2):
    all_extracted_data = []
    
    for domain in DOMAINS:
        query = f'"{topic}" "{location}" "contact us" "{domain}"'
        print(f"🔍 CSE API Request for: {query}")

        for i in range(pages):
            start = (i * 10) + 1
            url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX_ID}&start={start}"
            
            try:
                response = requests.get(url).json()
                if "error" in response:
                    print(f"⚠️ API Error: {response['error']['message']}")
                    return all_extracted_data

                items = response.get("items", [])
                for item in items:
                    snippet = item.get("snippet", "")
                    link = item.get("link", "")
                    title = item.get("title", "")

                    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', snippet)
                    
                    for email in emails:
                        clean_email = email.lower()
                        # Verify domain match
                        if any(d in clean_email for d in DOMAINS):
                            all_extracted_data.append({
                                "Email": clean_email,
                                "Business Name": title,
                                "Source": link,
                                "Topic": topic,
                                "Location": location
                            })
                # Small wait to respect API limits
                time.sleep(1)
            except Exception as e:
                print(f"Error making API call: {e}")
                break
                
    return all_extracted_data

# ==========================================
# 5. DATA SAVING LOGIC (JSON + CSV)
# ==========================================
def save_data(data, topic):
    if not data:
        return
        
    filename_base = os.path.join(OUTPUT_DIR, topic.lower().replace(' ', '_').replace('/', '_'))
    json_file = f"{filename_base}.json"
    csv_file = f"{filename_base}.csv"
    
    # Existing data check to prevent duplicates
    existing_emails = set()
    existing_data = []
    
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            existing_data = json.load(f)
            existing_emails = {row['Email'] for row in existing_data}
            
    # Add only new unique emails
    for row in data:
        if row['Email'] not in existing_emails:
            existing_data.append(row)
            existing_emails.add(row['Email'])
            
    # Save JSON
    with open(json_file, "w") as f:
        json.dump(existing_data, f, indent=4)
        
    # Save CSV
    if existing_data:
        keys = existing_data[0].keys()
        with open(csv_file, "w", newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(existing_data)

# ==========================================
# 6. RUN MANAGER (Picks 3 locations daily)
# ==========================================
def run_automation(target_topic, locations_per_run=3):
    progress = load_progress()
    
    if target_topic not in progress:
        progress[target_topic] = []
        
    completed_locations = progress[target_topic]
    pending_locations = [loc for loc in LOCATIONS if loc not in completed_locations]
    
    if not pending_locations:
        print(f"✅ Sabhi 54 locations '{target_topic}' ke liye scrape ho chuki hain!")
        return

    # Select the next batch of locations
    locations_to_scrape = pending_locations[:locations_per_run]
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Automation Started!")
    print(f"Topic: {target_topic} | Target Locations Today: {locations_to_scrape}\n")

    daily_data = []
    for loc in locations_to_scrape:
        new_leads = extract_emails_via_cse(topic=target_topic, location=loc, pages=2)
        daily_data.extend(new_leads)
        
        # Mark location as completed
        progress[target_topic].append(loc)
        save_progress(progress)
        print(f"✅ {loc} Done! Found {len(new_leads)} emails.")

    save_data(daily_data, target_topic)
    print(f"\n🎉 Daily Run Complete! Saved total {len(daily_data)} new leads in {OUTPUT_DIR}/ folder.")

if __name__ == "__main__":
    # Yahan apna target topic badal sakte hain
    CURRENT_TOPIC = "Dentists" 
    run_automation(target_topic=CURRENT_TOPIC)
