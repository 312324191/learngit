#! /usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'XT'

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver = webdriver.Chrome()
driver.maximize_window()
try:
    driver.implicitly_wait(60)
    driver.get("http://www.lepiaoyun.com")
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/button[1]").click()
    # driver.switch_to_frame("login-form")
    sleep(1)
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("123456")
    sleep(1)
    driver.find_element_by_id("login-btn").click()
    admin = driver.find_element_by_xpath("/html/body/div/div[1]/header/nav/div[1]/ul/li/a").text
    assert(admin, "admin")
    driver.find_element_by_xpath("//*[@id=\"contentWrapper\"]/div/section/div/a[2]/img").click()
    piaofang = driver.find_element_by_xpath("//*[@id=\"mainSidebar\"]/div/ul/li[1]/a/span").text
    assert(piaofang, "票房规划")
    driver.find_element_by_xpath("//*[@id=\"mainSidebar\"]/div/ul/li[1]/a/span").click()
    sleep(1)
    driver.find_element_by_xpath("//*[@id=\"mainSidebar\"]/div/ul/li[1]/ul/li[1]/a").click()
    xjgh = driver.find_element_by_xpath("//*[@id=\"contentWrapper\"]/div/section/h3").text
    assert(xjgh, "新建项目票房规划")
    driver.find_element_by_id("designName").send_keys("xt_0605")
    driver.find_element_by_id("expectIncome").send_keys("1")
    driver.find_element_by_id("hasSeat").click()
    sleep(1)
    driver.find_element_by_id("selVenueBtn").click()
    driver.find_element_by_id("queryVenueName").send_keys("XT")
    driver.find_element_by_id("queryVenue").click()
    sleep(1)
    driver.find_element_by_xpath("//*[@id=\"venueListBody\"]/tr/td[5]/input").click()
    driver.find_element_by_xpath("//*[@id=\"contentWrapper\"]/div/section/h3/input").click()
    sleep(10)
    tingguan = driver.find_element_by_xpath("//*[@id=\"contentWrapper\"]/div[1]/div/h3/div").text
    assert(tingguan, "xt_0605 XT-XT厅馆")
    driver.find_element_by_xpath("//*[@id=\"contentWrapper\"]/div[1]/div/h3/p[1]").click()

    canvas = driver.find_element_by_xpath("//*[@id=\"_seats_canvas\"]")
    ActionChains(driver).move_to_element_with_offset(canvas, 230, 76).click_and_hold().release().perform()
    sleep(5)
    baocun = driver.find_element_by_xpath("//*[@id=\"box-pop\"]/p/span").text
    assert(baocun, "保存票房规划成功！")
    driver.find_element_by_id("yl-btn-submit").click()
    sleep(5)
# except Exception as e:
#     raise e
finally:
    driver.quit()




