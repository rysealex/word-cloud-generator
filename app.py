from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import matplotlib
matplotlib.use('Agg')
import func as fc

app = Flask(__name__)
CORS(app) # enable CORS

@app.route("/generate-cloud", methods=["POST"])
def generate_cloud():
    data = request.get_json()
    # get user input
    theme_word = data.get("theme_word", "")
    num_words = int(data.get("num_words", 10))
    bkg_color = data.get("bkg_color", "white")
    theme_color = data.get("theme_color", "red")
    other_colors = data.get("other_colors", ["blue", "green", "yellow"])
    font_weight = data.get("font_weight", "normal")
    font_type = data.get("font_type", "sans-serif")

    # check if valid theme word
    if not fc.is_valid_word(theme_word):
        return jsonify({"error": "Invalid theme word"}), 400
    # check if enough related words found
    related_words = fc.get_related_words(theme_word, num_words-1)
    if len(related_words) != num_words:
        return jsonify({"error": "Not enough related words found"}), 400
    
    # generate image
    img_buffer = fc.basic_word_cloud(
        related_words,
        bkg_color,
        theme_color,
        other_colors[0],
        other_colors[1],
        other_colors[2],
        font_weight,
        font_type
    )
    return send_file(img_buffer, mimetype="image/png")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)