from flask import request, jsonify
import chromadb
import openai
import os, json
import dotenv
import logging
from datetime import datetime
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", force=True)

client = openai()

# ✅ OpenAI & ChromaDB Initialization
OPENAI_API_KEY = os.getenv("Chroma_KEY")
if not OPENAI_API_KEY:
    logging.error("⚠️ OpenAI API Key retrieval failed!")
    raise RuntimeError("OpenAI API Key missing.")

client = openai.openai(api_key=OPENAI_API_KEY)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path="D:/ChromaDB_Storage")
collection = chroma_client.get_or_create_collection(name="memory_store")

# ✅ PostgreSQL Connection
db_settings = {
    "dbname": "nexa_memory",
    "user": "postgres",
    "password": "TheGardenGate1+",
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    try:
        return psycopg2.connect(**db_settings)
    except Exception as e:
        logging.error(f"❌ Database connection error: {e}")
        return None  # Prevents crashes if DB connection fails

def get_openai_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding
def register_memory_endpoints(app):

    @app.route("/store_memory", methods=["POST"])
    def store_memory():
        data = request.json
        required = {"memory_entry", "memory_content", "memory_type"}
        if not required.issubset(data):
            return error_response("Missing memory details.", 400)

        memory_content = data["memory_content"]

        # Generate embedding
        embedding = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[memory_content]
        ).data[0].embedding

        # Store in ChromaDB for vector search
        collection.add(
            ids=[data["memory_entry"]],
            documents=[memory_content],
            embeddings=[embedding]
        )

        # Generate a summary (Placeholder: Improve with GPT-based summarization)
        summary = " ".join(memory_content.split()[:20]) + "..." if len(memory_content.split()) > 20 else memory_content

        # Sentiment Analysis
        sentiment = TextBlob(memory_content).sentiment.polarity
        sentiment_label = "positive" if sentiment > 0 else "negative" if sentiment < 0 else "neutral"

        # PostgreSQL Storage with Enhanced Fields
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO memory_store 
                        (memory_entry, memory_type, memory_content, full_text, summary, sentiment_analysis, created_at, last_modified_at, confidence_score, importance_score, decay_rate) 
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s)
                    ON CONFLICT (memory_entry) 
                    DO UPDATE SET 
                        memory_type = EXCLUDED.memory_type, 
                        memory_content = EXCLUDED.memory_content, 
                        full_text = EXCLUDED.full_text,
                        summary = EXCLUDED.summary,
                        sentiment_analysis = EXCLUDED.sentiment_analysis,
                        last_modified_at = NOW();
                """, (data["memory_entry"], data["memory_type"], memory_content, memory_content, summary, sentiment_label, 1.0, 1.0, 0.1))  # Default confidence, importance, decay rate

            conn.commit()

        return jsonify({"message": "Memory stored successfully with full metadata!"})


    @app.route('/update_memory', methods=['POST'])
    def update_memory():
        data = request.get_json()
        memory_entry = data.get('memory_entry')
        if not memory_entry:
            return jsonify({'error': 'Missing memory_entry'}), 400

        try:
            file_path = f'memory/{memory_entry}.json'
            if not os.path.exists(file_path):
                return jsonify({'error': 'Memory entry not found'}), 404

            with open(file_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)

            existing.update({
                'content': data.get('updated_content', existing.get('content', '')),
                'importance_score': data.get('importance_score', ''),
                'tags': data.get('tags', ''),
                'sentiment_analysis': data.get('sentiment_analysis', '')
            })

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing, f, indent=2)

            return jsonify({'status': 'Memory updated'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/retrieve_memory', methods=['POST'])
    def retrieve_memory():
        data = request.get_json()
        memory_entry = data.get('memory_entry')
        if not memory_entry:
            return jsonify({'error': 'Missing memory_entry'}), 400

        try:
            file_path = f'memory/{memory_entry}.json'
            if not os.path.exists(file_path):
                return jsonify({'error': 'Memory entry not found'}), 404

            with open(file_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)
            return jsonify({'memory': memory}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/link_memories', methods=['POST'])
    def link_memories():
        data = request.get_json()
        memory_entry = data.get('memory_entry')
        links = data.get('linked_memories', '')
        if not memory_entry:
            return jsonify({'error': 'Missing memory_entry'}), 400

        try:
            file_path = f'memory/{memory_entry}.json'
            if not os.path.exists(file_path):
                return jsonify({'error': 'Memory entry not found'}), 404

            with open(file_path, 'r', encoding='utf-8') as f:
                memory = json.load(f)

            memory['linked_memories'] = links

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2)

            return jsonify({'status': 'Memories linked'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

