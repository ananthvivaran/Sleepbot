import os
import logging
from sentence_transformers import SentenceTransformer  # type: ignore
import chromadb  # type: ignore
from llama_cpp import Llama  # type: ignore # New fast binding

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize embedding model & ChromaDB
embedding_model = SentenceTransformer('BAAI/bge-base-en')
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="sleep_expert")

# Path to your GGUF model
GGUF_MODEL_PATH = r"C:\Users\HP\OneDrive\Desktop\sleepliness\sleepcorpus\qwen2-1_5b-instruct-q5_k_m.gguf"

# Initialize llama-cpp model once (loads into RAM, very fast after that)
logging.info("Loading GGUF model with llama-cpp-python...")
llm = Llama(
    model_path=GGUF_MODEL_PATH,
    n_ctx=4096,        # Context length
    n_threads=6        # Adjust to your CPU
)

def retrieve_context(query, top_k=3):
    """Retrieve relevant context using ChromaDB"""
    query_embedding = embedding_model.encode([query], convert_to_numpy=True).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    context = results['documents'][0][0][:800] if results['documents'][0] else ""  # Use first chunk only, limit to 800 chars
    logging.info(f"Retrieved context: {context[:100]}...")
    return context

def generate_answer(query, context, is_sleep_related=False):
    """Generate answer from GGUF model with tailored prompts"""
    if is_sleep_related:
        prompt = f"Context: {context}\nQuestion: {query}\nYou are a sleep chatbot. Use the context to provide a clear, natural answer (1-2 complete sentences) by synthesizing the information and adding general sleep knowledge if needed. Avoid repetition and stop after a full thought, even within the token limit."
    else:
        prompt = f"Question: {query}\nYou are a general assistant. Provide a short, accurate answer (1 sentence) using the most current knowledge available, and suggest asking about sleep if relevant."

    logging.info(f"Prompt: {prompt[:100]}...")
    output = llm(
        prompt,
        max_tokens=150,    # Ensures complete sentences
        temperature=0.7,
        repeat_penalty=1.3,  # Increased to reduce repetition
        # No stop condition to allow natural completion
    )
    answer = output["choices"][0]["text"].strip()
    # Ensure answer ends with a complete sentence
    if not answer.endswith(".") and not answer.endswith("!") and not answer.endswith("?"):
        sentences = answer.split(".")
        answer = ".".join(sentences[:-1]) + "." if len(sentences) > 1 else answer
    logging.info(f"Generated answer: {answer}")
    return answer

def rag_pipeline(query):
    # Define casual greetings and non-sleep fallback
    casual_greetings = ["hi", "hello", "hey", "hola"]
    question_lower = query.lower().strip()

    # Return casual response for simple greetings
    if question_lower in casual_greetings:
        return f"Hi there! How can I assist you today? 😊"

    # Check for sleep-related keywords to trigger RAG
    sleep_keywords = ["sleep", "insomnia", "duration", "screen", "night", "circadian", "rest", "dream", "cycle"]
    is_sleep_related = any(keyword in question_lower for keyword in sleep_keywords)

    if is_sleep_related:
        context = retrieve_context(query)
        answer = generate_answer(query, context, is_sleep_related=True)
    else:
        context = ""  # No context needed for non-sleep queries
        answer = generate_answer(query, context, is_sleep_related=False)

    return answer

if __name__ == "__main__":
    question = "What is circadian rhythm?"
    logging.info(f"Query: {question}")
    answer = rag_pipeline(question)
    print(f"\n💡 Answer: {answer}")

    # Additional test
    question2 = "who is the president of india"
    logging.info(f"Query: {question2}")
    answer2 = rag_pipeline(question2)
    print(f"\n💡 Answer: {answer2}")