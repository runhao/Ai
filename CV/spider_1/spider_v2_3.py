'''
    Spider_Nail 指甲
    from:image.baidu
    selenium:3.141.0
    chromedriver:80.0.3987.106
    Google Chrome:80.0.3987.116
    by:freefish
    version:2.2 (With agent)
'''

from selenium import webdriver
import time
import datetime
import random
import os
import requests
import json

class BaiduImageSpider:
    def __init__(self, keyword, ty = None):
        self.keywords = keyword
        self.ty = ty
        # 定义代理,私密代理
        self.name = 1549971272
        self.pwd = 'wp5d19y2'
        self.secret_id = 'off4m0u1qdhnkpcsd6ar'
        self.secret_key = 'fz7fide1cvhazwr9kq6in9nncsygojay'
        if self.ty != None:
            self.save_to = './data/%s_BaiduImage/%s/'%(self.keywords, self.ty)
        else:self.save_to = './data/%s_BaiduImage/'%(self.keywords)
        try:
            os.makedirs(self.save_to)  # 创建文件夹
        except Exception as e:
            self.log_w("\n" + str(e) + ":n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.browser = webdriver.Chrome()
        self.url = 'https://image.baidu.com/'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
        }

    def get_ip(self):
        '''
            从三方代理获取私密ip,并填充至proxies
        :return: None
        '''
        token_url = 'https://auth.kdlapi.com/api/get_secret_token'
        data_token = {
            'secret_id': f'{self.secret_id}',
            'secret_key': f'{self.secret_key}'
        }
        res = requests.post(token_url, data_token).json()
        self.secrettoken = res["data"]["secret_token"]
        ip_url = 'https://dps.kdlapi.com/api/getdps?secret_id=' + self.secret_id + '&num=1&signature=' + self.secrettoken
        res = requests.get(ip_url)
        self.ip = res.text
        self.proxies = { # 'http':'http://用户名:密码@IP:端口号
            'http': f'http://{self.name}:{self.pwd}@{self.ip}',
            'https': f'https://{self.name}:{self.pwd}@{self.ip}'
        }

    def log_w(self, c, p = "log.txt", w = 'a'): #定义写文件
        '''
            以w方式的方式打开p文件，并写入c内容
        :param p: Pathname,默认写log.txt
        :param w: Way,默认以追加方式
        :param c: Content
        :return: None
        '''
        with open(p, w) as fw:
            fw.write(c)
            fw.close()

    def download_image(self, url, number):
        '''
            下载当前图片
        :param url: 网页地址
        :param number: 保存文件名前缀
        :return: 成功返回1,失败返回0
        '''
        filename = str(number) + '.jpg'
        pathname = os.path.join(self.save_to, filename)
        resp = None
        i = 0
        while resp == None and i < 4:
            try :
                self.get_ip()
                res = requests.get(url, proxies = self.proxies, headers=self.headers, timeout = 5) # 5秒超时判定代理ip状态
                resp = res
            except Exception as e:
                self.log_w('\n\n' + str(e) + '\n')
                i += 1
                time.sleep(1)
            try:
                self.log_w(resp.content, pathname, 'wb')
                print(filename)
            except Exception as e:
                self.log_w("\n"+ str(e))
            self.log_w("\n" + filename+ "----" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "----" + self.ip + "\n" + url)
            return 1
        self.log_w("获取代理IP失败，请检查用户信息")
        return 0

    def enter_image_page(self, i=1):
        '''
            页面操作
        :param i:默认为1,表示从第i个开始增量
        :return: None
        '''
        self.browser.maximize_window()
        # 进入百度图片首页
        self.browser.get(self.url)
        element = self.browser.find_element_by_xpath('//*[@id="kw"]')
        element.send_keys(self.keywords)  # 输入关键字
        element = self.browser.find_element_by_xpath('//*[@id="homeSearchForm"]/span[2]/input')
        element.click()  # 进行搜索
        element = self.browser.find_element_by_xpath('//*[@id="typeFilter"]/div[2]/ul/li[2]')
        element.click()  # 点击'高清'
        if self.ty == None:
            self.log_w("\n" + "未选择类型" + "    " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            # for item in self.browser.find_element_by_xpath('//*[@id="topRS"]').find_elements_by_tag_name("div"):
                # if item.text == self.ty:
                #     element = item
            list_n = self.browser.find_element_by_xpath('//*[@id="topRS"]').find_elements_by_tag_name("div")
            for i in range(len(list_n)):
                if list_n[i].text == self.ty: # //*[@id="topRS"]/div[{len(list_n)}]/div
                    n = int(i/15)
                    for _ in range(n):
                        element = self.browser.find_element_by_xpath(f'//*[@id="topRS"]/div[{len(list_n)-2}]/div')
                        element.click()
                    element = list_n[i]
                    try:
                        element.click()
                    except Exception as e: # 元素被遮挡
                        self.browser.fullscreen_window()
                        element.click()
                        time.sleep(0.1)
                        self.browser.maximize_window()
        # 进入预览界面
        time.sleep(1)
        n = 200
        while n > 0:
            try:
                element = self.browser.find_element_by_xpath(f'//*[@id="imgid"]/div[{1+int(i/24)}]/ul/li[{i%24}]/div/div/a') # //*[@id="imgid"]/div[8]/ul/li[1]/div[1]/div[2]/a/img
                print("划条滚动第：%s次"%(201-n))
                self.log_w("划条滚动第：%s次"%(201-n))
                break
            except Exception as e:
                self.browser.execute_script("window.scrollBy(0,1000)")
                print("页面未加载完全，正在翻页")
                n -= 1
                time.sleep(0.7)
        element.click()
        # 切换窗口到
        all_handle = self.browser.window_handles # 获取当前所有句柄（窗口）
        self.browser.switch_to.window(all_handle[1]) # 切换browser到新的窗口，获取新窗口的对象

    def parse_link_and_download(self, l, f=1):
        '''
            在页面中循环下载及翻页
        :param v:
        :return:
        '''
        i = f
        # for i in range(f, l):
        while i < l:
            element = self.browser.find_element_by_xpath('//*[@id="currentImg"]')
            url = element.get_attribute('src') # 获取属性值
            if self.download_image(url, i):
                try:
                    next_page_element = self.browser.find_element_by_xpath('//*[@id="container"]/span[2]')
                    next_page_element.click()
                    i += 1
                    time.sleep(random.uniform(0.1, 0.2))
                except Exception as e:
                    self.log_w(str(e))
                    return 0
            else:return 0
        return 1

    def run(self, l):
        try:
            self.log_w("\n" + self.keywords + "  "+ self.ty + "  spider开始！    " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            max_i = 1
            if len(os.listdir(os.getcwd() + self.save_to[1:])) == 0: # 判断是否为增量爬取
                print(f"{self.save_to[1:]}    目录下无文件")
                self.enter_image_page()
            else:
                for item in os.listdir(os.getcwd() + self.save_to[1:]):
                    max_i = max(max_i, int(item[:-4])) # 增量爬取求最后一次文件名
                if max_i < l:
                    self.enter_image_page(max_i) # 进入增量爬取界面
            if self.parse_link_and_download(l, max_i):
                self.log_w("\n" + self.keywords + "  " + self.ty + "  获取完成！    " + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'))
            else:
                self.log_w("\n" + self.keywords + "  " + self.ty + "  获取失败！    " + datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print(e)
            self.log_w("\n" + self.keywords + "  " + self.ty + "  获取失败！    " + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + "\n" + str(e))

if __name__ == '__main__':
    spider1 = BaiduImageSpider('指甲', "Nail_Normal")
    spider1.run(500)
    spider2 = BaiduImageSpider('指甲', "Nail_Art")
    spider2.run(500)