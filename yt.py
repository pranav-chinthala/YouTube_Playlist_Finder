from googleapiclient.discovery import build

API_KEY = 'AIzaSyACWZzIpgIWFKlkfHxBMeHvxv51jOJb6Kk'
youtube = build('youtube', 'v3', developerKey=API_KEY)

VIDEO_ID = '9vM4p9NN0Ts' # Replace with the video ID you're checking

CHANNEL_INPUT = 'stanfordonline'  # Replace with either CHANNEL ID ('UC...') or CUSTOM NAME ('@CustomName')

def find_channel_id_by_custom_name(custom_name):
    search_response = youtube.search().list(
        q=custom_name,
        part='snippet',
        type='channel',
        maxResults=1
    ).execute()

    if search_response['items']:
        return search_response['items'][0]['snippet']['channelId']
    else:
        return None

def list_channel_playlists(channel_id):
    playlists = []
    next_page_token = None
    while True:
        response = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        playlists += response.get('items', [])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return playlists

def is_video_in_playlist(playlist_id):
    next_page_token = None
    index = 1
    while True:
        response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
        
        for item in response.get('items', []):
            if item['snippet']['resourceId']['videoId'] == VIDEO_ID:
                return True, index
            index += 1
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return False, None

def main(channel_id_or_custom_name):
    if channel_id_or_custom_name.startswith('UC'):
        channel_id = channel_id_or_custom_name
    else:
        channel_id = find_channel_id_by_custom_name(channel_id_or_custom_name)
        if not channel_id:
            print(f"Could not find channel ID for: {channel_id_or_custom_name}")
            return

    playlists = list_channel_playlists(channel_id)
    print(f"Found {len(playlists)} playlists in the channel.")

    for playlist in playlists:
        playlist_id = playlist['id']
        found, index = is_video_in_playlist(playlist_id)
        if found:
            video_url = f"https://www.youtube.com/watch?v={VIDEO_ID}"
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            combined_url = f"{video_url}&list={playlist_id}&index={index}"
            print(f"Video {VIDEO_ID} is in playlist: {playlist['snippet']['title']} ({playlist_id})")
            print(f"Video URL: {video_url}")
            print(f"Playlist URL: {playlist_url}")
            print(f"Combined URL: {combined_url}")
            break
    else:
        print("Video is not in any of the channel's playlists.")

if __name__ == "__main__":
    main(CHANNEL_INPUT)