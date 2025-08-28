import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_csv("SpotifyFeatures.csv")

df = load_data()


# Page title
st.title("🎶 Music Emotion Dashboard")
st.write("Analyze emotions in music using Spotify dataset")

def get_mood(valence, energy):
    if valence > 0.6 and energy > 0.6:
        return "Happy"
    elif valence <= 0.4 and energy <= 0.4:
        return "Sad"
    elif energy > 0.7:
        return "Energetic"
    else:
        return "Chill"

df["mood"] = df.apply(lambda row: get_mood(row["valence"], row["energy"]), axis=1)

st.subheader("Mood Distribution of Songs")
fig = px.pie(df, names="mood", title="Mood Breakdown")
st.plotly_chart(fig)



mood_features = ["valence", "energy", "danceability", "acousticness", "liveness", "speechiness", "instrumentalness", "loudness"]
# Dropdown to select mood
selected_feature = st.selectbox("Select a mood:", mood_features, index=0)
# Group by artist and compute mean of the selected feature
top_artists = (
    df.groupby("artists")[selected_feature]
      .mean()
      .nlargest(10)
      .reset_index()
)
# Bar chart
fig2 = px.bar(
    top_artists,
    x="artists",
    y=selected_feature,
    labels={"artists": "Artist", selected_feature: f"{selected_feature.capitalize()} Score"},
    title=f"Top 10 Artists by {selected_feature.capitalize()}",
    color=selected_feature,
    color_continuous_scale="viridis"
)
fig2.update_layout(xaxis_tickangle=-30)
st.subheader(f"Top 10 Artists by {selected_feature.capitalize()}")
st.plotly_chart(fig2)



st.subheader("Compare Songs Emotion Features")
songs = st.multiselect("Pick at least 2 Songs", df['track_name'].unique()[:100])

features = ["danceability", "energy", "valence", "speechiness"]

if songs:
    fig3 = go.Figure()
    for song in songs:
        row = df[df['track_name'] == song][features].iloc[0]
        fig3.add_trace(go.Scatterpolar(
            r=row.values,
            theta=features,
            fill='toself',
            name=song
        ))
    fig3.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        showlegend=True
    )
    st.plotly_chart(fig3)


st.subheader("Playlist Emotional Journey")
artist = st.selectbox("Choose Artist", df['artists'].unique())
playlist = df[df['artists'] == artist].head(20)
fig4 = px.line(playlist, x="track_name", y="valence",
               title=f"Emotional Journey of {artist}'s Songs")
st.plotly_chart(fig4)
