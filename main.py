import sys
from PyQt5 import QtWidgets
from Sticker import Sticker

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    s = Sticker(img_path='gif/left.gif', xy=[-80, 200], on_top=False)

    s1 = Sticker('gif/amongus/red_vent.gif', xy=[780, 1020], size=0.3, on_top=True)

    s2 = Sticker('gif/amongus/orange.gif', xy=[1200, 1020], size=0.3, on_top=True)

    s3 = Sticker('gif/amongus/blue_green.gif', xy=[400, 920], size=1.0, on_top=True)

    s4 = Sticker('gif/amongus/mint.gif', xy=[1000, 950], size=0.2, on_top=True)
    s4.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=120)

    s5 = Sticker('gif/amongus/brown.gif', xy=[200, 1010], size=0.75, on_top=True)

    s6 = Sticker('gif/amongus/yellow.gif', xy=[1850, 800], size=0.75, on_top=True)
    s6.walk_diff(from_xy_diff=[0, 800], to_xy_diff=[1850, 800], speed=240)

    s7 = Sticker('gif/amongus/magenta.gif', xy=[1500, 900], size=0.5, on_top=True)
    s7.walk_diff(from_xy_diff=[-100, 0], to_xy_diff=[100, 0], speed=180)

    sys.exit(app.exec_())