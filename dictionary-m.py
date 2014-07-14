#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# SCRIPT: PERSDIC
# AUTHOR: Kasra Ahmadvand // kasra.ahmadvand@gmail.com
# DATE:   2013/7/20
# REV:    1.1.0.T (Valid are A, B, T and P)
#         (For Alpha, Beta, Test and Production)
#
# PLATFORM: (SPECIFY: all linux distros)
#
#
# PURPOSE: Make a offline persisan dictionary for linux   
#                 
#               
#
# REV LIST:
#       DATE: 
#       BY:
#       MODIFICATION: 
#
#
# set -n  # Uncomment to check your syntax, without execution.
#         # NOTE: Do not forget to put the comment back in or
#         #       the shell script will not execute!
# set -x  # Uncomment to debug this shell script
#
##########################################################
########### DEFINE FILES AND VARIABLES:###################
#Generic_English_Persian.m2 : a free word data base ! 
#dic1 :
#a:
#item:
##########################################################
##########################################################
############### FUNCTIONS: ###################
#
##########################################################
##########################################################
from datetime import datetime
from pymongo import Connection
from pymongo.errors import ConnectionFailure
import sys,codecs
import string 
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QFrame, QPalette
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QColor, QPixmap

class mongo:
 try:
  client = Connection(host="localhost", port=27017)
 except ConnectionFailure, e:
  sys.stderr.write("Could not connect to MongoDB: %s" % e)
  sys.exit(1)
 dbh = client["mydb3"]
#assert dbh.connection == client
 def ins(self,word,mean):
  dic={"word":word,
      "mean":mean}
  self.dbh.users.insert(dic, safe=True)
   #self.dbh.users.insert(self.user_doc2, safe=True)
   #print "Successfully inserted document: %s" % user_doc
 def prin(self,word):
  #print self.dbh.users.find_one({"word":"example"})# for find a dictionary 
  users = self.dbh.users.find({"word":word})
  for user in users:
   return user.get("mean")
 def update(self,word,mean):
  new_user_doc={"word":word,"mean":mean}
  self.dbh.users.update({"word":word}, new_user_doc, safe=True)
 def find(self,case):
   #print self.dbh.users.find_one({"word":"example"})# for find a dictionary 
  if self.dbh.users.find_one({"word":case}) :
   return True
  return False
#import data from database
#classes and other objects 
class InputDialog(QtGui.QWidget):
 
 def __init__(self, parent=None):
  QtGui.QWidget.__init__(self, parent)
  lbl3 = QtGui.QLabel('Enter yor word here !', self)
  lbl3.move(134,13)
  self.setGeometry(500,700,500,600)
  self.setWindowTitle('PERSDIC')
  #self.botton=HoverButton(self)
  self.button = QtGui.QPushButton('Translate',self)
  self.button.setIconSize(QtCore.QSize(183,30))
  #self.button.setFocusPolicy(QtCore.Qt.NoFocus)
  self.button.move(135,80)
  self.connect(self.button, QtCore.SIGNAL('clicked()'), self.insert)
  self.button1= QtGui.QPushButton('Update Translete', self)
  self.button1.move(10,560)
  self.connect(self.button1, QtCore.SIGNAL('clicked()'), self.update)
  self.setFocus()
  #self.icon1 = QtGui.QIcon()
  #self.icon1.addPixmap(QtGui.QPixmap('unnamed.png'))
  self.label = QtGui.QLineEdit(self)
  self.label.setGeometry(130,40,260,30)
  self.ba = QtGui.QLabel(self)
  self.ba.setPixmap(QtGui.QPixmap('png1.png'))
  self.mess=QtGui.QMessageBox(self)
  #self.errorMessageDialog = QtGui.QErrorMessage(self)
  self.dialogbox=QtGui.QInputDialog()
  self.dialogbox1=QtGui.QInputDialog()
  self.lbl5 = QtGui.QTextEdit(self)
  self.lbl5.setReadOnly(True)
  self.lbl5.setGeometry(30,150,430,400)
  self.setStyleSheet("QWidget {border:inset;border-radius:3px;color :black;font-weight:500; font-size: 10pt}QPushButton{color:#099000;border-style: outset;border-width: 2px;border-radius: 10px;border-color: beige;font: bold 14px;min-width: 10em;padding: 6px;}QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}")
  self.M=mongo()
  #bottom = QtGui.QFrame(self)
  #bottom.setFrameShape(QtGui.QFrame.StyledPanel)
  #bottom.setGeometry(30,150,430,400)
  with open('Words.txt','a+') as f:
   if len(f.read()) == 0 : 
    f.write("#SCRIPT: PERSDIC\n# AUTHOR: Kasra Ahmadvand // kasra.ahmadvand@gmail.com\n# DATE:   2013/7/20\n# REV:    1.1.0.T (Valid are A, B, T and P)\n#         (For Alpha, Beta, Test and Production)')\n************************ WORDS LIST ************************\n") 
   else:
    b= sum(1 for line in f)
    lbl4 = QtGui.QLabel('['+ str(b)+']'+	' word exist in your dict...!', self)
    lbl4.move(110,125)
    f.close()
 def insert(self):
    flag=True
    pox=2
    inword=(self.label.text()).toLower()
    if self.M.find(str(inword)):
     with open('Words.txt','a+') as f:
      for line in f:
       if line==(str(inword)+'\n'):
        self.mess.information(self,"Word exist in personal words !", self.M.prin(str(inword)))
        #self.label.clear()
        flag=False
        break
      if flag:
       self.lbl5.clear()
       self.lbl5.append(self.M.prin(str(inword)))
       f.write(str(inword))
       f.write('\n')
       #self.msg.setText(dic1[i].decode('utf8'))
       #self.msg.exec_()
       #self.label.clear()
    else:
     text,ok=self.dialogbox.getText(QtGui.QInputDialog(),'Create Persian meaning','Enter meaning here: ',QtGui.QLineEdit.Normal,'meaning')
     if ok :  
       self.M.ins(str(inword),unicode(text))
       #self.label.clear()
       with open('Words.txt','a+') as f:
        f.write(inword)
        f.write('\n')

 def update(self):
  M=mongo()
  inword=(self.label.text()).toLower()
  text,ok=self.dialogbox1.getText(QtGui.QInputDialog(),'Update meaning','Enter meaning here: ',QtGui.QLineEdit.Normal,M.prin((str(inword))))
  if ok :
   self.M.update(str(inword),unicode(text))
 

 def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.insert()


if __name__ == "__main__":
 app = QtGui.QApplication(sys.argv)
 icon = InputDialog()
 icon.show()
 app.exec_()


