import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo
from llama_index.core.query_engine import RetrieverQueryEngine
from config import init_settings, DB_DIR


def chat():
    # 1. 설정 초기화
    init_settings()

    print("세계수와 접촉 중...")
    db = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db.get_or_create_collection("genshin_lore")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    # 2. 메타데이터 스키마 정의
    # name과 target의 설명을 명확히 구분하여 AI가 혼동하지 않도록 함
    vector_store_info = VectorStoreInfo(
        content_info="원신(Genshin Impact) 종려(Zhongli) 캐릭터와 리월 지역의 상세 설정, 스토리, 인물 관계 정보",
        metadata_info=[
            MetadataInfo(
                name="category",
                type="str",
                description="정보의 대분류 (예: 프로필, 전투, 인물 관계, 스토리, 장비, 역사)"
            ),
            MetadataInfo(
                name="subcategory",
                type="str",
                description="정보의 소분류 (예: 생일, 전설 임무, 무기, 선인, 신원)"
            ),
            MetadataInfo(
                name="name",
                type="str",
                description="질문의 '핵심 대상' 이름. 종려 본인뿐만 아니라 야타용왕, 귀종, 호두, 소, 타르탈리아 등 관련 인물이나 기술명은 모두 이 키를 사용하세요."
            ),
            MetadataInfo(
                name="region",
                type="str",
                description="국가 또는 지역 (예: 리월, 몬드)"
            ),
            MetadataInfo(
                name="date",
                type="str",
                description="날짜 관련 정보 (예: 12월 31일)"
            )
        ]
    )

    # 3. 자동 검색기(AutoRetriever) 생성
    retriever = VectorIndexAutoRetriever(
        index,
        vector_store_info=vector_store_info,
        similarity_top_k=5,
        verbose=True  # AI가 어떤 필터를 걸었는지 터미널에 출력
    )

    # 4. 쿼리 엔진 연결
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        system_prompt="당신은 티바트 대륙의 역사 기록관입니다. 검색된 정보를 바탕으로 답변하세요. 모르는 내용은 지어내지 마세요."
    )

    print("=== 티바트 세계수(Auto-Filter Mode) ===")
    print("질문에 따라 자동으로 메타데이터 필터를 적용.")

    while True:
        user_input = input("\n여행자 (종료: q): ")
        if user_input.lower() in ["q", "exit"]:
            break

        response = query_engine.query(user_input)
        print(f"\n세계수 : {response}\n")

        # [디버깅] 검색 결과 및 적용된 메타데이터 확인
        print("-" * 50)
        if response.source_nodes:
            print(f"참고한 문서 개수: {len(response.source_nodes)}개")
            first_node = response.source_nodes[0]
            print(f"1순위 문서 메타데이터: {first_node.metadata}")
            print(f"내용 일부: {first_node.node.get_content()[:50]}...")
        else:
            print("조건에 맞는 문서를 찾지 못했습니다.")
        print("-" * 50)


if __name__ == "__main__":
    chat()