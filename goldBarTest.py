from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Constants
URL = "http://sdetchallenge.fetch.com/"
WAIT_TIME = 15

# Initialize WebDriver
driver = webdriver.Chrome()
driver.get(URL)

def clear_and_set_bowl(bowl, value):
    """Clear the bowl and set the given value."""
    bowl.clear()
    bowl.send_keys(value)

def perform_weighing(left, right):
    """Weigh the bars and return the result."""
    bowls = [driver.find_element(By.XPATH, f"//*[@id='left_{i}']") for i in range(3)]
    bowls += [driver.find_element(By.XPATH, f"//*[@id='right_{i}']") for i in range(3)]
    weigh_button = driver.find_element(By.ID, "weigh")
    reset_button = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[4]/button[1]")

    for i in range(3):
        clear_and_set_bowl(bowls[i], left[i])
        clear_and_set_bowl(bowls[i + 3], right[i])

    weigh_button.click()
    time.sleep(WAIT_TIME)

    last_weighing = driver.find_element(By.CSS_SELECTOR, '.game-info ol').find_elements(By.TAG_NAME, 'li')[-1].text
    reset_button.click()
    return last_weighing

def find_fake_gold_bar():
    """Determine which bar is fake based on the weight."""
    while True:
        result_1 = perform_weighing([0, 1, 2], [3, 4, 5])

        if "=" in result_1:
            result_2 = perform_weighing([6, 7, 8], ["", "", ""])
            if "=" in result_2:
                return 8
            return 7 if ">" in result_2 else 6

        if ">" in result_1:
            result_2 = perform_weighing([3, 4, 5], ["", "", ""])
            if "=" in result_2:
                return 5
            return 4 if ">" in result_2 else 3

        result_2 = perform_weighing([0, 1, 2], ["", "", ""])
        if "=" in result_2:
            return 2
        return 1 if ">" in result_2 else 0

def main():
    """Main function to find and click the fake gold bar."""
    fake_bar_number = find_fake_gold_bar()
    driver.find_element(By.XPATH, f"//*[@id='coin_{fake_bar_number}']").click()

    alert = driver.switch_to.alert
    alert_message = alert.text
    if "Yay" in alert_message:
        print(f"We have found the correct fake bar")
        print(f"Fake Gold Bar: {fake_bar_number}")
    alert.accept()
    driver.quit()

if __name__ == "__main__":
    main()
