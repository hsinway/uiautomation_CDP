import logging
import string

import allure
import yaml
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from test_CDP_Web.test_frame.popup_handle import BlackList, popup_wrapper
from test_CDP_Web.test_frame.web import Web


class Base:
    def __init__(self):
        self.driver = Web().driver  # 实例化Web并获得driver
        # 获取blacklist列表
        self.black_list = BlackList().blacklist

    @popup_wrapper
    def find(self, by, value=None):
        if value is None:
            # 如果传入的数据是元组,则加*解包为两个元素,第一个作为find_element的by参数第二个作为find_element的value参数
            return self.driver.find_element(*by)
        else:
            # 如果传入的数据是正常
            return self.driver.find_element(by=by, value=value)

    def finds(self, by, value=None):
        if value is None:
            # 如果传入的数据是元组,则加*解包为两个元素,第一个作为find_element的by参数第二个作为find_element的value参数
            return self.driver.find_elements(*by)
        else:
            # 如果传入的数据是正常
            return self.driver.find_elements(by=by, value=value)

    def find_and_click(self, by, value=None):
        if value is None:
            # 如果传入的数据是元组,则加*解包为两个元素,第一个作为find_element的by参数第二个作为find_element的value参数
            return self.find(*by).click()
        else:
            # 如果传入的数据是正常
            return self.find(by=by, value=value).click()

    def find_and_send(self, by, value, content):
        return self.find(by, value).send_keys(content)

    def find_lable_and_dropdown_select(self, label, *args):
        """
        下拉列表的操作
        :param label: 标签名
        :param args: 选择列表中的选项,可为一个list
        :return:
        """
        # 点开下拉列表
        self.find_and_click(By.XPATH, f"//label[text()='{label}']/..//span[@class='el-input__suffix']")
        logging.info(f"期望标签:{args}")
        for arg in args:
            logging.info(f"选择标签:{arg}")
            self.wait_to_clickable((By.XPATH, f"//span[contains(text(),'{arg}')]"))
            self.find_and_click(By.XPATH, f"//span[contains(text(),'{arg}')]")
        # 收起下拉列表
        self.find_and_click(By.XPATH, f"//label[text()='{label}']/..//span[@class='el-input__suffix']")

    def dropdown_select(self, *args):
        """
        :param args: 选择列表中的选项,只能选择一个
        :return:
        """
        # 点开下拉列表
        self.find_and_click(By.XPATH, "//div[@class='channel channel-select']//span[@class='el-input__suffix']")
        for arg in args:
            self.find_and_click(By.XPATH, f"//span[text()='{arg}']")

    def drag_and_drop_slider(self, locator_slider, locator_slider_button, slide_len):
        """
        滑动条操作
        :param locator_slider: 滑动条
        :param locator_slider_button: 滑动条按钮
        :param slide_len: 滑动百分比,必须为整数,例如50代表滑动50%
        :return:
        """
        _ele_slider = self.find(locator_slider)
        _width_total = int(_ele_slider.size['width'])
        _ele_slider_bar = self.find(locator_slider_button)
        _style_button = _ele_slider_bar.get_attribute("style")
        _xoffset = _width_total * (int(slide_len) / 100)
        action = ActionChains(self.driver)
        if "left: 0%;" not in _style_button:
            action.drag_and_drop_by_offset(_ele_slider_bar, -_width_total, 0).perform()  # 首先滑动回起始点
        action.drag_and_drop_by_offset(_ele_slider_bar, _xoffset, 0).perform()

    def drag_and_drop(self, drag_locator, drop_locator):
        """
        拖动操作
        :param drag_locator:拖动元素定位
        :param drop_locator:释放元素定位
        :return:
        """
        # todo: 完成拖拽有效性
        drag_ele = self.find(drag_locator)
        # drag_ele = self.driver.find_element(By.XPATH,"//div[@id='component-title']/../aside//div[text()='性别']")
        drop_ele = self.find(drop_locator)
        action = ActionChains(self.driver)
        action.move_to_element(drag_ele).pause(1)
        # action.click(drag_ele).pause(3)
        # drag_ele1 = self.find(drag_locator)
        # action.drag_and_drop_by_offset(drag_ele1,20,50).perform()
        action.click_and_hold(drag_ele).pause(1)
        action.move_by_offset(1, 0).pause(1)
        action.move_to_element(drop_ele)
        action.move_by_offset(1, 0).pause(1)
        action.release().perform()

    def get_displayed_labels(self, *args):
        lables = []
        for arg in args:
            eles = self.finds(By.XPATH,
                              f"//span[text()='{arg}']/../..//div[@class='el-tree-node__children']//span[@class='el-tree-node__label']")
            for ele in eles:
                lables.append(ele.text)
        return lables

    def wait_to_visible(self, locator):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(locator))

    def wait_to_invisible(self, locator):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.invisibility_of_element(locator))

    def wait_to_clickable(self, locator):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(locator))

    def get_scrrenshot(self, filepath):
        self.driver.save_screenshot(filepath)

    def allure_add_screenshot(self, filepath, pic_name):
        with open(filepath, 'rb') as f:  # 图片，不需要加uft-8 打开图片用rb模式binary mode
            picture_data = f.read()
        allure.attach(picture_data, name=pic_name, attachment_type=allure.attachment_type.PNG)

    def key_value_step_driven_yaml(self, yaml_path, func_name, variables: dict = None):
        """
        关键字驱动
        :param yaml_path: yaml文件路径
        :param func_name: page func名
        :param variables: 需要替换的参数,默认不提供参数
        :return:
        """
        _find = 'find'
        _action = 'action'
        _content = 'content'
        _select = 'select'

        _find_and_click = 'find_and_click'
        _send = 'send'
        _dropdown_select = 'dropdown_select'

        with open(yaml_path, 'r', encoding="utf-8") as f:
            rawdata = yaml.safe_load(f)[func_name]
            data = string.Template(str(rawdata))
            if variables is not None:
                data = data.substitute(**variables)
            data = eval(data)
            # print(data)
        # step: find, action
        for step in data:
            # 关键字可变问题:设置类常量
            keyword = step.get(_find)
            action = step.get(_action)
            # 函数调用
            if action == _find_and_click:
                self.find_and_click(By.XPATH, keyword)
            elif action == _send:
                content = step.get(_content)  # 取出发送文本
                self.find_and_send(By.XPATH, keyword, content)
            elif action == _dropdown_select:
                select = step.get(_select)
                self.find_lable_and_dropdown_select(keyword, *select)

    def refresh(self):
        self.driver.refresh()

    def quit(self):
        self.driver.quit()

    def goback_homepage(self):
        self.find_and_click(By.XPATH, "//*[@alt='Menu']")
        self.find_and_click(By.LINK_TEXT, "主页")
