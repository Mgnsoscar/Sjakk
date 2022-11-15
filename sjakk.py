# Ble ikke helt ferdig. Blir ferdig til demonstrasjonen

#### For å kunne kjøre koden må du installere:
#    pip install PyQt5
#    pip install BlurWindow
####

from PyQt5 import QtCore as qc, QtGui as qg, QtWidgets as qw
import sys
from customQtWidgets import *
from BlurWindow.blurWindow import blur



class Main(qw.QMainWindow):
    def __init__(self):

        # Bool to know if the window is maximized or normal
        self.maximized = False

        # initialize the main window, remove frames, make translucent, set size
        qw.QMainWindow.__init__(self)
        self.setWindowFlags(qc.Qt.FramelessWindowHint), self.resize(1000, 1000), self.setAttribute(qc.Qt.WA_TranslucentBackground)

        #### Init a centralwidget, add to main, init central frame, add to central widget
        self.cw = mywidget(self, "v", radius=9)
        self.cf = myframe(self.cw, "v", "cf", add=True, radius=9, color=(0,0,0,0))
        self.setCentralWidget(self.cw), self.cf.addstyle("background-color", "background-color: rgb(0,0,0,0); border-radius: 9px;")

        # Blur everything thats behind main window
        hWnd = self.winId()
        blur(hWnd)

        #### Create title bar, credit bar and main frame
        mainframe = {}
        for i in range(1, 4):
            mainframe[str(i)] = myframe(self.cf, "h", f"mainframe{i}", add=True)

        mainframe["1"].customradius(9, 9, 0, 0),    mainframe["1"].setFixedHeight(30),  mainframe["1"].bg(0, 0, 0, 100)
        mainframe["3"].customradius(0, 0, 9, 9),    mainframe["3"].setFixedHeight(20),  mainframe["3"].bg(0,0,0, 100)
        self.mainframe = mainframe

        #### Add the chessboard to the main frame
        board = Grid(mainframe["2"], self, "v", add=True)

        #### Create 2 frames in the top mainframe
        topframe = {}
        for i in range(1, 3):
            topframe[str(i)] = myframe(mainframe["1"], "h", f"topframe{i}", add=True, color=(0,0,0,0))

        topframe["2"].setFixedWidth(200),           topframe["2"].margins(135, 0, 0, 0)
        topframe["2"].customradius(0,9,0,0),        topframe["1"].customradius(9,0,0,0)
        self.topframe = topframe

        #### Create three buttons in the top right frame, set radius, individual colors, hover- and pressed color
        button = {}
        for i in range(1, 4):
            button[str(i)] = mybutton(topframe["2"], objectName=f"button{i}", radius=7, add=True, align="center")
            button[str(i)].setFixedSize(14, 14)

        button["1"].bg(255, 255, 0, 255),           button["1"].hcolor(255, 255, 0, 150),       button["1"].pcolor(255, 255, 0, 50)
        button["2"].bg(0, 255, 0, 255),             button["2"].hcolor(0, 255, 0, 150),         button["2"].pcolor(0, 255, 0, 50)
        button["3"].bg(255, 0, 0, 255),             button["3"].hcolor(255, 0, 0, 150),         button["3"].pcolor(255, 0, 0, 50)
        self.button = button

        #### Create 4 frames in the bottom mainframe
        btmframe = {}
        for i in range(1, 5):
            btmframe[str(i)] = myframe(mainframe["3"], "v", f"btmframe{i}", add=True)

        btmframe["4"].setFixedWidth(20),btmframe["1"].setFixedWidth(20)

        # Add "from" Entry:
        fromentry = myinput(btmframe["2"],          add=True, color=(0,0,0,0), text="",         align="center")
        fromentry.setValidator(None),               fromentry.setInputMask(None),               fromentry.setPlaceholderText("Fra rute...")
        fromentry.valida("[ABCDEFGHabcdefgh]{1}[1-8]{1}")
        # Add "to" entry:
        toentry = myinput(btmframe["3"],            add=True, color=(0, 0, 0, 0),               text="", align="center")
        toentry.setValidator(None),                 toentry.setInputMask(None),                 toentry.setPlaceholderText("Til rute...")
        toentry.valida("[ABCDEFGHabcdefgh]{1}[1-8]{1}")

        #### Add size-grip to the bottom right corner
        sizegrip = qw.QSizeGrip(btmframe["4"])
        btmframe["4"].lay.addWidget(sizegrip, 0,qc.Qt.AlignBottom)
        sizegrip.setStyleSheet("background-color: rgb(0,0,0,0);")

        # Link some functions
        self.mainframe["1"].mouseMoveEvent = self.moveWindow
        Functions.buttonconfig(self)

    # Make sure the window can be moved
    def moveWindow(self,event):

            if event.buttons() == qc.Qt.LeftButton:

                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
    # Define function every time the mouse is pressed
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

