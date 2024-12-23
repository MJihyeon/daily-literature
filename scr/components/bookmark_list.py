from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame, QPushButton)  # PyQt6의 GUI 컴포넌트
from PyQt6.QtCore import Qt     # Qt 핵심 기능
from PyQt6.QtGui import QFont   # 폰트 기능
from utils.data_manager import save_bookmarks   # 북마크 저장 기능

# 북마크 목록 창 클래스
class BookmarkWindow(QMainWindow):
    def __init__(self, bookmarked_quotes):
        super().__init__()  # 부모 클래스 초기화
        self.bookmarked_quotes = bookmarked_quotes  # 북마크된 구절 저장
        self.initUI(bookmarked_quotes)  # UI 초기화
        
    def initUI(self, bookmarked_quotes):
        self.setWindowTitle("북마크 목록")  # 제목
        self.setFixedSize(350, 500)     # 창 크기
        
        # 중앙 위젯
        central_widget = QWidget()  # 메인 컨테이너 위젯
        self.setCentralWidget(central_widget)   # 중앙 위젯으로 설정
        
        # 메인 레이아웃
        layout = QVBoxLayout(central_widget)    # 세로 방향
        
        # 스크롤 영역
        scroll = QScrollArea()
        scroll.setWidgetResizable(True) # 내용에 따라 크기 조절
        
        # 스크롤 내용을 담을 위젯
        content_widget = QWidget()  # 컨텐츠를 담는 위젯
        content_layout = QVBoxLayout(content_widget)    # 세로 방향
        
        # 제목
        title = QLabel("북마크된 구절") # 제목 레이블
        title.setFont(QFont('Arial', 16))   # 폰트, 크기
        title.setStyleSheet('padding: 10px;')   # 여백
        content_layout.addWidget(title)
        
        # 북마크 목록
        if not bookmarked_quotes:   # 북마크 없는 경우 아래 문구 표시
            no_bookmarks = QLabel("북마크된 구절이 없습니다.")
            no_bookmarks.setAlignment(Qt.AlignmentFlag.AlignCenter) # 가운데 정렬
            content_layout.addWidget(no_bookmarks)
        else:   # 북마크 있는 경우
            for i, quote in enumerate(bookmarked_quotes):   # 각 북마크에 대해
                quote_widget = self.create_quote_widget(quote, i)   # 구절 위젯 생성
                content_layout.addWidget(quote_widget)  # 레이아웃 추가
        
        content_layout.addStretch()     # 남는 공간 채움
        scroll.setWidget(content_widget)    # 스크롤 영역에 컨텐츠 설정
        layout.addWidget(scroll)    # 레이아웃 추가
    
    # 북마크된 구절 위젯
    def create_quote_widget(self, quote, index):
        widget = QFrame()   # 프레임 위젯
        widget.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #ddd;
                margin: 5px;
                padding: 10px;
            }
        ''')    # 배경색, 모서리 라운드, 테두리, 바깥 여백, 안쪽 여백
        
        layout = QVBoxLayout(widget)    # 세로 방향
        
        # 상단 영역 (구절과 삭제 버튼) 
        top_layout = QHBoxLayout()  # 가로 방향
        
        # 구절 텍스트
        text = QLabel(quote["text"])
        text.setWordWrap(True)  # 자동 줄바끔
        text.setStyleSheet('font-size: 14px; color: #333;') # 폰트 크기, 색상
        top_layout.addWidget(text)
        
        # 삭제 버튼
        delete_btn = QPushButton('×')   # 버튼
        delete_btn.setFixedSize(20, 20) # 버튼 크기
        delete_btn.setStyleSheet('''
            QPushButton {
                border: none;
                color: #999;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
            QPushButton:hover {
                color: #ff4444;
            }
        ''')    # 테두리, 색상, 글자 크기, 글씨 굵기, 배경, 마우스 오버시 색 표시
        
        # 클릭 이벤트 연결
        delete_btn.clicked.connect(lambda: self.delete_bookmark(index))
        top_layout.addWidget(delete_btn)
        
        # 작품 정보 레이블
        info = QLabel(f"{quote['work']}\n{quote['author']} | {quote['genre']}")
        info.setStyleSheet('font-size: 12px; color: #666;')
        
        layout.addLayout(top_layout)    # 상단 레이아웃 추가
        layout.addWidget(info)  # 작품 정보 추가
        
        return widget
    
    # 북마크 삭제 메서드
    def delete_bookmark(self, index):
         # 북마크 리스트에서 제거
        self.bookmarked_quotes.pop(index)
        # 변경사항 저장
        save_bookmarks(self.bookmarked_quotes)
        # UI 새로고침
        self.initUI(self.bookmarked_quotes)