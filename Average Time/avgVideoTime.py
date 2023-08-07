import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Set up the OAuth2 credentials
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    "client_secrets.json", scopes
)
credentials = flow.run_console()

# Create the YouTube API client
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Get the playlist ID from user input
playlist_id = input("Enter the playlist ID: ")

# Get the playlist details using the YouTube API
playlist_request = youtube.playlistItems().list(
    part="contentDetails",
    playlistId=playlist_id,
    maxResults=50
)
playlist_response = playlist_request.execute()

# Calculate the average time of every video in the playlist
total_duration = 0
num_videos = 0
for item in playlist_response["items"]:
    video_id = item["contentDetails"]["videoId"]
    video_request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    video_response = video_request.execute()
    duration = video_response["items"][0]["contentDetails"]["duration"]
    total_duration += int(duration[2:-1])
    num_videos += 1

average_duration = total_duration / num_videos

print(f"The average time of every video in the playlist is {average_duration} seconds.")