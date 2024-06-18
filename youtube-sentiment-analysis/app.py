from flask import Flask, request, jsonify, render_template
import requests
from transformers import pipeline

app = Flask(__name__)

YOUTUBE_API_KEY = 'PASTE_YOUR_YOUTUBE_API_KEY_HERE'
# Initialize sentiment analysis models
sentiment_analyzer_default = pipeline('sentiment-analysis', model="cardiffnlp/twitter-roberta-base-sentiment")
sentiment_analyzer_siebert = pipeline('sentiment-analysis', model="siebert/sentiment-roberta-large-english")
sentiment_analyzer_bert = pipeline('sentiment-analysis', model="sbcBI/sentiment_analysis_model")

SENTIMENT_MAP = {
    'LABEL_0': 'Negative',
    'LABEL_1': 'Neutral',
    'LABEL_2': 'Positive',
    'NEGATIVE': 'Negative',
    'POSITIVE': 'Positive'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No search query provided.'})

    youtube_data = fetch_youtube_data(query)
    if 'error' in youtube_data:
        return jsonify(youtube_data)
    
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}

    for video in youtube_data:
        for comment in video['comments']:
            sentiments = {
                'default': SENTIMENT_MAP[sentiment_analyzer_default(comment['text'])[0]['label']],
                'siebert': SENTIMENT_MAP[sentiment_analyzer_siebert(comment['text'])[0]['label']],
                'bert': SENTIMENT_MAP[sentiment_analyzer_bert(comment['text'])[0]['label']]
            }
            comment['sentiments'] = sentiments

            # Update sentiment counts
            sentiment_counts[sentiments['default']] += 1
            sentiment_counts[sentiments['siebert']] += 1
            sentiment_counts[sentiments['bert']] += 1

    return jsonify({'videos': youtube_data, 'sentiment_counts': sentiment_counts})

def fetch_youtube_data(query):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API_KEY}&maxResults=5"
    search_response = requests.get(search_url)
    if search_response.status_code != 200:
        return {'error': 'Failed to fetch data from YouTube API.'}
    
    search_results = search_response.json()
    videos = []

    for item in search_results['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        likes = fetch_video_likes(video_id)
        comments = fetch_video_comments(video_id)
        videos.append({'title': title, 'likes': likes, 'comments': comments})

    return videos

def fetch_video_likes(video_id):
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    video_response = requests.get(video_url)
    if video_response.status_code != 200:
        return 0

    video_data = video_response.json()
    return int(video_data['items'][0]['statistics'].get('likeCount', 0))

def fetch_video_comments(video_id):
    comments_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_API_KEY}&maxResults=5&order=relevance"
    comments_response = requests.get(comments_url)
    if comments_response.status_code != 200:
        return []

    comments_data = comments_response.json()
    comments = []

    for item in comments_data['items']:
        comment_text = item['snippet']['topLevelComment']['snippet']['textOriginal']
        comment_likes = int(item['snippet']['topLevelComment']['snippet'].get('likeCount', 0))
        comments.append({'text': comment_text, 'likes': comment_likes})

    return comments

if __name__ == '__main__':
    app.run(debug=True)

