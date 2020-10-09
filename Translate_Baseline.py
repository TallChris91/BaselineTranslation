# Make imports
import time
import clipboard
from selenium import webdriver
import regex as re
import pickle
import os

currentpath = os.getcwd()

#Open the English baseline output
with open(currentpath + '/baseline_WebNLG-2020-FORGe2020-12-2_submission.txt', 'rb') as f:
    baselines = f.readlines()

#Decode it and remove the \n's.
baselines = [x.decode('utf-8') for x in baselines]
baselines = [re.sub(r'\n', '', x) for x in baselines]

translatedlines = []

#Go over each line separately
for sentence in baselines:
    with open(currentpath + '/Originallines.pkl', 'rb') as f:
        originallines = pickle.load(f)
    # Define text to translate
    text_to_translate = sentence

    # Start a Selenium driver
    chromedriver = currentpath + '/chromedriver.exe'

    driver = webdriver.Chrome(chromedriver)

    # Reach the deepL website
    deepl_url = 'https://www.deepl.com/ru/translator'
    driver.get(deepl_url)

    #Go to the input area
    input_css = 'div.lmt__inner_textarea_container textarea'
    input_area = driver.find_element_by_css_selector(input_css)

    # Send the sentence to the translator
    input_area.clear()
    input_area.send_keys(text_to_translate)

    # Wait for translation to appear on the web page
    time.sleep(3)

    #Go to the cookie button and click on it
    button_css = 'button.dl_cookieBanner--buttonAll'
    button = driver.find_element_by_css_selector(button_css)
    button.click()

    time.sleep(1)

    #Go to the copy button and click on it
    button_css = ' div.lmt__target_toolbar__copy button'
    button = driver.find_element_by_css_selector(button_css)
    button.click()

    # Get content from clipboard
    content = clipboard.paste()

    # Quit selenium driver
    driver.quit()

    # Display results
    print('_'*50)
    print('Original    :', text_to_translate)
    print('Translation :', content)
    print('_'*50)
    translatedlines.append(content)

    #Save the translated lines in one document
    if os.path.isfile(currentpath + '/Originallines.pkl'):
        with open(currentpath + '/Originallines.pkl', 'rb') as f:
            originallines = pickle.load(f)

        originallines.append(text_to_translate)

        with open(currentpath + '/Originallines.pkl', 'wb') as f:
            pickle.dump(originallines, f)
    else:
        with open(currentpath + '/Originallines.pkl', 'wb') as f:
            pickle.dump([text_to_translate], f)

    if os.path.isfile(currentpath + '/Translatedlines.pkl'):
        with open(currentpath + '/Translatedlines.pkl', 'rb') as f:
            testlines = pickle.load(f)

        testlines.append(content)

        with open(currentpath + '/Translatedlines.pkl', 'wb') as f:
            pickle.dump(testlines, f)
    else:
        with open(currentpath + '/Translatedlines.pkl', 'wb') as f:
            pickle.dump([content], f)

print(translatedlines)

