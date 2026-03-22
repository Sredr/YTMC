from flask import Flask, request, jsonify, redirect
from ytmusicapi import YTMusic
import yt_dlp
import os

app = Flask(__name__)
ytmusic = YTMusic()

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = ytmusic.search(query, filter="songs", limit=3)
    simple_results = [{"id": r['videoId'], "title": r['title'], "artist": r['artists'][0]['name']} for r in results]
    return jsonify(simple_results)

@app.route('/stream/<video_id>')
def stream(video_id):
    ydl_opts = {'format': 'bestaudio[ext=m4a]/bestaudio', 'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return redirect(info['url']) 

if __name__ == '__main__':
    # Render сам задає порт через змінні оточення
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
