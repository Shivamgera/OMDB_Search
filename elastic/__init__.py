from elasticsearch_dsl import connections, Index

from .elastic_index import MoviesIndex, indexing, ELASTIC_INDEX

connections.create_connection()

if not Index(ELASTIC_INDEX).exists():
    MoviesIndex.init()
    indexing()
    MoviesIndex._index.refresh()
