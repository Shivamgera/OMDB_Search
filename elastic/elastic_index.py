import pickle
from datetime import datetime

from elasticsearch_dsl import connections, Document, Completion, Text, Integer, Float, Keyword, analyzer, tokenizer, \
    Date, Index

ELASTIC_INDEX = 'movies-suggestions'
custom_analyzer = analyzer(
    'my_analyzer',
    tokenizer=tokenizer('bigram', 'nGram', min_gram=2, max_gram=2),
    filter=['lowercase']
)


class MoviesIndex(Document):
    # title = Text(fields={'keyword': Keyword()})
    title = Text()
    rating = Float()
    year = Integer()
    genre = Text()
    suggest = Completion(analyzer=custom_analyzer)
    created = Date()

    def clean(self):
        self.suggest = {
            'input': self.title.split(),
            'weight': round(self.rating)
        }

    class Index:
        name = ELASTIC_INDEX
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }


def indexing():
    data = pickle.load(open(r'C:\Users\Student\PycharmProjects\TapChief\OMDB_Search\search\temp_data_dir\movies.pkl', 'rb'))
    for i in data:
        if i['imdbRating'].startswith('N'):
            MoviesIndex(title=i['Title'], rating=0.1, genre=i['Genre'], year=int(i['Year']), created=datetime.now()).save()
        else:
            MoviesIndex(title=i['Title'], rating=float(i['imdbRating']), genre=i['Genre'],
                   year=int(i['Year']), created=datetime.now()).save()

