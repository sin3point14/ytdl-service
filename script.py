from flask import Flask, request, redirect
import youtube_dl
import threading

output_dir = "./music/"

app = Flask(__name__)

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': output_dir + '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
}

@app.route("/")
def root():
    return '''
    <form method="POST" action="/download">
    <input type="text" name="links" />
    <input type="submit" value="Submit" />
    </form>'''

def download_async(links):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(links)

@app.route('/download', methods=['POST'])
def download():
    print(request.form["links"])
    t = threading.Thread(target=download_async, args=[request.form["links"].split(' ')])
    t.start()
    return redirect('/')