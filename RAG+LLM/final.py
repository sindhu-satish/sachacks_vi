from flask import Flask, request, jsonify
import openai
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
import os

app = Flask(__name__)

# Securely fetch OpenAI API key from environment
openai.api_key = "OPENAIKEY"

# Define ChromaDB directory
folder_path = "db"
embedding = FastEmbedEmbeddings()

# Text splitter for chunking PDF text
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

def ask_openai(query, context=None):
    """Function to send request to OpenAI's GPT-4o model using retrieved context (if available)."""
    if context:
        messages = [
            {"role": "system", "content": "You are an AI career counselor providing expert guidance."},
            {"role": "user", "content": f"Question: {query}\nContext: {context}\nAnswer:"}
        ]
    else:
        messages = [
            {"role": "system", "content": "You are an AI career counselor providing expert guidance."},
            {"role": "user", "content": f"Question: {query}\nAnswer:"}
        ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.5
        )
        return response["choices"][0]["message"]["content"].strip()

    except openai.error.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"

@app.route("/ai", methods=["POST"])
def aiPost():
    """ Query GPT-4o with document retrieval (RAG) if relevant information is found; otherwise, let GPT-4o answer. """
    print("Post /ai called")

    try:
        json_content = request.get_json(force=True, silent=True)
        if not json_content or "query" not in json_content:
            return jsonify({"error": "Invalid JSON. Ensure 'query' field is included."}), 400

        query = json_content["query"]
        print(f"Query: {query}")

        # Load the vector database
        vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

        # Retrieve relevant documents based on query
        retriever = vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )
        docs = retriever.get_relevant_documents(query)

        # If relevant context is found, use it; otherwise, let GPT-4o answer freely
        if docs:
            context = "\n\n".join([doc.page_content for doc in docs])
            response = ask_openai(query, context)

            sources = [{"source": doc.metadata.get("source", "Unknown"), "page_content": doc.page_content} for doc in docs]

            return jsonify({"answer": response, "sources": sources})
        else:
            response = ask_openai(query)
            return jsonify({"answer": response, "sources": "No relevant information found in RAG; AI-generated answer provided."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload_pdf", methods=["POST"])
def uploadPDF():
    """ Upload and process PDF (scraped Medium articles) into vector store """
    try:
        file = request.files["file"]
        file_name = file.filename
        save_file = f"pdf/{file_name}"
        
        os.makedirs("pdf", exist_ok=True)
        file.save(save_file)
        print(f"Filename: {file_name}")

        # Load PDF and split into chunks
        loader = PDFPlumberLoader(save_file)
        docs = loader.load_and_split()
        print(f"Docs len={len(docs)}")

        chunks = text_splitter.split_documents(docs)
        print(f"Chunks len={len(chunks)}")

        # Store chunks in ChromaDB
        vector_store = Chroma.from_documents(
            documents=chunks, embedding=embedding, persist_directory=folder_path
        )
        vector_store.persist()

        response = {
            "status": "Successfully Uploaded",
            "filename": file_name,
            "doc_len": len(docs),
            "chunks": len(chunks),
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_app():
    app.run(host="0.0.0.0", port=8084, debug=True)

if __name__ == "__main__":
    start_app()
