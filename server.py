import os
import openai
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from flask import Flask, request
from werkzeug.utils import secure_filename

numFiles = 0
openai.api_key = "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"

app = Flask(__name__)

@app.post("/feedback")
def get_feedback():
    global numFiles
    numFiles += 1
    file = list(request.files.values())[0]
    ext = os.path.splitext(secure_filename(file.filename))[1]
    filePath = f"files/{numFiles}{ext}"
    file.save(filePath)
    reader = SimpleDirectoryReader(
        input_files=[filePath]
    )
    docs = reader.load_data()
    index = VectorStoreIndex.from_documents(docs)
    query_engine = index.as_query_engine()
    response = query_engine.query("Reproduce the text with a number next to every grammar mistake, and create a list of those numbers with an explanation of the reasoning behind each mistake. Generate a new paragraph with the correct grammer while keeping the meaning the same")
    print(str(response))
    return str(response)

# open -a Google\ Chrome --args --disable-web-security --user-data-dir="/Users/Esha/Library/ApplicationSupport/Google/Chrome"
# flask --app server run

