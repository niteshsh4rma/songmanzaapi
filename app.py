from flask import Flask, request, redirect, jsonify, json
import time
import jiosaavn
import os
from traceback import print_exc
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET",'SECRETKEY')
CORS(app)


@app.route('/')
def home():
    return "<h2>API is UP and Running. API by <a href='https://linkedin.com/in/niteshsh4rma'>Nitesh Sharma</a></h2>"

@app.route('/song/')
def search():
    lyrics = False
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True
    if query:
        return jsonify(jiosaavn.search_for_song(query,lyrics))
    else:
        error = {
            "status": False,
            "error":'Query is required to search songs!'
        }
        return jsonify(error)

@app.route('/playlist/')
def playlist():
    lyrics = False
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True
    if query:
        id = jiosaavn.get_playlist_id(query)
        songs = jiosaavn.get_playlist(id,lyrics)
        return jsonify(songs)
    else:
        error = {
            "status": False,
            "error":'Query is required to search playlists!'
        }
        return jsonify(error)

@app.route('/album/')
def album():
    lyrics = False
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True
    if query:
        id = jiosaavn.get_album_id(query)
        songs = jiosaavn.get_album(id,lyrics)
        return jsonify(songs)
    else:
        error = {
            "status": False,
            "error":'Query is required to search albums!'
        }
        return jsonify(error)

@app.route('/lyrics/')
def lyrics():
    query = request.args.get('query')

    if query:
        try:
            if 'http' in query and 'saavn' in query:
                id = jiosaavn.get_song_id(query)
                lyrics = jiosaavn.get_lyrics(id)
            else:
                lyrics = jiosaavn.get_lyrics(query)
            response = {}
            response['status'] = True
            response['lyrics'] = lyrics
            return jsonify(response)
        except Exception as e:
            error = {
            "status": False,
            "error": str(e)
            }
            return jsonify(error)
        
    else:
        error = {
            "status": False,
            "error":'Query containing song link or id is required to fetch lyrics!'
        }
        return jsonify(error)


@app.route('/result/')
def result():
    lyrics = False
    query = request.args.get('query')
    lyrics_ = request.args.get('lyrics')
    if lyrics_ and lyrics_.lower()!='false':
        lyrics = True

    if 'saavn' not in query:
        return jsonify(jiosaavn.search_for_song(query,lyrics))
    try:
        if '/song/' in query:
            print("Song")
            song_id = jiosaavn.get_song_id(query)
            song = jiosaavn.get_song(song_id,lyrics)
            return jsonify(song)

        elif '/album/' in query:
            print("Album")
            id = jiosaavn.get_album_id(query)
            songs = jiosaavn.get_album(id,lyrics)
            return jsonify(songs)

        elif '/playlist/' or '/featured/' in query:
            print("Playlist")
            id = jiosaavn.get_playlist_id(query)
            songs = jiosaavn.get_playlist(id,lyrics)
            return jsonify(songs)

    except Exception as e:
        print_exc()
        error = {
            "status": True,
            "error":str(e)
        }
        return jsonify(error)
    return None


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, use_reloader=True, threaded=True)
