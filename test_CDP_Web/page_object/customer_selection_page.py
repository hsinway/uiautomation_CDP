import logging

from selenium.webdriver.common.by import By
from test_CDP_Web.page_object.pre_page import PrePage


class CustomerSelectionPage(PrePage):
    _locator_group_name = (By.XPATH, "//label[text()='群组名称']/..//input")
    _locator_customer_cnt = (By.XPATH, "//*[@id='selection-num-selection']")
    _locator_circular_1 = (By.XPATH, "//div[text()='群组统计信息']/../..//*[@class='circular']")
    _locator_circular_2 = (By.XPATH, "//div[text()='群组创建']/../..//*[@class='circular']")
    _locator_group_name_new = (By.XPATH, "//div[text()='该客户群组需使用新群组名进行另存']/../..//input")
    _locator_group_list = (By.XPATH, "//a[text()='双十一大促']/../../..//*[@class='el-menu-item-group']//a")
    _locator_group_status = (By.XPATH, "//label[text()='分发状态']/..//span")
    _locator_distribute_execute = (By.XPATH, "//span[text()='执行分发']")
    _locator_slider = (By.XPATH, "//div[@id='channel-container']/div[last()]//div[@class='el-slider__runway']")
    _locator_slider_button = (
        By.XPATH, "//div[@id='channel-container']/div[last()]//div[@class='el-slider__button-wrapper']")
    _locator_dist_number = (By.XPATH, "//div[@id='channel-container']/div[last()]//div[@class='num']")

    def goto_group(self, group_father, group_children=None):
        """
        选择一个群组
        :param group_father:父群组
        :param group_children:子群组
        :return:
        """
        self.base.find(By.LINK_TEXT, group_father).click()
        if group_children is None:
            self.base.find_and_click(By.XPATH, "//span[text()='创建新分组']")
        else:
            self.base.find(By.LINK_TEXT, group_children).click()
        self.base.wait_to_clickable(self._locator_group_name)
        return self

    def select_lable(self, lable, selections: list, screenshot_path=None):
        """
        群组选择标签
        :param lable: 标签名
        :param selections: 标签选项,列表形式
        :param screenshot_path: 截屏路径，默认None
        :return:
        """
        self.base.find_and_click(By.XPATH, "//div[text()='基础标签']/../..//div[text()='更多标签']")
        # 标签选择
        self.base.find_lable_and_dropdown_select(lable, *selections)
        if screenshot_path is not None:
            self.base.get_scrrenshot(screenshot_path)
            self.base.allure_add_screenshot(screenshot_path, "attach_pic")
        labels = self.base.get_displayed_labels(lable)
        return labels

    def click_customer_cal(self):
        """
        计算客户数量
        :return:
        """
        # 选择性别
        self.base.find_lable_and_dropdown_select("性别", "男")
        count_before = self.base.find(By.XPATH, "//*[@id='selection-num-selection']").text
        self.base.find_and_click(By.XPATH, "//span[text()='计算客户数']")
        # 先等待转圈出现,再等待转圈消失
        self.base.wait_to_visible(self._locator_circular_1)
        self.base.wait_to_invisible(self._locator_circular_1)
        count_after = self.base.find(By.XPATH, "//*[@id='selection-num-selection']").text
        return count_before, count_after

    def create_group(self, group_name, screenshot_path=None):
        """
        创建新群组
        :param group_name: 新群组名称
        :param screenshot_path: 截屏路径，默认None
        :return:
        """
        variables = {
            'new_group_name': group_name
        }
        self.base.key_value_step_driven_yaml("../file/customer_selection_page.yaml", "create_group", variables)
        # 截图
        if screenshot_path is not None:
            self.base.get_scrrenshot(screenshot_path)
            self.base.allure_add_screenshot(screenshot_path, "attach_pic")
        return self

    def create_group_8082(self, group_name, screenshot_path=None):
        """
        创建新群组
        :param group_name: 新群组名称
        :param screenshot_path: 截屏路径，默认None
        :return:
        """
        drag = (By.XPATH, "//div[@id='component-title']/../aside//div[text()='性别']")
        drop = (By.XPATH, "//div[@id='cust-set-config-container']")

        self.base.find_and_click(By.XPATH, "//div[@id='component-title']/../aside//div[text()='基础标签']")
        self.base.drag_and_drop(drag, drop)
        self.base.drag_and_drop((By.XPATH, "//div[@id='component-title']/../aside//div[text()='学历状况']"),
                                (By.XPATH, "//div[contains(@class,'tag-drop-zone')]"))

        # self.base.find_and_click(By.XPATH, "//div[text()='国籍']")
        # 填写群组名称
        self.base.find_and_send(*self._locator_group_name, group_name)
        # 点击保存按钮
        # self.base.find_and_click(By.XPATH, "//span[text()='保存']")
        # 截图
        if screenshot_path is not None:
            self.base.get_scrrenshot(screenshot_path)
        return self

    def distribute_execute(self, *args, distribute=False, screenshot_path=None):
        """
        分发配置以及执行分发
        :param args: 分发渠道,SMS,WeChat等
        :param distribute: 默认False,不执行分发.若设为True则执行分发
        :return:
        """
        self.base.find_and_click(By.XPATH, "//span[text()='分发']")
        # self.base.wait_to_visible(self._locator_distribute_execute)
        total_dist_number_epx = 0
        for arg in args:
            # 添加分发渠道
            self.base.find_and_click(By.XPATH, "//i[@class='el-icon-circle-plus-outline']")
            self.base.dropdown_select(arg)
            self.base.drag_and_drop_slider(self._locator_slider, self._locator_slider_button, 75)
            # 获得实际分发人数
            dist_number = self.base.find(self._locator_dist_number).text
            total_dist_number_epx = total_dist_number_epx + int(dist_number.split()[0].replace(",", ""))
        if screenshot_path is not None:
            self.base.get_scrrenshot(screenshot_path)
            self.base.allure_add_screenshot(screenshot_path, "attach_pic")
        if distribute is True:
            # 执行分发
            self.base.find_and_click(self._locator_distribute_execute)
            return self
        else:
            total_dist_number_act = self.base.find(By.XPATH,
                                                   "//div[contains(text(),'分发选择总人数')]//div[@class='cust-num']").text
            return total_dist_number_epx, int(total_dist_number_act.replace(",", ""))

    def get_group_name_status(self, group_father, group_children, expected_status=None):
        """
        获取群组名称和状态
        :param group_father: 父群组
        :param group_children: 子群组
        :param expected_status: 期望群组状态,默认为None
        :return:
        """
        self.base.wait_to_visible((By.LINK_TEXT, group_father))
        self.goto_group(group_father, group_children)
        group_name = self.base.find(self._locator_group_name).get_attribute("value")
        group_status = self.base.find(self._locator_group_status).text
        # 若设置期望值则等待当前状态是否等于期望状态.等待周期为10次刷新
        if expected_status is not None:
            i = None
            for i in range(11):
                if group_status.lower() == expected_status:
                    break
                else:
                    self.base.refresh()
                    self.goto_group(group_father, group_children)
                    group_status = self.base.find(self._locator_group_status).text
            logging.info(f"\n{i}次刷新后群组状态为:{group_status}")
        return group_name, group_status
