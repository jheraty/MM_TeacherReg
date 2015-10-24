__author__ = 'jheraty'


# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from datetime import datetime

class BasicReg(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.mobymax.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Reg(self):
        driver = self.driver
        driver.get(self.base_url)
        driver.find_element_by_xpath(".//*[@id='toplinks']/ul[1]/li[8]/a/img").click()
        time.sleep(3)

        current = (time.strftime("%H-%M"))

        #Start registration for teacher
        driver.find_element_by_id("signin_as_select").click()
        ListFunction = Select(driver.find_element_by_id("signin_as_select"))
        ListFunction.select_by_visible_text("Teacher")
        driver.find_element_by_id("signin_as_select").send_keys(Keys.RETURN)
        driver.find_element_by_link_text("Don't have a MobyMax account yet? Sign up today.").click()

        #Register
        driver.find_element_by_name("data[FirstName]").clear()
        driver.find_element_by_name("data[FirstName]").send_keys("Jennifer")
        driver.find_element_by_name("data[LastName]").clear()
        driver.find_element_by_name("data[LastName]").send_keys("Heraty")
        driver.find_element_by_xpath("//form[@id='register-element-form']/div[3]/div/img").click()
        driver.find_element_by_css_selector("div.custom-radio.custom-radio-1 > img").click()
        driver.find_element_by_name("data[ZipCode]").clear()
        driver.find_element_by_name("data[ZipCode]").send_keys("92127")
        driver.find_element_by_name("data[School]").click()
        driver.find_element_by_id("100412").click()
        driver.find_element_by_name("data[Email]").clear()
        driver.find_element_by_name("data[Email]").send_keys(current + "@gmail.com")
        driver.find_element_by_name("data[Password]").clear()
        driver.find_element_by_name("data[Password]").send_keys("password")
        driver.find_element_by_id("register-button").click()
        time.sleep(3)

        #Make sure the welcome video displays
        for i in range(60):
            try:
                if driver.find_element_by_xpath("//*[@id='video-dialog']/div/div[1]").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("The Welcome video never displayed")


    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
