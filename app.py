import os
from flask import Flask, render_template, send_from_directory
from moviepy import VideoFileClip

app = Flask(__name__)

VIDEO_FOLDER = 'static/videos'
THUMBNAIL_FOLDER = 'static/thumbnails'

def generate_thumbnails():
    for filename in os.listdir(VIDEO_FOLDER):
        if filename.endswith('.mp4'):
            thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f'{filename}.png')
            video_path = os.path.join(VIDEO_FOLDER, filename)
            if not os.path.exists(thumbnail_path):
                    clip = VideoFileClip(video_path)
                    clip.save_frame(thumbnail_path, t=1.0)
                    clip.reader.close()

@app.route('/')
def index():
    generate_thumbnails()
    videos = []
    for filename in os.listdir(VIDEO_FOLDER):
        if filename.endswith('.mp4'):
            video_info = {
                'filename': filename,
                'name': filename.removesuffix('.mp4'),
                'thumbnail': f'thumbnails/{filename}.png'
            }
            videos.append(video_info)
    return render_template('index.html', videos=videos)

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
