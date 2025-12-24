# 설정 관리 (모델명, 청킹 사이즈 ...)

import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

# .env 파일 로드
load_dotenv()

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "source")
DB_DIR = os.path.join(BASE_DIR, "data", "vector_db")

def init_settings():
    # 모델 설정 초기화
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError(".env 파일에 GOOGLE_API_KEY가 없습니다.")

    Settings.llm = Gemini(
        model_name="models/gemini-2.0-flash-lite",
        temperature=0.1
    )
    Settings.embed_model = GeminiEmbedding(
        model_name="models/text-embedding-004"
    )