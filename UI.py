import sys
import urllib.request
from Recommendation.System import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QWidget, QGroupBox,
                             QTabWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QLineEdit)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.Qt import Qt



class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Movie Recommendation')

        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.showMaximized()

class MyTabWidget(QScrollArea):
    def __init__(self, parent):

        #label의 텍스트 포맷 지정 -> 글씨 크기는 20, 볼드체.
        textFormat = QFont()
        textFormat.setBold(True)
        textFormat.setPointSize(20)

        super(MyTabWidget, self).__init__(parent)
        self.setMouseTracking(True)

        self.layout = QVBoxLayout()

        # Initialize tab screen
        #기존의 데이터로 사용자 맞춤 추천을 하는 tab1
        #사용자가 영화제목을 검색하면 이와 가장 유사한 영화를 보여주는 검색기능을 하는 tab2로 구성.
        self.tabs = QTabWidget()
        self.tab1 = QScrollArea()
        self.tab1.setWidget(QWidget())
        self.tab2 = QScrollArea()
        self.tab2.setWidget(QWidget())

        self.tabs.resize(350, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "추천영상")
        self.tabs.addTab(self.tab2, "검색")

        # Create first tab
        self.EntireLayout = QVBoxLayout(self)
        self.tab1.setWidgetResizable(True)
        self.EntireLayout.setAlignment(Qt.AlignTop)


        # Creating Best Movie Layout
        self.TrendingLayout = QVBoxLayout(self.widget())
        self.EntireLayout.addLayout(self.TrendingLayout)
        trendingLabel = QLabel("Best Movies")
        trendingLabel.setFont(textFormat)
        self.TrendingLayout.addWidget(trendingLabel)
        self.TrendingPosterLayout = QHBoxLayout(self)
        self.TrendingLayout.addLayout(self.TrendingPosterLayout)
        self.trending()
        self.TrendingLayout.setAlignment(Qt.AlignTop)

        # Creating Popularity Layout
        self.PopularityLayout = QVBoxLayout(self.widget())
        self.EntireLayout.addLayout(self.PopularityLayout)
        popularityLabel = QLabel("Popularity")
        popularityLabel.setFont(textFormat)
        self.PopularityLayout.addWidget(popularityLabel)
        self.PopularPosterLayout = QHBoxLayout(self)
        self.PopularityLayout.addLayout(self.PopularPosterLayout)
        self.popularity()
        self.PopularityLayout.setAlignment(Qt.AlignTop)

        # Creating user Simialrity Layout
        self.SimilarityLayout = QVBoxLayout(self.widget())
        self.EntireLayout.addLayout(self.SimilarityLayout)
        similarityLabel = QLabel("사용자가 즐겨본 'Avatar'와 유사한 영화입니다.")
        similarityLabel.setFont(textFormat)
        self.SimilarityLayout.addWidget(similarityLabel)
        self.SimilarPosterLayout = QHBoxLayout(self)
        self.SimilarityLayout.addLayout(self.SimilarPosterLayout)
        self.similarity()
        self.SimilarityLayout.setAlignment(Qt.AlignTop)

        # Creating Genre Similarity Layout1
        self.GenreLayout1 = QVBoxLayout(self.widget())
        self.EntireLayout.addLayout(self.GenreLayout1)
        genreLabel1 = QLabel("Romance 추천영화")
        genreLabel1.setFont(textFormat)
        self.GenreLayout1.addWidget(genreLabel1)
        self.GenrePosterLayout1 = QHBoxLayout(self)
        self.GenreLayout1.addLayout(self.GenrePosterLayout1)
        self.genre1()
        self.GenreLayout1.setAlignment(Qt.AlignTop)

        # Creating Genre Similarity Layout2
        self.GenreLayout2 = QVBoxLayout(self.widget())
        self.EntireLayout.addLayout(self.GenreLayout2)
        genreLabel2 = QLabel("Action 추천영화")
        genreLabel2.setFont(textFormat)
        self.GenreLayout2.addWidget(genreLabel2)
        self.GenrePosterLayout2 = QHBoxLayout(self)
        self.GenreLayout2.addLayout(self.GenrePosterLayout2)
        self.genre2()
        self.GenreLayout2.setAlignment(Qt.AlignTop)



        #tab1의 스크롤 레이아웃 지정.
        groupBox = QGroupBox()
        groupBox.setLayout(self.EntireLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        self.scrollLayout = QVBoxLayout()
        self.scrollLayout.addWidget(scroll)
        self.tab1.setLayout(self.scrollLayout)

        #tab2(검색화면)의 레이아웃 지정.
        self.tab2.EntireLayout = QVBoxLayout()
        self.SearchLayout = QVBoxLayout()
        self.SearchTextLayout = QHBoxLayout()
        self.PosterLayout1 = QHBoxLayout()
        self.PosterLayout2 = QHBoxLayout()
        self.PosterLayout3 = QHBoxLayout()

        self.label2 = QLabel("Search Movies")
        self.label2.setFixedHeight(30)
        self.label2.setFont(textFormat)
        self.SearchLayout.addWidget(self.label2)

        self.movieSearchField = QLineEdit(self)
        searchButton = QPushButton("검색")
        searchButton.clicked.connect(self.clickedMethod)
        self.movieSearchField.setFixedHeight(30)
        searchButton.setFixedHeight(30)
        #검색어를 넣을 수 있는 텍스트필드 지정.
        self.SearchTextLayout.addWidget(self.movieSearchField)
        self.SearchTextLayout.addWidget(searchButton)
        self.SearchLayout.addLayout(self.SearchTextLayout)
        self.SearchLayout.setAlignment(Qt.AlignTop)
        #검색결과 나오는 포스터의 이미지를 넣을 수 있는 레이아웃 3개 지정.
        self.PosterLayout1.setAlignment(Qt.AlignTop)
        self.PosterLayout2.setAlignment(Qt.AlignTop)
        self.PosterLayout3.setAlignment(Qt.AlignTop)
        self.tab2.EntireLayout.addLayout(self.SearchLayout)
        self.tab2.EntireLayout.addLayout(self.PosterLayout1)
        self.tab2.EntireLayout.addLayout(self.PosterLayout2)
        self.tab2.EntireLayout.addLayout(self.PosterLayout3)

        #tab2(검색화면)의 스크롤 기능 구현.
        tab2_groupBox = QGroupBox()
        tab2_groupBox.setLayout(self.tab2.EntireLayout)
        tab2_scroll = QScrollArea()
        tab2_scroll.setWidget(tab2_groupBox)
        tab2_scroll.setWidgetResizable(True)
        self.tab2_scrollLayout = QVBoxLayout()
        self.tab2_scrollLayout.addWidget(tab2_scroll)

        self.tab2.setLayout(self.tab2_scrollLayout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    #trending layout에 영화 포스터를 띄우는 함수.
    def trending(self):
        idx = trendingNow()
        for i in range(6):
            self.thumb = QLabel(self)
            url = get_poster_urls(movie_id[idx[i]])
            image = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap = pixmap.scaledToHeight(250)
            self.thumb.setPixmap(pixmap)
            self.TrendingPosterLayout.addWidget(self.thumb)

    #popularity 레이아웃에 영화 포스터를 띄우는 기능 구현.
    def popularity(self):
        idx = popularityNow()
        for i in range(6):
            self.thumb = QLabel(self)
            url = get_poster_urls(movie_id[idx[i]])
            image = urllib.request.urlopen(url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap = pixmap.scaledToHeight(250)
            self.thumb.setPixmap(pixmap)
            self.PopularPosterLayout.addWidget(self.thumb)

    #similarity 레이아웃에 영화 포스터를 띄우는 기능 구현.
    def similarity(self):
        url = similarity1()
        for i in range(6):
            self.thumb = QLabel(self)
            image = urllib.request.urlopen(url[i]).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap = pixmap.scaledToHeight(250)
            self.thumb.setPixmap(pixmap)
            self.thumb.resize(300, 300)
            self.SimilarPosterLayout.addWidget(self.thumb)

    #Romance장르 기반 추천을 통해 나온 결과로 영화 포스터를 띄우는 기능 구현.
    def genre1(self):
        url = romance_chart()
        for i in range(6):
            self.thumb = QLabel(self)
            image = urllib.request.urlopen(url[i]).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap = pixmap.scaledToHeight(250)
            self.thumb.setPixmap(pixmap)
            self.GenrePosterLayout1.addWidget(self.thumb)

    #Action장르 기반 추천을 통해 나온 결과로 영화 포스터를 띄우는 기능 구현.
    def genre2(self):
        url = action_chart()
        for i in range(6):
            self.thumb = QLabel(self)
            image = urllib.request.urlopen(url[i]).read()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap = pixmap.scaledToHeight(250)
            self.thumb.setPixmap(pixmap)
            self.GenrePosterLayout2.addWidget(self.thumb)

    #tab2에서 검색 버튼을 눌렀을때 실행되는 함수
    #텍스트필드의 검색어를 받아와서 검색 후 나오는 결과를 통해 이미지를 띄워준다.
    def clickedMethod(self):
        self.idx = []
        self.movie = self.movieSearchField.text()
        self.idx = get_recommendations(self.movie)
        k = 0
        for i in range(3):
            for j in range(5):
                self.thumb = QLabel(self)
                self.thumb.resize(300,300)
                url = get_poster_urls(movie_id[self.idx[k]])
                image = urllib.request.urlopen(url).read()
                pixmap = QPixmap()
                pixmap.loadFromData(image)
                pixmap = pixmap.scaledToHeight(300)
                self.thumb.setPixmap(pixmap)
                if i == 0:
                    self.PosterLayout1.addWidget(self.thumb)
                elif i == 1:
                    self.PosterLayout2.addWidget(self.thumb)
                elif i == 2:
                    self.PosterLayout3.addWidget(self.thumb)
                k += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())