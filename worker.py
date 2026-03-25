import sqlite3
import time
import random
from datetime import datetime

# --- CONFIGURATION ---
SEARCH_TERM = "Jordan 4 Military Blue"
MAX_PRICE = 180.00
SHOE_SIZE = "UK 9"
CHECK_INTERVAL = 60  # Seconds

# --- DATABASE SETUP ---
def setup_db():
    conn = sqlite3.connect('shoe_listings.db')
    cursor = conn.cursor()
    # Create a table to store IDs we've already seen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id TEXT PRIMARY KEY,
            title TEXT,
            price REAL,
            link TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    return conn

def is_new_listing(conn, listing_id):
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM listings WHERE id = ?', (listing_id,))
    return cursor.fetchone() is None

def save_listing(conn, item):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO listings VALUES (?, ?, ?, ?, ?)', 
                  (item['id'], item['title'], item['price'], item['link'], datetime.now()))
    conn.commit()

# --- MOCK SCRAPER (Replace this with real API/Scraping Logic) ---
def fetch_listings(query, size):
    """
    In a real scenario, you would use requests.get() to eBay API or Vinted.
    This returns a list of dictionaries simulating what those sites provide.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Scanning for {query} in {size}...")
    
    # Simulating data returned from a website
    mock_results = [
        {"id": "ebay_123", "title": "Jordan 4 Military Blue - New", "price": 165.00, "link": "https://ebay.com/itm/123"},
        {"id": "vinted_456", "title": "Jordan 4 Military Blue Size 9", "price": 210.00, "link": "https://vinted.com/items/456"}
    ]
    return mock_results

# --- MAIN ENGINE ---
def run_bot():
    db_conn = setup_db()
    
    try:
        while True:
            # 1. Fetch data
            items = fetch_listings(SEARCH_TERM, SHOE_SIZE)
            
            for item in items:
                # 2. Logic: Is it cheap enough?
                if item['price'] <= MAX_PRICE:
                    
                    # 3. Logic: Have we seen it before?
                    if is_new_listing(db_conn, item['id']):
                        
                        # 4. ALERT! (This is where you'd send a Telegram/Discord message)
                        print(f"!!! DEAL FOUND !!!")
                        print(f"Item: {item['title']}")
                        print(f"Price: £{item['price']}")
                        print(f"Link: {item['link']}")
                        print("-" * 20)
                        
                        # 5. Save to DB so we don't alert again
                        save_listing(db_conn, item)
            
            # Wait for next cycle with a bit of randomness to look "human"
            sleep_time = CHECK_INTERVAL + random.randint(-5, 5)
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\nStopping the bot...")
        db_conn.close()

if __name__ == "__main__":
    run_bot()
