# from django_elasticsearch_dsl import Document, Index, fields, Completion
# from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, Search, token_filter, Text, Keyword,Date, Integer, Float, Document, Completion
from itertools import permutations
import pickle
# MOVIES_INDEX = Index('test_movies')
# MOVIES_INDEX.settings(
#     number_of_shards=1,
#     number_of_replicas=0,
# )
ascii_fold = analyzer(
    'ascii_fold',
    # we don't want to split O'Brian or Toulouse-Lautrec
    tokenizer='whitespace',
    filter=[
        'lowercase',
         token_filter('ascii_fold', 'asciifolding')
    ]
)
S_index = 'index-shivam'
class MoviesAutoIndex(Document):
    title = Text(fields={'keyword': Keyword()})
    created = Date()
    year = Integer()
    rating = Float()
    genre = Text()
    suggest = Completion(analyzer=ascii_fold)
    def clean(self):
        self.suggest = {
            # 'input': [' '.join(p) for p in permutations(self.title.split())],
            # 'input': [' '.join(p) for p in permutations(["the","batman"])],
            # 'input': [''.join(p) for p in self.title.split(" ")],
            # i = self.title
            'input': [self.title[:j] for j in range(len(self.title),1,-1)],
        }
    class Index:
        name = S_index
        settings = {'number_of_shards':1,
                    'number_of_replicas':0}


def indexing_s():
    dbfile = open('search/temp_data_dir/movies.pkl','rb')
    db = pickle.load(dbfile)
    for i in db[124:]:
        if i['imdbRating']!='N/A':
            MoviesAutoIndex(title=i['Title'],year=i['Year'],rating=i['imdbRating'],genre=i['Genre']).save()
            
        else:
            MoviesAutoIndex(title=i['Title'],year=i['Year'],rating=0.1,genre=i['Genre']).save()




