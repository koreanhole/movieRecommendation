import requests
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval



#데이터 읽어오는 부분.
movies = pd.read_csv('data/tmdb_5000_movies.csv')
id_map = pd.read_csv('data/links_small.csv')
ratings = pd.read_csv('data/ratings_small.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')
movies_metadata = pd.read_csv('data/movies_metadata.csv')

movie_index = pd.Series(movies.index, index=movies['title']).drop_duplicates()
movie_id = movies['id']

credits.columns = ['id','tittle','cast','crew']
movies = movies.merge(credits,on='id')

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
#imdb API key
KEY = '8e1ab3bb4d09b69e88b3f9431752a135'


def _get_json(url):
    r = requests.get(url)
    return r.json()

config = _get_json(CONFIG_PATTERN.format(key=KEY))
base_url = config['images']['base_url']
sizes = config['images']['poster_sizes']

# imdb의 movie id를 입력값으로 넣으면 imdb의 api를 통해 영화 포스터의 이미지 주소를 가져오는 함수
def get_poster_urls(imdbid):
    config = _get_json(CONFIG_PATTERN.format(key=KEY))
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']
    def size_str_to_int(x):
        return float("inf") if x == 'original' else int(x[1:])
    max_size = max(sizes, key=size_str_to_int)

    posters = _get_json(IMG_PATTERN.format(key=KEY,imdbid=imdbid))['posters']
    poster_urls = []
    for poster in posters:
        rel_path = poster['file_path']
        url = "{0}{1}{2}".format(base_url, max_size, rel_path)
        poster_urls.append(url)

    return poster_urls[0]

#데이터의 대문자를 제거 한 후 소문자로 대체해준다.
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''
#키워드, 주연배우, 감독, 장르데이터를 합쳐서 하나의 데이터로 만드는 함수.
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
#데이터를 입력받은 후 해당하는 영화의 감독 이름을 받아온다.
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #입력받은 리스트에서 첫 세개의 항목만 받아온다. 만약 세개보다 적을 경우 전체 항목을 반환한다.
        if len(names) > 3:
            names = names[:3]
        return names

    #잘못된 데이터가 있을 경우 빈 배열 반환.
    return []

#입력한 영화와 다른 영화간의 코사인 유사도를 계산한후 상위 15개 영화의 인덱스를 반환받는다.
def get_recommendations(title):

    #코사인 유사도를 구할 feature를 정한다.
    #주연배우, 제작진, 키워드, 장르.
    features = ['cast', 'crew', 'keywords', 'genres']
    for feature in features:
        movies[feature] = movies[feature].apply(literal_eval)

    #crew 데이터를 통해 감독의 이름(director)만 가져온다.
    movies['director'] = movies['crew'].apply(get_director)
    features = ['cast', 'keywords', 'genres']
    for feature in features:
        movies[feature] = movies[feature].apply(get_list)

    features = ['cast', 'keywords', 'director', 'genres']
    for feature in features:
        movies[feature] = movies[feature].apply(clean_data)

    movies['soup'] = movies.apply(create_soup, axis=1)

    #위에서 추출한 feature를 통해 코사인 유사도를 구한다.
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(movies['soup'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    #데이터에서 영화의 제목과 인덱스만 추출한다.
    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()
    #입력한 영화제목의 인덱스를 구한다.
    idx = indices[title]

    #입력한 영화제목과 다른 영화와의 코사인 유사도를 리스트로 만든다.
    sim_scores = list(enumerate(cosine_sim[idx]))

    #코사인 유사도를 내림차순으로 정렬한다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #코사인 유사도 상위 15개의 영화를 반환받는다.
    sim_scores = sim_scores[1:16]
    movie_indices = [i[0] for i in sim_scores]
    #검색결과인 영화의 리스트를 반환한다.
    return movie_indices




#weighted rating을 적용한 후 상위 6개의 영화의 인덱스를 반환받는다.
def trendingNow():
    C = movies['vote_average'].mean()
    m = movies['vote_count'].quantile(0.9)
    q_movies = movies.copy().loc[movies['vote_count'] >= m]

    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['vote_average']
        return (v/(v+m)*R) + (m/(m+v)*C)
    q_movies['score'] = q_movies.apply(weighted_rating, axis = 1)
    q_movies = q_movies.sort_values('score', ascending=False)
    trending = q_movies[['title']].head(6)
    indices = trending.index.tolist()
    return indices

#인기도 순으로 영화를 정렬하는 함수, 영화의 인덱스를 반환한다.
def popularityNow():
    popular = movies.sort_values('popularity', ascending=False)
    indices = popular.head(10).index.tolist()
    return indices

#기존에 계산된 similarity matrix를 읽어온 후 내림차순으로 poster_url을 계산한다.
def similarity1():
    user1_Avatar = pd.read_csv("data/user1_Avatar_similar")
    title = user1_Avatar['title']
    movie_title = movies_metadata['title']
    movie_id = movies_metadata['id']
    movie = pd.DataFrame({'id': movie_id, 'title': movie_title})
    url = []
    for j in title:
        for i in range(len(movie)):
            if movie['title'][i] == j:
                idk = movie_id[i]
                url.append(get_poster_urls(idk))
    return url

#기존에 계산된 romance chart matrix를 읽어온 후 내림차순으로 poster_url을 계산한다.
def romance_chart():
    romance = pd.read_csv("data/romance_chart.csv")
    title = romance['title']
    movie_title = movies_metadata['title']
    movie_id = movies_metadata['id']
    movie_indices = pd.Series(movies_metadata.index, index=movies_metadata['title']).drop_duplicates()
    url = []
    for j in title:
        for i in range(len(movie_title)):
            if movie_title[i] == j:
                id = movie_id[movie_indices[movie_title[i]]]
                url.append(get_poster_urls(id))
    return url

#기존에 계산된 action chart matrix를 읽어온 후 내림차순으로 poster_url을 계산한다.
def action_chart():
    action = pd.read_csv("data/action_chart.csv")
    title = action['title']
    movie_title = movies_metadata['title']
    movie_id = movies_metadata['id']
    movie = pd.DataFrame({'id': movie_id, 'title': movie_title})
    url = []
    for j in title:
        for i in range(len(movie)):
            if movie['title'][i] == j:
                idk = movie_id[i]
                url.append(get_poster_urls(idk))
    return url


