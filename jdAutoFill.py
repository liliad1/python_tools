# coding=utf-8

import time
import os

import docx
from selenium import webdriver


DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
# 创建可见的Chrome浏览器， 方便调试
driver = webdriver.Chrome()
# 创建Chrome的无头浏览器
# opt = webdriver.ChromeOptions()
# opt.set_headless()
# driver = webdriver.Chrome(options=opt)
driver.implicitly_wait(10)

driver.get("https://dr.jd.com/page/login.html")
driver.switch_to.frame('login_frame')
driver.find_element_by_id('loginname').send_keys('19969324972')
driver.find_element_by_id('nloginpwd').send_keys('wq235680')
driver.find_element_by_id('paipaiLoginSubmit').click()
for fpathe, dirs, fs in os.walk(DATA_PATH):
    for f in dirs:
        file = os.path.join(fpathe, f) + '\\' + f + '.docx'
        doc = docx.Document(file)
        paragraphs = []
        for para in doc.paragraphs:
            paragraphs.append(para.text)
        driver.find_element_by_xpath("//*[text()='渠道投稿']").click()
        driver.find_element_by_xpath("//*[text()='文章']").click()
        handles = driver.window_handles
        driver.switch_to.window(handles[1])
        driver.find_element_by_xpath("//*[@id='ui-input']/input").send_keys(paragraphs[0])
        driver.find_element_by_xpath(
            "//*[@id='richtext-editor-box']/div[2]/div[2]/div/div/div/div/div/div/span").send_keys('\n'.join(paragraphs[1:]))
        driver.find_element_by_xpath(".//input[@value='保存草稿']").click()
        time.sleep(2)
        driver.close()
        driver.switch_to.window(handles[0])



# driver.find_element_by_xpath("//*[@id='module-image-cut']/div/div/div/div[2]/input").send_keys(r'D:\temp\data\Dior后台粉底液\O1CN01djooat2054bU9LgWE_!!737296797-0-beehive-scenes.jpg')
# time.sleep(1)
# driver.find_element_by_xpath(".//input[@value='上传']").click()
# time.sleep(1)
# driver.find_element_by_xpath("//*[@id='rte-cutupload-box']/input").send_keys(r'D:\temp\data\Dior后台粉底液\O1CN01DlM2dX2054bPXcl8L_!!737296797-0-beehive-scenes.jpg')
# time.sleep(1)
# driver.find_element_by_xpath(".//input[@value='上传']").click()
# time.sleep(1)
