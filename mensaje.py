from PyQt4 import QtCore, QtGui, uic


class Mensaje():

	def cartel(self,titulo,mensaje,tipo):
	
		msgBox=QtGui.QMessageBox()
		msgBox.setIcon(tipo)
		msgBox.setWindowTitle(titulo)
		msgBox.setText(mensaje)
		msgBox.exec_()
		
