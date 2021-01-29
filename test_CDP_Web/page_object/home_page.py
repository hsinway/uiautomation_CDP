from selenium.webdriver.common.by import By

from test_CDP_Web.page_object.customer_selection_page import CustomerSelectionPage
from test_CDP_Web.page_object.pre_page import PrePage


class HomePage(PrePage):
    def goto_customer_selection(self):
        """
        跳转到客户筛选页面
        :return:
        """
        self.base.find(By.LINK_TEXT, "客户筛选").click()
        return CustomerSelectionPage(self.base)

    def goto_customer_selection_8082(self):
        """
        跳转到客户筛选页面
        :return:
        """
        self.base.find(By.LINK_TEXT, "人群筛选").click()
        return CustomerSelectionPage(self.base)
