from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_free_proxies():
    """获取免费的代理"""
    url = "http://www.goubanjia.com/"
    # 远程连接Chrome
    driver = webdriver.Remote(command_executor="http://192.168.219.5:4444/wd/hub",
                              desired_capabilities=DesiredCapabilities.CHROME)
    driver.get(url)
    # 用selenium+chrome获取到的页面来实例化soup对象
    soup = BeautifulSoup(driver.page_source, "html.parser")
    trs = soup.find_all("tr")  # 找到所有的tr标签，其中包含着ip port等信息
    ip_list = {"http": [], "https": []}
    for tr in trs[1:]:  # 遍历tr标签
        td_list = tr.find_all("td")  # 找出所有td标签，每个td都对应一行中一列数据
        td1 = td_list[0]  # 这是ip：port的列
        td3 = td_list[2]  # 这是类型的列
        ip_type = td3.string
        for t in td1:
            if t.name:
                style = t.attrs.get("style")  # 过滤到style为display：none的标签
                if style and "none" in style:
                    t.decompose()
        # 拼接得到ip:port形式的字符串，这就获取到要获取的信息了
        ip = "".join([x.string for x in td1 if x.string is not None])
        # print(ip)
        ip_list[ip_type].append(ip)

    return ip_list


if __name__ == '__main__':
    get_free_proxies()
