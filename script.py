from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import time
import pickle
import os
import config

fileout = open('debug.log', 'w')

# load words dictionary
with open('words.pickle', 'rb') as f:
    words_dict = pickle.load(f)
with open('words_set.pickle', 'rb') as f:
    words_set = pickle.load(f)

reset_duolingo = config.reset_duolingo
n = config.n


capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Redmi Note 10 Pro',
    appPackage='com.duolingo',
    appActivity='.app.StreakSocietyLauncher',
    language='en',
    locale='US',
    noReset=True,
    fullReset=False,
    forceAppLaunch=reset_duolingo,
    waitForIdleTimeout=0,
    actionAcknowledgmentTimeout=0,
)


appium_server_url = 'http://localhost:4723'


driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

driver.implicitly_wait(10)


def boot_up_match_madness():
    time.sleep(3)
    print("Clicking on League tab")
    driver.find_element("id", "com.duolingo:id/tabLeagues").click()
    print("Clicked on League tab")

    driver.find_element("id", "com.duolingo:id/rampUpFab").click()

#starts the match madness
def start_game():
    time.sleep(2)
    print("Clicking Start button")
    driver.find_element("id", "com.duolingo:id/matchMadnessStartChallenge").click()
    print("Clicked Start button")


    driver.find_element("id", 'com.duolingo:id/coachContinueButton').click()

    # The promo power up is not always there, need a try except
    try:
        driver.find_element("id", 'com.duolingo:id/rowBlasterNoThanksButton').click()
    except:
        pass

def get_elements():
    elements = driver.find_elements("id", "com.duolingo:id/optionText")
    return elements[::2] + elements[1::2]

def get_element_wrappers():
    element_wrappers = driver.find_elements("xpath", '//*[@resource-id="com.duolingo:id/optionText"]/..')
    return element_wrappers[::2] + element_wrappers[1::2]

def match_words():
    elements = get_elements()
    element_wrappers = get_element_wrappers()
    coordinates = list(map(lambda e: tuple(e.location_in_view.values()), elements))


    while True:
        for i in range(5):
            eng_word = elements[i].text

            not_clickable = not (element_wrappers[i].get_attribute('clickable') == 'true')
            if not_clickable:
                continue

            was_selected = False

            if eng_word in words_dict:
                german_word = words_dict[eng_word]
                print("I know this word: " + eng_word + " " + german_word)
                for j in range(5, 10):
                    if elements[j].text == german_word:
                        was_selected = True
                        os.system(f"adb shell \"input tap {coordinates[i][0]} {coordinates[i][1]} && input tap {coordinates[j][0]} {coordinates[j][1]}\"")
                        break
            else:
                # brute force, what is the other language version
                for j in range(5, 10):
                    not_clickable = not (element_wrappers[j].get_attribute('clickable') == 'true')

                    if not_clickable:
                        continue

                    word1 = elements[i].text
                    word2 = elements[j].text

                    if word2 in words_set:
                        continue

                    # click on word, faster version
                    os.system(f"adb shell \"input tap {coordinates[i][0]} {coordinates[i][1]} && input tap {coordinates[j][0]} {coordinates[j][1]}\"")

                    time.sleep(1.5)
                    not_clickable1 = not (element_wrappers[i].get_attribute('clickable') == 'true')
                    not_clickable2 = not (element_wrappers[j].get_attribute('clickable') == 'true')


                    if not_clickable1 or not_clickable2:
                        print("Added: " + word1 + " " + word2)
                        words_dict[word1] = word2
                        words_set.add(word2)
                        was_selected = True
                        break
            
            if not was_selected:
                for j in range(5, 10):
                    not_clickable = not (element_wrappers[j].get_attribute('clickable') == 'true')

                    if not_clickable:
                        continue

                    word1 = elements[i].text
                    word2 = elements[j].text

                    # click on word
                    os.system(f"adb shell \"input tap {coordinates[i][0]} {coordinates[i][1]} && input tap {coordinates[j][0]} {coordinates[j][1]}\"")

                    time.sleep(1.5)
                    not_clickable1 = not (element_wrappers[i].get_attribute('clickable') == 'true')
                    not_clickable2 = not (element_wrappers[j].get_attribute('clickable') == 'true')


                    if not_clickable1 or not_clickable2:
                        print("Added: " + word1 + " " + word2)
                        words_dict[word1] = word2
                        words_set.add(word2)
                        was_selected = True
                        break
def exit_game():
    try:
        driver.find_element("id", "com.duolingo:id/boostsDrawerNoThanksButton").click()
        driver.find_element("id", "com.duolingo:id/rampUpQuitEndSession").click()

    except:
        pass
    time.sleep(4)
    while True:
        try:
            driver.find_element("id", "com.duolingo:id/sessionEndContinueButton").click()
            time.sleep(1)
        except:
            break
    try:
        driver.find_element("id", "com.duolingo:id/secondaryButton").click()
    except:
        pass

def save_data():
    with open('words.pickle', 'wb') as f:
        pickle.dump(words_dict, f)
    with open('words_set.pickle', 'wb') as f:
        pickle.dump(words_set, f)

    print('Data saved!')
    
def play_a_round():
    start_game()
    while True:
        try:
            match_words()
        except:
            try:
                driver.find_element("id", "com.duolingo:id/coachContinueButton").click()
                continue
            except:
                exit_game()
                return
            
def play_n_times(n: int):
    for i in range(n):
        play_a_round()
        if i % config.data_save_frequency == 0:
            save_data()


if reset_duolingo:
    boot_up_match_madness()
play_n_times(n)



fileout.write(driver.page_source)

