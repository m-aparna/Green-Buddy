import responses
import re

@responses.activate
def test_youtube_api(client):
    # Mock data
    mock_youtube_api_data = {
        'kind': 'youtube#searchListResponse', 
        'etag': 'some_etag', 
        'nextPageToken': 'some_token', 
        'regionCode': 'IN', 
        'pageInfo': {'totalResults': 1000000, 'resultsPerPage': 2}, 
        'items': [
            {'kind': 'youtube#searchResult', 
            'etag': '_A1B2c3d4', 
            'id': {'kind': 'youtube#video', 'videoId': 'Ems6ZnpcRWo'}, 
            'snippet': {
                'publishedAt': 'some_time', 
                'channelId': 'some_channel_id', 
                'title': 'some_Neem_plant_care_title', 
                'description': 'How To Care NEEM plant', 
                'thumbnails': {
                                'default': {
                                    'url': 'some_url', 
                                    'width': 120, 
                                    'height': 90}, 
                                'medium': {
                                    'url': 'some_url', 
                                    'width': 320, 
                                    'height': 180}, 
                                'high': {
                                    'url': 'some_url', 
                                    'width': 480, 
                                    'height': 360}}, 
                'channelTitle': 'some_channel_title', 
                'liveBroadcastContent': 'none', 
                'publishTime': 'some_time'}},
            {'kind': 'youtube#searchResult', 
            'etag': '_A1B2c3d4', 
            'id': {'kind': 'youtube#video', 'videoId': 'Ems6ZnpcRWo'}, 
            'snippet': {
                'publishedAt': 'some_time', 
                'channelId': 'some_channel_id', 
                'title': 'some_Neem_plant_care_title', 
                'description': 'How To Care NEEM plant', 
                'thumbnails': {
                                'default': {
                                    'url': 'some_url', 
                                    'width': 120, 
                                    'height': 90}, 
                                'medium': {
                                    'url': 'some_url', 
                                    'width': 320, 
                                    'height': 180}, 
                                'high': {
                                    'url': 'some_url', 
                                    'width': 480, 
                                    'height': 360}}, 
                'channelTitle': 'some_channel_title', 
                'liveBroadcastContent': 'none', 
                'publishTime': 'some_time'}}]}
            
    # Mock api response, using regex to accomodate the dynamically typed API key part of the URL
    responses.add(
        responses.GET,
        re.compile(r'https://www.googleapis.com/youtube/v3/search\?key=.*&q=Neem\+plant\+care&part=snippet&type=video&maxResults=2&order=rating&videoDuration=medium&relevanceLanguage=en'),
        json=mock_youtube_api_data,
        status=200
    )

    # Simulate login
    mock_data = {
        "email": "test@test.com",
        "username": "Test User",
        "password1": "testpassword",
        "password2": "testpassword"
    }

    client.post("/sign-up", data=mock_data)

    # Test youtube api
    response = client.post("/plant-care", data={"query": "Neem"})

    print("Intercepted requests:")
    for request in responses.calls:
        print(f"Method: {request.request.method}")
        print(f"URL: {request.request.url}")

    # Check status code
    assert response.status_code == 200

    # Check returned video IDs 
    expected_video_1 = b'<iframe src="https://www.youtube.com/embed/yvBMUblfEuI"></iframe>'
    expected_video_2 = b'<iframe src="https://www.youtube.com/embed/Ems6ZnpcRWo"></iframe>'

    assert expected_video_1 in response.data
    assert expected_video_2 in response.data
