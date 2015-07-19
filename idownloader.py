#!/usr/bin/env python
'''
Donwload images
'''
import os
import os.path
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod

class BaseClass:
    __metaclass__ = ABCMeta

    @abstractmethod 
    def get_image_urls(self, url): pass


class Umei_cc(BaseClass):
    '''
    for www.umei.cc
    '''
    def get_image_urls(self, url):
        page_urls = self._get_page_urls(url)
        img_urls = []
        for p_url in page_urls:
            img_urls += self._get_image_urls(p_url)
        return img_urls

    def _get_page_urls(self, url):
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        img_pages = soup.findAll('div', {'class': 'pages'})[1]
        a = img_pages.findAll('a')[1:-1] # exclude next and previous buttons uri
        basenames = [i['href'] for i in a]

        uri_list = [url]
        uri_list += [os.path.join(os.path.dirname(url), b) for b in basenames]
        return uri_list
        
    def _get_image_urls(self, url):
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        img_show = soup.findAll('img', {'class': 'IMG_show'})
        img_urls = [i['src'] for i in img_show]
        return img_urls
    

def get_domain(url):
    return urllib.parse.urlparse(url).netloc

def download_file(url, out_dir):
    if not os.path.exists(out_dir):
        print('create %s directory' % out_dir)
        os.makedirs(out_dir)

    basename = os.path.basename(url)
    out_path = os.path.join(out_dir, basename)

    print('download %s' % url, end="")
    urllib.request.urlretrieve(url, out_path)
    print(' -> done!')

def download_files(urls, out_dir):
    for url in urls:
        download_file(url, out_dir)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Donwload iamges')
    parser.add_argument('url', nargs='+')
    parser.add_argument('-o', '--output_dir', default='.')
    args = parser.parse_args()

    for url in args.url:
        if get_domain(url) == 'www.umei.cc':
            site = Umei_cc()
            
        img_urls = site.get_image_urls(url)

        basename = os.path.basename(url)
        name, ext = os.path.splitext(basename)
        out_dir = os.path.join(args.output_dir, name)

        download_files(img_urls, out_dir)
