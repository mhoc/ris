# RIS: A Reddit Image Scraper

That's... pretty much what it is. Nothing that fancy.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python scraper.py -h
python scraper.py earthporn
```

This will create a folder tree that looks like

```
reddit-scraper
|-> images
    |-> earthporn
        |-> (author OR title) # see --organize
            |-> (singleimages).jpg
            |-> (albumid)
                |-> (singleimages).jpg
```

There are some flag options you can pass it. See `python scraper.py -h`.

`--limit` allows you to set how many reddit posts to scan. This is passed directly to the reddit api.

`--dest` allows you to set the parent folder where images are downloaded.

`--organize [author,title]` changes how posts are organized. Note that any posts in the same subreddit by the same author will be combined under the author's folder. And likewise, any posts in the same subreddit with the exact same title will be combined. Which... IMO is kind of helpful, right? It should never overwrite images, because the images are stored under the same name as imgur gave them.

# Known Issues

See github issues. There are some.
