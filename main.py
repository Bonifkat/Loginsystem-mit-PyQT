from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import sqlite3
import bcrypt
import sys

min_pw_lenght = 8

conn = sqlite3.connect("userdatabase.db")
cur = conn.cursor()

class Welcome_page(QDialog):
    def __init__(self):
        super(Welcome_page, self).__init__()
        loadUi("welcome_page.ui", self)
        self.login_btn.clicked.connect(self.gotoLogin)
        self.register_btn.clicked.connect(self.gotoRegister)

    def gotoLogin(self):
        login_page=Login_page()
        widget.addWidget(login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoRegister(self):
        register_page=Register_page()
        widget.addWidget(register_page)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Login_page(QDialog):
    def __init__(self):
        super(Login_page, self).__init__()
        loadUi("login.ui", self)
        self.back.clicked.connect(self.gotoBack)
        self.login_button.clicked.connect(self.loginfuction)

    def loginfuction(self):

        encoded_password = b""

        user = self.login_username.text()
        password = self.login_password.text()
        encoded_password = password.encode("utf-8")

        gethashed = cur.execute("SELECT password FROM userdata WHERE username = ?", (user,))

        password_import_from_db = ""
        for password_import_from_db in cur.fetchall():
            password_from_db = password_import_from_db[0]


        if len(user) == 0 or len(password) == 0:
            self.error_label.setText("Please input all fields!")

        else:
            try:

                #check if the password is the same as the hashed one
                if bcrypt.checkpw(encoded_password, password_from_db):
                    #Login Success.
                    self.error_label.setText("Successfull login!")

                else:
                    self.error_label.setText("Wrong username or password.")
                    
            except:
                self.error_label.setText("Wrong username or password.")




    def gotoBack(self):
        welcome_page = Welcome_page()
        widget.addWidget(welcome_page)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Register_page(QDialog):
    def __init__(self):
        super(Register_page, self).__init__()
        loadUi("register.ui", self)
        self.back.clicked.connect(self.gotoBack)
        self.Register_btn.clicked.connect(self.registerfunction)

    def gotoBack(self):
        welcome_page = Welcome_page()
        widget.addWidget(welcome_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def registerfunction(self):
        userreg = self.register_username.text()
        passwordreg = self.register_password.text()
        passwordreg2 = self.register_password2.text()
        emailreg = self.register_email.text()


        if len(userreg) == 0 or len(passwordreg) == 0 or len(passwordreg2) == 0 or len(emailreg) == 0:
            self.error_label.setText("Please input all fields!")
             
        else:
            if len(str(passwordreg)) >= min_pw_lenght:

                    if passwordreg.isalnum() == True:

                        if passwordreg == passwordreg2:
                            password_to_hash = passwordreg
                            #Password encryption
                            encrypt_password = bcrypt.hashpw(password_to_hash.encode("utf-8"), bcrypt.gensalt())

                            hashed_registered_password = encrypt_password

                            #Database check for username
                            cur.execute("SELECT username FROM userdata WHERE username = ?", (userreg,))

                            usernames_in_db = 0
                            for checkusername in cur.fetchall():
                                usernames_in_db = checkusername[0]

                            if usernames_in_db != userreg:

                                conn.execute("INSERT INTO userdata (username, password, email) VALUES (?, ?, ?)",
                                (userreg, hashed_registered_password, emailreg))
                                conn.commit()

                                self.error_label.setText("Successfull register!")

                            else:
                                self.error_label.setText("Username already has been taken.")

                        else:
                            self.error_label.setText("Passwords doesn't match.")

                    else:
                        self.error_label.setText("Use only alphanumerical characters.")
            else:
                    lenght_error = "Your password has to be at least {0} characters long."
                    self.error_label.setText(lenght_error.format(min_pw_lenght))






app = QApplication(sys.argv)
mainwindow = Welcome_page()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()
app.exec_()