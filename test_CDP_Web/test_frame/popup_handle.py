from selenium.webdriver.common.by import By


class BlackList:
    def __init__(self):
        self.blacklist = [(By.XPATH, "//span[contains(text(),'确认')]")]


def popup_wrapper(fun):
    def run(self, *args, **kwargs):
        try:
            return fun(self, *args, **kwargs)
        except Exception as e:
            black_list = self.black_list
            for locator in black_list:
                eles = self.finds(locator)
                if len(eles) > 0:
                    eles[0].click()
                    return fun(self, *args, **kwargs)
            raise e

    return run
