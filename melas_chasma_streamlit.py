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
day_power = px.bar(attack_logs.groupby(['DAY', 'FACTION']).sum().reset_index(), x="DAY", y="power", color='FACTION', barmode='group')
st.plotly_chart(day_power, use_container_width=True)

st.markdown("""## Total power spent per faction (Logarithmic)
""")

power_spent_per_faction = px.bar(attack_logs.groupby('FACTION').sum('power').reset_index(), x='FACTION', y='power', log_y=True, color='FACTION')
st.plotly_chart(power_spent_per_faction, use_container_width=True)

st.markdown("""## Power spent hourly - Whole week
""")

hour_power = px.line(attack_logs.groupby(['HOUR', 'FACTION']).sum().reset_index(), x="HOUR", y="power", color='FACTION')
st.plotly_chart(hour_power, use_container_width=True)

st.markdown("""## Power spent hourly - Distribution
""")

attack_logs['HOUR_ONLY'] = attack_logs['HOUR'].dt.hour
hour_only_power = px.bar(attack_logs.groupby('HOUR_ONLY').sum('power').reset_index(), x="HOUR_ONLY", y="power")
st.plotly_chart(hour_only_power, use_container_width=True)

st.markdown("""## Locations held per skirmish
""")

skirmish_df = pd.read_json('skirmish.json', lines=True).rename(columns={'defense':'LOCATIONS_HELD'})
skirmish_chart = px.line(skirmish_df, x='skirmish', y='LOCATIONS_HELD', color='owner')
st.plotly_chart(skirmish_chart, use_container_width=True)

st.markdown("""## Locations held per skirmish - cumulative
""")

skirmish_df['LOCATIONS_HELD_CUMSUM'] = skirmish_df.groupby('owner')['LOCATIONS_HELD'].cumsum(axis=0).reset_index()['LOCATIONS_HELD']

skirmish_cumsum_chart = px.line(skirmish_df, x='skirmish', y='LOCATIONS_HELD_CUMSUM', color='owner')
st.plotly_chart(skirmish_cumsum_chart, use_container_width=True)