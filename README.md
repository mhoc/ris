# RIS: A Reddit Image Scraper

That's... pretty much what it is. Nothing that fancy.

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python scraper.py -h
python scraper.py earthporn
```

By default (or `--organize title`) this will create a folder tree that looks like

```
--dest
  |-> earthporn
      |-> (title)
          |-> (images).jpg
```

You can modify this a bit with `--organize author`

```
--dest
  |-> earthporn
      |-> (author)
          |-> (title)
              |-> (images).jpg
```

There are some flag options you can pass it. See `python scraper.py -h`.

`--limit` allows you to set how many reddit posts to scan. This is passed directly to the reddit api.

`--dest` allows you to set the parent folder where images are downloaded.

`--listing [hot, new]` which listing to use from reddit.

# Concerns

The main one is that if the exact same title appears in a subreddit twice, the images this downloads will be put in the same folder. I don't personally have a problem with this because if the purpose of a title is to "label" what an image should be then it kind of makes sense that similar images should be in the same directory. But the situation is pretty rare anyway. It definitely shouldn't crash, at least.

# Known Issues

See github issues.
