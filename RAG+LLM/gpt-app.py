from flask import Flask, request, jsonify
import openai
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
import os

app = Flask(__name__)

# Set your OpenAI API key (ensure you set this as an environment variable for security)
openai.api_key = "sk-P4P9EQcJrQXOxop6oTxdInEr308ZHyRPr_k-B6gyjRT3BlbkFJ0BQ4nxMvxQjwFO53Ud4Cwu0e4Kd2zmw_y5CI9YWpQA"

folder_path = "db"
embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

# Define the prompt template for OpenAI GPT-3.5
raw_prompt = PromptTemplate.from_template(
    """ 
    You are a technical assistant good at searching documents. If you do not have an answer from the provided information, say so.
    
    Question: {input}
    Context: {context}
    Answer:
    """
)

def ask_openai(query, context=""):
    """Function to send request to OpenAI's GPT-3.5 model using the new API format."""
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant skilled in retrieving relevant document information."},
        {"role": "user", "content": f"Question: {query}\nContext: {context}\nAnswer:"}
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()

    except openai.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"

@app.route("/ai", methods=["POST"])
def aiPost():
    """ Simple query to GPT-3.5 without RAG """
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"Query: {query}")

    response = ask_openai(query)

    print(response)

    return jsonify({"answer": response})

@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    """ Query GPT-3.5 with document retrieval """
    print("Post /ask_pdf called")
    json_content = request.json
    query = json_content.get("query")

    print(f"Query: {query}")

    print("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    print("Creating retrieval chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.1,
        },
    )

    document_chain = create_stuff_documents_chain(ask_openai, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    print(result)

    sources = []
    for doc in result["context"]:
        sources.append(
            {"source": doc.metadata["source"], "page_content": doc.page_content}
        )

    response_answer = {"answer": result["answer"], "sources": sources}
    return jsonify(response_answer)

@app.route("/pdf", methods=["POST"])
def pdfPost():
    """ Upload and process PDF into vector store """
    file = request.files["file"]
    file_name = file.filename
    save_file = f"pdf/{file_name}"
    
    os.makedirs("pdf", exist_ok=True)  # Ensure directory exists
    file.save(save_file)
    print(f"Filename: {file_name}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    print(f"Docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"Chunks len={len(chunks)}")

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

def start_app():
    app.run(host="0.0.0.0", port=8083, debug=True)

if __name__ == "__main__":
    start_app()
