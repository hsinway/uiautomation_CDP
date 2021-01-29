import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By

from test_CDP_Web.test_frame.base import Base
from test_CDP_Web.page_object.home_page import HomePage


class Web(Base):

    def driver_ini(self):
        """
        初始化driver
        :return:
        """
        if self.driver is None:
            options = webdriver.ChromeOptions()
            options.debugger_address = '127.0.0.1:9222'  # 复用浏览器,跳过登陆和验证码部分
            options.add_argument('lang=zh-CN.UTF-8')
            self.driver = webdriver.Chrome(chrome_options=options)
        # else:
        #     self.driver = self.driver
        self.driver.implicitly_wait(5)
        self.__cookie_login()
        return self.driver
        # self.__login()

    def __login(self):
        self.driver.get("http://10.22.181.60/#/Login")
        self.driver.maximize_window()
        self.find(By.CSS_SELECTOR, "[id='username']").send_keys("")
        self.find(By.CSS_SELECTOR, "[id='password']").send_keys("")
        self.find(By.XPATH, "//*[@id='password']/../..//button").click()

    def __cookie_login(self):
        """
        使用cookie登陆
        :return:
        """
        # 使用cookie登陆前要打开一次和cookie一致的页面
        self.driver.get("http://10.22.181.60/#/Home")
        yaml_data = yaml.safe_load(open("../file/cookie.yaml", encoding="UTF-8"))
        for cookie in yaml_data:
            self.driver.add_cookie(cookie)
        self.driver.get("http://10.22.181.60/#/Home")

    def goto_home_page(self):
        return HomePage(self.driver)

    def quit(self):
        self.driver.quit()
