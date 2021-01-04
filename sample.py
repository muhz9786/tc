from time import sleep
from tqdm import tqdm
import tc

base_url = "https://twitcasting.tv/kaguramea_vov/movie/"
id_list = [
    "565930810",
    "556218506",
]

for aid in id_list:
    url = base_url + aid
    archive = tc.Archive(url)

    print(archive.datetime)  # datetime of stream start
    print(archive.duration)  # duration of stream
    print(archive.commentnum)  # comment number
    print(archive.wrapper)  # wrapper's url of stream

    with open("./{}.txt".format(archive.id), "a", encoding="utf-8") as f:
        # You can use "pages" to get every page of comments, or several pages you need.
        # But for an old archive, there were only later 5000(250p) comments had be retained.
        for page in tqdm(range(archive.pages)):
            comments = archive.get_comments(page)
            for comment in comments:
                time = comment["datetime"]  # datetime of comment
                user = comment["user"]  # id of user
                text = comment["text"]  # content text
                f.write("[{}]{}: {}".format(time, user, text))
                sleep(0.3)
