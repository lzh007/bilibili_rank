import requests
from bs4 import BeautifulSoup
import csv
import datetime

#B站排行榜
url = 'https://www.bilibili.com/v/popular/rank/all'
#发起网络请求
respones = requests.get(url)
#请求返回码  200 代表成功
code = respones.status_code
html_text = respones.text
#对 HTML 解析
soup = BeautifulSoup(html_text,"html.parser")

#对象
class Video:
    def __init__(self, title, score, rank, visit, up_name, up_id, video_url):
        self.title = title
        self.score = score
        self.rank = rank
        self.visit = visit
        self.up_name = up_name
        self.up_id = up_id
        self.video_url = video_url

    def to_csv(self):
        return [ self.title, self.score, self.rank, self.visit, self.up_name, self.up_id, self.video_url]

    #静态方法
    @staticmethod
    def csv_title():
        return ['标题', '分数', '排名', '播放量', '阿婆主名字', '阿婆主ID', '视频地址']

#提取列表
items = soup.find_all('li',{'class':'rank-item'})
#对象列表
videos = []

for item in items:
    #标题
    title = item.find('a',{'class':'title'}).text
    #综合得分
    score = item.find('div',{'class':'pts'}).find('div').text
    #排名
    rank = item.find('div',{'class':'num'}).text
    #播放量
    visit = item.find('span',{'class':'data-box'}).text
    #UP主名字
    up_name = item.find('span',{'class':'data-box up-name'}).text
    #UP主Id
    space = item.find_all('a',{'target':'_blank'})[2].get('href')
    up_id = space[len('//space.bilibili.com/'):]
    # 视频url
    video_url = item.find('a', {'class': 'title'}).get('href')
    #构造对象
    v = Video(title, score, rank, visit, up_name, up_id, video_url)
    videos.append(v)

#时间
now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
#文件名
file_name = f'bilibili_top100_{now_str}.csv'
#打开一个文件 取名 f，向里面 （w）写
with open(file_name, 'w', newline='') as f:
    #创建一个往 CSV 写数据的源
    writer = csv.writer(f)
    writer.writerow(Video.csv_title())
    for v in videos:
        writer.writerow(v.to_csv())