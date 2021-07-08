import json
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


class Notices():
    def __init__(self, paginate_from=0):
        self.response = requests.get(
            f"https://bpatcsc.org/pages/notice/{paginate_from}",
            headers={'User-Agent': 'Mozilla/5.0'}
        )

    def format_notices(self, raw):
        raw = str(raw)
        link = raw[raw.find('href="')+6:raw.find('">')]
        content = raw[raw.find('">')+2:raw.find('</a>')]
        raw_date = raw[raw.find('</a> - ')+7:raw.find('</li>')]
        date_object = datetime.strptime(raw_date, '%d/%m/%Y')
        posted_on = f"{date_object.day} {date_object.strftime('%B')}, {date_object.year}"

        return json.dumps({
            "content": content,
            "link": link,
            "posted_on": posted_on
        }, ensure_ascii=True)

    def fetch(self):
        notices = []

        try:
            if self.response.ok is True:
                parse = bs(self.response.text, 'html.parser')
                notices_raw_list = parse.find(
                    "div", {"class": "col-lg-9 col-md-9 col-sm-12 col-xs-12"}
                ).find('ul').find_all('li')

                for notice in notices_raw_list:
                    notices.append(self.format_notices(notice))

            else:
                return f"[Error {resp.status_code}] Couldn't fetch notices"

        except Exception as error:
            print(f"[ERROR] {error}")

            return None

        return notices if notices else None

    def __call__(self):
        return self.fetch()