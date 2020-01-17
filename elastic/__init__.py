from elasticsearch_dsl import connections, Index
from elasticsearch import Elasticsearch

from .elastic_index import MoviesIndex, indexing, ELASTIC_INDEX
import re
from .elastic_index_s import MoviesAutoIndex, S_index, indexing_s



bonsai = "https://h4qrprc9p:7igk580k6e@search-app-9843249466.ap-southeast-2.bonsaisearch.net:443"
auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

# optional port
match = re.search('(:\d+)', host)
if match:
  p = match.group(0)
  host = host.replace(p, '')
  port = int(p.split(':')[1])
else:
  port=443

# Connect to cluster over SSL using auth for best security:
# es_header = [{
#  'host': host,
#  'port': port,
#  'use_ssl': True,
#  'http_auth': (auth[0],auth[1])
# }]

# Instantiate the new Elasticsearch connection:
# connections.create_connection('default',
#     hosts=['https://search-app-9843249466.ap-southeast-2.bonsaisearch.net/'],
#     http_auth=('h4qrprc9p','7igk580k6e'),
#     timeout=60,
# )



# if not Index(ELASTIC_INDEX).exists():
#     MoviesIndex.init()
#     indexing()
#     MoviesIndex._index.refresh()
# if not Index('index-shivam').exists():
#     MoviesAutoIndex.init()
# indexing_s()
# MoviesAutoIndex._index.refresh()