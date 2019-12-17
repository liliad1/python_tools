# coding=utf-8

import time

from selenium import webdriver


class DarenSpider(object):

    # 创建可见的Chrome浏览器， 方便调试
    driver = webdriver.Chrome()

    # 创建Chrome的无头浏览器
    # opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # driver = webdriver.Chrome(options=opt)

    driver.implicitly_wait(10)

    total = 1526  # 预先计算的总数据量
    count = 0  # 已爬取的数据量

    # 记录解析以及翻页位置
    location = 0
    click_times = 0

    def run(self):
        """
        开始爬虫
        :return:
        """
        # get方式打开网页
        self.driver.get("https://m.tb.cn/h.ey6Vxn0?sm=29ae31")
        self.driver.find_element_by_xpath("//span[text()='帖子']").click()

        self.parselist()
    #
    #     while self.count < self.total:
    #         if self.click_times == 2:
    #
    #             self.driver.find_element_by_css_selector('#subShowContent1_page > span:nth-child(6) > a').click()
    #
    #             # 等待页面加载完成
    #             time.sleep(5)
    #             self.click_times = 0
    #             self.location = 0
    #         else:
    #             self.driver.find_element_by_css_selector('#subShowContent1_loadMore').click()
    #
    #             # 等待页面加载完成
    #             time.sleep(3)
    #             self.click_times += 1
    #
    #         # 分析加载的新内容，从location开始
    #         self.parselist()
    #
    #     self.driver.quit()
    #
    def parselist(self):
        """
        解析列表
        :return:
        """
        divs = self.driver.find_elements_by_xpath(".//span[@class = 'rax-text  rax-text--overflow-hidden rax-text--multiline' and text() != '']")
        # divs[0].click()
        time.sleep(5)

        # for i in range(self.location, len(divs)):
        #     link = divs[i].find_element_by_tag_name('a').get_attribute("href")
        #     print(link)
        #
        #     self.location += 1
        #     self.count += 1
        # print(self.count)


if __name__ == '__main__':
    spider = DarenSpider()
    spider.run()
