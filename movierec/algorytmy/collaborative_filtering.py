import pandas as pd
import numpy as np
from scipy import spatial

ratings= pd.read_csv('movierec/algorytmy/dane/ratings.csv',encoding='latin-1')
movies = pd.read_csv('movierec/algorytmy/dane/movies.csv',encoding='latin-1')
tags = pd.read_csv('movierec/algorytmy/dane/tags.csv',encoding='latin-1')

def add_user(data):
    new_matrix = ratings.append(data, ignore_index=True)
    return new_matrix
#first we need to normalize ratings
def normalize_ratings(matrix):
    rating_pd = matrix.pivot_table(index='userId', columns='movieId', values='rating')
    mean = rating_pd.mean(axis=1,skipna=True).to_frame().rename(columns={0:'mean'})
    mean_matrix=pd.merge(matrix, mean, on='userId')

    # for every user we substract the mean rating of a user from every rating
    mean_matrix['centered_cosine']= mean_matrix['rating'] - mean_matrix['mean']

    # we fill missing values with 0, with is the average rating of every user
    normalized_ratings = mean_matrix.pivot_table(index='userId', columns='movieId', values='centered_cosine').fillna(0)
    return normalized_ratings

def generate_similar_users(normalized_ratings,user_id,n_users):
    # we choose to recommend movies for first user so we set his cosine similarity to 1
    cosine_similarity=[1]
    eps=0.00001
    normalized_ratings_values = normalized_ratings.values
    # for every user except the one chosen before we count cosine similarity to user 1
    for user in range(user_id+1,610):
        if sum(normalized_ratings_values[user])==0:
            normalized_ratings_values[user][0] = eps
        cosine_similarity.append(1 - spatial.distance.cosine(normalized_ratings_values[0], normalized_ratings_values[user]))
    cosine_similarity = list(enumerate(cosine_similarity,0))
    # we sort user by cosine similarity (the higher the more similar)
    sorted_cosine_similarity= sorted(cosine_similarity, key=lambda tup: tup[1],reverse=True)
    # we choose top n similar users
    sorted_cosine_similarity=sorted_cosine_similarity[0:n_users]
    # dataframe with top n similar user and their ratings for every movie
    similar_users = pd.DataFrame()
    for user in sorted_cosine_similarity:
        similar_users = similar_users.append(normalized_ratings.loc[user[0]])


# similar_users['cosine_similarity']=[user[1] for user in sorted_cosine_similarity]

    # we predict user 1 rating by counting weighted average for every non-rated movie
    #wages are cosine similarites

    sum_wages = 0
    for x in sorted_cosine_similarity:
        sum_wages = sum_wages+x[1]

    index=0
    for movie in similar_users.loc[0]:
        weighted_sum = 0
        if movie==0.0:
            for user in range(0,n_users):
                weighted_sum += similar_users.values[user][index]*(sorted_cosine_similarity[user][1])
            predicted_value=weighted_sum/sum_wages
            similar_users.loc[0][index+1]=predicted_value
        index+=1
    return(similar_users)

def generate_reccomendation(data,n_movies):
    matrix = add_user(data)
    normalized_ratings = normalize_ratings(matrix)
    similar_users = generate_similar_users(normalized_ratings,0,10)
    moviesId = list(similar_users.columns)
    predicted_ratings = similar_users.loc[0].values
    recommended_movies = list(zip(moviesId,predicted_ratings))
    recommended_movies.sort(key=lambda tup: tup[1],reverse=True)
    rated_movies=[]
    for x in data:
       rated_movies.append(x['movieId'])
    recommended_movies_list =[]
    for movie in recommended_movies:
        if movie[0] not in rated_movies:
            recommended_movies_list.append(str(movie[0]))
    return(recommended_movies_list[0:n_movies])

