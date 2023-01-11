try:
	from Get_data import Get_Settings, get_data
	import time
	from playsound import playsound


	def Notifications(window, a):
		while True:
			try:
				Turn_Notifications = Get_Settings(0)
				lav = Get_Settings(3)
				hoej = Get_Settings(5) # høj
				to_pile_ned = Get_Settings(4)
				arrowTxT = get_data()[2]
				mmol = get_data()[0]
				mmol = float(mmol)
				lav = float(lav)
				hoej = float(hoej)

				if Turn_Notifications == "OFF":
					break
				
				if mmol <= lav:
					change_window("red", window, "alarmLav.wav")
				elif mmol >= hoej:
					change_window("yellow", window, "HojAlarm.wav")
				
				if to_pile_ned == "ON":
					if arrowTxT == "DOUBLE_UP":
						change_window("red", window, "alarmLav.wav")
					elif arrowTxT == "DOUBLE_DOWN":
						change_window("yellow", window, "HojAlarm.wav")
			except Exception as e:
				print("ERROR: Sytem Error", "\n" + "File: Notifications.py", "Function: Notifications", "Exception:", e)



	def change_window(color, window, sound):
		try:
			window.background_Color(color)
			playsound(f"sounds/{sound}")
			window.background_Color("white")
			time.sleep(1) # 1 + 4 = 5
			window.background_Color(color)
			time.sleep(4) # 5 + 895 = 900
			window.background_Color("white")
			time.sleep(895) #900 sec = 15 min
		except:
			print("ERROR: Sytem Error", "\n" + "File: Notifications.py", "Function: change_window", "Exception:", e)
			quit()
except Exception as e:
	print("ERROR: Sytem Error", "\n" + "File: Notifications.py", "Function: None", "Exception:", e)