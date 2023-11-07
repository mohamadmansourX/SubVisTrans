from flask import Flask, render_template, request,jsonify
import srt
from flask_cors import CORS  # Import CORS from flask_cors


app = Flask(__name__)
CORS(app)

class Subtitle:
    def __init__(self, index, start, end, value, translation=None):
        self.index = index
        self.start = start
        self.end = end
        self.value = value
        self.translation = translation

@app.route('/')
def index():
    return render_template('index.html', subtitles=None)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        subtitles = []
        content = uploaded_file.read().decode('utf-8')
        subtitles_list = list(srt.parse(content))
        for idx, subtitle in enumerate(subtitles_list):
            subtitle_obj = Subtitle(index=idx + 1, start=subtitle.start, end=subtitle.end, value=subtitle.content)
            subtitles.append(subtitle_obj)
        return render_template('index.html', subtitles=subtitles)
    else:
        return render_template('index.html', subtitles=None)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        subtitles_list = request.get_json()
        translated_subtitles = []

        # Perform translation (for demonstration, echo back the same subtitles)
        for subtitle in subtitles_list:
            translated_subtitle = Subtitle(
                index=subtitle['index'],
                start=subtitle['start'],
                end=subtitle['end'],
                value=subtitle['value'],
                translation=subtitle['value']  # Echo back the same subtitle text as translation
            )
            translated_subtitles.append(translated_subtitle.__dict__)

        return jsonify(translated_subtitles)
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
