import urllib.request
from urllib.error import URLError
from html.parser import HTMLParser
import datetime
import json
import time

class money_finder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.status = 0;

    def handle_starttag(self, tag, attrs):
        etalon = ('class', 'bold counter-now')
        if self.status == 0 and tag == "span":
            for attr in attrs:
                if attr == etalon:
                    self.status = 1

    def handle_endtag(self, tag):
        if self.status == 1:
            self.status = 2

    def handle_data(self, data):
        if self.status == 1:
            self.result = data

    def get_result(self):
        return self.result

def get_current_amount():
    repeat = True
    req = urllib.request.Request('http://28panfilovcev.com/index.php')
    
    while repeat:
        try:
            response = urllib.request.urlopen(req)
            the_page = response.read().decode('utf-8')
            repeat = False
        except URLError as error:
            time.sleep(5)
    
    money_parser = money_finder()
    money_parser.feed(the_page)
    amount = money_parser.get_result().replace(' ', '')

    current_datetime = datetime.datetime.isoformat(datetime.datetime.now())
    
    money_trace_data = open('/home/ramamba/Documents/28trace.json', 'a', encoding='utf-8')
    line = json.dumps({'datetime': current_datetime, 'amount': amount})
    money_trace_data.write(line + "\n")

if __name__ == "__main__":
    # execute only if run as a script
    get_current_amount()