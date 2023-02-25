from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen


def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")

    cookies = {
        '_ga': 'GA1.2.1429312257.1677318021',
        '_gid': 'GA1.2.378579401.1677318021',
        '_gat_UA-3524196-6': '1',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.2.1429312257.1677318021; _gid=GA1.2.378579401.1677318021; _gat_UA-3524196-6=1',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'OGVMYXE1',
    }

    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    # Feel free to change the download directory
    with open(f"videos/bluberrythebun/{id}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break


print("STEP 1: Open Chrome browser")
driver = webdriver.Chrome()
# Change the tiktok link
driver.get("https://www.tiktok.com/@bluberrythebun")

# IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
# to 60 seconds, just enough time for you to complete the captcha yourself.
time.sleep(10)

scroll_pause_time = 10
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if (screen_height) * i > scroll_height:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")
# this class may change, so make sure to inspect the page and find the correct class
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

print(f"STEP 3: Time to download {len(videos)} videos")
for index, video in enumerate(videos):
    print(f"Downloading video: {index}")
    try:
        downloadVideo(video.a["href"], index)
    except Exception as ex:
        print("Error", ex)
        time.sleep(20)
        continue
    time.sleep(10)
