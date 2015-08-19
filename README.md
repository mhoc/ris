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
reddit-scraper
|-> images
    |-> earthporn
        |-> (title)
            |-> (images).jpg
```

You can modify this a bit with `--organize author`

```
reddit-scraper
|-> images
    |-> earthporn
        |-> (author)
            |-> (title)
                |-> (images).jpg
```

There are some flag options you can pass it. See `python scraper.py -h`.

`--limit` allows you to set how many reddit posts to scan. This is passed directly to the reddit api.

`--dest` allows you to set the parent folder where images are downloaded.

`--listing [hot, new]` which listing to use from reddit.

# Known Issues

See github issues.
