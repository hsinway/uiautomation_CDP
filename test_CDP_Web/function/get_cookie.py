import yaml
from selenium import webdriver

def test_get_cookie():
    """
    步骤:
    1.下载并安装版本合适的Chromedriver
    2.关闭所有Chrome进程
    3.执行chrome --remote-debugging-port=9222开启复用浏览器
    4.打开测试页面并手动登陆一次
    5.执行下面的代码获取cookie并保存
    :return:
    """
    option = webdriver.ChromeOptions()
    # 设置debug地址
    option.debugger_address = '127.0.0.1:9222'
    driver = webdriver.Chrome(options=option)
    driver.get('http://10.22.181.60/#/Home')
    driver.implicitly_wait(5)
    cookies = driver.get_cookies()
    print(cookies)
    yaml.dump(cookies, open('../file/cookie.yaml', 'w', encoding='UTF-8'))