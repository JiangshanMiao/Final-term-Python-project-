from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the browser driver
driver = webdriver.Chrome()

# List of URLs
urls = [
    "https://www.indeed.com/jobs?q=walmart&l=Hoboken%2C+NJ",
    "https://www.indeed.com/jobs?q=walmart&l=Hoboken%2C+NJ&from=searchOnHP&vjk=ec1c62764cd7723f",
    "https://www.indeed.com/jobs?q=walmart&l=Hoboken%2C+NJ&from=searchOnHP&vjk=4da71f382da87dbf",
    "https://www.indeed.com/jobs?q=walmart&l=Hoboken%2C+NJ&from=searchOnHP&vjk=d8008ab2c5c0d48f",
    "https://www.indeed.com/jobs?q=walmart&l=Hoboken%2C+NJ&from=searchOnHP&vjk=f8942aaead8f0fad",
]

# Extract salary information
for url in urls:
    print(f"Fetching salary information from: {url}")


    driver.get(url)


    try:

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))


        hourly_salary_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'an hour')]")

        if hourly_salary_elements:
            print("Hourly salary info:")
            for element in hourly_salary_elements:
                print(f" - {element.text}")
        else:
            print("No hourly salary info found.")


        per_mile_salary_elements = driver.find_elements(By.XPATH, "//span[contains(text(), 'per mile')]")

        if per_mile_salary_elements:
            print("\nPer mile salary info:")
            for element in per_mile_salary_elements:
                print(f" - {element.text}")
        else:
            print("No per mile salary info found.")

    except Exception as e:
        print(f"Error occurred while fetching salary from {url}: {e}")
    print("\n" + "=" * 50 + "\n")

# Close the browser
driver.quit()