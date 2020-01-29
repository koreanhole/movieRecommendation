# movieRecommendation

imdb의 Movie dataset를 이용해서 사용자가 가장 좋아할만한 영화를 추천해주는 pyqt5 기반 GUI 어플리케이션.
imdb의 api를 통해 imdb서버의 포스터 이미지를 가져온 후 이를 표시해준다.

다음과 같은 추천기능을 갖고 있다.
  1. 인구통계학적 필터링을 이용한 weighted rating을 통한 상위 6개 영화 추천
  2. 사용자의 평점을 기반으로 코사인 유사도를 통한 영화 추천
  3. 각 영화마다의 특징을 추출한 후 특징을 기반으로 한 weighted rating을 통한 상위 6개의 영화 추천
  4. 영화를 검색하면 코사인 유사도를 이용해서 검색한 영화와 가장 유사한 영화를 표시해준다.
  
작동영상: https://youtu.be/g_Akbj57Oho
