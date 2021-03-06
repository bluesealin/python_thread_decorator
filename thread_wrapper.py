import sys, time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def exec_time(object):
    print "exec time"
    return object

class GuiThread(QThread):
    def __init__(self, method, args=None, exec_times=None):
        super(GuiThread, self).__init__()
        self.method = method
        self.args = args
        self.parent = None
        self.run = True
        self.exec_times = exec_times

    def set_args(self, args):
        self.args = args

    def stop(self):
        self.run = False

    def run(self):
        exec_times = self.exec_times
        self.run = True
        print "starting thread type {} name {}".format(type(self.method), self.method.__name__)
        while self.run:
            self.method(*self.args)
            time.sleep(0.5)
            self.exec_times -= 1 if self.exec_times else None
            if self.exec_times == 0:
                self.stop()
        self.exec_times = exec_times


def thread_this_method(execs=None):
    print "creating decorator"
    def wrap1(method):
        def wrapper(*args, **kwargs):
            instance = args[0]
            print "Type of {} is {}".format(method.__name__, type(instance.__getattribute__(method.__name__)))
            thread = GuiThread(method, exec_times=execs)
            thread.set_args(args)
            instance.__setattr__(method.__name__, thread.start)
            instance.__getattribute__(method.__name__)()
        return wrapper
    return wrap1


class Form(QDialog):
    sig = pyqtSignal()
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        layout = QVBoxLayout()
        self.b1 = QPushButton("Button1")
        self.b1.setCheckable(True)
        self.b1.toggle()
        self.b1.clicked.connect(lambda: self.whichbtn(self.b1))
        self.b1.clicked.connect(self.btnstate)
        layout.addWidget(self.b1)

        self.b2 = QPushButton()
        self.b2.setIcon(QIcon(QPixmap("python.gif")))
        self.b2.clicked.connect(lambda: self.whichbtn(self.b2))
        layout.addWidget(self.b2)
        self.setLayout(layout)
        self.b3 = QPushButton("Disabled")
        self.b3.setEnabled(False)
        layout.addWidget(self.b3)

        self.b4 = QPushButton("&Default")
        self.b4.setDefault(True)
        self.b4.clicked.connect(lambda: self.whichbtn(self.b4))
        layout.addWidget(self.b4)

        self.setWindowTitle("Button demo")
        self.sig.connect(self.myslot)
        self.bt4state = True

    @thread_this_method(execs=10)
    def bt4toggle(self):
        self.b4.setDown(self.bt4state)
        self.bt4state ^= True

    def btnstate(self):
        self.sig.emit()
        if self.b1.isChecked():
            print "button pressed"
        else:
            print "button released"

    def whichbtn(self, b):
        print "clicked button is " + b.text()

    def myslot(self):
        #self.bt4toggle.set_parent(self)
        self.bt4toggle()

    def myslot2(self):
        print "my slot2"


def main():
    app = QApplication(sys.argv)
    ex = Form()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
