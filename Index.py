from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3
import re
from PyQt5.uic import loadUiType
from cryptography.fernet import Fernet
from dateutil import parser
import datetime
from xlsxwriter import *
import time




ui , _ = loadUiType('Library.ui')
LogIN , _ =loadUiType('LogIN.ui')

Key =b'orHzoGOLuivudX_Obkc3C-WGOzFXlPG1vkglGF3qwk4='

class LogIN(QMainWindow ,LogIN):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.center()
        self.pushButton.clicked.connect(self.HandleLogIN)

    def center(self):
        # geometry of the main windowy
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def HandleLogIN(self):
        UserName = self.lineEdit.text()
        Password = self.lineEdit_2.text()
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT UserEmail FROM Users WHERE UserName = ?''',[(UserName)])
        Data = self.cur.fetchall()
        if len(Data) >0:
            self.lineEdit.setText('')
            if Password =="":
                self.label.setText('Password Field Not be Empty')
                self.label.setStyleSheet('color:red')
            else:
                self.cur.execute('''SELECT UserPassword FROM Users WHERE UserName = ?''',[(UserName)])
                Data = self.cur.fetchall()
                if Password == CipherSuite.decrypt(Data[0][0]).decode('utf-8'):
                    self.label.setText('')
                    self.statusBar().showMessage('Logged In')
                    self.lineEdit_2.setText('')
                    self.Window2 = MainApp()
                    self.close()
                    self.Window2.show()
        elif UserName=='':
            self.label.setText('Username Field Not be Empty')
            self.label.setStyleSheet('color:red')
        else:
            self.label.setText('Username Not Registered')
            self.label.setStyleSheet('color:red')






CipherSuite = Fernet(Key)
class MainApp(QMainWindow , ui):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setupUi(self)
        self.center()
        self.HandleButtons()
        self.HandleUI_Changes()
        self.Show_Publisher()
        self.Show_Author()
        self.Show_Category()
        self.Show_Client()
        self.Show_Category_ComboBox()
        self.Show_Author_ComboBox()
        self.Show_Publisher_ComboBox()
        self.ShowBooks()
        self.Show_DayToDay_Operation()

    def HandleUI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)



    def HandleButtons(self):
        self.DayOperationTab_Button.clicked.connect(self.DayToDay_Tab)
        self.Account_Button.clicked.connect(self.Users_Tab)
        self.BookTab_Button.clicked.connect(self.Books_Tab)
        self.SettingTab_Button.clicked.connect(self.Setting_Tab)
        self.AddBookTab_Save_Button.clicked.connect(self.Add_Books)
        self.Setting_AddNewCategory_Button.clicked.connect(self.Add_Category)
        self.Setting_AddAuthor_Button.clicked.connect(self.Add_Author)
        self.Setting_AddPublisher_Button.clicked.connect(self.Add_Publisher)
        self.EditBookTab_Search.clicked.connect(self.Search_Books)
        self.EditBookTab_Save_Button.clicked.connect(self.Edit_Books)
        self.EditBookTab_Delete_Button.clicked.connect(self.Delete_Books)
        self.User_RAddUser_Button.clicked.connect(self.AddNew_User)
        self.User_LogIN_Button.clicked.connect(self.LogIN)
        self.User_EAddUser_Button.clicked.connect(self.Edit_User)
        self.pushButton_5.clicked.connect(self.Themes_Tab)
        self.Theme_Pushbutton1.clicked.connect(self.Theme_1)
        self.Them_Pushbutton2.clicked.connect(self.Theme_2)
        self.Theme_Pushbutton1_2.clicked.connect(self.Theme_3)
        self.Them_Pushbutton2_2.clicked.connect(self.Theme_4)
        self.UsersTab_Button.clicked.connect(self.Account_Tab)
        self.AddBookTab_Save_Button_2.clicked.connect(self.Add_Client)
        self.EditBookTab_Search_2.clicked.connect(self.Search_Client)
        self.EditBookTab_Save_Button_2.clicked.connect(self.Edit_Client)
        self.EditBookTab_Delete_Button_2.clicked.connect(self.Delete_Client)
        self.DayAdd_Button.clicked.connect(self.HandleDayOperation)
        self.DayAdd_Button_2.clicked.connect(self.Export_DayToDay_Data)
        self.DayAdd_Button_3.clicked.connect(self.Export_Book_Data)
        self.DayAdd_Button_4.clicked.connect(self.Export_Client_Data)




    ########--------------OPENING TABS--------------########
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def DayToDay_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    def Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def Setting_Tab(self):
        self.tabWidget.setCurrentIndex(4)

    def Themes_Tab(self):
        self.tabWidget.setCurrentIndex(5)
    def Account_Tab(self):
        self.tabWidget.setCurrentIndex(2)
    def Theme_1(self):
        style=open('Themes/style4.css','r')
        style=style.read()
        self.setStyleSheet(style)

    def Theme_2(self):
        style=open('Themes/style2.css','r')
        style=style.read()
        self.setStyleSheet(style)

    def Theme_3(self):
        style=open('Themes/style1.css','r')
        style=style.read()
        self.setStyleSheet(style)
    def Theme_4(self):
        style=open('Themes/style.css','r')
        style=style.read()
        self.setStyleSheet(style)


    ########--------------OPENING TABS--------------########

    ########---------HANDLE_DAY_OPERATION-----------########

    def HandleDayOperation(self):
        Books_Title= self.DayBookTitle_TextBox.text()
        Clien_Name = self.DayBookTitle_TextBox_2.text()
        Type= self.DayOperation_ComboBox.currentText()
        days= self.DayDays_ComboBox.currentIndex() +1
        from_date = (datetime.date.today())
        to_date = from_date + datetime.timedelta(days=int(days))
        days=int(days)
        from_date=str(from_date)
        to=str(to_date)
        self.db= sqlite3.connect('LibraryDatabase.db')
        self.cur= self.db.cursor()
        self.cur.execute('''INSERT INTO DayToDay (BookName , Type,Days,Date,To_Date,Client) VALUES (?,?,?,?,?,?)''',(Books_Title ,Type,days,from_date,to_date, Clien_Name))
        self.db.commit()
        self.statusBar().showMessage('Operation Added')
        self.Show_DayToDay_Operation()

    def Show_DayToDay_Operation(self):
        self.db= sqlite3.connect('LibraryDatabase.db')
        self.cur= self.db.cursor()
        self.cur.execute('''SELECT BookName , Client,Type ,Date,To_Date FROM DayToDay''')
        Data =self.cur.fetchall()
        self.Day_Table.setRowCount(0)
        self.Day_Table.insertRow(0)
        for row ,form in enumerate(Data):
            for column,item in enumerate(form):
                self.Day_Table.setItem(row , column,QTableWidgetItem(str(item)))
                column+=1
            row_position=self.Day_Table.rowCount()
            self.Day_Table.insertRow(0)




    ########---------HANDLE_DAY_OPERATION-----------########

    #######---------------EXPORT_DATA---------------########

    def Export_DayToDay_Data(self):
        self.db= sqlite3.connect('LibraryDatabase.db')
        self.cur= self.db.cursor()
        self.cur.execute('''SELECT BookName , Client,Type ,Date,To_Date FROM DayToDay''')
        Data =self.cur.fetchall()

        WB = Workbook("DayOperationExport.xlsx")
        Sheet1 = WB.add_worksheet()

        Sheet1.write(0,0,'Book Title')
        Sheet1.write(0,1,'Client Name')
        Sheet1.write(0,2,'Type')
        Sheet1.write(0,3,'From Date')
        Sheet1.write(0,4,'To date')

        rowNumber=1
        for row in Data:
            columnNumber=0
            for item in row:
                Sheet1.write(rowNumber,columnNumber,str(item))
                columnNumber+=1
            rowNumber+=1

        WB.close()
        self.statusBar().showMessage('Report Exported Successfully')

    def Export_Book_Data(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT BookName ,BookDescription , BookCode  , BookCategory  ,BookAuthor  ,BookPublisher , BookPrice  FROM Book''')

        Data = self.cur.fetchall()
        self.db.commit()
        WB = Workbook("BookDataExport.xlsx")
        Sheet1 = WB.add_worksheet()

        Sheet1.write(0,0,'Book Name')
        Sheet1.write(0,1,'Book Description')
        Sheet1.write(0,2,'Book Category')
        Sheet1.write(0,3,'Book Author')
        Sheet1.write(0,4,'Book publisher')
        Sheet1.write(0,5,'Book Price')

        rowNumber=1
        for row in Data:
            columnNumber=0
            for item in row:
                Sheet1.write(rowNumber,columnNumber,str(item))
                columnNumber+=1
            rowNumber+=1

        WB.close()
        self.statusBar().showMessage('Report Exported Successfully')

    def Export_Client_Data(self):

        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT ClientName , ClientEmailID , ClientMobileNumber , ClientNationalID FROM Client''')

        Data = self.cur.fetchall()
        self.db.commit()

        WB = Workbook("ClientDataExport.xlsx")
        Sheet1 = WB.add_worksheet()

        Sheet1.write(0,0,'Client Name')
        Sheet1.write(0,1,'Client EmailID')
        Sheet1.write(0,2,'Client Mobile Number')
        Sheet1.write(0,3,'Client nationalID')


        rowNumber=1
        for row in Data:
            columnNumber=0
            for item in row:
                Sheet1.write(rowNumber,columnNumber,str(item))
                columnNumber+=1
            rowNumber+=1

        WB.close()
        self.statusBar().showMessage('Report Exported Successfully')



    #######---------------EXPORT_DATA---------------########

    ########-----------------CLIENT-----------------########

    def Add_Client(self):
        Client_Name = self.AddBookTab_BookTitle_TextBox_2.text()
        Client_Email = self.AddBookTab_BookCode_TextBox_2.text()
        Client_Mobile = self.AddBookTab_BookCode_TextBox_3.text()
        Client_NationalID = self.AddBookTab_BookCode_TextBox_4.text()
        self.db= sqlite3.connect('LibraryDatabase.db')
        self.cur= self.db.cursor()
        if Client_Name =='':
            self.label_22.setText('ClientName Field not be Empty')
            self.label_22.setStyleSheet('color:red')
        elif len(Client_Name) < 5:
            self.label_22.setText('ClientName Too Short')
            self.label_22.setStyleSheet('color:red')
        else:
            self.label_22.setText('')
            if Client_Email == '':
                    self.label_23.setText('Email Field not be Empty')
                    self.label_23.setStyleSheet('color:red')
            else:
                if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', Client_Email) == None :
                    self.label_23.setText('Invalid Email Address')
                    self.label_23.setStyleSheet('color:red')
                else:
                    self.cur.execute('''SELECT * FROM Client WHERE ClientEmailID = ?''',[(Client_Email)])
                    Data = self.cur.fetchall()
                    if len(Data)>0:
                        self.label_23.setText('Email Already Registered')
                        self.label_23.setStyleSheet('color:red')
                    else:
                        self.label_23.setText('')
                        if Client_Mobile=='':
                            self.label_24.setText('Mobile Number Field not be Empty')
                            self.label_24.setStyleSheet('color:red')
                        elif len(Client_Mobile) !=10:
                            self.label_24.setText('Mobile Number not valid')
                            self.label_24.setStyleSheet('color:red')
                        else:
                            self.cur.execute('''SELECT * FROM Client WHERE ClientMobileNumber= ?''',[(Client_Mobile)])
                            Data =self.cur.fetchall()
                            if len(Data)>0:
                                self.label_24.setText('Mobile Number Already Registered')
                                self.label_24.setStyleSheet('color:red')
                            else:
                                if Client_Mobile.isnumeric()==False:
                                    self.label_24.setText('Mobile Number Not Valid')
                                    self.label_24.setStyleSheet('color:red')
                                else:
                                    self.label_24.setText('')
                                    Client_Mobile=int(Client_Mobile)
                                    if Client_NationalID=="":
                                        self.label_25.setText("Field Not be left Empty")
                                        self.label_25.setStyleSheet('color: red')
                                    else:
                                        self.cur.execute('''INSERT INTO Client (ClientName , ClientEmailID , ClientMobileNumber , ClientNationalID) VALUES (?,?,?,?)''',(Client_Name ,Client_Email ,Client_Mobile , Client_NationalID,))
                                        self.db.commit()
                                        self.statusBar().showMessage('Client Registered')

                                        self.AddBookTab_BookTitle_TextBox_2.setText('')
                                        self.AddBookTab_BookCode_TextBox_2.setText('')
                                        self.AddBookTab_BookCode_TextBox_3.setText('')
                                        self.AddBookTab_BookCode_TextBox_4.setText('')
                                        self.Show_Client()






    def Search_Client(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        Client_Name = self.AddBookTab_BookTitle_TextBox_3.text()

        self.cur.execute(''' SELECT * FROM Client WHERE ClientName=?''' , [(Client_Name)])
        Data = self.cur.fetchone()
        self.db.commit()
        if Data==None:
            if QMessageBox.warning(self,'Error' , 'Client Not Found' , QMessageBox.Ok ) == QMessageBox.Ok:
                self.AddBookTab_BookTitle_TextBox_3.setText('')
                self.AddBookTab_BookCode_TextBox_9.setText('')
                self.AddBookTab_BookCode_TextBox_8.setText('')
                self.AddBookTab_BookCode_TextBox_10.setText('')
        else:
            self.statusBar().showMessage('Client Found')
            self.AddBookTab_BookTitle_TextBox_3.setText(Data[1])
            self.AddBookTab_BookCode_TextBox_9.setText(Data[2])
            self.AddBookTab_BookCode_TextBox_8.setText(str(Data[3]))
            self.AddBookTab_BookCode_TextBox_10.setText(Data[4])
            self.Show_Client()

    def Edit_Client(self):
        Client_Name = self.AddBookTab_BookTitle_TextBox_3.text()
        Client_Email = self.AddBookTab_BookCode_TextBox_9.text()
        Client_Mobile = self.AddBookTab_BookCode_TextBox_8.text()
        Client_NationalID = self.AddBookTab_BookCode_TextBox_10.text()
        Client_Mobile = int(Client_Mobile)
        self.cur.execute('''UPDATE Client SET ClientName = ? ,ClientEmailID =  ?, ClientMobileNumber = ?  , ClientNationalID = ?  ''' , (Client_Name , Client_Email ,Client_Mobile, Client_NationalID ))

        self.db.commit()
        self.statusBar().showMessage("Client Detail Updated")
        self.AddBookTab_BookTitle_TextBox_3.setText('')
        self.AddBookTab_BookCode_TextBox_9.setText('')
        self.AddBookTab_BookCode_TextBox_8.setText('')
        self.AddBookTab_BookCode_TextBox_10.setText('')
        self.Show_Client()




    def Delete_Client(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        Client_Name = self.AddBookTab_BookTitle_TextBox_3.text()
        self.cur.execute(''' SELECT ClientEmailID FROM Client WHERE ClientName=?''' , [(Client_Name)])
        Data = self.cur.fetchall()
        if len(Data)>0:
            if QMessageBox.warning(self , 'Delete Client' , 'Are You Sure' , QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.cur.execute('''DELETE FROM Client WHERE ClientName = ?''' , [(Client_Name)])
                self.db.commit()
                self.statusBar().showMessage('Client Detail Deleted')
                self.AddBookTab_BookTitle_TextBox_3.setText('')
                self.AddBookTab_BookCode_TextBox_9.setText('')
                self.AddBookTab_BookCode_TextBox_8.setText('')
                self.AddBookTab_BookCode_TextBox_10.setText('')
                self.Show_Client()



    def Show_Client(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT ClientName , ClientEmailID , ClientMobileNumber , ClientNationalID FROM Client''')

        Data = self.cur.fetchall()
        self.db.commit()
        if Data:
            self.Day_Table_3.setRowCount(0)
            self.Day_Table_3.insertRow(0)
            for row , form in enumerate(Data):
                for column , value in enumerate(form):
                    self.Day_Table_3.setItem(row , column , QTableWidgetItem(str(value)))
                    column+=1
                Row_Position = self.Day_Table_3.rowCount()
                self.Day_Table_3.insertRow(Row_Position)
        self.db.commit()


    ########------------------CLIENT-----------------########

    ########------------------BOOKS-----------------########

    def Add_Books(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()

        Book_Title = self.AddBookTab_BookTitle_TextBox.text()
        Book_Description = self.AddBookTab_TextBox.toPlainText()
        Book_Code = self.AddBookTab_BookCode_TextBox.text()
        Book_Category = self.AddBookTab_Category_ComboBox.currentIndex()
        Book_Author = self.AddBookTab_Author_ComboBox.currentIndex()
        Book_Publisher = self.AddBookTab_Publisher_ComboBox.currentIndex()
        Book_Price = self.AddBookTab_BookPrice_TextBox.text()

        if Book_Title == '' or Book_Description == '' or Book_Code == '' or Book_Category == 0 or Book_Author==0 or Book_Publisher == 0 or Book_Price == '':
            InfoBox = QMessageBox()
            InfoBox.setIcon(QMessageBox.Information)
            InfoBox.setText("Fields Not Be left Empty!!")
            InfoBox.setWindowTitle("Information")
            InfoBox.setStandardButtons(QMessageBox.Ok)
            InfoBox.exec_()
        else:
            Book_Category = self.AddBookTab_Category_ComboBox.currentText()
            Book_Author = self.AddBookTab_Author_ComboBox.currentText()
            Book_Publisher = self.AddBookTab_Publisher_ComboBox.currentText()
            Book_Price = float(Book_Price)

            self.cur.execute('''INSERT INTO Book (BookName,BookDescription , BookCode , BookCategory,BookAuthor,BookPublisher , BookPrice) VALUES (?,?,?,?,?,?,?)''',(Book_Title , Book_Description,Book_Code,Book_Category , Book_Author,Book_Publisher,Book_Price))
            self.db.commit()

            self.statusBar().showMessage("Book Added")

            self.AddBookTab_BookTitle_TextBox.setText('')
            self.AddBookTab_TextBox.setPlainText('')
            self.AddBookTab_BookCode_TextBox.setText('')
            self.AddBookTab_Category_ComboBox.setCurrentIndex(0)
            self.AddBookTab_Author_ComboBox.setCurrentIndex(0)
            self.AddBookTab_Publisher_ComboBox.setCurrentIndex(0)
            self.AddBookTab_BookPrice_TextBox.setText('')
            self.ShowBooks()




    def Edit_Books(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()

        Book_Title = self.EditBookTab_BookTitle_TextBox.text()
        Book_Description = self.EditBookTab_TextBox.toPlainText()
        Book_Code = self.EditBookTab_BookCode_TextBox.text()
        Book_Category = self.EditBookTab_Category_ComboBox.currentText()
        Book_Author = self.EditBookTab_Author_ComboBox.currentText()
        Book_Publisher = self.EditBookTab_Publisher_ComboBox.currentText()
        Book_Price = self.EditBookTab_BookPrice_TextBox.text()




        self.cur.execute('''UPDATE Book SET BookName = ? ,BookDescription =  ?, BookCode = ?  , BookCategory = ? ,BookAuthor = ? ,BookPublisher = ?, BookPrice = ? ''' , (Book_Title , Book_Description ,Book_Code, Book_Category ,Book_Author, Book_Publisher ,Book_Price))
        self.db.commit()
        self.statusBar().showMessage("Book Updated")

        self.EditBookTab_BookTitle_TextBox.setText('')
        self.EditBookTab_TextBox.setPlainText('')
        self.EditBookTab_BookCode_TextBox.setText('')
        self.EditBookTab_Category_ComboBox.setCurrentIndex(0)
        self.EditBookTab_Author_ComboBox.setCurrentIndex(0)
        self.EditBookTab_Publisher_ComboBox.setCurrentIndex(0)
        self.EditBookTab_BookPrice_TextBox.setText('')
        self.ShowBooks()


    def Delete_Books(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        BookTitle = self.EditBookTab_BookTitle_TextBox.text()
        self.cur.execute('''SELECT BookPrice FROM Book WHERE BookName = ?''',([BookTitle]))
        Data = self.cur.fetchall()
        if len(Data)>0:
            if QMessageBox.warning(self , 'Delete Book' , 'Are You Sure' , QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                self.cur.execute('''DELETE FROM Book WHERE BookName = ?''' , [(BookTitle)])
                self.db.commit()
                self.statusBar().showMessage('Book Deleted')
                self.EditBookTab_BookTitle_TextBox.setText('')
                self.EditBookTab_TextBox.setPlainText('')
                self.EditBookTab_BookCode_TextBox.setText('')
                self.EditBookTab_Category_ComboBox.setCurrentIndex(0)
                self.EditBookTab_Author_ComboBox.setCurrentIndex(0)
                self.EditBookTab_Publisher_ComboBox.setCurrentIndex(0)
                self.EditBookTab_BookPrice_TextBox.setText('')
                self.ShowBooks()

    def Search_Books(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        BookTitle = self.EditBookTab_BookTitle_TextBox.text()

        self.cur.execute(''' SELECT * FROM Book WHERE BookName=? ''' , [(BookTitle)])
        Data = self.cur.fetchone()
        self.db.commit()

        if Data==None:
            if QMessageBox.warning(self,'Error' , 'Book Not Found' , QMessageBox.Ok ) == QMessageBox.Ok:
                self.EditBookTab_BookTitle_TextBox.setText('')

        else:
            self.EditBookTab_TextBox.setPlainText(Data[2])
            self.EditBookTab_BookCode_TextBox.setText(Data[3])
            self.EditBookTab_Category_ComboBox.setCurrentText(Data[4])
            self.EditBookTab_Author_ComboBox.setCurrentText(Data[5])
            self.EditBookTab_Publisher_ComboBox.setCurrentText(Data[6])
            self.EditBookTab_BookPrice_TextBox.setText(str(Data[7]))
            self.ShowBooks()


    def ShowBooks(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT BookName ,BookDescription , BookCode  , BookCategory  ,BookAuthor  ,BookPublisher , BookPrice  FROM Book''')

        Data = self.cur.fetchall()
        self.db.commit()
        if Data:
            self.Day_Table_2.setRowCount(0)
            self.Day_Table_2.insertRow(0)
            for row , form in enumerate(Data):
                for column , value in enumerate(form):
                    self.Day_Table_2.setItem(row , column , QTableWidgetItem(str(value)))
                    column+=1
                Row_Position = self.Day_Table_2.rowCount()
                self.Day_Table_2.insertRow(Row_Position)


    ########------------------BOOKS-----------------########

    ########------------------USERS-----------------########

    def AddNew_User(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur  = self.db.cursor()

        Username = self.User_RUsername_Textbox.text()
        Email = self.User_REmail_Textbox.text()
        Password = self.User_RPassword_TextBox.text()
        ConfirmPassword = self.User_RConfirmPassword_TextBox.text()
        Mobile_No = self.Mobile_TextBox.text()



        if Username =='':
            self.UserName_Label.setText('Username Field not be Empty')
            self.UserName_Label.setStyleSheet('color:red')
        elif len(Username) < 5:
            self.UserName_Label.setText('Username Too Short')
            self.UserName_Label.setStyleSheet('color:red')
        else:

            self.cur.execute('''SELECT * FROM Users WHERE UserName= ?''',[(Username)])
            Data =self.cur.fetchall()
            if len(Data)>0:
                self.UserName_Label.setText('Username already exist')
                self.UserName_Label.setStyleSheet('color:red')
            else:
                self.UserName_Label.setText('')
                if Email == '':
                    self.Email_Label.setText('Email Field not be Empty')
                    self.Email_Label.setStyleSheet('color:red')
                else:
                    if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', Email) == None :
                        self.Email_Label.setText('Invalid Email Address')
                        self.Email_Label.setStyleSheet('color:red')
                    else:

                        self.cur.execute('''SELECT * FROM Users WHERE UserEmail = ?''',[(Email)])
                        Data = self.cur.fetchall()
                        if len(Data)>0:
                            self.Email_Label.setText('Email Already Registered')
                            self.Email_Label.setStyleSheet('color:red')
                        else:
                            self.Email_Label.setText('')
                            if Mobile_No=='':
                                self.MobileNo_Label.setText('Mobile Number Field not be Empty')
                                self.MobileNo_Label.setStyleSheet('color:red')
                            elif len(Mobile_No) !=10:
                                self.MobileNo_Label.setText('Mobile Number not valid')
                                self.MobileNo_Label.setStyleSheet('color:red')
                            else:
                                self.cur.execute('''SELECT * FROM Users WHERE MobileNumber= ?''',[(Mobile_No)])
                                Data =self.cur.fetchall()
                                if len(Data)>0:
                                    self.MobileNo_Label.setText('Mobile Number Already Registered')
                                    self.MobileNo_Label.setStyleSheet('color:red')
                                else:
                                    if Mobile_No.isnumeric()==False:
                                        self.MobileNo_Label.setText('Mobile Number Not Valid')
                                        self.MobileNo_Label.setStyleSheet('color:red')
                                    else:
                                        self.MobileNo_Label.setText('')
                                        Mobile_No=int(Mobile_No)
                                        if len(Password)<8:
                                            self.Password_Label1.setText("Password Will be 8-12 Character Long")
                                            self.Password_Label1.setStyleSheet('color: red')
                                        elif len(Password)>12:
                                            self.Password_Label1.setText("Password Will be 8-12 Character Long")
                                            self.Password_Label1.setStyleSheet('color: red')
                                        else:

                                            if Password != ConfirmPassword:
                                                self.Password_Label1.setText('')
                                                self.Password_Label2.setText("Password and Confirm Password does'nt Match ")
                                                self.Password_Label2.setStyleSheet('color: red')
                                            else:
                                                self.Password_Label2.setText("")
                                                Password=CipherSuite.encrypt(bytes(Password,'utf-8'))
                                                self.cur.execute('''INSERT INTO Users (UserName , UserEmail , UserPassword , MobileNumber) VALUES (?,?,?,?)''',(Username ,Email ,Password , Mobile_No,))
                                                self.db.commit()
                                                self.statusBar().showMessage('User Registered')

                                                self.User_RUsername_Textbox.setText('')
                                                self.User_REmail_Textbox.setText('')
                                                self.User_RPassword_TextBox.setText('')
                                                self.User_RConfirmPassword_TextBox.setText('')
                                                self.Mobile_TextBox.setText('')

    def LogIN(self):

        UserName = self.User_LUsername_Textbox.text()
        Password = self.User_LPassword_TextBox.text()
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT UserEmail FROM Users WHERE UserName = ?''',[(UserName)])
        Data = self.cur.fetchall()

        if len(Data) >0:
            self.Login_Username.setText('')
            if Password =="":
                self.LogINPassword.setText('Password Field Not be Empty')
                self.LogINPassword.setStyleSheet('color:red')
            else:
                self.cur.execute('''SELECT UserPassword FROM Users WHERE UserName = ?''',[(UserName)])
                Data = self.cur.fetchall()
                if Password == CipherSuite.decrypt(Data[0][0]).decode('utf-8'):
                    self.LogINPassword.setText('')
                    self.statusBar().showMessage('Logged In')
                    self.User_LUsername_Textbox.setText('')
                    self.User_LPassword_TextBox.setText('')
                    self.User_EUsername_Textbox.setDisabled(False)
                    self.User_EEmail_Textbox.setDisabled(False)
                    self.User_EPassword_TextBox.setDisabled(False)
                    self.User_EConfirmPassword_TextBox.setDisabled(False)
                    self.User_EAddUser_Button.setDisabled(False)
                    self.Mobile_TextBox_2.setDisabled(False)
                else:
                    self.LogINPassword.setText('Password Not Correct')
                    self.LogINPassword.setStyleSheet('color:red')

        elif UserName=='':
            self.Login_Username.setText('Username Field Not be Empty')
            self.Login_Username.setStyleSheet('color:red')
        else:
            self.Login_Username.setText('Username Not Registered')
            self.Login_Username.setStyleSheet('color:red')



    def Edit_User(self):
        Username=self.User_EUsername_Textbox.text()
        Email=self.User_EEmail_Textbox.text()
        Password=self.User_EPassword_TextBox.text()
        Mobile_No=self.Mobile_TextBox_2.text()
        ConfirmPassword=self.User_EConfirmPassword_TextBox.text()

        if Username =='':
            self.label_46.setText('Username Field not be Empty')
            self.label_46.setStyleSheet('color:red')
        elif len(Username) < 5:
            self.label_46.setText('Username Too Short')
            self.label_46.setStyleSheet('color:red')
        else:
            self.label_46.setText('')
            if Email == '':
                self.label_47.setText('Email Field not be Empty')
                self.label_47.setStyleSheet('color:red')
            else:
                if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', Email) == None :
                    self.label_47.setText('Invalid Email Address')
                    self.label_47.setStyleSheet('color:red')

                else:
                    self.label_47.setText('')
                    if Mobile_No=='':
                        self.label_48.setText('Mobile Number Field not be Empty')
                        self.label_48.setStyleSheet('color:red')
                    elif len(Mobile_No) !=10:
                        self.label_48.setText('Mobile Number not valid')
                        self.label_48.setStyleSheet('color:red')
                    else:
                        if Mobile_No.isnumeric()==False:
                            self.label_48.setText('Mobile Number Not Valid')
                            self.label_48.setStyleSheet('color:red')
                        else:
                            self.label_48.setText('')
                            Mobile_No=int(Mobile_No)
                            if len(Password)<8:
                                self.label_49.setText("Password Will be 8-12 Character Long")
                                self.label_49.setStyleSheet('color: red')
                            elif len(Password)>12:
                                self.label_49.setText("Password Will be 8-12 Character Long")
                                self.label_49.setStyleSheet('color: red')
                            else:
                                if Password != ConfirmPassword:
                                    self.label_49.setText('')
                                    self.label_50.setText("Password and Confirm Password does'nt Match ")
                                    self.label_50.setStyleSheet('color: red')
                                else:
                                    self.Password_Label2.setText("")
                                    Password=CipherSuite.encrypt(bytes(Password,'utf-8'))
                                    self.cur.execute('''UPDATE Users SET UserName = ? , UserEmail = ? , UserPassword = ?, MobileNumber= ? ''',(Username ,Email ,Password , Mobile_No,))
                                    self.db.commit()
                                    self.statusBar().showMessage('User Registered')

                                    Username=self.User_EUsername_Textbox.setText('')
                                    Email=self.User_EEmail_Textbox.setText('')
                                    Password=self.User_EPassword_TextBox.setText('')
                                    Mobile_No=self.Mobile_TextBox_2.setText('')
                                    ConfirmPassword=self.User_EConfirmPassword_TextBox.setText('')


    ########------------------USERS-----------------########

    ########-----------------SETTING----------------########

    def Add_Category(self):

        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()

        Category_Name = self.Setting_Category_Textbox.text()
        self.cur.execute('''SELECT CategoryID FROM Category WHERE CategoryName = ?''' , [(Category_Name)])
        Data = self.cur.fetchall()
        self.db.commit()
        if Category_Name != '':
            if len(Data)==0:
                self.db = sqlite3.connect('LibraryDatabase.db')
                self.cur = self.db.cursor()
                self.cur.execute('''INSERT INTO Category (CategoryName) VALUES (?)''', (Category_Name,))
                self.db.commit()
                self.statusBar().showMessage('New Category Added')
                self.Show_Category()
                self.Show_Category_ComboBox()
                self.Setting_Category_Textbox.setText('')
            else:
                QMessageBox.warning(self ,'Warning' , 'Category Allready Exist' , QMessageBox.Ok)
        else:
            QMessageBox.warning(self , 'Warning'  ,'Fields Not Be Empty' , QMessageBox.Ok)



    def Add_Author(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()

        Author_Name = self.Setting_NewAuthor_TextBox.text()
        self.cur.execute('''SELECT AuthorID FROM Author WHERE AuthorName = ?''' , [(Author_Name)])
        Data = self.cur.fetchall()
        self.db.commit()
        if Author_Name !='':
            if len(Data)==0:
                self.db = sqlite3.connect('LibraryDatabase.db')
                self.cur = self.db.cursor()
                self.cur.execute('''INSERT INTO Author (AuthorName) VALUES (?)''', (Author_Name,))
                self.db.commit()
                self.statusBar().showMessage('New Author Added')
                self.Show_Author()
                self.Show_Author_ComboBox()
                self.Setting_NewAuthor_TextBox.setText('')
            else:
                QMessageBox.warning(self , 'Warning' , 'Author Name Already present', QMessageBox.Ok)
        else:
            QMessageBox.warning(self , 'Warning'  ,'Fields Not Be Empty' , QMessageBox.Ok)

    def Add_Publisher(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()

        Publisher_Name = self.Setting_NewPublisher_TextBox.text()
        self.cur.execute('''SELECT PublisherID FROM Publisher WHERE PublisherName = ?''' , [(Publisher_Name)])
        Data = self.cur.fetchall()
        self.db.commit()

        if Publisher_Name != '':
            if len(Data)==0:
                self.db = sqlite3.connect('LibraryDatabase.db')
                self.cur = self.db.cursor()
                self.cur.execute('''INSERT INTO Publisher (PublisherName) VALUES (?)''', (Publisher_Name,))
                self.db.commit()
                self.Show_Publisher()
                self.Show_Publisher_ComboBox()
                self.Setting_NewPublisher_TextBox.setText('')
                self.statusBar().showMessage('New Publisher Added')
                time.sleep(3)
                self.statusBar().showMessage('')
            else:
                QMessageBox.warning(self,'Warning' , 'Publisher Name Already Present',QMessageBox.Ok)
        else:
            QMessageBox.warning(self , 'Warning'  ,'Fields Not Be Empty' , QMessageBox.Ok)


    ########-----------------SETTING----------------########

    ########---------------SHOW_SETTING-------------########
    def Show_Category(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT CategoryName FROM Category''')

        Data = self.cur.fetchall()
        self.db.commit()

        if Data:
            self.Setting_Category_Table.setRowCount(0)
            self.Setting_Category_Table.insertRow(0)
            for row , form in enumerate(Data):
                for column , value in enumerate(form):
                    self.Setting_Category_Table.setItem(row , column , QTableWidgetItem(str(value)))
                    column+=1
                Row_Position = self.Setting_Category_Table.rowCount()
                self.Setting_Category_Table.insertRow(Row_Position)

    def Show_Author(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT AuthorName FROM Author''')

        Data = self.cur.fetchall()
        self.db.commit()
        if Data:
            self.Setting_Author_Table.setRowCount(0)
            self.Setting_Author_Table.insertRow(0)
            for row , form in enumerate(Data):
                for column , value in enumerate(form):
                    self.Setting_Author_Table.setItem(row , column , QTableWidgetItem(str(value)))
                    column+=1
                Row_Position = self.Setting_Author_Table.rowCount()
                self.Setting_Author_Table.insertRow(Row_Position)

    def Show_Publisher(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT PublisherName FROM Publisher''')

        Data = self.cur.fetchall()
        self.db.commit()
        if Data:
            self.Setting_Publisher_Table.setRowCount(0)
            self.Setting_Publisher_Table.insertRow(0)
            for row ,form in enumerate(Data):
                for column ,item in enumerate(form):
                    self.Setting_Publisher_Table.setItem(row , column , QTableWidgetItem(str(item)))
                    column+=1
                Row_Position = self.Setting_Publisher_Table.rowCount()
                self.Setting_Publisher_Table.insertRow(Row_Position)

    ########---------------SHOW_SETTING-------------########

    ########----------SHOW_SETTING_COMBOBOX---------########

    def Show_Category_ComboBox(self):
        self.db = sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT CategoryName FROM Category''')

        Data = self.cur.fetchall()
        self.db.commit()
        self.AddBookTab_Category_ComboBox.clear()
        self.AddBookTab_Category_ComboBox.addItem('Select Category')

        for item in Data:
            self.AddBookTab_Category_ComboBox.addItem(item[0])
        self.EditBookTab_Category_ComboBox.addItem('Select Category')
        for item in Data:
            self.EditBookTab_Category_ComboBox.addItem(item[0])

    def Show_Author_ComboBox(self):
        self.db= sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT AuthorName FROM Author''')

        Data = self.cur.fetchall()
        self.db.commit()
        self.AddBookTab_Author_ComboBox.clear()
        self.AddBookTab_Author_ComboBox.addItem('Select Author')
        for item in Data:
            self.AddBookTab_Author_ComboBox.addItem(item[0])

        self.EditBookTab_Author_ComboBox.addItem('Select Author')
        for item in Data:
            self.EditBookTab_Author_ComboBox.addItem(item[0])

    def Show_Publisher_ComboBox(self):
        self.db= sqlite3.connect('LibraryDatabase.db')
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT PublisherName FROM Publisher''')

        Data = self.cur.fetchall()
        self.db.commit()
        self.AddBookTab_Publisher_ComboBox.clear()
        self.AddBookTab_Publisher_ComboBox.addItem('Select Publisher')
        for item in Data:
            self.AddBookTab_Publisher_ComboBox.addItem(item[0])

        self.EditBookTab_Publisher_ComboBox.addItem('Select Publisher')
        for item in Data:
            self.EditBookTab_Publisher_ComboBox.addItem(item[0])


    ########----------SHOW_SETTING_COMBOBOX---------########

def main():
    app = QApplication(sys.argv)

    window = LogIN()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()


