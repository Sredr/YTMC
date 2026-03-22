from flask import Flask, request, jsonify, redirect
from ytmusicapi import YTMusic
import yt_dlp

app = Flask(__name__)
ytmusic = YTMusic()

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return "Error: No query", 400

    results = ytmusic.search(query, filter="songs", limit=3)

    # Важлива зміна для Java ME!
    # Замість JSON віддаємо звичайний текст, де пісні розділені "---"
    text_response = ""
    for r in results:
        text_response += f"{r['videoId']}|{r['title']}|{r['artists'][0]['name']}---"

    return text_response

@app.route('/stream/<video_id>')
def stream(video_id):
    ydl_opts = {'format': 'bestaudio[ext=m4a]/bestaudio', 'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
        return redirect(info['url']) 

if __name__ == '__main__':
    # Запускаємо на порті 5000 локально
    app.run(host='0.0.0.0', port=5000)
