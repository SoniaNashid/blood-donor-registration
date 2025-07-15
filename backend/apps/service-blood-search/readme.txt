1. search-service/ 🔍
Handles donor search logic.

indexer/index_builder.py: Builds indexes of donor data, possibly including:

Blood type

Geo-coordinates

Last donation date

search/search_engine.py:

Implements filters (blood type, location).

Could use a simple in-memory index, or plug into a spatial DB or Elasticsearch.

✅ This is where matching algorithms and proximity search happen.
