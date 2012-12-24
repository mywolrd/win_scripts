#coding=korean
import win32file, win32api, os, Tkinter, tkFileDialog, shutil, fileinput, re

class Patch:
	def getDirectory(self):
		tempDrives = win32api.GetLogicalDriveStrings()
		tempDrives = tempDrives.split("\x00")
		lolDir = "Riot Games\\League of Legends\\"
		drives = []
		found = ""
		
		for drv in tempDrives:
			if win32file.GetDriveType(drv) == win32file.DRIVE_FIXED:
				drives.append(drv+lolDir)

		drives.append(os.getenv("ProgramFiles")+lolDir)			
		
		for drv in drives:
			if os.path.isdir(drv):
				self.lolDir = drv
	
	def changeFontSWF(self):
		path = self.lolDir +"RADS\\projects\\lol_air_client\\releases\\"
		kor = "fonts_ko_KR.swf"
		fonts = "fonts.swf"
		
		if os.path.isdir(path):
			dirList = [path+d for d in os.listdir(path)]
			path = max(dirList, key=lambda x: os.path.getmtime(x))
			
			path += "\\deploy\\css\\"
			
			if os.path.isdir(path):
				original_font = path+fonts
				kor_font = path+kor
				if os.path.isfile(kor_font) and os.path.isfile(original_font):
					shutil.copy(original_font, original_font+".backup")
					shutil.copy(kor_font, original_font)
		
	def changeFontFile(self):
		font = "fontconfig_en_US.txt"
		path = "RADS\\projects\\lol_game_client_en_us\\managedfiles\\"
		path = self.lolDir + path
		searchStr = ["fontlib", "$ButtonFont", "$NormalFont", "$TitleFont", "$IMECandidateListFont"]
		newLine = ""
		
		if os.path.isdir(path):
			dirList = [path+d for d in os.listdir(path)]
			path = max(dirList, key=lambda x: os.path.getmtime(x))
			
		path += "\\Data\\Menu"
		if os.path.isdir(path):
			path += "\\"+font
			if not os.path.isfile(path+".backup"):
				shutil.copy(path, path+".backup")
				
				for line in fileinput.input(path, inplace=1):
					if searchStr[0] in line:
						newLine = re.sub(r"gfxfontlib.swf", "fonts_kr.swf", line)
						print "%s" % (newLine),
					elif searchStr[1] in line:
						newLine = re.sub(r"=[\s]*\"(.+?)*\"", "= \"UttumDotum\"", line)
						print "%s" % (newLine),
					elif searchStr[2] in line:
						newLine = re.sub(r"=[\s]*\"(.+?)*\"", "= \"UttumDotum\"", line)
						print "%s" % (newLine),
					elif searchStr[3] in line:
						newLine = re.sub(r"=[\s]*\"(.+?)*\"", "= \"UttumDotum\"", line)
						print "%s" % (newLine),
					elif searchStr[4] in line:
						newLine = re.sub(r"=[\s]*\"(.+?)*\"", "= \"UttumDotum\"", line)
						print "%s" % (newLine),
					else:
						print "%s" % (line),
				
				self.status = True
				fileinput.close()
				
	def changeToBackUp(self):
		font = "fontconfig_en_US.txt"
		path = "RADS\\projects\\lol_game_client_en_us\\managedfiles\\"
		path = self.lolDir + path
		
		if os.path.isdir(path):
			dirList = [path+d for d in os.listdir(path)]
			path = max(dirList, key=lambda x: os.path.getmtime(x))
			
		path += "\\Data\\Menu"
		if os.path.isdir(path):
			path += "\\"+font
			if os.path.isfile(path+".backup"):
				if os.path.isfile(path):
					os.remove(path)					
					shutil.copy(path+".backup", path)
					os.remove(path+".backup")
					self.status = True
		
		path = self.lolDir + "RADS\\projects\\lol_air_client\\releases\\"
		fonts = "fonts.swf"
		
		if os.path.isdir(path):
			dirList = [path+d for d in os.listdir(path)]
			path = max(dirList, key=lambda x: os.path.getmtime(x))
			
			path += "\\deploy\\css\\"
			
			if os.path.isdir(path):
				original_font = path+fonts
				if os.path.isfile(original_font+".backup"):
					shutil.copy(original_font+".backup", original_font)
		
	def patchKor(self):
		self.getDirectory()
		
		if len(self.lolDir) == 0 :		
			lolDir = tkFileDialog.askdirectory(title='못찾겠다. 롤 폴더를 찾아서 선택'.decode("korean"))
		
		self.changeFontFile()
		self.changeFontSWF()
		if self.status:
			self.strvar.set("끝".decode("korean"))
		else:
			self.strvar.set("실패. 끝".decode("korean"))
			
	def rollBack(self):
		self.getDirectory()
		self.changeToBackUp()
		if self.status:
			self.strvar.set("끝".decode("korean"))
		else:
			self.strvar.set("실패. 끝".decode("korean"))
		
	def __init__(self, root):
		
		self.lolDir = ""
		self.frame = Tkinter.Frame(root, height=100, width=150)
		self.frame.pack()
		self.frame.pack_propagate(0)
		
		self.status = False
		
		self.strvar = Tkinter.StringVar()
		self.strvar.set("로비 & 게임 내 한글 패치".decode("korean"))
		self.w = Tkinter.Label(self.frame, textvariable=self.strvar)
		self.w.pack()
		
		self.patchButton = Tkinter.Button(self.frame, text="Patch", command = self.patchKor)
		self.patchButton.pack(side=Tkinter.LEFT)
		
		self.rollBackButton = Tkinter.Button(self.frame, text="Roll Back", command = self.rollBack)
		self.rollBackButton.pack(side=Tkinter.LEFT)
		
		self.quitButton = Tkinter.Button(self.frame, text="Quit", command = root.quit)
		self.quitButton.pack(side=Tkinter.BOTTOM)
		
root = Tkinter.Tk()
Patch(root)
root.mainloop()
			