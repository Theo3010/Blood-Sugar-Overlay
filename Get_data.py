try:
	from datetime import datetime
	import time
	from bs4 import BeautifulSoup
	import requests
	import re

	last_updata = ""

	def Get_Settings(FileNumber):
		try:
			file = open("Settings/settings.txt").readlines()
			if FileNumber != None:
				return file[FileNumber].strip("\n")
			else:
				return file[0].strip("\n"), file[1].strip("\n"), file[2].strip("\n"), file[3].strip("\n"), file[4].strip("\n"), file[5].strip("\n"), file[6].strip("\n")
		except Exception as e:
			print("ERROR: Sytem Error", "\n" + "File: Get_data.py", "Function: Get_Settings", "Exception:", e)

	def update_data(w, a):
		try:
			print("Staring new window\n\n")
			last_mmol = ""
			last_stining = ""
			

			while True:
				data = get_data() #get data
				
				#assign data
				mmol_arrow = data[3] 
				stining = data[1]
				
				#check if the data has update and change the labels
				if mmol_arrow != last_mmol or stining != last_stining:
					global last_updata
					last_updata = data[4]
					w.label1.setText(mmol_arrow) #mmol_arrow
					w.label2.setText(stining) #stining
					last_mmol = mmol_arrow
					last_stining = stining

				
		except Exception as e:
			print("ERROR: Sytem Error", "\n" + "File: Get_data.py", "Function: update_data", "Exception:", e)
	
	def change_clock(w, a):
		try:
			time.sleep(3)
			global last_updata
			last_updata = last_updata.split(":")
			last_updata = (int(last_updata[0]), int(last_updata[1]))
			while True:
				data = get_data()
				clock_now = data[4]
				clock_now = clock_now.split(":")
				clock_now = (int(clock_now[0]), int(clock_now[1]))
				clock_now_in_minutes = clock_now[0]*60+clock_now[1]
				last_updata_in_minutes = last_updata[0]*60+last_updata[1]
				time_to_updata = clock_now_in_minutes - last_updata_in_minutes
				print(clock_now_in_minutes, last_updata_in_minutes)
				w.label.setText(f"minutes to next updata: time_to_updata") #updating the clock
				w.label3.setText(f"clock now: {data[4]}") #updating the clock
		except Exception as e:
			print("ERROR: Sytem Error", "\n" + "File: Get_data.py", "Function: change_clock", "Exception:", e)

	def get_data():
		try:
			#get the time of the day
			date = datetime.now()
			timer = date.strftime("%H:%M")

			#get the link to sugarmate!
			link = Get_Settings(2)
			
			mmolPileTxt = ""
			reading = ""
			mmolstingning = "0.0"
			
			#try to see if the link works
			try:
				source = requests.get(link).text
			except Exception as e:
				print("wrong link", e)
				quit()
			soup = BeautifulSoup(source, 'lxml')

			#Get only the impoten data by using RE
			pattern_reading = re.compile(r'"reading":"\d+.\d+')
			macthes_reading = pattern_reading.finditer(str(soup))
			for match in macthes_reading:
				reading = match.group(0)
			
			pattern_mmolPile = re.compile(r'words":"\w+')
			macthes_mmolPile = pattern_mmolPile.finditer(str(soup))
			for match in macthes_mmolPile:
				mmolPileTxt = match.group(0)
			
			
			pattern_mmolstingning = re.compile(r'(\+?-?0.\d+ | \+?-?1.\d+ | \+?-?2.\d+ | \+?-?3.\d+ | .OLD. )')
			macthes_mmolstingning = pattern_mmolstingning.finditer(str(soup))
			for match in macthes_mmolstingning:
				mmolstingning = match.group(0)
			
			mmol = reading[11:]
			
			#Making the arrow a image from txt
			arrowsTxt = ["FORTY_FIVE_UP", "FLAT", "FORTY_FIVE_DOWN", "SINGLE_UP", "DOUBLE_DOWN", "DOUBLE_UP"] #list of the arrow as txt
			arrowsimg = [" ➚", " →", " ➘", " ↑", " ↓", " ↓↓", " ↑↑"] #list of the arrows as image
			mmolPile = None
			for i in range(0, len(arrowsTxt)): 
				if mmolPileTxt[8:] == arrowsTxt[i]:
					mmolPile = mmol + arrowsimg[i]
			if mmolPile == None:
				mmolPile = mmol
			

			#return the values
			return (mmol, mmolstingning.strip(" []"), mmolPileTxt[8:], mmolPile, timer) #mmol (5.1), stining (+0.2), stining_txt (FLAT), mmol+pille (5.1 →), timer (14:55)
		except Exception as e:
			print("ERROR: Sytem Error", "\n" + "File: Get_data.py", "Function: Get_data", "Exception:", e)
except Exception as e:
	print("ERROR: Sytem Error", "\n" + "File: Get_data.py", "Function: None", "Exception:", e)