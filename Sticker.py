import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QMovie

class Sticker(QtWidgets.QMainWindow):
    def __init__(self, img_path, xy, size=1.0, on_top=False):
        super(Sticker, self).__init__()
        self.timer = QtCore.QTimer(self)
        self.img_path = img_path
        self.xy = xy
        self.from_xy = xy
        self.from_xy_diff = [0,0]
        self.to_xy = xy
        self.to_xy_diff = [0,0]
        self.speed = 60
        self.direction = [0, 0] # x : 0(left), 1(right), y : 0(up), 1(down)
        self.size = size
        self.on_top = on_top
        self.localPos = None

        self.setupUi()
        self.show()

    # 마우스 놓았을 때
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.to_xy_diff == [0,0] and self.from_xy_diff == [0,0]:
            pass
        else:
            self.walk_diff(self.from_xy_diff, self.to_xy_diff, self.speed, restart=True)

    # 마우스 눌렀을 때
    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.localPos = a0.localPos()

    # 드래그할 때
    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.timer.stop()
        self.xy = [(a0.globalX() - self.localPos.x()), (a0.globalY() - self.localPos.y())]
        self.move(*self.xy)

    def walk(self, from_xy, to_xy, speed=60):
        """
        스티커의 움직임을 나타냄
        :param from_xy: 어디에서
        :param to_xy: 어디까지
        :param speed: 어느속도로
        :return: 움직임
        """
        self.from_xy = from_xy
        self.to_xy = to_xy
        self.speed = speed

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.__walkHandler)
        self.timer.start(1000 / self.speed)

    def walk_diff(self, from_xy_diff, to_xy_diff, speed=60, restart=False):
        self.from_xy_diff = from_xy_diff
        self.to_xy_diff = to_xy_diff
        self.from_xy = [self.xy[0] + self.from_xy_diff[0], self.xy[1], self.from_xy_diff[1]]
        self.to_xy = [self.xy[0] + self.to_xy_diff[0], self.xy[1], self.to_xy_diff[1]]
        self.speed = speed
        if restart:
            self.timer.start()
        else:
            self.timer.timeout.connect(self.__walkHandler)
            self.timer.start(1000 / self.speed)

    def __walkHandler(self):
        if self.xy[0] >= self.to_xy[0]:
            self.direction[0] = 0
        elif self.xy[0] < self.from_xy[0]:
            self.direction[0] = 1

        if self.direction[0] == 0:
            self.xy[0] -= 1
        else:
            self.xy[0] += 1

        if self.xy[1] >= self.to_xy[1]:
            self.direction[1] = 0
        elif self.xy[1] < self.from_xy[1]:
            self.direction[1] = 1

        if self.direction[1] == 0:
            self.xy[1] -= 1
        else:
            self.xy[1] += 1

        self.move(*self.xy)

    def setupUi(self):
        """
        위젯을 화면 위에 올리기
        :return:
        """
        # contralWidget 정의 :: 정의 안하면 안보임
        centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(centralWidget)
        # FramelessWindowHint :: 창의 윗부분이 사라짐(닫기, 최소화 등등 있는 것)
        # WindowStaysOnTopHint :: 화면 항상 위에 있어라. 아래 if문을 만족하면
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
                                      if self.on_top else QtCore.Qt.FramelessWindowHint)
        # Wa_ :: 창 배경을 깨끗하고 맑고 투명하게
        self.setWindowFlags(flags)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        label = QtWidgets.QLabel(centralWidget) # 만든 contralWidget을 label에 올리기
        movie = QMovie(self.img_path) # 위치확인
        label.setMovie(movie) # 라벨셋팅
        movie.start()
        movie.stop() # 크기를 구하기위해 한번 켰다끄기
        #사이즈 정의
        w = int(movie.frameRect().size().width() * self.size)
        h = int(movie.frameRect().size().height() * self.size)
        movie.setScaledSize(QtCore.QSize(w, h))
        movie.start()
        # 크기 위치 정의
        self.setGeometry(self.xy[0], self.xy[1], w, h)

    def mouseDoubleClickEvent(self, e):
        """
        더블클릭 하면 종료
        :param e:
        :return:
        """
        QtWidgets.qApp.quit()

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#
#     s = Sticker('gif/left.gif', xy=[-80, 200], on_top=False)
#     #
#     # s1 = Sticker('gif/amongus/red_vent.gif', xy=[780, 1020], size=0.3, on_top=True)
#     #
#     # s2 = Sticker('gif/amongus/orange.gif', xy=[1200, 1020], size=0.3, on_top=True)
#     #
#     #
#     # s3 = Sticker('gif/amongus/blue_green.gif', xy=[400, 920], size=1.0, on_top=True)
#     #
#     # s4 = Sticker('gif/amongus/mint.gif', xy=[1000, 950], size=0.2, on_top=True)
#     # s4.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=120)
#     #
#     # s5 = Sticker('gif/amongus/brown.gif', xy=[200, 1010], size=0.75, on_top=True)
#     #
#     # s6 = Sticker('gif/amongus/yellow.gif', xy=[1850, 800], size=0.75, on_top=True)
#     # # s6.walk(from_xy=[0, 800], to_xy=[1850, 800], speed=240)
#     #
#     # s7 = Sticker('gif/amongus/magenta.gif', xy=[1500, 900], size=0.5, on_top=True)
#     # s7.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=180)
#
#     sys.exit(app.exec_())