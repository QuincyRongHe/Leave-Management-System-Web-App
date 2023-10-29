from selenium import webdriver
from time import sleep

from selenium.common import NoSuchElementException

users = [
    {"email": "lily.brown@lincoln.ac.nz", "password": "ejohohoew9"},
    {"email": "david.green@lincoln.ac.nz", "password": "dkhh80&5"},
    {"email": "chris.epke@lincoln.ac.nz", "password": "greo087%"},
    {"email": "john.smith@lincoln.ac.nz", "password": "bieiowo0@"},
    {"email": "emily.johnson@lincoln.ac.nz", "password": "siweolz@1"},
    {"email": "michael.davis@lincoln.ac.nz", "password": "iwieooi$2"},
    {"email": "sophia.wilson@lincoln.ac.nz", "password": "hwoaap#8"},
    {"email": "daniel.taylor@lincoln.ac.nz", "password": "kowgagzu%3"},
    {"email": "olivia.anderson@lincoln.ac.nz", "password": "aewioh45#"},
    {"email": "matthew.thomas@lincoln.ac.nz", "password": "koea95@^"},
    {"email": "chloe.roberts@lincoln.ac.nz", "password": "jlko68!$"},
    {"email": "ethan.clark@lincoln.ac.nz", "password": "geaopq&4"},
    {"email": "emma.walker@lincoln.ac.nz", "password": "kaweu78^%"},
    {"email": "james.hill@lincoln.ac.nz", "password": "dhaepo@5"},
    {"email": "mia.baker@lincoln.ac.nz", "password": "wieho02#$"},
    {"email": "abigail.parker@lincoln.ac.nz", "password": "kie34&^*"},
    {"email": "benjamin.carter@lincoln.ac.nz", "password": "hjaep86@$"},
    {"email": "grace.turner@lincoln.ac.nz", "password": "aleiop$7!"},
    {"email": "henry.cooper@lincoln.ac.nz", "password": "weio43&^"},
    {"email": "sofia.lewis@lincoln.ac.nz", "password": "qweap92@$"},
    {"email": "jacob.gonzalez@lincoln.ac.nz", "password": "eipok43#*"},
    {"email": "ava.hernandez@lincoln.ac.nz", "password": "alop92@&$"},
    {"email": "william.parker@lincoln.ac.nz", "password": "aeiop29@&"},
    {"email": "samantha.carter@lincoln.ac.nz", "password": "kiop34^*"},
    {"email": "joseph.cooper@lincoln.ac.nz", "password": "oapq92&^"},
    {"email": "natalie.ross@lincoln.ac.nz", "password": "kwoi85@#$"},
    {"email": "jonathan.roberts@lincoln.ac.nz", "password": "lkhg76#$"},
    {"email": "isabella.wright@lincoln.ac.nz", "password": "poiuy63*$"},
    {"email": "joshua.jackson@lincoln.ac.nz", "password": "qazws19@#"},
    {"email": "sophie.turner@lincoln.ac.nz", "password": "mnbvc27^*"},
    {"email": "daniel.lee@lincoln.ac.nz", "password": "zxcvb51&^"},
    {"email": "mila.gonzalez@lincoln.ac.nz", "password": "asdfg93@#$"},
    {"email": "david.hernandez@lincoln.ac.nz", "password": "hjklp25^*"},
    {"email": "avery.cooper@lincoln.ac.nz", "password": "ertyu38@#$"},

    {"email": "", "password": "ertyu38@#$"},
    {"email": "avery.cooper@lincoln.ac.nz", "password": ""},
    {"email": "avery.cooper@lincoln.ac.nz", "password": "11111"},
    {"email": "david.hernandez@lincoln.ac.nz", "password": "ertyu38@#$"},

]

# Counter for successful logins
successful_logins = 0

# Loop through the users
for user in users:
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000/")
    email = driver.find_element("css selector", "#email")
    password = driver.find_element("css selector", "#password")
    email.send_keys(user["email"])
    password.send_keys(user["password"])
    driver.find_element("css selector", "#submit").click()
    sleep(2)

    # Check if login was successful
    if "login" not in driver.current_url.lower():
        successful_logins += 1
    else:
        try:
            # Check if there is an error message displayed
            error_msg = driver.find_element("css selector", ".flash").text
            print(f"Login failed for user: {user['email']}. Error: {error_msg}")
        except NoSuchElementException:
            print(f"Login failed for user: {user['email']}. Required field missing.")

    # Perform actions after login (e.g., navigate to other pages, perform tasks, etc.)
    # ...

    driver.quit()

# Print the report
print(f"Total users: {len(users)}")
print(f"Successful logins: {successful_logins}")
print(f"Failed logins: {len(users) - successful_logins}")
