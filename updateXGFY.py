import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
import time
import requests

#将pyppeteer封装成pyfechUrl函数，用于发起网络请求和获取源码
async def pyfechUrl(url):
    browser = await launch({'headless':False,'dumpio':True,'autoClose':True})
    page = await browser.newPage()

    await page.goto(url)
    await asyncio.wait([page.waitForNavigation()])
    str = await page.content()
    await browser.close()
    return str

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyfechUrl(url))

#获取第一页文章标题和链接
def getTitle(html):
    beautifulsoup = BeautifulSoup(html,'html.parser')
    titleList = beautifulsoup.find('div',attrs={"class":"list"}).ul.find_all("li")
    for item in titleList:
        link = "http://www.nhc.gov.cn" + item.a["href"];
        title = item.a["title"]
        yield title,link

#获取消息列表第一个消息并返回列表名和链接
def titlelist():
    url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
    source = fetchUrl(url)
    lis =[]
    for title,link in getTitle(source):
        lis.append(title)
        lis.append(link)
        break
    return lis

#获取第一个正文内容
def getContent():
    lis = titlelist()
    html = fetchUrl(lis[1])
    bsobj = BeautifulSoup(html,'html.parser')
    content = bsobj.find('div', attrs={"id":"xw_box"}).find_all("p")
    txt = ""
    if content:
        for item in content:
            txt =item.text
            return txt
    return "抓取正文失败！"

#消息推送api
def send(oldlis):
    import requests
    api = "https://sc.ftqq.com/SCU142264T4d121577bbae7f4fcf9f22a2e9b0af595fecc72fec677.send"#SCKEY去server酱官网注册可得
    title = oldlis[0]
    content = getContent()
    
    data = {
        "text":title,
        "desp":content
        }
    req = requests.post(api,data = data)


#主函数
if __name__=="__main__":
    t=3600      #设置定时时长，单位为秒
    oldlis = titlelist()
    while True:     #间隔t时间查看网页是否更新
        newlis = titlelist()
        if oldlis!=newlis:
            oldlis = newlis
            send(oldlis)
        time.sleep(t)

