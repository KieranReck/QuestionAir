from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv
import os
from datetime import datetime

# Set up Selenium WebDriver with Firefox
firefox_options = Options()
# firefox_options.add_argument("--headless")  # Optional
# service = Service("/snap/bin/firefox.geckodriver")  # NOTE needed if firefox installed thru snap
# driver = webdriver.Firefox(service=service, options=firefox_options)
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

try:
    # Open the webpage
    driver.get("https://www.kleenex.co.uk/pollen-count/cambridge")

    time.sleep(1)
    # Wait for the cookies popup banner to be present
    WebDriverWait(driver, 3000).until(
        EC.presence_of_element_located((By.ID, 'onetrust-consent-sdk'))
    )

    # Click the 'Reject All' button on the cookies banner
    reject_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Reject All")]'))  # Adjust XPath as needed
    )
    reject_all_button.click()
    
    # Allow time for the cookies banner overlay to animate 
    time.sleep(1)

    # # Wait for the 'View Pollen Analysis' button to be clickable
    view_pollen_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.pollen-analysis-btn'))
    )
    view_pollen_button.click()

    print(f"Sucessfully reached data, performing extraction..")
    
    # Wait for the additional data to be visible
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'grass-tab'))  # Adjust class name as needed
    )

    # # Extract and print the data
    # # print("---Grass Pollen---")
    # grass_tab = driver.find_elements(By.CLASS_NAME, 'grass-tab')
    # for element in grass_tab:
    #     print(element.text)

    # # print("---Tree Pollen---")
    # trees_tab = driver.find_elements(By.CLASS_NAME, 'trees-tab')
    # for element in trees_tab:
    #     print(element.text)


    # # print("---Weed Pollen---")
    # weeds_pollen_data_elements = driver.find_elements(By.CLASS_NAME, 'weeds-tab')
    # for element in weeds_pollen_data_elements:
    #     print(element.text)

    # Extract the data
    data = []

    grass_tab = driver.find_element(By.CLASS_NAME, 'grass-tab')
    grass_elements = grass_tab.find_elements(By.TAG_NAME, 'li')
    for element in grass_elements:
        data.append(element.text.split("\n"))

    trees_tab = driver.find_element(By.CLASS_NAME, 'trees-tab')
    trees_elements = trees_tab.find_elements(By.TAG_NAME, 'li')
    for element in trees_elements:
        data.append(element.text.split("\n"))

    weeds_tab = driver.find_element(By.CLASS_NAME, 'weeds-tab')
    weeds_elements = weeds_tab.find_elements(By.TAG_NAME, 'li')
    for element in weeds_elements:
        data.append(element.text.split("\n"))

    # print(weeds)
    # [print(element.text) for element in weeds_elements]
    # data = grass + trees + weeds
    # print(data)
   
    # Generate the filename with current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'pollen_data_{timestamp}.csv'

    # Check if the file already exists
    if os.path.exists(filename):
        print(f"Filename already exists, waiting 1 seconds")
        time.sleep(1)
        filename = f'pollen_data_{timestamp}.csv'


    # Write data to CSV file
    with open(filename, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['Pollen Type', 'Count', 'Unit', 'Indicator'])
        # for row in data:
        #     csvwriter.writerow([row])  # Write each string as a single-element list
        csvwriter.writerows(data)
    print(f"Data has been written to {filename}")

    # print(data)


except Exception as e:
    # Print any exceptions that occur
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()
