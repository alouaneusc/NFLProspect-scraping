from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the URL
url = 'https://www.nflmockdraftdatabase.com/big-boards/2025/consensus-big-board-2025'
driver.get(url)

# Locate elements using XPATH
players = driver.find_elements(By.XPATH, '//div[@class="player-name player-name-smaller"]')
under_99_rankings = driver.find_elements(By.XPATH, '//div[@class="pick-number with-subtitle"]')
over_99_rankings = driver.find_elements(By.XPATH, '//div[@class="pick-number with-subtitle large-pick-number"]')
details = driver.find_elements(By.XPATH, '//div[@class="player-details college-details"]')

# Combine rankings under and over 99
rankings = under_99_rankings + over_99_rankings

# Extract data
scraped_data = []
num_players = min(len(players), len(rankings), len(details))  # Handle potential mismatches in lengths

for i in range(num_players):
    player_name = players[i].text
    player_ranking = int(rankings[i].text)
    position = details[i].text.split(' | ')[0]  # Extract position
    school = details[i].find_element(By.TAG_NAME, 'a').text  # Extract school name

    scraped_data.append({
        "Rank": player_ranking,
        "Player": player_name,
        "Position": position,
        "School": school
    })

# Create a DataFrame for better handling of data
df = pd.DataFrame(scraped_data)

# Print and save the DataFrame
print(df.head(10))

# Close the WebDriver
driver.quit()


# df.to_csv("nfl_mock_draft_2025.csv", index=False)
