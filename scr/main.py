# main.py
import sys  # 파이썬 인터리프리터 시스템 모듈
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout # PyQt6 GUI 위젯들 import
from components.quote_card import QuoteCard # QuoteCard 컴포넌트

# MainWindow 클래스 (회색 전체 창)
# QMainWindow를 상속받아 메인 창 생성
class MainWindow(QMainWindow):
    def __init__(self):     # 클래스 초기화 메서드
        super().__init__()  # QMainWindow 초기화 메서드
        self.setWindowTitle('문학 구절 생성기')     # 창의 제목
        self.setFixedSize(400, 600)     # 전체 창 사이즈 설정 (400x600)
        
        # 중앙 위젯 (하얀색 배경 카드)
        central_widget = QWidget()      # 중앙 위젯 생성
        self.setCentralWidget(central_widget)   # 중앙 위젯을 메인 창에 설정
        layout = QVBoxLayout(central_widget)    # 세로 방향 레이아웃 생성
        layout.setContentsMargins(20, 20, 20, 20)   # 레이아웃 여백 (좌, 상, 우, 하)
        
        # 카드 생성 (내용이 적히는 부분)
        self.quote_card = QuoteCard()   # QApplication 인스턴스
        layout.addWidget(self.quote_card)   # 레이아웃에 카드 추가

def main():
    app = QApplication(sys.argv)    # QApplication 인스턴스
    window = MainWindow()   # MainWindow 인스턴스
    window.show()       # 창 표시
    sys.exit(app.exec())    # 앱 실행 및 종료 시 정리

if __name__ == '__main__':  # 파일이 직접 실행될 때만 main함수 실행
    main()