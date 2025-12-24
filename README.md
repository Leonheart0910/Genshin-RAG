

# 📜 세계수 : 티바트 지맥 정보 시스템 (Teyvat Ley Line RAG)
### 별과 심연을 향해! 안녕 여행자, 혹시 룩카데바타를 만났어? 세계수에게 티바트의 별하늘의 진실에 대해 물어 보렴.
<img width="1000" height="562" alt="image" src="https://github.com/user-attachments/assets/3773aede-b204-4e80-98bc-602e74816fe8" />

본 프로젝트는 원신(Genshin Impact) 티바트 대륙의 방대한 정보 (세계관, 스토리, 캐릭터 설정 등)을 보다 정확하게 검색하고 답변하는 RAG(Retrieval-Augmented Generation) 시스템입니다. 

## 제작중 (열심히 데이터 수집하고 태깅중...)

## 🛠 기술 스택

- **Framework**: LlamaIndex
- **LLM**: Upstage Solar (solar-pro), Google Gemini 1.5/2.0, Groq (Llama 3.1/3.3)
- **Embedding**: Google Gemini (text-embedding-004)
- **Vector Database**: ChromaDB
- **Language**: Python 3.10+

## 📂 프로젝트 구조
```plaintext
genshin-rag/
├── data/
│   ├── source/          # 원본 JSON 데이터 파일 (지식 소스)
│   └── vector_db/       # ChromaDB 물리 저장소 (인덱싱 데이터)
├── src/
│   ├── config.py        # API 키 보안 및 모델 설정 관리
│   ├── build_db.py      # 데이터 인덱싱 및 DB 초기화/구축 스크립트
│   └── chat_bot.py      # 챗봇 실행 및 Auto-Retrieval 검색 로직
├── .env                 # API 키 관리 파일 (GOOGLE, GROQ, SOLAR)
└── requirements.txt     # 프로젝트 의존성 패키지 목록
```

## ⚙️ 설정 및 설치

### 1. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 발급받은 API 키를 입력합니다.
```ini
GOOGLE_API_KEY=your_google_key
GROQ_API_KEY=your_groq_key
SOLAR_API_KEY=your_upstage_key
```

### 2. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

## 📖 사용 방법

### 1. 데이터 베이스 구축 (Indexing)

`data/source/` 폴더에 구조화된 JSON 데이터를 넣은 후 인덱싱을 수행합니다. 실행 시 기존 데이터는 초기화되고 최신 JSON 내용으로 DB가 새로 구축됩니다.
```bash
python src/build_db.py
```

### 2. 챗봇 실행 (Query)

질문을 입력하면 AI가 질문의 의도를 분석해 적절한 메타데이터 필터를 적용하고 답변을 생성합니다.
```bash
python src/chat_bot.py
```
