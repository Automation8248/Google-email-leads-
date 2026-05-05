import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import os
import time
import random
from datetime import datetime

# ==========================================
# 1. FULL LISTS (100 Topics & 54 Locations)
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
# 2. FORCEFUL DIRECTORY & PROGRESS SETUP
# ==========================================
OUTPUT_DIR = "leads_output"
PROGRESS_FILE = "progress.json"

# FORCE LOGIC: Run hote hi check karega aur folder banayega
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_progress():
    # FORCE LOGIC: Agar progress file nahi hai, toh forcefully ek khali {} file banayega
    if not os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
        
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # FORCE LOGIC: Agar file corrupt hai, toh use fix karega
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}

def save_progress(progress_data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, indent=4)

# ==========================================
# 3. BING SCRAPING LOGIC (15 PAGES)
# ==========================================
def scrape_bing_emails(topic, location, total_pages=15):
    all_extracted_data = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    for domain in DOMAINS:
        query = f'"{topic}" "{location}" "contact us" "{domain}"'
        print(f"\n🔍 Searching Bing: {query}")

        for page in range(total_pages):
            first_param = (page * 10) + 1 
            url = f"https://www.bing.com/search?q={query}&first={first_param}"
            
            try:
                response = requests.get(url, headers=headers, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = soup.find_all('li', class_='b_algo')
                
                if not results:
                    print(f"  -> Page {page + 1}: No more results found. Stopping for this domain.")
                    break 

                emails_found_on_page = 0
                for result in results:
                    title_tag = result.find('h2')
                    title = title_tag.text if title_tag else "Unknown Business"
                    
                    link_tag = result.find('a')
                    link = link_tag['href'] if link_tag else ""
                    
                    snippet_tag = result.find('p')
                    snippet = snippet_tag.text if snippet_tag else ""

                    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', snippet)
                    
                    for email in emails:
                        clean_email = email.lower()
                        if any(d in clean_email for d in DOMAINS):
                            emails_found_on_page += 1
                            all_extracted_data.append({
                                "Email": clean_email,
                                "Business Name": title,
                                "Source": link,
                                "Topic": topic,
                                "Location": location
                            })
                
                print(f"  -> Page {page + 1} Done! Found {emails_found_on_page} emails.")
                time.sleep(random.uniform(2, 4)) 
                
            except Exception as e:
                print(f"⚠️ Error on Page {page + 1}: {e}")
                break
                
    return all_extracted_data

# ==========================================
# 4. FORCEFUL DATA SAVING LOGIC (JSON & CSV)
# ==========================================
def save_data(data, topic):
    if not data:
        print("No new data to save.")
        return
        
    # Dobara double check karega ki folder delete toh nahi hua script chalne ke beech
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
    filename_base = os.path.join(OUTPUT_DIR, topic.lower().replace(' ', '_').replace('/', '_'))
    json_file = f"{filename_base}.json"
    csv_file = f"{filename_base}.csv"
    
    existing_emails = set()
    existing_data = []
    
    # FORCE LOGIC: Agar JSON file pehle se nahi hai toh automatically banayega
    if not os.path.exists(json_file):
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump([], f)
            
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            existing_emails = {row['Email'] for row in existing_data}
    except json.JSONDecodeError:
        print(f"⚠️ Warning: {json_file} is corrupted. Fixing forcefully.")
        existing_data = []
            
    # Sirf naye aur unique emails add honge
    for row in data:
        if row['Email'] not in existing_emails:
            existing_data.append(row)
            existing_emails.add(row['Email'])
            
    # Naye data ko file mein FORCEFULLY likhna (Purani file overwrite hoke update hogi)
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4)
        
    # CSV Backup bhi forcefully banayega
    if existing_data:
        keys = existing_data[0].keys()
        with open(csv_file, "w", newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(existing_data)
            
    print(f"✅ Data forcefully updated! Total leads in {json_file}: {len(existing_data)}")

# ==========================================
# 5. AUTOMATION RUN MANAGER
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

    locations_to_scrape = pending_locations[:locations_per_run]
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Bing Automation Started!")
    print(f"Topic: {target_topic} | Target Locations Today: {locations_to_scrape}\n")

    daily_data = []
    for loc in locations_to_scrape:
        new_leads = scrape_bing_emails(topic=target_topic, location=loc, total_pages=15)
        daily_data.extend(new_leads)
        
        progress[target_topic].append(loc)
        save_progress(progress)
        print(f"✅ Location '{loc}' Done!\n")

    save_data(daily_data, target_topic)
    print(f"\n🎉 Run Complete! All data saved securely in {OUTPUT_DIR}/ folder.")

if __name__ == "__main__":
    # Abhi "Dentists" target ho raha hai. Aap chahein toh loop laga sakte hain ya yahan naam change kar sakte hain.
    CURRENT_TOPIC = "Dentists" 
    run_automation(target_topic=CURRENT_TOPIC, locations_per_run=3)
