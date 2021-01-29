from datetime import datetime

import pytest
import yaml

from test_CDP_Web.page_object.home_page import HomePage
from test_CDP_Web.test_frame.base import Base


class TestCustomerGroup:
    """
    cmd:
    pytest test_customer_group.py --alluredir ../allure_result --clean-alluredir
    allure serve ../allure_result
    allure generate ../allure_result -o ../allure_report --clean
    """
    _time = datetime.now()
    _new_group_name = f"test_{_time.month}_{_time.day}_{_time.hour}{_time.minute}"
    # _new_group_name='test_1_29_1354'
    _test_data = yaml.safe_load(open("../file/test_data.yaml", "r", encoding="utf-8"))

    def setup_class(self):
        self.basepage = Base()
        self.start = HomePage(self.basepage)

    def teardown_class(self):
        # self.basepage.quit()
        pass

    def teardown(self):
        self.basepage.goback_homepage()
        pass

    @pytest.mark.parametrize("lable, selections",
                             _test_data["test_select_lable"]["test_data"],
                             ids=_test_data["test_select_lable"]["test_ids"]
                             )
    def test_select_lable(self, lable, selections):
        """
        验证标签的选择
        :return:
        """
        res = self.start.goto_customer_selection().goto_group("双十一大促") \
            .select_lable(lable, selections, screenshot_path=f"../file/test_select_lable_{lable}.png")
        for selection in selections:
            assert selection in res

    def test_customer_calculation(self):
        """
        验证计算客户数功能
        :return:
        """
        res = self.start.goto_customer_selection().goto_group("双十一大促").click_customer_cal()
        assert int(res[1].replace(",", "")) == 13774

    # @pytest.mark.skip
    def test_group_creation(self):
        """
        验证新建群组
        :return:
        """
        res = self.start.goto_customer_selection().goto_group("双十一大促") \
            .create_group(self._new_group_name).get_group_name_status("双十一大促", self._new_group_name)
        assert res[0] == self._new_group_name and res[1].lower() == "saved"

    def test_distribute_config(self):
        """
        验证分发配置
        :return:
        """
        res = self.start.goto_customer_selection().goto_group("双十一大促", self._new_group_name) \
            .distribute_execute("SMS", "WeChat",screenshot_path=f"../file/test_distribute_config.png")
        assert int(res[0]) == int(res[1])

    # @pytest.mark.skip
    def test_distribute_execute(self):
        """
        验证分发执行
        :return:
        """
        res = self.start.goto_customer_selection().goto_group("双十一大促", self._new_group_name) \
            .distribute_execute("WeChat", distribute=True) \
            .get_group_name_status("双十一大促", self._new_group_name, "delivered")
        assert res[1].lower() == "delivered"

    @pytest.mark.skip
    def test_group_creation_8082(self):
        # todo:待拖拽功能完成
        self.start.goto_customer_selection_8082().goto_group("618Campaign").create_group_8082('test111')
