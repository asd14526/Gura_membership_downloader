# -*- coding:utf-8 -*-
import os
import time
import requests
import re
from http import cookiejar
from bs4 import BeautifulSoup


def run():
    # 取得cookie然後用以下網址裡面的curl指令做成cookiejar.txt
    # https://www.alexleo.click/%E7%AD%86%E8%A8%98%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8-youtube-dl-%E4%B8%8B%E8%BC%89-youtube-%E6%9C%83%E5%93%A1%E9%99%90%E5%AE%9A%E7%9A%84%E5%BD%B1%E7%89%87/
    cookie = cookiejar.MozillaCookieJar()
    cookie.load('cookiejar.txt', ignore_discard=True, ignore_expires=True)

    while True:
        # 取得Gawr Gura的Community頁面(需要cookie才會取得會員專屬的內容)
        resp = requests.get('https://www.youtube.com/channel/UCoSrY_IQQVpmIRZ9Xf-y93g/community',
                            cookies=cookie)
        soup = BeautifulSoup(resp.text, "html.parser")  # 使用BeautifulSoup擷取html內容
        # print(soup.prettify())  # 輸出排版後的HTML內容
        match = re.search('"\/watch\?v=(.*?)"', resp.text)  # 找到關鍵的那一個網址
        message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 目前找到的影片網址為: ' + match[
            0]  # ""/watch?v=YlcnFHma6fQ""
        print_and_write_file(message)

        # 找到網址了，然後確認是存檔還是新的(用scheduledStartTime分)
        videoURL = 'https://youtube.com/watch?v=' + match[1]  # 組合成正確的網址
        resp2 = requests.get(videoURL, cookies=cookie)  # 取得直播的影片頁面
        match2 = re.search('"scheduledStartTime":"(.*?)"', resp2.text)  # 找到開始直播時間：   "scheduledStartTime":"1605960000"
        if match2 is not None:
            message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 是準備開始的直播呢~'
            print_and_write_file(message)
            # 只要和現在時間相減就知道要睡幾秒後再繼續
            sleep_time = int(match2[1]) - int(time.time())  # 1605960000 - 1605875568 = 84432
            if sleep_time > 0:
                message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(match2[1]))) + ' 才開始，晚安'  # 轉成字串
                print_and_write_file(message)
                time.sleep(sleep_time)  # 睡到直播開始

            # 還沒開始直播：	\"playabilityStatus\":{\"status\":\"LIVE_STREAM_OFFLINE\",\"reason\":\"這個現場直播將於 23 分鐘 後開始。\"
            # 等待開始直播：	\"playabilityStatus\":{\"status\":\"LIVE_STREAM_OFFLINE\",\"reason\":\"這場現場直播將於幾分鐘後開始。\"
            #               {\"scheduledStartTime\":\"1605841200\",\"mainText\":{\"runs\":[{\"text\":\"正在等待「\"},{\"text\":\"鹿乃 \/ Kano\"},{\"text\":\"」開始直播\"}]}
            # 正在直播：		\"playabilityStatus\":{\"status\":\"OK\"

            isStart = False
            while not isStart:
                resp3 = requests.get(videoURL, cookies=cookie)  # 取得直播的影片頁面 記得改回videoURL
                match3 = re.search('\"playabilityStatus\":{\"status\":\"(.*?)"', resp3.text)
                if match3[1] == 'OK':
                    message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 開始下載'
                    print_and_write_file(message)
                    # 以下方法需要使用cookie，並且用cmd執行
                    command = "H:\\Gura_membership_downloader\\youtube-dl.exe -o [%(upload_date)s]%(title)s.%(ext)s --cookies=cookiejar.txt -f best " + videoURL
                    print_and_write_file(command)
                    if os.system(command) == 0:
                        message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 下載完成，退出中...'
                        print_and_write_file(message)
                        isStart = True
                    else:
                        message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 3秒後重新下載...'
                        print_and_write_file(message)
                        time.sleep(3)  # 每3秒重下載
                else:
                    message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 10秒後再度測試...'
                    print_and_write_file(message)
                    time.sleep(10)  # 每10秒測試開台了沒

        else:
            message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 是存檔呢~半小時後見~\n'
            print_and_write_file(message)
            time.sleep(1800)  # 睡半小時


def print_and_write_file(message):
    print(message)
    f = open('history.log', 'a')
    print(message, file=f)
    f.close()


if __name__ == '__main__':
    message = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '] 開始執行此程式...'
    print_and_write_file(message)
    run()
