pyCrawler
=========

Threaded python web crawler with MongoDB backend.

The file crawlerLinks.py grabs a random link from a given collection. It crawls for new http links and if they're unique it does a new insert into the collection.

The other file named crawlerMeta.py grabs a random link from a collection and extracts some meta data using Beautiful Soup 4. The meta data gets saved together with the crawled link. The number of threads used can easily be modified in the scripts.
