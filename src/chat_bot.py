import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.postprocessor import SentenceTransformerRerank  # [추가] 리랭커 모듈
from config import init_settings, DB_DIR


def chat():
    init_settings()

    print("지식 저장소를 불러오는 중...")
    db = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db.get_or_create_collection("genshin_lore")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    index = VectorStoreIndex.from_vector_store(vector_store)

    # [핵심 수정] 리랭커 모델 설정
    # RTX 3090이 있으므로 'BAAI/bge-reranker-v2-m3' 같은 고성능 모델 사용 가능
    # 처음 실행 시 모델을 다운로드 받느라 시간이 조금 걸립니다.
    reranker = SentenceTransformerRerank(
        model="BAAI/bge-reranker-v2-m3",
        top_n=5  # 최종적으로 LLM에게 넘겨줄 문서 개수 (정예 멤버)
    )

    # 쿼리 엔진 생성
    query_engine = index.as_query_engine(
        similarity_top_k=20,  # [핵심] 일단 20개를 넓게 가져옵니다. (생일 문서가 여기 포함되도록)
        node_postprocessors=[reranker],  # 가져온 20개를 리랭커가 검사해서 순위를 뒤집습니다.
        system_prompt="당신은 티바트 대륙의 역사 기록관입니다. 제공된 문맥(Context)을 꼼꼼히 확인하여 사실에 기반해 답변하세요."
    )

    print("=== 원신 AI 기록관 (With Reranker) ===")
    while True:
        user_input = input("\n질문: ")
        if user_input.lower() in ["q", "exit"]:
            break

        response = query_engine.query(user_input)
        print(f"\n답변: {response}\n")

        # [디버깅] 리랭커가 선택한 문서 확인 (이제 생일이 1등으로 뜰 겁니다)
        print("=" * 20 + " [최종 선택된 문서] " + "=" * 20)
        for node in response.source_nodes:
            print(f"[점수: {node.score:.4f}] {node.node.get_content()[:50]}...")
        print("=" * 60)


if __name__ == "__main__":
    chat()