class Grid(myframe):

    #### Define chess pieces:

    wking   =   "♔"
    wqueen  =   "♕"
    wrook   =   "♖"
    wbishop =   "♗"
    wknight =   "♘"
    wpawn   =   "♙"
    bking   =   "♚"
    bqueen  =   "♛"
    brook   =   "♜"
    bbishop =   "♝"
    bknight =   "♞"
    bpawn   =   "♟"

    list = ["A", "B", "C", "D", "E", "F", "G", "H"]

    def __init__(self, parent, main, *args, **kwargs):
        myframe.__init__(self, parent, *args, **kwargs)

        grid = myframe(self, "g", "maingrid", add=True, color=(255,255,255,100))

        frame = {}
        piece = {}

        for i in Grid.list:
            frame[i],   piece[i]     =      ["placeholder"],     ["placeholder"]
            for j in range(1,9):
                frame[i].append(myframe(grid, "v", f"{i}{j}"))
                piece[i].append(mylabel(frame[i][j], f"piece{i}{j}", add=True, align="center", size=60))
                grid.lay.addWidget(frame[i][j], 8-j, Grid.list.index(i)+1)

    #### Color the black frames black
        color = 0
        for i in frame:
            for j in range(1,9,2):
                if color%2==0:
                    frame[i][j].bg(0,0,0,100)
                    frame[Grid.list[Grid.list.index(i)+1]][j+1].bg(0, 0, 0, 100)
            color += 1

        self.setBoard(piece)
        self.checkMove('piece["B"][2]',     piece["B"][2],      'piece["B"][1]',        piece["B"][1], piece)

    def setBoard(self, piece):
        #### Set the board:

        for i in self.list:
            piece[i][2].setText("♙"),  piece[i][2].setStyleSheet("color: rgb(0,0,0); size: 60px;")
            piece[i][7].setText("♟"), piece[i][7].setStyleSheet("color: rgb(0,0,0); size: 60px;")

        for i in [piece["A"][1], piece["H"][1]]:
            i.setText("♖"), i.setStyleSheet("color: rgb(0,0,0); size: 60px;")
        for i in [piece["A"][8], piece["H"][8]]:
            i.setText("♜"), i.setStyleSheet("color: rgb(0,0,0); size: 60px;")
        for i in [piece["B"][1], piece["G"][1]]:
            i.setText("♘"), i.setStyleSheet("color: rgb(0,0,0); size: 60px;")
        for i in [piece["B"][8], piece["G"][8]]:
            i.setText("♞"), i.setStyleSheet("color: rgb(0,0,0); size: 60px;")
        for i in [piece["C"][1], piece["F"][1]]:
            i.setText("♗"), i.setStyleSheet("color: rgb(0,0,0); size: 60px;")
        for i in [piece["C"][8], piece["F"][8]]:
            i.setText("♝"), i.setStyleSheet("color: rgb(0,0,0); size: 60px;")
        piece["D"][1].setText("♕"), piece["D"][1].setStyleSheet("color: rgb(0,0,0); size: 60px;")
        piece["D"][8].setText("♛"), piece["D"][8].setStyleSheet("color: rgb(0,0,0); size: 60px;")
        piece["E"][1].setText("♔"), piece["E"][1].setStyleSheet("color: rgb(0,0,0); size: 60px;")
        piece["E"][8].setText("♚"), piece["E"][8].setStyleSheet("color: rgb(0,0,0); size: 60px;")
    def checkEmpty(self, piece):

        if piece.text() == "":
            return True
        else:
            return False
    def checkPiece(self, piece):

        if piece.text() == "":
            return ""
        elif piece.text() == Grid.wking:
            return "wking"
        elif piece.text() == Grid.wqueen:
            return "wqueen"
        elif piece.text() == Grid.wrook:
            return "wrook"
        elif piece.text() == Grid.wbishop:
            return "wbishop"
        elif piece.text() == Grid.wknight:
            return "wknight"
        elif piece.text() == Grid.wpawn:
            return"wpawn"
        elif piece.text() == Grid.bking:
            return "bking"
        elif piece.text() == Grid.bqueen:
            return "bqueen"
        elif piece.text() == Grid.brook:
            return "brook"
        elif piece.text() == Grid.bbishop:
            return "bbishop"
        elif piece.text() == Grid.bknight:
            return "bknight"
        elif piece.text() == Grid.bpawn:
            return "bpawn"
    def checkPlayer(self, piece):
        player = self.checkPiece(piece)
        return player[0]
    def checkMove(self, stringfrom, fromframe, stringto, toframe, grid):

        piece = self.checkPiece(fromframe)[1:]
        player = self.checkPlayer(fromframe)

        x , y, pos   = Grid.list.index(stringfrom[7])+1,    stringfrom[11], stringfrom[7]+stringfrom[11]
        x2, y2, pos2 = Grid.list.index(stringto[7])+1,      stringto[11],   stringto[7]  +stringto[11]

        print(x,y,pos,x2,y2,pos2)

        if type == "pawn":

        #### Is the player's pawn at their second row?
            pawnx2 = bool
            if( (pos =="A2" and player == "w") or (pos=="B2" and player == "w") or
                (pos =="C2" and player == "w") or (pos=="D2" and player == "w") or
                (pos =="E2" and player == "w") or (pos=="F2" and player == "w") or
                (pos =="G2" and player == "w") or (pos=="H2" and player == "w") or
                (pos =="A7" and player == "b") or (pos=="B7" and player == "b") or
                (pos =="C7" and player == "b") or (pos=="D7" and player == "b") or
                (pos =="E7" and player == "b") or (pos=="F7" and player == "b") or
                (pos =="G7" and player == "b") or (pos=="H7" and player == "b") ):
                pawnx2 = True
            else:
                pawnx2 = False


class Functions(Main):

    def max_restore(self):

        if self.maximized == False:
            self.cw.radius(0),  self.cf.radius(0),  self.mainframe["1"].customradius(0, 0, 0, 0)
            self.showMaximized()
            self.maximized = True

        else:
            self.cw.radius(10), self.cf.radius(10), self.mainframe["1"].customradius(10, 10, 0, 0)
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.maximized = False

    def buttonconfig(self):
        # close/maximize/minimize buttons:
        self.button["1"].clicked.connect(self.showMinimized)
        self.button["2"].clicked.connect(lambda: Functions.max_restore(self))
        self.button["3"].clicked.connect(self.close)

#### Run Aplication

if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    Main = Main()
    Main.show()
    sys.exit(app.exec_())
