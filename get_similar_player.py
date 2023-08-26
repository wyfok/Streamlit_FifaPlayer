import pandas as pd
from scipy.spatial.distance import cosine

from get_parameter import get_parameter



def calculation(user_inputs,input_df):
    gender = user_inputs['gender']
    raw_df = input_df

    filtered_df = raw_df[['preferred_foot','pace','shooting','passing','dribbling','defending','physic']]
    filtered_df.dropna(inplace=True)
    filtered_df['feature'] = filtered_df[['pace','shooting','passing','dribbling','defending','physic']].agg(list, axis=1)

    preferred_foot = user_inputs['preferred_foot']
    filtered_df = filtered_df[(filtered_df['preferred_foot']==preferred_foot)]

    user_feature_list = [user_inputs['pace'],
                                             user_inputs['shooting'],
                                             user_inputs['passing'],
                                             user_inputs['dribbling'],
                                             user_inputs['defending'],
                                             user_inputs['physic']]
    filtered_df['cosine'] = filtered_df.apply(lambda x: cosine(x['feature'], user_feature_list), axis = 1 )
    id_result = filtered_df.cosine.idxmin()
    return id_result        
