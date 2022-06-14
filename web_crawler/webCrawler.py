from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

url = "https://steamcommunity.com/app/292730/negativereviews/?browsefilter=toprated&snr=1_5_100010_&filterLanguage=tchinese" # 爬蟲目標網址
driver = webdriver.Chrome()
driver.get(url)
# 每隔3.5秒，頁面往下滑到底，手動更新steam評論頁面
for i in range(0, 2): # 要取幾筆就設定多少迴圈
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(3.5)
    print(i)

html_page = driver.page_source.encode('utf-8')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 獲取評論
reviews = soup.find_all('div', {'class': 'apphub_Card'})
file = open('steam.xlsx', 'w+', encoding='utf-8')
for review in reviews:
    # title = review.find('div', {'class': 'title'})
    comment = review.find('div', {'class': 'apphub_CardTextContent'})
    comment = comment.text.split('\n')[2].replace("\t", "")
    # file.write(
    #     comment + '\t' + title.text + '\n')

    file.write(comment + '\n')
file.close()
