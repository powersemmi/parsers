# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Firefox()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
# https://xn--80ac9aeh6f.xn--p1ai/slava-korolyu/noindex-glava-1-ya-korol/
from selenium import webdriver
from time import sleep


def save_text(text_list: list):
    part = open('end.txt', 'w', encoding="utf-8")
    part.write('\n'*3)
    for i in text_list:
        part.write(i)
    part.write('\n'*3)
    part.close()


browser = webdriver.Firefox()
browser.get('https://xn--80ac9aeh6f.xn--p1ai/slava-korolyu/noindex-glava-1-ya-korol/')
sleep(3)
text_list = browser.page_source

# print(text_list[0].text)
save_text(text_list)

print(text_list)

browser.close()

