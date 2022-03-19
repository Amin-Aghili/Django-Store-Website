from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from googletrans import Translator
from selenium.common.exceptions import TimeoutException, InvalidArgumentException, WebDriverException, NoSuchElementException
import re
from django.contrib import messages
# from threading import Lock
from time import sleep


class TrendyolShop:
    translator = Translator()
    options = Options()
    options.headless = False
    # profile = webdriver.FirefoxProfile('/home/amin/.mozilla/firefox/1czivhxu.default-release')

    url = "https://www.tgju.org/profile/price_try"
    driver = webdriver.Firefox(options=options)  # (options=option, firefox_profile=profile)

    def exchange_rates(self):
        try:
            self.driver.get(self.url)
            self.driver.refresh()
            tl_rial = self.driver.find_elements(By.CLASS_NAME, "text-left")
            tl_rial_int = int(tl_rial[2].text.replace(",", ""))
            return tl_rial_int/10 + 100
        except (InvalidArgumentException, WebDriverException):
            messages.error('Cal to admin', 'danger')

    def check_trendyol_url(self, request, url):
        try:
            regex = re.compile(r'^(https://)(?:www.trendyol.com|ty.gl)(/((?:[\w?!@#$%^&*()+|~><:;{}\][\=&-]*)(?<!/)))+/?',
                               re.IGNORECASE)
            if re.match(regex, url) is not None and re.match(regex, url).group() == url:
                self.driver.get(url)
                return True
            else:
                messages.error(request, 'Please enter a valid URL', 'danger')
                return False
        except (InvalidArgumentException, WebDriverException):
            messages.error(request, 'Please try again...', 'danger')
            return False

    def is_sizes(self):
        try:
            self.driver.implicitly_wait(10)
            is_size = self.driver.find_elements(By.CLASS_NAME, "variants")
            if len(is_size) > 0:
                list_size = self.driver.find_elements(By.CLASS_NAME, "sp-itm")
                list_size = [i.text for i in list_size]
                so_sizes = self.driver.find_elements(By.CLASS_NAME, "so.sp-itm")
                so_size = [size.text for size in so_sizes]
                list_size_tuple = [list_size[x] for x in range(len(list_size))]
                cd_size = [size_tuple for size_tuple in list_size_tuple if size_tuple not in so_size]
                print(cd_size)
                print(type(cd_size))
                return cd_size
            else:
                return False
        except (InvalidArgumentException, WebDriverException):
            return False

    def selected_size(self, size, request, tl):
        chain = ActionChains(self.driver)
        try:
            # with Lock():
            self.driver.implicitly_wait(10)
            chain.click(self.driver.find_element(By.XPATH, f"//div[@class='variants']/div[text()='{size}']")).perform()
            sleep(1)
            return self.price(request, tl)
        finally:
            pass

    def price(self, request, tl):
        exchange = tl
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//div[@class= "product-price-container"]//span[starts-with(@class, "prc-")]'))
            )
            price_tl = float([i.text.split() for i in element][-1][0].replace('.', '').replace(',', '.'))
            price = (int(round(round(price_tl, 1) * exchange * 1.28, -3)))
            return price, price_tl
        except (NoSuchElementException, TimeoutException):
            messages.error(request, 'URL is wrong !!!', 'danger')

    def images_url(self):
        try:
            self.driver.implicitly_wait(10)
            images_ = self.driver.find_element(By.XPATH, "//div[@class='base-product-image']//img").get_attribute("src")
            return images_
        except (InvalidArgumentException, WebDriverException, NoSuchElementException):
            return False

    def details(self):
        try:
            self.driver.implicitly_wait(10)
            details = self.driver.find_elements(By.CLASS_NAME, "detail-attr-container")
            if len(details) > 0:
                details = [i.text for i in details]
                details = (details[0].split('\n'))
                return details
            else:
                pass
        except (InvalidArgumentException, WebDriverException):
            pass

    def close(self):
        self.driver.quit()

