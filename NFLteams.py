from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = 'https://www.tankathon.com/nfl/full_draft'
driver.get(url)

# Find all rows containing draft picks
draft_rows = driver.find_elements(By.XPATH, '//tbody/tr')

# Extract data
draft_order = []

for row in draft_rows:
    try:
        # Extract Pick Number
        pick_number = row.find_element(By.CLASS_NAME, 'pick-number').text

        # Extract Team Name
        team_name = row.find_element(By.CLASS_NAME, 'desktop').text

        # Extract Team URL
        team_url = row.find_element(By.CLASS_NAME, 'team-link').find_element(By.TAG_NAME, 'a').get_attribute('href')

        # Append the data to the draft_order list
        draft_order.append({
            "Pick Number": pick_number,
            "Team": team_name,
            "Team URL": team_url
        })
    except Exception as e:
        print(f"Error extracting data for row: {e}")

# Create a DataFrame
df = pd.DataFrame(draft_order)

# Print and save the DataFrame
print(df.head(2))  # Print first 10 rows
# df.to_csv('nfl_full_draft_order_tankathon.csv', index=False)  # Save to CSV

# Close the browser
driver.quit()
