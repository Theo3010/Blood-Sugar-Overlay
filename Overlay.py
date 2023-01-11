try:
	from PyQt5 import QtGui, QtCore
	from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QPushButton, QLineEdit
	import sys
	import _thread
	from Get_data import update_data, get_data, Get_Settings, change_clock
	from Notifications import Notifications

	LinkDexcomVAR = "Past the link her!"
	TransparentB = "ON"
	NotificitonsB = "ON"
	ArrowsB = "ON"
	GraphB = "OFF"
	highAlert = "high (10.0)"
	lowAlert = "low (3.9)"
	try:
		class Window(QWidget):
			def __init__(self ):
				super().__init__()
				self.title = "Overlay"
				self.top, self.left, self.width, self.height = 200, 500, 200, 100
				data = get_data()
				self.timer, self.mmol, self.stining = data[4], data[3], data[1]
				self.notifications, self.transparentBoolen , self.Link , self.lav , self.to_pile_ned, self.hoej, self.Graph = Get_Settings(None)
				self.initWindow()
			
			def initWindow(self):
				#InitWindow
				self.setWindowTitle(self.title)
				self.setWindowIcon(QtGui.QIcon("icons/blodsukkerMain.png"))
				self.setGeometry(self.left, self.top, self.width, self.height)
				
				#Make the window Frameless(overlay)
				flags = QtCore.Qt.WindowFlags(QtCore.Qt.WindowStaysOnTopHint)
				self.setWindowFlags(flags)
				#transparent OPTION
				if self.transparentBoolen.strip("\n") == "ON":
					self.setWindowOpacity(0.5)
				
				#buttoms
				# button = QPushButton("Settings", self)
				# button.setIcon(QtGui.QIcon("settings.png"))
				# button.clicked.connect(self.Settings)
				
				#Display Text To screen
				vbox = QVBoxLayout()
				
				self.Text_to_screen()
				vbox.addWidget(self.label)
				vbox.addWidget(self.label3)
				vbox.addWidget(self.label1)
				vbox.addWidget(self.label2)
				#vbox.addWidget(button) 
				
				self.setLayout(vbox)
				
				self.show()
			
			def Settings(self):
				self.setWindowOpacity(0)
				print("hej")
				self.Settings_window = Settings_Window()
				self.Settings_window.show()
			
			def show_again(self):
				if self.transparentBoolen.strip("\n") == "ON":
					print(0.5)
					self.setWindowOpacity(0.5)
				else:
					self.setWindowOpacity(1)
			
			def update(self):
				Transparent = Get_Settings(1)
				if Transparent.strip("\n") == "ON":
					self.setWindowOpacity(0.5)
				else:
					self.setWindowOpacity(1)
				QApplication.processEvents()
				
			def background_Color(self, color):
				self.setStyleSheet(f"background-color: {color};")
			
			def Text_to_screen(self):
				self.label = QLabel(f"Last Update: {self.timer}")
				self.label.setFont(QtGui.QFont("Sanserif", 10))
				self.label1 = QLabel(self.mmol)
				self.label1.setFont(QtGui.QFont("Sanserif", 50))
				self.label2 = QLabel(self.stining)
				self.label2.setFont(QtGui.QFont("Sanserif", 15))
				self.label3 = QLabel(f"clock now: {self.timer}")
				self.label3.setFont(QtGui.QFont("Sanserif", 9))
				hboxlayout = QHBoxLayout()
	except Exception as e:
		print("ERROR: Sytem Error", "\n" + "File: Overlay.py", "Function: Window", "Exception:", e)

	try:
		class Settings_Window(QWidget):
			def __init__(self, parent = None, ):
				global w
				super(Settings_Window, self).__init__(parent)
				self.title = "Settings"
				self.top = 200
				self.Main_Window = w
				self.left = 500	
				self.width = 250
				self.height = 200
				self.setFixedSize(self.width, self.height) 
				self.initWindow()
			
			def initWindow(self):
				#InitWindow
				self.setWindowTitle(self.title)
				self.setWindowIcon(QtGui.QIcon("icons/settings.png"))
				self.setGeometry(self.left, self.top, self.width, self.height)
				
				
				#if the low and hight alert allredy defined
				global lowAlert
				global highAlert
				try:
					file = open("Settings/settings.txt", "r").readlines()
					if file[3] != "low (3.9)":
						lowAlert = file[3]
					if file[5] != "high (10.0)":
						highAlert = file[5]
				except:
					pass
				
				try:
					global TransparentB
					file = open("Settings/settings.txt", "r").readlines()
					if file[1].strip("\n") == "ON":
						TransparentB = "ON"
					if file[1].strip("\n") == "OFF":
						TransparentB = "OFF"
				except:
					pass
				
				#add buttons 
				self.vbox = QVBoxLayout()
				self.buttons()
				self.setLayout(self.vbox)
				
				
				#if the Dexcom allredy linked
				global LinkDexcomVAR
				try:
					file = open("Settings/settings.txt", "r").readlines()
					if file[2] != "None":
						LinkDexcomVAR = file[2]
						self.button4.setText("Link Dexcom: Linked")
				except:
					pass
				
				
				self.show()
			
			def buttons(self):
				global TransparentB
				global LinkDexcomVAR
				global GraphB
				#Create Buttons
				self.button = QPushButton("Open Overlay", self)
				self.button2 = QPushButton("Notificitons", self)
				self.button3 = QPushButton("Transparent: " + TransparentB, self)
				self.button4 = QPushButton("Link Dexcom: Not linked", self)
				#self.button5 = QPushButton("Graph: " + GraphB, self)
				
				#Add a icon
				self.button.setIcon(QtGui.QIcon("icons/blodsukker.png"))
				self.button.setIconSize(QtCore.QSize(32, 32))
				self.button2.setIcon(QtGui.QIcon("icons/alarm.png"))
				self.button2.setIconSize(QtCore.QSize(32, 32))
				self.button3.setIcon(QtGui.QIcon("icons/Transparent.jpg"))
				self.button3.setIconSize(QtCore.QSize(32, 32))
				self.button4.setIcon(QtGui.QIcon("icons/icon.png"))
				self.button4.setIconSize(QtCore.QSize(32, 32))  
				#self.button5.setIcon(QtGui.QIcon("icons/Graph.png"))
				#self.button5.setIconSize(QtCore.QSize(32, 32))
				
				#Add a function to the button
				self.button.clicked.connect(self.OpenOverlay)
				self.button2.clicked.connect(self.Notificitons)
				self.button3.clicked.connect(self.Transparent)
				self.button4.clicked.connect(self.LinkDexcom)
				#self.button5.clicked.connect(self.Graph)
				
				
				#add it to the widget
				self.vbox.addWidget(self.button)
				self.vbox.addWidget(self.button2)
				self.vbox.addWidget(self.button4) #don't swith the to it's bad
				self.vbox.addWidget(self.button3)
				#self.vbox.addWidget(self.button5)
				


			def OpenOverlay(self):
				self.Settings_To_File()
				self.Main_Window.show_again()
				self.Main_Window.update()
				self.close()
				

			def Notificitons(self):
				self.sub = Notificitons_Window()
				self.sub.show()
			
			def Transparent(self):
				global TransparentB
				if TransparentB == "ON":
					self.button3.setText("Transparent: OFF")
					TransparentB = "OFF"
					self.Settings_To_File()
				elif TransparentB == "OFF":
					self.button3.setText("Transparent: ON")
					TransparentB = "ON"
					self.Settings_To_File()
			
			def LinkDexcom(self):
				self.button4.setText("Link Dexcom: Linked")
				self.sub = LinkDexcom_Window()
				self.sub.show()
			
			def Graph(self):
				global GraphB
				if GraphB == "OFF":
					self.button5.setText("Graph: ON")
					GraphB = "ON"
					self.Settings_To_File()
				elif GraphB == "ON":
					self.button5.setText("Graph: OFF")
					GraphB = "OFF"
					self.Settings_To_File()
			
			def Settings_To_File(self):
				global LinkDexcomVAR
				global lowAlert
				global highAlert
				if LinkDexcomVAR == "Past the link her!":
					LinkDexcomVAR = "None"
				if highAlert == "high (10.0)":
					highAlert = "10.0"
				if lowAlert == "low (3.9)":
					lowAlert = "3.9"
				try:
					highAlert = float(highAlert)
					lowAlert = float(lowAlert)
					highAlert = str(highAlert)
					lowAlert = str(lowAlert)
				except:
					highAlert = "10.0"
					lowAlert = "3.9"
				file = open("Settings/settings.txt", "w")
				file.write(NotificitonsB + "\n") #notifications
				file.write(TransparentB + "\n") #transparent
				file.write(LinkDexcomVAR) #Link
				file.write(lowAlert + "\n") #lav
				file.write(ArrowsB + "\n") #to_pile_ned
				file.write(highAlert + "\n") #høj
				file.write(GraphB) #Graph
				file.close()
	except Exception as e:
		print("ERROR: Sytem Error", "\n" + "File: Overlay.py", "Function: Settings_Window", "Exception:", e)

	try:
		class Notificitons_Window(QWidget):
			def __init__(self, parent = None):
				super(Notificitons_Window, self).__init__(parent)
				self.title = "Notificitons Settings"
				self.top = 500
				self.left = 500	
				self.width = 200
				self.height = 200
				self.initWindow()
			
			
			def initWindow(self):
				global NotificitonsB
				global ArrowsB
				#InitWindow
				self.setWindowTitle(self.title)
				self.setWindowIcon(QtGui.QIcon("icons/alarm.png"))
				self.setGeometry(self.left, self.top, self.width, self.height)
				
				
				file = open("Settings/settings.txt", "r").readlines()
				NotificitonsB = file[0].strip("\n")
				ArrowsB = file[4].strip("\n")
				print(NotificitonsB, ArrowsB)
				
				
				#add buttons 
				self.vbox = QVBoxLayout()
				self.buttons()
				self.EditBox()
				self.setLayout(self.vbox)
			 
				
				self.show()
			
			def buttons(self):
				global NotificitonsB
				global ArrowsB
				#Create Buttons
				self.button = QPushButton("Notificitons: " + NotificitonsB, self)
				self.button2 = QPushButton("Arrows UP/DOWN: " + ArrowsB, self)
				self.button3 = QPushButton("Apply", self)
				
				#Add a icon
				self.button.setIcon(QtGui.QIcon("icons/alarm.png"))
				self.button.setIconSize(QtCore.QSize(32, 32))		
				self.button2.setIcon(QtGui.QIcon("icons/arrowUp.png"))
				self.button2.setIconSize(QtCore.QSize(32, 32))		
				self.button3.setIcon(QtGui.QIcon("icons/apply.png"))
				self.button3.setIconSize(QtCore.QSize(32, 32))

				
				#Add a function to the button
				self.button.clicked.connect(self.Notificitons_ON_OFF)
				self.button2.clicked.connect(self.Arrows)
				self.button3.clicked.connect(self.Apply)

				
				
				#add it to the widget
				self.vbox.addWidget(self.button)
				self.vbox.addWidget(self.button2)
			
			def EditBox(self):
				global lowAlert
				global highAlert
				#Add a edit box
				self.EditBox = QLineEdit()
				self.EditBox2 = QLineEdit()
				
				#Give the box som values
				self.EditBox.setObjectName("low")
				self.EditBox.setText(lowAlert)
				self.EditBox2.setObjectName("high")
				self.EditBox2.setText(highAlert)
				
				#set the box to a widget
				self.vbox.addWidget(self.EditBox)
				self.vbox.addWidget(self.EditBox2)
				
				#add the apply button after the the editboxs
				self.vbox.addWidget(self.button3)
			
			def Notificitons_ON_OFF(self):
				global NotificitonsB
				w = Settings_Window()
				if NotificitonsB == "ON":
					self.button.setText("Notificitons: OFF")
					NotificitonsB = "OFF"
					w.Settings_To_File()
				elif NotificitonsB == "OFF":
					self.button.setText("Notificitons: ON")
					NotificitonsB = "ON"
					w.Settings_To_File()
			
			def Arrows(self):
				global ArrowsB
				w = Settings_Window()
				if ArrowsB == "ON":
					self.button2.setText("Arrows UP/DOWN: OFF")
					ArrowsB = "OFF"
					w.Settings_To_File()
				elif ArrowsB == "OFF":
					self.button2.setText("Arrows UP/DOWN: ON")
					ArrowsB = "ON"
					w.Settings_To_File()
			
			def Apply(self):
				global lowAlert
				global highAlert
				w = Settings_Window()
				lowAlert = self.EditBox.text()
				highAlert = self.EditBox2.text()
				w.Settings_To_File()
				self.close() 
	except Exception as e:
		print("ERROR: Sytem Error", "\n" + "File: Overlay.py", "Function: Notificitons_Window", "Exception:", e)

	try:
		class LinkDexcom_Window(QWidget):
			def __init__(self, parent = None):
				super(LinkDexcom_Window, self).__init__(parent)
				self.title = "Link Dexcom"
				self.top = 500
				self.left = 500	
				self.width = 200
				self.height = 200
				self.initWindow()
			
			
			def initWindow(self):
				#InitWindow
				self.setWindowTitle(self.title)
				self.setWindowIcon(QtGui.QIcon("icons/icon.png"))
				self.setGeometry(self.left, self.top, self.width, self.height)
				
				#add buttons 
				self.vbox = QVBoxLayout()
				self.EditBox()
				self.buttons()
				self.setLayout(self.vbox)
				
				self.show()
			
			def buttons(self):
				#Create Buttons
				self.button = QPushButton("Enter", self)
				
				#Add a icon
				self.button.setIcon(QtGui.QIcon("icons/apply.png"))
				self.button.setIconSize(QtCore.QSize(32, 32))

				
				#Add a function to the button
				self.button.clicked.connect(self.Enter)

				
				
				#add it to the widget
				self.vbox.addWidget(self.button)
			
			def EditBox(self):
				global LinkDexcomVAR
				#Add a edit box
				self.EditBox = QLineEdit()
				
				#Give the box som values
				self.EditBox.setObjectName("LinkDexcom")
				self.EditBox.setText(LinkDexcomVAR)
				
				#set the box to a widget
				self.vbox.addWidget(self.EditBox)
			
			def Enter(self):
				global LinkDexcomVAR
				w = Settings_Window()
				LinkDexcomVAR = self.EditBox.text()
				w.Settings_To_File()
				self.close()
	except Exception as e:
		print("ERROR: Sytem Error", "\n" + "File: Overlay.py", "Function: LinkDexcom_Window", "Exception:", e)

	try:
		if __name__ == "__main__":
			App = QApplication(sys.argv)
			global w
			w = Window()
			_thread.start_new_thread(update_data, (w, "a") )
			_thread.start_new_thread(Notifications, (w, "a") )
			_thread.start_new_thread(change_clock, (w, "a") )
			sys.exit(App.exec_())
	except Exception as e:
		print("ERROR: Sytem Error", "\n" + "File: Overlay.py", "Function: Starting...", "Exception:", e)
except Exception as e:
	print("ERROR: Sytem Error", "\n" + "File: Overlay.py", "Function: None", "Exception:", e)

