import streamlit as st
from PIL import Image
import plotly.express as px
import pandas as pd
import json


st.set_page_config(layout="wide")
# battles = Image.open("battles.png")
# st.image(battles)

st.title("""BATTLE OF MELAS CHASMA - STATS RECAP
""")

st.markdown("""---""")


st.markdown("""## Power spent per day per faction
""")
attack_logs = pd.read_json('attack_logs.json', lines=True)
attack_logs['DAY'] = pd.to_datetime(attack_logs['DAY'],unit='ms')
attack_logs['HOUR'] = pd.to_datetime(attack_logs['HOUR'],unit='ms')
day_power = px.bar(attack_logs.groupby(['DAY', 'FACTION']).sum().reset_index(), x="DAY", y="power", color='FACTION', barmode='group', color_discrete_map={"Free Martians": 'red', 'Guardians':'blue', 'Terrans':'gold', 'Council':'green'})
st.plotly_chart(day_power, use_container_width=True)

st.markdown("""## Total power spent per faction (Logarithmic)
""")

power_spent_per_faction = px.bar(attack_logs.groupby('FACTION').sum('power').reset_index(), x='FACTION', y='power', log_y=True, color='FACTION', color_discrete_map={"Free Martians": 'red', 'Guardians':'blue', 'Terrans':'gold', 'Council':'green'})
st.plotly_chart(power_spent_per_faction, use_container_width=True)

st.markdown("""## Power spent hourly - Whole week
""")

hour_power = px.line(attack_logs.groupby(['HOUR', 'FACTION']).sum().reset_index(), x="HOUR", y="power", color='FACTION', color_discrete_map={"Free Martians": 'red', 'Guardians':'blue', 'Terrans':'gold', 'Council':'green'})
st.plotly_chart(hour_power, use_container_width=True)

st.markdown("""## Power spent hourly - Distribution
""")

attack_logs['HOUR_ONLY'] = attack_logs['HOUR'].dt.hour
hour_only_power = px.bar(attack_logs.groupby('HOUR_ONLY').sum('power').reset_index(), x="HOUR_ONLY", y="power")
st.plotly_chart(hour_only_power, use_container_width=True)

st.markdown("""## Locations held per skirmish
""")

skirmish_df = pd.read_json('skirmish.json', lines=True).rename(columns={'defense':'LOCATIONS_HELD'})
skirmish_chart = px.line(skirmish_df, x='skirmish', y='LOCATIONS_HELD', color='owner', color_discrete_map={"free_martians": 'red', 'guardians':'blue', 'terrans':'gold', 'council':'green'})
st.plotly_chart(skirmish_chart, use_container_width=True)

st.markdown("""## Locations held per skirmish - cumulative
""")

skirmish_df['LOCATIONS_HELD_CUMSUM'] = skirmish_df.groupby('owner')['LOCATIONS_HELD'].cumsum(axis=0).reset_index()['LOCATIONS_HELD']

skirmish_cumsum_chart = px.line(skirmish_df, x='skirmish', y='LOCATIONS_HELD_CUMSUM', color='owner', color_discrete_map={"free_martians": 'red', 'guardians':'blue', 'terrans':'gold', 'council':'green'})
st.plotly_chart(skirmish_cumsum_chart, use_container_width=True)

st.markdown("""## Count of discord messages sent during week per faction
""")

all_factions_discord_message = pd.read_json('battles_discord_messages.json', lines=True)
all_factions_discord_message['HOUR'] = pd.to_datetime(all_factions_discord_message['HOUR'],unit='ms')
battles_messages_graph = px.line(all_factions_discord_message[['HOUR', 'FACTION', 'content']].groupby(['HOUR','FACTION']).count().reset_index(), x="HOUR", y="content", 
color='FACTION', color_discrete_map={"free_martians": 'red', 'guardians':'blue', 'terrans':'gold', 'council':'green'})
st.plotly_chart(battles_messages_graph , use_container_width=True)

st.markdown("""## Total messages sent during battles per faction
""")
total_messages_sent = all_factions_discord_message[['FACTION', 'content']].groupby('FACTION').count().reset_index().rename(columns={'content':'count_of_messages'})
total_messages_sent_graph = px.bar(total_messages_sent, x='FACTION', y='count_of_messages', color='FACTION', color_discrete_map={"free_martians": 'red', 'guardians':'blue', 'terrans':'gold', 'council':'green'})
st.plotly_chart(total_messages_sent_graph, use_container_width=True)


st.markdown("""## Messages sent count vs Count of Locations held per skirmish
""")
skirmish_messages_sent = pd.read_json('skirmish_messages_sent.json', lines=True).rename(columns={'content':'messages_sent_count'})
skirmish_messages_scatter = px.scatter(skirmish_messages_sent, x='messages_sent_count',y='locations_held',  color='FACTION', color_discrete_map={"free_martians": 'red', 'guardians':'blue', 'terrans':'gold', 'council':'green'})
st.plotly_chart(skirmish_messages_scatter, use_container_width=True)
st.text('The distribution for the most part makes sense; the count of messages sent appears to be correlated with the number of locations held.\nInterestingly, Free Martians held both outliers in the plot above.')
