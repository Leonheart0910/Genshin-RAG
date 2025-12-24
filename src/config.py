import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.llms.upstage import Upstage  # [추가] Upstage Solar 라이브러리
from llama_index.llms.gemini import Gemini
from llama_index.llms.groq import Groq
from llama_index.embeddings.gemini import GeminiEmbedding

# .env 파일 로드
load_dotenv()

# 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "source")
DB_DIR = os.path.join(BASE_DIR, "data", "vector_db")


def init_settings():
    # 1. API 키 확인
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    solar_key = os.getenv("SOLAR_API_KEY")

    if not all([google_key, groq_key, solar_key]):
        raise ValueError(".env 파일에 필요한 API 키(GOOGLE, GROQ, SOLAR) 중 일부가 없습니다.")

    # 2. LLM 설정 (현재 Upstage Solar 사용)
    # 한국어 이해도가 높고 추론 능력이 좋아 Auto-Retrieval에 적합합니다.
    Settings.llm = Upstage(
        model="solar-pro2",  # 혹은 "solar-1-mini-chat"
        api_key=solar_key,
        temperature=0.1
    )

    """
    # 필요에 따라 다른 모델로 교체할 때 아래 주석을 활용하세요.

    # [Groq - 초고속 추론]
    # Settings.llm = Groq(model="llama-3.1-8b-instant", api_key=groq_key)

    # [Gemini - 강력한 멀티모달/긴 문맥]
    # Settings.llm = Gemini(model_name="models/gemini-2.5-flash", api_key=google_key)
    """

    # 3. 임베딩 모델 설정 (Gemini 유지)
    # Solar는 임베딩 API도 제공하지만, 기존 벡터 DB와의 호환성을 위해 Gemini를 유지합니다.
    Settings.embed_model = GeminiEmbedding(
        model_name="models/text-embedding-004",
        api_key=google_key
    )