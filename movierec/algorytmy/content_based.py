import itertools

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
ratings= pd.read_csv('movierec/algorytmy/dane/ratings.csv',encoding='latin-1')
movies = pd.read_csv('movierec/algorytmy/dane/movies.csv',encoding='latin-1')
tags = pd.read_csv('movierec/algorytmy/dane/tags.csv',encoding='latin-1')
# creates dataframe with every movie and genres according to that movie
def TFIDF(movies):
    tf = TfidfVectorizer(analyzer=lambda s: (c for i in range(1,4)
                                             for c in combinations(s.split('|'), r=i)))
    tfidf_matrix = tf.fit_transform(movies['genres'])
    genre_combinations = tf.get_feature_names()
    all_movies_tfifd = pd.DataFrame(tfidf_matrix.todense(), columns=genre_combinations, index=movies.movieId)
    return all_movies_tfifd
# add user from website for whom we generate reccomendations
def add_user(data):
    new_matrix = ratings.append(data,ignore_index=True)
    # matrix = new_matrix.pivot(index='userId', columns='movieId',values='rating')
    return new_matrix
# returns best rated movies by user taking into account rating>4 and time
def best_rated_movies(ratings,matrix,user_id):
    # jeśli będziemy dodawać użytkownika jako id 0 to wtedy zmienić user_id
    rated_films = matrix.iloc[user_id].to_frame().rename(columns={1:'rating'}).sort_values(by=['rating'],ascending=[False])
    rated_films.dropna()
    best_movies = rated_films.loc[rated_films['rating']>4.0]
    timestamp = ratings.loc[ratings['userId']==user_id][['movieId','timestamp']]
    best_movies_with_time = pd.merge(best_movies,timestamp,on='movieId')
    sorted_movies = best_movies_with_time.sort_values(by=['timestamp'],ascending=[False])
    best_rated_movies = list(sorted_movies.movieId)
    return best_rated_movies
    #based on how many movies reccomendations will be generated
    # if len(best_movies)>5:
    #     best_movies = best_movies[0:5]

# return reccomended movie_id, takes rating data from a user
def generate_ratings(data,n_movies):
    ratings = add_user(data)
    matrix = ratings.pivot(index='userId', columns='movieId',values='rating')
    all_movies_tfidf = TFIDF(movies)
    best_movies = best_rated_movies(ratings,matrix,1)
    best_movies_tfidf = all_movies_tfidf[all_movies_tfidf.index.isin(best_movies)]

    cosine_matrix = cosine_similarity(all_movies_tfidf,best_movies_tfidf)
    similarity_df = pd.DataFrame(cosine_matrix,columns = best_movies, index=movies['movieId'])
    recommended_movies=[]
    for x in range (len(similarity_df.columns)):
        # we can choose how many similar movies per one movie function returns
        recommended_movies.append(list(similarity_df.sort_values(similarity_df.columns[x],ascending=False).head(1).index.values))

    return(list(itertools.chain.from_iterable(recommended_movies[0:n_movies])))

