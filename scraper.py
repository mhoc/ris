
import argparse
import os
import os.path
import requests
import shutil

# This aint a secret key. Its the client ID registered to this application.
# Go ahead and use it or make your own.
# Imgur is stupid for requiring a registered application just to convert a
# public album Id to a list of image URLs
IMGUR_CLIENT_ID = "f450cf45844671a"

class Arguments():

    def get(self):
        parser = argparse.ArgumentParser(
            description='Scrape and download images from reddit.'
        )
        parser.add_argument('subreddit',
            metavar='subreddit',
            help='subreddit name to scrape (earthporn)'
        )
        parser.add_argument('--limit',
            dest='limit',
            default=20,
            metavar='L',
            type=int,
            help='limit the number of results to the top N (default: 20)'
        )
        parser.add_argument('--listing',
            dest='listing',
            default='hot',
            metavar='L',
            choices=['hot', 'new'],
            help='the listing type you want to scrape. either \'hot\' or \'new\' (default: hot)'
        )
        parser.add_argument('--organize',
            dest='org',
            default='title',
            metavar='TYPE',
            choices=['author', 'title'],
            help='how to name the folder which contains the images and albums; either by title of the post or author of the post'
        )
        parser.add_argument('--dest',
            dest='dest',
            default='./images',
            metavar='D',
            help='the folder where the images will be downloaded (default: ./images)'
        )
        return parser.parse_args()

args = Arguments().get()
subr, limit, listing, org, dest = args.subreddit, args.limit, args.listing, args.org, args.dest

class PostHandler():

    allowed_chars = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm "

    def __init__(self, post):
        self.url = post["url"]
        self.title = ''.join(c for c in post["title"] if c in self.allowed_chars)[:40]
        if self.title[-1] == " ":
            self.title = self.title[:-1]
        self.author = ''.join(c for c in post["author"] if c in self.allowed_chars)
        if self.author[-1] == " ":
            self.author = self.author[:-1]

    def handle(self):
        path = self.create_path()
        if "imgur" in self.url:
            Imgur(self.url, path).get()
        else:
            print "Post type not supported"

    def create_path(self):
        if org == "author":
            return os.path.join(dest, subr, self.author, self.title)
        elif org == "title":
            return os.path.join(dest, subr, self.title)

class Imgur():

    def __init__(self, url, path):
        self.url = url
        self.path = path

    def get(self):
        if "gifv" in self.url:
            return
        if "imgur.com/a/" in self.url:
            return self.album()
        else:
            return self.single(self.url)

    def single(self, url):
        if "." not in url.split("/")[-1]:
            url += ".jpg"
        filename = url.split("/")[3]
        ImageDownloader(url, os.path.join(self.path, filename)).download()

    def album(self):
        album_id = self.url.split('/')[4]
        print "Processing album {}".format(album_id)
        imgur = 'https://api.imgur.com/3/album/' + album_id
        headers = { 'Authorization': 'Client-Id ' + IMGUR_CLIENT_ID }
        resp = requests.get(imgur, headers=headers).json()
        urls = [ image['link'] for image in resp['data']['images'] ]
        for url in urls:
            self.single(url)

class ImageDownloader():

    def __init__(self, url, path):
        self.url = url
        self.path = path

    def download(self):
        print "Downloading {}".format(self.path)
        if os.path.exists(self.path):
            return
        self.create_path()
        resp = requests.get(self.url, stream=True)
        resp.raw.decode_content = True
        with open(self.path, "w+") as f:
            shutil.copyfileobj(resp.raw, f)

    def create_path(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

def get_subr_listing(subreddit, listing, limit):
    url = 'http://www.reddit.com/r/{}/{}.json?limit={}'.format(subreddit, listing, limit)
    headers = {'user-agent': 'reddit-scraper:0.0.1 (by /u/mike_hman)'}
    response = requests.get(url, headers=headers)
    return [ post["data"] for post in response.json()["data"]["children"] ]

listing = get_subr_listing(subr, listing, limit)
for post in listing:
    PostHandler(post).handle()
