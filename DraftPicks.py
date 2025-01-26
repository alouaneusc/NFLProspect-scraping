from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")  # Run in headless mode for efficiency

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.set_page_load_timeout(180)  # Increase page load timeout to 180 seconds

# Open the Full Draft Order page
url = 'https://www.tankathon.com/nfl/full_draft'
driver.get(url)

# Find all rows in the draft table
draft_rows = driver.find_elements(By.XPATH, '//table[@class="full-draft"]//tr')

# Initialize a list to store pick data
draft_data = []

# Loop through the rows and extract pick details
for row in draft_rows:
    try:
        # Extract Pick Number
        pick_number = row.find_element(By.CLASS_NAME, 'pick-number').text

        # Extract Team Name
        team_name = row.find_element(By.CLASS_NAME, 'desktop').text

        # Append to the draft data list
        draft_data.append({
            "Pick Number": pick_number,
            "Team": team_name
        })
    except Exception as e:
        print(f"Error processing row: {e}")

# Close the WebDriver
driver.quit()

# Convert the data to a DataFrame
df = pd.DataFrame(draft_data)

# Group picks by team
grouped_by_team = df.groupby("Team").apply(lambda x: x.to_dict(orient="records"))

# Print grouped data in the desired format
for team, picks in grouped_by_team.items():
    print(f"{team}:")
    for pick in picks:
        print(f"  Pick Number {pick['Pick Number']}")

# Save raw data to a CSV file
# df.to_csv('nfl_full_draft_order.csv', index=False)
