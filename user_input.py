import streamlit as st

def user_input():

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox(
        'Gender',('Female','Male'))
    with col2:
        preferred_foot = st.selectbox(
        'Preferred Foot',('Right','Left'))
    col3, col4 = st.columns(2)
    with col3:
        pace = st.slider('Select the value for Pace', 0, 100, 50)
        shooting = st.slider('Select the value for Shooting', 0, 100, 50)
        passing = st.slider('Select the value for Passing', 0, 100, 50)
    with col4:
        dribbling = st.slider('Select the value for Dribbling', 0, 100, 50)
        defending = st.slider('Select the value for Defending', 0, 100, 50)
        physic = st.slider('Select the value for Physic', 0, 100, 50)
        
    return {'gender':gender,
            'preferred_foot':preferred_foot,
            'pace':(pace),
            'shooting':(shooting),
            'passing': (passing),
            'dribbling': (dribbling),
            'defending': (defending),
            'physic':(physic)}


