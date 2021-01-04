from bs4 import BeautifulSoup
import requests
import re

ARCHIVE_BASE_URL = "https://twitcasting.tv/{}/movie/{}"

COMMENTS_BASE_URL = "https://twitcasting.tv/{}/moviecomment/{}"

DEFAULT_HEADER = {
    "accept-encoding": "gzip, deflate, br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "twitcasting.tv",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63",
    "Accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,en-GB;q=0.6,en-US;q=0.5",
}

class Archive:
    """
    This class defines a stream archive

    `url` is the webpage of archive like `https://twitcasting.tv/.../movie/...`
    """
    def __init__(self, url):
        params = re.match("(https?://)?twitcasting.tv/(.+)/movie/([0-9]+)", url)
        self.liver = params.group(2)
        self.id = params.group(3)
        self.encoding = "utf-8"
        self.option = {  # option of requests.get()
            "headers": DEFAULT_HEADER,
        }
        self._init_info()

    def _init_info(self):
        """
        Init the info of archive.
        """
        url = ARCHIVE_BASE_URL.format(self.liver, self.id)
        r = requests.get(url, self.option)
        r.encoding = self.encoding
        soup = BeautifulSoup(r.text, 'lxml')
        commentnum = int(soup.find(id="comment-list-app")["data-cnum"])
        self.commentnum = commentnum
        self.pages = int(self.commentnum / 20 + 0.5)
        duration = soup.find(class_="tw-player-duration-time").string.strip()
        self.duration = duration
        datetime = soup.find(class_="tw-player-meta__status").find("time").string.strip()
        self.datetime = datetime
        wrapper = soup.find("img", class_="liveimage")["src"]
        self.wrapper = "https://twitcasting.tv" + wrapper

    def get_comments(self, page):
        """
        Getting comments of one page. 
        
        This will return a list of comments, which each is a dict that has 3 keys: 
        
        `datetime`, `user`, `text`.
        """
        commentList = []
        url = COMMENTS_BASE_URL.format(self.liver, self.id) + "-" + str(page)
        r = requests.get(url, self.option)
        r.encoding = self.encoding
        soup = BeautifulSoup(r.text, 'lxml')
        comments = soup.find_all(class_= "tw-comment-history-item")
        if len(comments) == 0:
            return commentList
        for comment in comments:
            text = comment.find(class_="tw-comment-history-item__content__text").string.strip()
            datetime = comment.find("time").string.strip()
            user = comment.find(class_="tw-comment-history-item__details__user-link").string.strip()
            commentList.append({"datetime": datetime, "user": user, "text":text})
        return commentList
        