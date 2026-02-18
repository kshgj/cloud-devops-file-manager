from flask import Flask, render_template, request
import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# AWS Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Create S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    # Upload to S3
    s3.upload_fileobj(file, BUCKET_NAME, file.filename)

    return "File uploaded to AWS S3 successfully!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


