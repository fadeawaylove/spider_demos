# python+bs4+docker-selenium爬取全网代理IP
## 1.分析需求
> 待爬地址：http://www.goubanjia.com/   
> 界面如下图所示，是一个静态页面，但是分析之后得知，页面使用了css混淆以及js加密，在请求页面后，得到的port并不是真实的port，页面会经过js加密重新更改port为真实的port

![全网代理IP](https://raw.githubusercontent.com/fadeawaylove/article-images/master/%E5%85%A8%E7%BD%91ip-1571987702.png)


通过`display: None`使得部分元素隐藏，如果直接从页面获取就会得到假的ip
![css混淆](https://raw.githubusercontent.com/fadeawaylove/article-images/master/css%E6%B7%B7%E6%B7%86-1571988278.png)

分析结果:
> css混淆使用bs4筛选出真实的信息，js加密用python模拟或者python运行js都理论可行，但此处得不偿失，直接使用selenium+chrome更为简单快捷

## 2.环境准备

考虑到电脑上安装Chrome比较麻烦，这里直接使用docker搭建环境，运行命令：
```shell
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.141.59-xenon
```
## 3.代码实现
> 代码中的注释写的已经很清楚了  
> bs4和selenium的使用，不熟悉的话可以自行百度查看下使用方法，此处都是很基本的使用  
> 需要注意的是如何过滤掉css设置的style为`display:none`的标签

```python
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
                style = t.attrs.get("style")  # 过滤掉style为display：none的标签
                if style and "none" in style:
                    t.decompose()
        # 拼接得到ip:port形式的字符串，这就获取到要获取的信息了
        ip = "".join([x.string for x in td1 if x.string is not None])
        # print(ip)
        ip_list[ip_type].append(ip)

    return ip_list


if __name__ == '__main__':
    get_free_proxies()

```

