#-*- coding:utf-8 -*-
from selenium import webdriver
from time import sleep
try:
	driver = webdriver.Chrome()
	driver.maximize_window()
	driver.get("http://www.baidu.com")
	driver.find_element_by_name("wd").send_keys("selenium")
	driver.find_element_by_id("su").click()
	sleep(2)
except Exception as e:
	raise e
finally:
	driver.quit()


2adee2462584275e25a6d31a41310d953d260c58