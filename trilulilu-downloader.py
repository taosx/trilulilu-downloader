'''
Python Trilulilu Downloader
Support for Video and Audio
Support for online view
Author: sharkyz of rstforums.com
'''

import re
from multiprocessing.pool import ThreadPool as Pool
import pyprind
import requests
import bs4


url = 'http://www.trilulilu.ro/bate-palma-cu-pisica-d'


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
                print('Downloading now...\nFile:{}\nSize:{}M'.format(local_name_file, round(file_size / 1000/ 1000, 2)))
                # Progress Bar
                bar = pyprind.ProgBar(file_size / 1024, monitor=True)
                file_downloaded_size = 0
                with open(local_name_file, 'wb') as f:
                    for chunk in respond.iter_content(chunk_size=1024):
                        if chunk:
                            file_downloaded_size += 1024
                            f.write(chunk)
                            f.flush()
                            bar.update()
                    print()
                    print(bar)





start = commands(url).main_function()
start


"""
        if __name__ == "__main__":
            if len(sys.argv) == 1:
                url = input('URL: ')
                start = commands(url)
                start.main_function()
                #start.dlfile(start.afrp())
            elif len(sys.argv) == 2:
                url = sys.argv[1]
                start = commands(url)
                start.afrp()
            else:
                print('Please try again, you\'re drunk!')

"""