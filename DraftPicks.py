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

# Initialize a list to store pick data
draft_data = []

# Get all elements with the round and pick data
sections = driver.find_elements(By.XPATH, '//div[@class="full-draft-round full-draft-round-nfl"]')

# Loop through sections to extract data
for section in sections:
    try:
        # Extract the round title
        round_title_element = section.find_element(By.CLASS_NAME, 'round-title')
        current_round = round_title_element.text

        # Find all rows in the associated table
        rows = section.find_elements(By.XPATH, './/table[@class="full-draft"]//tr')
        
        for row in rows:
            try:
                # Extract Pick Number
                pick_number_element = row.find_elements(By.CLASS_NAME, 'pick-number')
                pick_number = pick_number_element[0].text if pick_number_element else None

                # Extract Team Name
                team_name_element = row.find_elements(By.CLASS_NAME, 'desktop')
                team_name = team_name_element[0].text if team_name_element else None

                # Append to the draft data list if valid
                if pick_number and team_name:
                    draft_data.append({
                        "Round": current_round,
                        "Pick Number": pick_number,
                        "Team": team_name
                    })
            except Exception as e:
                print(f"Error processing row: {e}")
    except Exception as e:
        print(f"Error processing section: {e}")

# Close the WebDriver
driver.quit()

# Convert the data to a DataFrame
df = pd.DataFrame(draft_data)

# Print the DataFrame to check data
# print(df)

# Save to CSV file
df.to_csv('nfl_full_draft_order_with_rounds.csv', index=False)

# Optional: Group picks by round and print
grouped_by_round = df.groupby("Round").apply(lambda x: x.to_dict(orient="records"))

for round_name, picks in grouped_by_round.items():
    print(f"{round_name}:")
    for pick in picks:
        print(f"  Pick {pick['Pick Number']}: {pick['Team']}")
