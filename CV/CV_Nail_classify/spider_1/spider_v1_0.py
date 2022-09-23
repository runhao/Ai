'''
    Spider_Nail 指甲
    from:image.baidu
    selenium:3.141.0
    chromedriver:80.0.3987.106
    Google Chrome:80.0.3987.116
    by:freefish
    version:1.0 (No agent)
'''

from selenium import webdriver
import time
import datetime
import random
import os
import requests

class NailImageSpider:
    def __init__(self, keyword):
        self.keywords = keyword
        self.save_to = './data/%s_Baidu/'%self.keywords
        try:
            os.makedirs(self.save_to)  # 创建文件夹
        except Exception as e:
            print(self.save_to, ':', e)
            with open("log.txt", 'a') as fw:  # 创建日志
                fw.writelines("\n" + str(e) + ":n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        self.url = 'https://image.baidu.com/'
        self.browser = webdriver.Chrome()
        self.headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
        }

    def download_image(self, url, number):
        print(number, ":", url)
        filename = str(number) + '.jpg'
        pathname = os.path.join(self.save_to, filename)
        resp = requests.get(url, headers=self.headers)
        with open(pathname, 'wb') as fw:
            fw.write(resp.content)
        with open("log.txt", 'a') as fw:# 创建日志
            fw.writelines("\n" + filename+"    "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


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
        # 进入预览界面
        time.sleep(2)
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
                print(e)
                with open("log.txt", 'a') as fw:  # 创建日志
                    fw.writelines("\n" + str(e) + ":n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                break
            if i%20 == 0:
                time.sleep(random.randrange(2, 4))

    def run(self, v):
        with open("log.txt", 'a') as fw:  # 创建日志
            fw.writelines("\n" + self.keywords + "获取开始！    " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            fw.close()
        self.enter_image_page()
        self.parse_link_and_download(v)
        with open("log.txt", 'a') as fw:  # 创建日志
            fw.writelines("\n" + self.keywords + "获取完成！    " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    spider1 = NailImageSpider('指甲')
    spider1.run(1000)
    spider2 = NailImageSpider('手指甲')
    spider2.run(1000)