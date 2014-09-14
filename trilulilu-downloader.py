'''
Python Trilulilu Downloader
Support for Video and Audio
Support for online view
Author: sharkyz of rstforums.com
'''

import re
from multiprocessing.pool import ThreadPool as Pool
import requests
import bs4
import time
import curses
import sys #, os

#Terminal remaker
stdscr = curses.initscr()
curses.start_color()

url = 'http://www.trilulilu.ro/video-film/pitbull-ay-chico-lengua-afuera-1'

class commands(object):
    def __init__(self, httpadress):
        self.httpadress = httpadress

    def main_function(self):  # Acess, Find, Rewrite, Download
        pool = Pool(2)
        page = requests.get(self.httpadress)
        soup = bs4.BeautifulSoup(page.text, 'lxml')
        locatescript = soup.find(text=re.compile('swfobject.embedSWF'))
        keys = re.findall(r'"([^,]*?)":', locatescript)
        values = re.findall(r'(?<=:)(?:"(.*?)"|\d+)', locatescript)
        vovu = dict(zip(keys, values))

        video_test = ['http://fs{servers}.trilulilu.ro/stream.php?type=video&'
                     'source=site&hash={hashs}&username={userids}&key={keys}'
                     '&format=flv-vp6&sig=&exp='.format(servers=vovu['server'],
                                                         hashs=vovu['hash'],
                                                         userids=vovu['userid'],
                                                         keys=vovu['key']),
                     'http://fs{servers}.trilulilu.ro/stream.php?type=video&'
                     'source=site&hash={hashs}&username={userids}&key={keys}'
                     '&format=mp4-360p&sig=&exp='.format(servers=vovu['server'],
                                                         hashs=vovu['hash'],
                                                         userids=vovu['userid'],
                                                         keys=vovu['key'])]


        # Name the file
        page_title = soup.title.string # Title of trilulilu page
        title_chooser = page_title.split(' - ') # Split the title wherever '-' and create a list with elements


        # Search for the right link to download
        for link in video_test:
            respond = requests.get(link, stream=True)
            file_size = int(respond.headers.get('Content-Length', 0))
            if file_size > 1048576:
                # Check if the link was the mp4 or the flv format and choose name
                if 'mp4' in link:
                    local_name_file = '{} - {}.mp4'.format(title_chooser[0],title_chooser[1])
                elif 'flv' in link:
                    local_name_file = '{} - {}.flv'.format(title_chooser[0],title_chooser[1])
                else:
                    print('Download stopped, not recognizable format!')
                stdscr.addstr(0, 0,'Downloading now...\nFile:{}\nSize:{}M'.format(local_name_file, round(file_size / 1000/ 1000, 2)))

                file_downloaded_size = 0
                with open(local_name_file, 'wb') as f:
                    dl = 0
                    count = 0
                    start_time_local = time.mktime(time.localtime())
                    # Progress
                    for chunk in respond.iter_content(chunk_size=1024):
                        if chunk:
                            count += 1
                            dl += len(chunk)
                            f.write(chunk)
                            end_time_local = time.mktime(time.localtime())
                            f.flush()
                        if end_time_local > start_time_local:
                            dl_speed_raw = dl / (end_time_local - start_time_local)
                            stdscr.addstr(3, 0,'|{}|'.format('=' * 49))
                            percent_text = dl * 100 / file_size

                            for i in range(round(percent_text/2)):
                                x = 49 - i
                                stdscr.addstr(4, 0,'|{}{}|'.format('#' * i, '-' * x))

                            # Format of completed (perfection)

                            if len(str(round(percent_text))) == 1:
                                stdscr.addstr(5, 0,'|{es}{cd}{ee}|'.format(es=('=' * 17),cd=(' {:.0f}% completed  '.format(percent_text)),ee =('=' * 17)))
                            elif len(str(round(percent_text))) == 3:
                                stdscr.addstr(5, 0,'|{es}{cd}{ee}|'.format(es=('=' * 17),cd=(' {:.0f}% completed '.format(percent_text)),ee =('=' * 16)))
                            else:
                                stdscr.addstr(5, 0,'|{es}{cd}{ee}|'.format(es=('=' * 17),cd=(' {:.0f}% completed '.format(percent_text)),ee =('=' * 17)))

                            stdscr.addstr(6, 0,'Download Speed: {:.2f}Kbps \r'.format(dl_speed_raw / 1000))
                            stdscr.refresh()

# print('|{}|'.format('=' * 49))
# print('|#')
# print('|{es}{cd}{ee}|'.format(es=('=' * 17),cd=(' {}% completed '.format('30')),ee =('=' * 17)))

# 5000 / 100 = 50 *


start = commands(url).main_function()
start


