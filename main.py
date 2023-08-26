import streamlit as st
import pandas as pd
import numpy as np
import requests
from PIL import Image

import plotly.graph_objects as go
import plotly.express as px
from requests.exceptions import ConnectionError

from user_input import user_input
from get_similar_player import calculation
from get_parameter import get_parameter
from player import Player


parameter = get_parameter(r'https://raw.githubusercontent.com/wyfok/Streamlit_FifaPlayer/main/parameter.yaml')

st.set_page_config(layout="centered")


st.header('How good will you be as a football :soccer: player?')
st.image('https://i.giphy.com/media/VbVVXyxgxcNmLQcUZa/giphy.webp')

st.markdown('Have you ever dreamed of being a football player? Or have you ever created yourself in Fifa Career Mode?')
st.markdown('In the below section, you can select your gender, preferred foot, and six attributes.')
st.markdown('And I will find the closest player based on your input!')
st.markdown('Also, you can compare with some famous players and see if you are as good as them.')

st.caption("All players' data is based on Fifa22") 

st.divider()
st.subheader('Select your gender, preferred foot, and tell me how good you are in below six attributes.')
user_inputs = user_input()


def load_data(_gender):
    return pd.read_csv(parameter['input_file_path'][_gender])
                       
                       
input_df = load_data(user_inputs['gender'])
input_df = input_df.replace({'cdn.sofifa.com':'cdn.sofifa.net'}, regex=True)

user_feature_inputs = [user_inputs['pace'],
                             user_inputs['shooting'],
                             user_inputs['passing'],
                             user_inputs['dribbling'],
                             user_inputs['defending'],
                             user_inputs['physic']]

result_id = calculation(user_inputs,input_df)
player_result = Player(result_id,input_df)

st.divider()
st.subheader(f"The average Score from your inputs is: :red[{np.mean(user_feature_inputs):.1f}]")
st.subheader(f"You are similar to :red[{player_result.short_name}]")
if 1==1:
    try:
        r = requests.get(player_result.player_face_url, allow_redirects=False)
        if r.status_code != 302:
            st.image(player_result.player_face_url,width=150)
    except ConnectionError:
        pass


player_col1, player_col2 = st.columns(2)
with player_col1:
    st.subheader(f"Nationality: {player_result.nationality_name}")
    st.subheader(f"Preferred Position: {player_result.player_positions}")
    st.subheader(f"Overall: {player_result.overall}")
with player_col2:
    if isinstance(player_result.nation_flag_url, str) :
        try:
            r = requests.get(player_result.nation_flag_url, allow_redirects=False)
            if r.status_code != 302:
                st.image(player_result.nation_flag_url,width=100)
        except ConnectionError:
            pass
player_col3, player_col4 =st.columns(2)
with player_col3:
    if isinstance(player_result.club_name, str):
        st.subheader(f"Current Club: {player_result.club_name}")
        st.subheader(f"Current League: {player_result.league_name}")
with player_col4:
    if isinstance(player_result.club_logo_url, str):
        try:
            requests.get(player_result.club_logo_url)
            st.image(player_result.club_logo_url,width=100)
        except ConnectionError:
            pass

st.markdown("")
st.subheader(f"This radar chart compares between you and {player_result.short_name} in all six attributes.")
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=user_feature_inputs,
      theta=['Pace','Shooting','Passing','Dribbling','Defending','Physic'],
      fill='toself',
      name='You',
      marker_color = 'red'
))
fig.add_trace(go.Scatterpolar(
      r=player_result.feature,
      theta=['Pace','Shooting','Passing','Dribbling','Defending','Physic'],
      fill='toself',
      name=player_result.short_name,
      marker_color= 'cyan'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 100],
    ),
    angularaxis = dict(tickfont = dict(size = 20))
    ),
  showlegend=True
)

st.plotly_chart(fig)
st.caption('Double click the chart to reset')

st.subheader(f"Click [this link]({player_result.player_url}) to know more about {player_result.short_name}.")


st.divider()
st.subheader(f"How do you stand out from all {user_inputs['gender'].lower()} players?")
character_input = st.selectbox('Select which attribute you want to compare.',('Overall', 'Pace','Shooting','Passing','Dribbling','Defending','Physic'))

st.subheader(f"The :red[red vertical line] is your {character_input.lower()}.")
st.subheader(f"The :blue[blue curve] shows the distribution for all {user_inputs['gender'].lower()} players.")
st.text('The Y axis tells you are better than Y percent of all players.')
fig2 = px.ecdf(input_df, x=character_input.lower(), ecdfnorm ='percent' )
if character_input =='Overall':
    fig2.add_vline(x=np.mean(user_feature_inputs), line_width=3, line_dash="dash", line_color="red",name='You')
else:
    fig2.add_vline(x=user_inputs[character_input.lower()], line_width=3, line_dash="dash", line_color="red",name='You')
fig2.update_layout(
    xaxis_title=character_input,
    yaxis_title="You are better than X percent of all players!",
)

st.plotly_chart(fig2)
st.caption('Double click the chart to reset')

st.divider()
st.subheader(f"How are you compared with some famous {user_inputs['gender'].lower()} players?")
reputated_players = input_df[((input_df['international_reputation'].isin([4,5])) & (input_df['player_positions']!='GK'))]
reputated_player_selection = st.selectbox('Select a famous player',reputated_players['short_name'])
reputated_player = Player(reputated_players.index[reputated_players['short_name']==reputated_player_selection][0],input_df)

reputated_players_col1, reputated_players_col2 = st.columns(2)
with reputated_players_col1:
    st.subheader(f"{reputated_player.short_name}")
    st.subheader(f"Overall: {reputated_player.overall}")
    st.subheader(f"Nationality: {reputated_player.nationality_name}")
    
with reputated_players_col2:
    if 1==1:
        try:
            r = requests.get(reputated_player.player_face_url, allow_redirects=False)
            if r.status_code != 302:
                st.image(reputated_player.player_face_url,width=150)
        except ConnectionError:
            pass
    

fig3 = go.Figure()
fig3.add_trace(go.Scatterpolar(
      r=user_feature_inputs,
      theta=['Pace','Shooting','Passing','Dribbling','Defending','Physic'],
      fill='toself',
      name='YOU',
      marker_color = 'red'
))
fig3.add_trace(go.Scatterpolar(
      r=reputated_player.feature,
      theta=['Pace','Shooting','Passing','Dribbling','Defending','Physic'],
      fill='toself',
      name=reputated_player.short_name,
      marker_color= 'cyan'
))
fig3.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 100],
    ),
    angularaxis = dict(tickfont = dict(size = 20))
    ),
  showlegend=True
)
st.plotly_chart(fig3)
st.caption('Double click the chart to reset')

st.subheader(f"[Player Profile of {reputated_player.short_name}]({reputated_player.player_url})")
