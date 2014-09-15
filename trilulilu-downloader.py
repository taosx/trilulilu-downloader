#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Python Trilulilu Downloader
Support for Video and Audio
Support for online view
Author: sharkyz of rstforums.com
'''

import re
from requests_futures .sessions import  FuturesSession
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import time
import lxml
import sys #, os



url = 'http://www.trilulilu.ro/pisica-asta-chiar-isi-doreste-sa-vorbeasca'

class commands(object):
    def __init__(self, httpadress):
        self.httpadress = httpadress
        

    #@profile # Used for profiling the app line by line // Ignore
    def main_function(self):  # Acess, Find, Rewrite, Download
        session = FuturesSession(executor=ThreadPoolExecutor(max_workers=16))
        page = session.get(self.httpadress)
        page_result = page.result()
        page_result.encoding = 'utf-8'
        soup = BeautifulSoup(page_result.text, 'lxml')
        locatescript = soup.find(text=re.compile('swfobject.embedSWF'))
        keys = re.findall(r'"([^,]*?)":', locatescript)
        values = re.findall(r'(?<=:)(?:"(.*?)"|\d+)', locatescript)
        vovu = dict(zip(keys, values))

        video_test = {'videosrc_0':'http://fs{servers}.trilulilu.ro/stream.php?type=video&'
                     'source=site&hash={hashs}&username={userids}&key={keys}'
                     '&format=flv-vp6&sig=&exp='.format(servers=vovu['server'],
                                                         hashs=vovu['hash'],
                                                         userids=vovu['userid'],
                                                         keys=vovu['key']),
                     'videosrc_1':'http://fs{servers}.trilulilu.ro/stream.php?type=video&'
                     'source=site&hash={hashs}&username={userids}&key={keys}'
                     '&format=mp4-360p&sig=&exp='.format(servers=vovu['server'],
                                                         hashs=vovu['hash'],
                                                         userids=vovu['userid'],
                                                         keys=vovu['key'])}


        # Name the file
        page_title = soup.title.string # Title of trilulilu page
        title_chooser = page_title.split(' - ') # Split the title wherever '-' and create a list with elements


        # Search for the right file to download & Download it
        for link in video_test:
            respond = session.get(video_test[link], stream=True)
            file_size = int(respond.result().headers.get('Content-Length', 0))
            if file_size > 1048576:
                # Check if the link was the mp4 or the flv format and choose name
                if 'mp4' in video_test[link]:
                    local_name_file = '{} - {}.mp4'.format(title_chooser[0],title_chooser[1])
                elif 'flv' in video_test[link]:
                    local_name_file = '{} - {}.flv'.format(title_chooser[0],title_chooser[1])
                else:
                    print('Download stopped, not recognizable format!')

               

                with open(local_name_file, 'wb') as f:
                    dl = 0
                    count = 0
                    start_time_local = time.mktime(time.localtime())


                    # Writing file
                    for chunk in respond.result().iter_content(chunk_size=32 * 1024):
                        if chunk:
                            count += 1
                            dl += len(chunk)
                            f.write(chunk)
                            end_time_local = time.mktime(time.localtime())
                            f.flush()


                        #Configuring Progressbar
                        if end_time_local > start_time_local:
                            dl_speed = round((dl / (end_time_local - start_time_local)) / 1000, 2)
                            sys.stdout.flush()
                            #print('Downloading now...\nFile:{}\nSize:{}M'.format(local_name_file, round(file_size / 1000/ 1000, 2)))
                            percent_text = round(dl * 100 / file_size)
                            percent_text4 = round(percent_text/4)
                            #print(percent_text4)
                            #teleies1='.' * x
                            #asterisks1='*' * int(i/2)
                            i = round(percent_text4)
                            x = 12 - i
                            z = 25 - i



                            def asterisks0():
                                if percent_text <= 50:
                                    return '#' * int(i)
                                else:
                                    return '#' * 12
                            def teleies0():
                                if percent_text < 10:
                                    return '-' * int(x + 1)
                                elif percent_text <= 50:
                                    return '-' * int(x)
                                else:
                                    return ''
                            def asterisks1():
                                if percent_text > 50:
                                    str_asterisk1 = '#' * (i - 12)
                                    return '#' * (i - 12)
                                else:
                                    return ''
                            def teleies1():
                                if percent_text > 50:
                                    return '-' * z
                                else:
                                    return '-' * 12


                           # Progressbar printing
                            sys.stdout.write('[{}{}{}%{}{}] [ Speed: {}Kbps ]         \r'.format(asterisks0(),teleies0(),percent_text,asterisks1(),teleies1(),dl_speed))
                            sys.stdout.flush()



start = commands(url).main_function()
start


