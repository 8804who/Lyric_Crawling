from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
import pandas as pd


def craw_lyrics():
    try:
        artist = driver.find_elements(By.CLASS_NAME, 'artist')
        song_name = driver.find_elements(By.CLASS_NAME, 'song_name')
        lyric = driver.find_elements(By.CLASS_NAME, 'lyric')
        driver.implicitly_wait(60)

        lyrics = lyric[0].text.split('\n')

        artists.append(artist[0].text)
        song_names.append(song_name[0].text)
        ly.append(lyrics)
    except:
        return


for year in range(2021, 2022):
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동

    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    try:
        driver = webdriver.Chrome('D:/공부/수업자료/4-2/USG공유대학/캡스톤디자인/pp/chromedriver.exe', options=option)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome('D:/공부/수업자료/4-2/USG공유대학/캡스톤디자인/pp/chromedriver.exe', options=option)
    driver.implicitly_wait(10)

    driver.get('https://www.melon.com/chart/age/index.htm?chartType=YE&chartGenre=KPOP&chartDate={y}'.format(y=year))
    time.sleep(2)
    song_num = []
    artists = []
    song_names = []
    ly = []

    lst50 = driver.find_elements(By.CSS_SELECTOR, "#lst50 > td:nth-child(5) > div > button")
    lst100 = driver.find_elements(By.CSS_SELECTOR, "#lst100 > td:nth-child(5) > div > button")

    for i in lst50:
        song_num.append(i.get_attribute('data-song-no'))

    for i in lst100:
        song_num.append(i.get_attribute('data-song-no'))

    for i in song_num:
        driver.get('https://www.melon.com/song/detail.htm?songId={song_num}'.format(song_num=i))
        craw_lyrics()

    df = pd.DataFrame(artists, columns=['artist'])
    df['song_name'] = song_names
    df['lyric'] = ly

    df.to_csv("song{y}.csv".format(y=year), index=False, encoding='utf-8')
