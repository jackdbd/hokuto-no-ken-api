# Hokuto no Ken API

TODO

:warning: :construction_worker: WORK IN PROGRESS :building_construction: :construction:


## TODO: write brief description and instructions

Create the database updated to the latest revision. Run this command from the repository root directory (not from the `app` directory)

```shell
flask db upgrade
```

Populate the database by scraping the data from [Hokuto Renkitōza](http://hokuto.wikia.com/wiki/Main_Page). The spider will scrape all the Hokuto no Ken characters that have a wiki page, then an [Item Pipeline](https://doc.scrapy.org/en/latest/topics/item-pipeline.html) will populate all the tables.
