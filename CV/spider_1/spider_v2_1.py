'''
    Spider_Nail 指甲
    from:image.baidu
    selenium:3.141.0
    chromedriver:80.0.3987.106
    Google Chrome:80.0.3987.116
    by:freefish
    version:2.1 (With agent)
'''

from selenium import webdriver
import time
import datetime
import random
import os
import requests


class BaiduImageSpider:
    def __init__(self, keyword, ty = None):
        self.keywords = keyword
        self.ty = ty
        if self.ty != None:
            self.save_to = './data/%s_BaiduImage/%s/'%(self.keywords, self.ty)
        else:self.save_to = './data/%s_BaiduImage/'%(self.keywords)
        try:
            os.makedirs(self.save_to)  # 创建文件夹
        except Exception as e:
            self.log_w("log.txt", 'a', "\n" + str(e) + ":n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.url = 'https://image.baidu.com/'
        self.browser = webdriver.Chrome()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
        }
        # 定义代理,私密代理
        name = 1549971272
        pwd = "wp5d19y2"
        ip = "42.84.163.190:22452"

        # 'http':'http://用户名:密码@IP:端口号
        self.proxies = {
            'http': f'http://{name}:{pwd}@{ip}',
            'https': f'https://{name}:{pwd}@{ip}'
        }

    def log_w(self, p, w, c): #定义写文件
        '''
            以w方式的方式打开p文件，并写入c内容
        :param p: Pathname
        :param w: Way
        :param c: Content
        :return: None
        '''
        with open(p, w) as fw:
            fw.write(c)
            fw.close()

    def download_image(self, url, number):
        filename = str(number) + '.jpg'
        pathname = os.path.join(self.save_to, filename)
        resp = requests.get(url, proxies = self.proxies, headers=self.headers, )
        try:
            self.log_w(pathname, 'wb', resp.content)
            print('\n' + number + ".jpg")
        except Exception as e:
            self.log_w("log.txt", 'a', "\n"+ str(e))
        self.log_w("log.txt", 'a' , "\n" + filename+"    "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n" + url)

    def enter_image_page(self):
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
            self.log_w("log.txt", 'a', "\n" + "未选择类型" + "    " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            for item in self.browser.find_element_by_xpath('//*[@id="topRS"]').find_elements_by_tag_name("div"):
                if item.text == self.ty:
                    element = item
                    try:
                        element.click()
                    except Exception as e:
                        self.browser.fullscreen_window()
                        element.click()
                        self.browser.maximize_window()

        # 进入预览界面
        time.sleep(1)
        element = self.browser.find_element_by_xpath('//*[@id="imgid"]/div/ul/li[1]/div/div/a')
        element.click()
        # 切换窗口到
        all_handle = self.browser.window_handles # 获取当前所有句柄（窗口）
        self.browser.switch_to.window(all_handle[1]) # 切换browser到新的窗口，获取新窗口的对象

    def parse_link_and_download(self, v):
        for i in range(v):
            element = self.browser.find_element_by_xpath('//*[@id="currentImg"]')
            url = element.get_attribute('src') # 获取属性值
            self.download_image(url, i+1)
            try:
                next_page_element = self.browser.find_element_by_xpath('//*[@id="container"]/span[2]')
                next_page_element.click()
                time.sleep(random.uniform(0.2, 0.7))
            except Exception as e:
                self.log_w("log.txt", 'a', str(e))
                break

    def run(self, v):
        self.log_w("log.txt", 'a', "\n" + self.keywords + "  "+ self.ty + "获取开始！    " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.enter_image_page()
        self.parse_link_and_download(v)
        self.log_w("log.txt", 'a', "\n" + self.keywords + "  "+ self.ty + "获取完成！    " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    spider1 = BaiduImageSpider('指甲', "Nail_Normal")
    spider1.run(1000)
    spider2 = BaiduImageSpider('指甲', "Nail_Art")
    spider2.run(1000)