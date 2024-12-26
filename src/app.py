import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt


from dotenv import load_dotenv

# load the .env file variables
load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
artist_id = os.getenv('ARTIST_ID')
scope = os.getenv('SCOPE') # 'user-library-read'
redirect_uri = os.getenv('REDIRECT_URI') # 'http://localhost:8888/callback'

if not client_id or not client_secret:
    raise ValueError("Please set the CLIENT_ID and CLIENT_SECRET environment variables.")

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                    client_secret=client_secret,
                                                    redirect_uri=redirect_uri,
                                                    scope=scope))

# Get the artist's top tracks
top_tracks = spotify.artist_top_tracks(artist_id, country='US')


data = {'name': [], 'popularity': [], 'duration': []}

for i, top_track in enumerate(top_tracks['tracks'][:10], 1):
    data['name'].append(top_track['name'])
    data['popularity'].append(top_track['popularity'])
    data['duration'].append(top_track['duration_ms'] / 60000)
    print(f"{i}. {top_track['name']}")

df = pd.DataFrame(data)

#   Step 6: Transform to Pandas DataFrame
print(df[:3].sort_values(by='popularity', ascending=False))

# Step 7: Analyze statistical relationship

plt.figure(figsize=(10, 6))
plt.scatter(df['popularity'], df['duration'])
plt.xlabel('Popularity')
plt.ylabel('Duration (minutes)')
plt.show()