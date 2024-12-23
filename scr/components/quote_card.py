from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QMenu) # PyQt6의 GUI 컴포넌트
from PyQt6.QtCore import Qt # Qt 핵심 기능
from utils.data_manager import load_quotes, save_bookmarks, load_bookmarks  # 데이터 관리 함수

# QuoteCard 클래스
class QuoteCard(QFrame):
   def __init__(self):  # 초기화 메서드
       super().__init__()   # 부모 클래스 초기화
       
       # 데이터 초기화
       self.quotes = load_quotes()  # 문학구절 로드
       self.bookmarked_quotes = load_bookmarks()    # 저장된 북마크 로드
       self.current_quote = None    # 현재 표시된 구정 저장
       
       # 메인 레이아웃
       main_layout = QVBoxLayout(self)  # 세로 방향
       main_layout.setContentsMargins(0, 0, 0, 0)   # 여백 제거 (좌, 상, 우, 하)
       main_layout.setSpacing(10)   # 간격 설정
       
       # 하얀색 카드 생성
       card = QWidget()     # 배경색, 모서리 라운드, 겉 테두리 설정
       card.setStyleSheet('''
           QWidget {
               background-color: white;
               border-radius: 10px;
               border: 1px solid #ddd; 
           }
       ''')
       card_layout = QVBoxLayout(card)  # 카드 레이아웃
       card_layout.setSpacing(15)       # 내부 요소 간격
       
       # 타이틀 추가
       title = QLabel('문학 구절 생성기')   # 타이틀
       title.setStyleSheet('''
           QLabel {
               color: #333;
               font-size: 18px;
               font-weight: bold;
               padding: 5px;
           }
       ''')     # 색, 글씨 크기, 글씨 굵기, 내부 여백
       
       # 상단 바 (날짜, 북마크 버튼)
       top_bar = QWidget()  # 위젯 생성
       top_bar.setFixedHeight(30)  # 높이
       top_layout = QHBoxLayout(top_bar)
       top_layout.setContentsMargins(12, 7, 12, 7)  # 상하 여백
       top_layout.setSpacing(5)  # 요소 간격
       
       # 날짜 레이블 - 날짜, 글씨 색, 크기
       date_label = QLabel('2024.12.22')
       date_label.setStyleSheet('''
           QLabel {
               color: #666;
               font-size: 12px;
           }
       ''')
       
       # 버튼 컨테이너 (북마크, 공유 버튼 담는 영역)
       buttons_widget = QWidget()
       buttons_layout = QHBoxLayout(buttons_widget) # 가로 방향
       buttons_layout.setContentsMargins(0, 0, 0, 0)    # 여백 제거
       buttons_layout.setSpacing(5) # 버튼 간격
       
       # 북마크 목록, 북마크, 공유 버튼
       self.bookmark_list_btn = QPushButton('📚')
       self.bookmark_btn = QPushButton('☆')
       self.share_btn = QPushButton('📤')
       
       # 버튼 스타일
       for btn in [self.bookmark_list_btn, self.bookmark_btn, self.share_btn]:
           btn.setFixedSize(24, 24) # 버튼 크기 고정
           btn.setStyleSheet('''
               QPushButton {
                   border: none;
                   font-size: 15px;
                   background: transparent;
                   margin-top: -15px;
               }
           ''') # 테두리, 글자 크기, 배경 색, 위치 이동 (상)
           buttons_layout.addWidget(btn)    # 레이아웃에 버튼 추가
           
       # 버튼 연결
       self.bookmark_list_btn.clicked.connect(self.show_bookmark_list)  # 북마크 목록 표시
       self.bookmark_btn.clicked.connect(self.toggle_bookmark)  # 북마크 추가/제거
       self.share_btn.clicked.connect(self.show_share_menu)     # 공유 메뉴 표시
       
       # 상단 바에 날짜, 버튼 추가
       top_layout.addWidget(date_label)     # 날짜 (왼쪽)
       top_layout.addStretch()              # 빈 공간 (중간)
       top_layout.addWidget(buttons_widget) # 버튼 (오른쪽)
       
       # 구절 레이블
       self.quote_label = QLabel('터치하여 오늘의 구절 보기')   # 문구
       self.quote_label.setWordWrap(True)   # 자동 줄 바꿈
       self.quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 가운데 정렬
       self.quote_label.setMinimumHeight(200)   # 최소 높이
       self.quote_label.setStyleSheet('''
           QLabel {
               font-size: 14px;
               color: #333;
               padding: 20px;
           }
       ''') # 글자 크기, 색, 여백
       
       # 작품 정보 레이블
       self.work_info = QLabel('작품명\n작가명 | 장르')
       self.work_info.setStyleSheet('''
           QLabel {
               font-size: 13px;
               color: #666;
               padding: 10px;
           }
       ''') # 글자 크기, 색, 여백
       
       # 모든 요소를 카드 레이아웃에 추가
       card_layout.addWidget(title) # 제목
       card_layout.addWidget(top_bar)   # 상단 바
       card_layout.addWidget(self.quote_label)  # 구절
       card_layout.addWidget(self.work_info)    # 작품 정보
       
       # 메인 레이아웃에 카드 추가
       main_layout.addWidget(card)
       
       # 카드 클릭 이벤트 설정
       self.quote_label.mousePressEvent = self.show_new_quote   # 클릭 연결
   
   # 새로운 구절 표시 메서드
   def show_new_quote(self, event):
       import random    # 랜덤 표시
       if self.quotes:
           self.current_quote = random.choice(self.quotes)  # 랜덤 구절 선택
           self.quote_label.setText(self.current_quote["text"]) # 구절 표시
           self.work_info.setText(f"{self.current_quote['work']}\n{self.current_quote['author']} | {self.current_quote['genre']}")  # 작품 정보
           self.update_bookmark_status()    # 북마크 상태 업데이트
   
   # 북마크 추가/제거 메서드
   def toggle_bookmark(self):
       if not self.current_quote:
           return

        # 현재 북마크 상태 확인
       is_bookmarked = any(bm["text"] == self.current_quote["text"] 
                          for bm in self.bookmarked_quotes)
       
       if is_bookmarked:
           # 북마크 제거
           self.bookmarked_quotes = [bm for bm in self.bookmarked_quotes 
                                   if bm["text"] != self.current_quote["text"]]
           self.bookmark_btn.setText('☆')  # 빈 별로 변경
       else:
           # 북마크 추가
           self.bookmarked_quotes.append(self.current_quote)
           self.bookmark_btn.setText('★')  # 채워진 별로 변경
           
       save_bookmarks(self.bookmarked_quotes)
    
    # 북마크 상태 업데이트
   def update_bookmark_status(self):
       if not self.current_quote:   # 구절이 없는 경우 어떤 작업도 수행X
           return
         
       is_bookmarked = any(bm["text"] == self.current_quote["text"] # 현재 북마크 상태인지 확인  
                          for bm in self.bookmarked_quotes)
       self.bookmark_btn.setText('★' if is_bookmarked else '☆')   # 북마크 상태에 따라 버튼 텍스트 변경
   
   # 공유 메뉴 표시
   def show_share_menu(self):
       if not self.current_quote:   # 구절이 없는 경우 어떤 작업도 수행X
           return
           
       menu = QMenu(self)   # QMenu 객체를 생성하여 공유 메뉴 생성
       
       # 공유 옵션 추가
       gmail_action = menu.addAction("Gmail로 공유")
       insta_action = menu.addAction("Instagram으로 공유")
       kakao_action = menu.addAction("카카오톡으로 공유")
       
       # 옵션 이벤트 연결
       gmail_action.triggered.connect(lambda: self.share_to("gmail"))
       insta_action.triggered.connect(lambda: self.share_to("instagram"))
       kakao_action.triggered.connect(lambda: self.share_to("kakaotalk"))
       
       # 메뉴 표시 (버튼 위치 기준)
       menu.exec(self.share_btn.mapToGlobal(self.share_btn.rect().bottomRight()))
   
   # 플랫폼 공유 메서드
   def share_to(self, platform):
       if not self.current_quote:   # 구절이 없는 경우 어떤 작업도 수행X
           return
           
       share_text = f"{self.current_quote['text']}\n- {self.current_quote['author']}, {self.current_quote['work']}"     # 공유 텍스트 생성
       
       if platform == "gmail": 
           # Gmail 공유 (웹으로 URL 열림)
           import webbrowser
           gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&body={share_text}"
           webbrowser.open(gmail_url)
       else:
           # Instagram, 카카오 - 클립보드 복사로 대체
           from PyQt6.QtWidgets import QApplication
           QApplication.clipboard().setText(share_text)

    # 북마크 목록 창 표시
   def show_bookmark_list(self):
       from components.bookmark_list import BookmarkWindow
       self.bookmark_window = BookmarkWindow(self.bookmarked_quotes)
       self.bookmark_window.show()