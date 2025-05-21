from flask import Flask
import openai
import os
from modules.bridge.kobold_bridge import local_generate
from modules.perception.perception_core import interpret_frame
from modules.tasks.Action_Dispatcher import ActionDispatcher
from modules.system.endpoints_extra import register_routes as register_extra_routes
from modules.files.file_ops import register_file_ops
from modules.files import file_ops
from modules.system.system_tools import register_system_tools
from modules.memory.tiered_memory_system import register_tiered_memory_endpoint
from modules.memory.tiered_memory_system import force_migrate
from modules.tokens.token_chunk_manager import register_token_chunk_endpoints
from modules.perception.stream_audio import register_stream_audio_endpoint
from modules.perception.stream_vision import register_stream_vision_endpoint
from modules.memory.tiered_memory.memory_controller import memory_bp
from modules.VS.vs_module import vs_blueprint
from modules.chat.chat_handler import chat_bp
from modules import vision_streamer 
from Chromadb import get_openai_embedding
from modules.memory.tiered_memory.memory_router import memory_api as legacy_memory_api
from modules.memory.tiered_memory.memory_router import store_memory, retrieve_memory, delete_memory, list_memory_keys, promote_memory, tag_memory, rename_memory, archive_memory, query_embeddings, create_embedding
from modules.assistants.assistant_tools_blueprint import assistant_tools

app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"



# 🔌 Register core systems
app.register_blueprint(assistant_tools)
print("☑️ Assistant tools available for access!")
app.register_blueprint(chat_bp)
print("☑️ Chat Online")
register_extra_routes(app)
print("☑️ Extra Routes Registered")
file_ops.register_file_ops(app)
print("☑️ File Ops Registered")
register_system_tools(app)
print("☑️ Forge Toolset Available for Use")
register_tiered_memory_endpoint(app)
print("🧠 Memory Tiers Layered and Ready")
register_token_chunk_endpoints(app)
print("🧠 Token Cutter Ready for Chunking")
register_stream_audio_endpoint(app)
print("☑️ Audio Streamer Ready to Listen")
register_stream_vision_endpoint(app)
print("☑️ Vision Ready")
app.register_blueprint(legacy_memory_api, url_prefix='/legacy_memory')
print("🧠 Legacy Memory Fallback Available")
app.register_blueprint(vs_blueprint)
print("☑️  Visual Studio endpoints registered.")
app.register_blueprint(memory_bp, url_prefix="/memory")
print("🧠 Memory API module registered.")
try:
    from modules.perception.perception_core import interpret_audio, interpret_frame
    from modules.perception.perception_core import register_perception_core_endpoints
    register_perception_core_endpoints(app)
    print("✅ Perception Core endpoints registered.")
except ImportError as e:
    print("⚠️ Perception Core not loaded:", e)

# 🧠 Initialize perception systems (if setup is required)
#initialize_perception_core()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

    for rule in app.url_map.iter_rules():
        print(f"📍 {rule.endpoint} — {rule}")
