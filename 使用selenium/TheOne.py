"""
使用selenium自动化实现对boss直聘岗位信息的获取
"""

from selenium import webdriver
import time, csv
from selenium.webdriver.common.by import By

# boss直聘网址
url = "https://www.zhipin.com/web/geek/job?query=&city=100010000"


def scripy_One(url, value, csv_writer):
    # 进行获取
    driver = webdriver.Chrome()
    driver.get(url=url)
    time.sleep(5)

    # 向搜索框发送岗位名称，模拟点击
    driver.find_element(By.XPATH, '//input[@autocomplete="on"]').send_keys(value)
    driver.find_element(By.XPATH, '//a[@ka="job_search_btn_click"]').click()
    time.sleep(5)

    # boss直聘的展示界面为 10页，每页30条
    for i in range(10):
        scripy_Two(driver, csv_writer)

    driver.quit()


def scripy_Two(driver, csv_writer):
    # 获取当前页面的数据
    lists = driver.find_elements(By.XPATH, '//li[@class="job-card-wrapper"]')
    for li in lists:
        info_li = li.text.split("\n")
        # 写入csv文件
        csv_writer.writerow(
            [info_li[0], info_li[1], info_li[2], info_li[3], info_li[4], info_li[5], info_li[6], info_li[7],
             info_li[8:]])
        # 写入数据库使用
        # item = {}
        # item['title'] = info_li[0]
        # item['address'] = info_li[1]
        # item['wages'] = info_li[2]
        # item['experience'] = info_li[3]
        # item['education'] = info_li[4]
        # item['Recruiters'] = info_li[5]
        # item['corporate name'] = info_li[6]
        # item['company size'] = info_li[7]
        # item['Job description'] = info_li[8:]

    # 模拟点击下一页
    driver.find_element(By.XPATH, '//i[@class="ui-icon-arrow-right"]').click()
    time.sleep(10)


if __name__ == '__main__':
    # 向搜索栏发送的数据
    gjzs = [
        "计算机", "python开发", "Java开发", "大数据开发", "前端", "测试", "运维", "C++，", ".net开发",
        "嵌入式", "UI设计", "网络工PHP", "Golang", "Android开发", "CAD设计", "ETL工程师", "GIS工程师"
    ]

    # 保存文件

    file = open('./data.csv', 'a+', encoding="utf-8", newline="")  # 当前目录下
    csv_writer = csv.writer(file)
    csv_writer.writerow(
        ['标题', '地址', '薪资', '经验要求', '学历要求', '招聘人员', '招聘企业', '企业规模', '补充信息'])  # 列头

    for str in gjzs:
        scripy_One(url, str, csv_writer)

    file.close()
