from PyQt4 import QtCore, QtGui, uic


class Mensaje():

	def cartel(self,titulo,mensaje,tipo):
	
		msgBox=QtGui.QMessageBox()
		msgBox.setIcon(tipo)
		msgBox.setWindowTitle(titulo)
		msgBox.setText(mensaje)
		msgBox.exec_()
		
	def cartel_opcion(self,titulo,mensaje,tipo):
		msgBox=QtGui.QMessageBox()
		msgBox.setIcon(tipo)
		msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		
		msgBox.setWindowTitle(titulo)
		msgBox.setText(mensaje)
		r= msgBox.exec_()
		
		
		return r
