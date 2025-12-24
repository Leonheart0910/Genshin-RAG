# 대화용 스크립트

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from config import init_settings, DB_DIR


def chat():
    init_settings()

    # 저장된 DB 불러오기
    print("티바트 지맥 정보를 불러오는 중...")
    db = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db.get_or_create_collection("genshin_lore")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # 인덱스 로드 (from_vector_store 사용)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
    )

    # 쿼리 엔진 생성
    query_engine = index.as_query_engine(
        similarity_top_k=3,
        system_prompt="당신은 티바트 대륙의 역사 기록관 입니다. 사실에 기반하여 답변하세요."
    )

    print("=== 티바트 세계수 (종료: q) ===")
    while True:
        user_input = input("\n여행자 : ")
        if user_input.lower() == "q":
            break

        response = query_engine.query(user_input)
        print(f"세계수 : {response}")


if __name__ == "__main__":
    chat()