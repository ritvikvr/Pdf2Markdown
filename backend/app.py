from flask import Flask, request, jsonify
from flask_cors import CORS
import pdfplumber
import os

app = Flask(__name__)
CORS(app)  # Allow requests from any origin

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "GET":
        return """
        <h2>Upload PDF</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf"/>
            <input type="submit" value="Upload"/>
        </form>
        """

    if request.method == "POST":
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Invalid file type"}), 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Extract text using pdfplumber
        text = ""
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        return jsonify({"filename": file.filename, "markdown": text})

if __name__ == "__main__":
    app.run(debug=True)
