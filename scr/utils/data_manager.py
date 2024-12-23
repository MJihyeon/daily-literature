# utils/data_manager.py
import json # json 파일 처리 모듈
from pathlib import Path    # 파일 경로 처리 모듈

# 문학 구절 데이터 로드 - 목록을 딕셔너리 리스트 형태로 반환
def load_quotes():
    return [
        {
            "text": "산다는 것은 치열한 전투이다.", # 문학 구절
            "author": "루이제 린저",    # 작가
            "work": "산정 너머",    # 작품명
            "genre": "소설" # 장르
        },
        {
            "text": "삶이 있는 한 희망은 있다.",
            "author": "키케로",
            "work": "신의 본성에 관하여",
            "genre": "철학"
        },
        {
            "text": "꿈을 이루고자 하는 용기만 있다면 모든 꿈을 이룰 수 있다.",
            "author": "월트 디즈니",
            "work": "생각록",
            "genre": "에세이"
        },
        {
            "text": "오늘 할 수 있는 일에 전력을 다하라",
            "author": "괴테",
            "work": "격언집",
            "genre": "시"
        }
    ]

# 저장된 북마크 데이터 로드
def load_bookmarks():
    bookmark_file = Path("bookmarks.json")  # bookmarks.json 파일 경로 설정
    if not bookmark_file.exists():
        save_bookmarks([])  # 파일이 없으면 빈 파일 생성
    try:
        with open(bookmark_file, 'r', encoding='utf-8') as f:   # 파일을 열어서 데이터 읽음
            return json.load(f) # JSON 형식의 데이터를 파이썬 객체로 변환하여 반환
    except:
        return []   # 파일 읽기 실패시 빈 리스트 반환

# 북마크 데이터 저장
def save_bookmarks(bookmarks):
    with open('bookmarks.json', 'w', encoding='utf-8') as f:    # 북마크 데이터 Json형식으로 변환 -> 파일에 작성, 유니코드 문자 그대로 저장, 들여쓰기 2칸
        json.dump(bookmarks, f, ensure_ascii=False, indent=2)