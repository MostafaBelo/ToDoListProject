from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QIcon
from time import sleep
import sys
import requests

currenttoken = ''

class Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui', self)
        self.btn_login.clicked.connect(self.logmein)
        self.btn_register.clicked.connect(self.openregister)
        self.show()

    def logmein(self):
        global currenttoken
        link = 'http://127.0.0.1:8000/api/login/'
        r = requests.post(link, data={'username': self.le_username.text(), 'password': self.le_password.text()})
        if str(r) == '<Response [200]>':
            currenttoken = r.json()['token']
            window.refr()
            window.cbb_user.setItemText(0, 'Hello ' + self.le_username.text())
            window.show()
            self.le_username.setText('')
            self.le_password.setText('')
            self.hide()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText('Error')
            msg.setInformativeText('Username OR Password is incorrect')
            msg.setWindowTitle('Error')
            msg.exec_()

    def openregister(self):
        self.reg = Register()
        self.hide()

class Register(QtWidgets.QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        uic.loadUi('register.ui', self)
        self.btn_login.clicked.connect(self.openlogin)
        self.btn_signup.clicked.connect(self.registerme)
        self.show()

    def registerme(self):
        global currenttoken
        link = 'http://127.0.0.1:8000/api/register/'
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error')
        msg.setWindowTitle('Error')
        if self.le_password.text() == self.le_password_2.text():
            r = requests.post(link, data={'username': self.le_username.text(), 'password': self.le_password.text(), 'password1': self.le_password.text(), 'password2': self.le_password.text(), 'email': self.le_email.text()})
            if str(r) == '<Response [200]>':
                if 'response' in r.json():
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('Success')
                    msg.setWindowTitle('Registration')
                    msg.setInformativeText('Successfully Registered')
                    msg.exec_()
                    currenttoken = r.json()['token']
                    window.refr()
                    window.cbb_user.setItemText(0, 'Hello ' + self.le_username.text())
                    window.show()
                    self.hide()
                elif 'username' in r.json():
                    msg.setInformativeText(r.json()['username'][0])
                    msg.exec_()
                elif 'email' in r.json():
                    msg.setInformativeText(r.json()['email'][0])
                    msg.exec_()
            else:
                msg.setInformativeText('Password is too easy')
                msg.exec_()
        else:
            msg.setInformativeText('Passwords don\'t match')
            msg.exec_()

    def openlogin(self):
        self.login = Login()
        self.hide()

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi('todolist.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.items = []
        self.btn_clr.clicked.connect(self.clear)
        self.btn_add.clicked.connect(self.add)
        self.lv_items.itemDoubleClicked.connect(self.viewit)
        self.btn_refr.clicked.connect(self.refr)
        self.cbb_user.currentIndexChanged.connect(self.logout)
        self.show()


    def logout(self, ind):
        global currenttoken
        if ind == 1:
            currenttoken = ''
            logerin.show()
            self.cbb_user.setCurrentIndex(0)
            self.hide()

    def refr(self):
        self.items.clear()
        self.lv_items.clear()
        link = 'http://127.0.0.1:8000/api_show/'
        r = requests.post(link, data={'tid':0, 'token':currenttoken})
        self.items = r.json()
        for i in range(len(self.items)):
            if self.items[i]['done']:
                item = QtWidgets.QListWidgetItem('{}- {}  (Done)'.format(i + 1, self.items[i]['task']))
            else:
                item = QtWidgets.QListWidgetItem('{}- {}'.format(i + 1, self.items[i]['task']))
            self.lv_items.addItem(item)

    def clear(self):
        link = 'http://127.0.0.1:8000/api_del/'
        r = requests.delete(link, data={'tid': 0, 'token': currenttoken})
        self.refr()

    def add(self):
        self.adder = Add()
        self.hide()

    def viewit(self, index):
        indexitem = self.items[self.lv_items.currentRow()]
        self.viewer = Viewer()
        self.viewer.item = indexitem
        self.viewer.lbl_task.setText('Task: '+indexitem['task'])
        self.viewer.lbl_duedate.setText('Due Date: '+indexitem['duedate'])
        self.viewer.lbl_person.setText('Person: '+indexitem['person'])
        self.viewer.cb_status.setChecked(indexitem['done'])
        self.hide()

class Add(QtWidgets.QMainWindow):
    def __init__(self):
        super(Add, self).__init__()
        uic.loadUi('adding.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.de_duedate.setDisplayFormat("yyyy-MM-dd")
        self.btn_add.clicked.connect(self.addit)
        self.btn_back.clicked.connect(self.back)
        self.show()

    def back(self):
        window.show()
        self.hide()

    def addit(self):
        if self.le_task.text() == '' or self.le_person.text() == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText('Error')
            msg.setInformativeText('Please make sure that both the task and person fields are filled')
            msg.setWindowTitle('Error')
            msg.exec_()
        else:
            mydata = {
                "task": self.le_task.text(),
                "duedate": str(self.de_duedate.date().toPyDate()),
                "person": self.le_person.text(),
                'token': currenttoken
            }
            link = 'http://127.0.0.1:8000/api_add/'
            r = requests.post(link, data=mydata)
            window.refr()
            window.show()
            self.hide()

class Viewer(QtWidgets.QMainWindow):
    def __init__(self):
        self.item = {}
        super(Viewer, self).__init__()
        uic.loadUi('viewtask.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.btn_edit.clicked.connect(self.edit)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_back.clicked.connect(self.back)
        self.cb_status.toggled.connect(self.toggledone)
        self.show()

    def back(self):
        window.refr()
        window.show()
        self.hide()

    def edit(self):
        self.edit = Editer()
        date = self.item['duedate'].split('-')
        self.edit.de_duedate.setDate(QtCore.QDate(int(date[0]), int(date[1]), int(date[2])))
        self.edit.le_task.setText(self.item['task'])
        self.edit.le_person.setText(self.item['person'])
        self.edit.id = self.item['id']
        self.hide()

    def toggledone(self, state):
        link = 'http://127.0.0.1:8000/api_update/'
        mydata = {
            "task": self.item['task'],
            "duedate": self.item['duedate'],
            "person": self.item['person'],
            "done": state,
            "tid": self.item['id'],
            "token": currenttoken
        }
        r = requests.put(link, data=mydata)
        window.refr()

    def delete(self):
        link = 'http://127.0.0.1:8000/api_del/'
        r = requests.delete(link, data={'tid': self.item['id'], 'token': currenttoken})
        window.refr()
        window.show()
        self.hide()

class Editer(QtWidgets.QMainWindow):
    def __init__(self):
        super(Editer, self).__init__()
        uic.loadUi('adding.ui', self)
        self.setWindowIcon(QIcon('icon.png'))
        self.de_duedate.setDisplayFormat("yyyy-MM-dd")
        self.id = None
        self.setWindowTitle('Editing')
        self.btn_add.setText('Update')
        self.btn_add.clicked.connect(self.editit)
        self.btn_back.clicked.connect(self.back)
        self.show()

    def back(self):
        window.show()
        self.hide()

    def editit(self):
        if self.le_task.text() == '' or self.le_person.text() == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText('Error')
            msg.setInformativeText('Please make sure that both the task and person fields are filled')
            msg.setWindowTitle('Error')
            msg.exec_()
        else:
            mydata = {
                "task": self.le_task.text(),
                "duedate": str(self.de_duedate.date().toPyDate()),
                "person": self.le_person.text(),
                "tid": self.id,
                "token": currenttoken
            }
            link = 'http://127.0.0.1:8000/api_update/'
            r = requests.put(link, data=mydata)
            window.refr()
            window.show()
            self.hide()

app = QtWidgets.QApplication(sys.argv)
logerin = Login()
window = Main()
window.hide()
sys.exit(app.exec_())
