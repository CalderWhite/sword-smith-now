import logging,json, tkinter, time, threading, sys
from tkinter import ttk
class gui(object):
	def __init__(self):
		self.tk = tkinter.Tk()
		self.tk.geometry("760x480+0+0")
		##self.tk.resizable(width=False, height=False)
		self.tk.title("Launching...")
		# text
		self.log_field = tkinter.Text(self.tk,height=10,width=95 )
		self.log_text = ""
		self.log_field.configure(state=tkinter.DISABLED)
		self.log_field.grid(row=0)
		##self.log_field.pack()
		pass
class launcher(object):
	def __init__(self,mode,log_file,info_file,initial_gui=False):
		if mode == 0 or mode == 1 or mode == 2:
			# mode index:
			# 0 : normal mode; nothing special.
			# 1 : developer mode; will check modules, as if it were being run by the python interperator instead of .exe format.
			# 2 : cheats mode; nothing yet, going to be a version of dev mode to test bosses with hacks.
			self.mode = mode
			print("Running log configuration.\nAll other logging/debugging messages will be sent to the specified log file once configured.")
			logging.basicConfig(filename=log_file,level="INFO")
			self.game_info_name = info_file
			self.game_name = "GAME NAME IS UNKNOWN"
			self.initial_gui = initial_gui
			self.allow_run = None
			self.waiting = True
		else:
			raise Exception("Launch mode [%s] not supported" % mode)
		pass
	def try_launch(self):
		if self.allow_run:
			self.log("Launching [%s]..." % self.game_name)
		elif self.allow_run == False:
			self.log("There were errors during checks, no launch may be run.",level="ERROR")
		elif self.allow_run == None:
			self.log("Launch was attempted by user, but all checks have not yet been completed.",level="WARNING")
			pass
	def load(self):
		if self.initial_gui:
			logging.log(logging.INFO,"Running Launcher with gui.")
			#creating and defining window
			self.gui = gui()
			# start the mainloop thread
			self.gui.tk.update()
			self.log("Running launcher in gui...")
			s = ttk.Style()
			s.configure('my.TButton', font=("Arial", 12,"bold"),padding=17,width=25,justify="center")
			self.play_b = ttk.Button(self.gui.tk, text="Play", command=self.try_launch,style="my.TButton")
			self.play_b.grid(row=1)
			checks = self.do_checks()
			if checks:
				self.log("Load was succesful.")
				self.allow_run = True
			else:
				self.allow_run = False
			self.waiting_loop()
		else:
			self.log("Running launcher in non-gui mode.")
			checks = self.do_checks()
			if checks:
				self.log("Load was succesful.")
				self.allow_run = True
				def ask_launch():
					x = input("Launch?(Y/N):")
					y = recive_input(x)
					return y
				def recive_input(x):
					x = x.upper()
					if x == "Y":
						return True
					elif x == "N":
						self.log("Succesful load, user decided not to launch.")
					else:
						self.log("Got answer that was neither \"Y\" or \"N\". Asking again...")
						print("Please Enter either Y or N")
						ask_launch()
				z = ask_launch()
				if z:
					self.try_launch()

			else:
				self.log("Stopping launch, shutting down program...")
				self.allow_run = False
		self.log("--------------------------------------------------------")
	def waiting_loop(self):
		"""Just wait for some user input"""
		self.gui.tk.mainloop()
	def log(self,msg,level="INFO"):
		logging.log(logging.__getattribute__(level),msg)
		if self.initial_gui:
			self.gui.log_field.pack_forget()
			self.gui.log_field = tkinter.Text(self.gui.tk,height=10,width=95 )
			self.gui.log_text = self.gui.log_text + "[" + level + "] : " + msg + "\n"
			##print(self.gui.log_text)
			self.gui.log_field.insert(tkinter.END,self.gui.log_text)
			self.gui.log_field.grid(row=0)
			self.gui.log_field.configure(state=tkinter.DISABLED)
			##self.gui.log_field.pack()
			self.gui.tk.update()
			self.gui.log_field.see(tkinter.END)
		pass
	def module_checklist(self):
		self.log("Loading the game info file [%s]..." % (self.game_info_name))
		r = open(self.game_info_name,'r').read()
		info = json.loads(r)
		try:
			x = info["modules"]
			x = info["name"]
		except IndexError:
			self.log("Couldn't find \"modules\" in game info file (%s)" % self.game_info_name,level="ERROR")
			raise Exception("Couldn't find \"modules\" in game info file (%s)" % self.game_info_name)
		else:
			self.game_name = info["name"]
			if self.initial_gui:
				self.gui.tk.title(self.game_name + " Launcher")
			self.log("Checking required modules...")
			for i in info["modules"]:
				try:
					__import__(i)
				except:
					self.log("No [%s] module, which is required." % i,level="ERROR")
			self.log("All required modules present.")
	def do_checks(self):
		if self.mode == 0:
			print("CONSUMER VERSION IS NOT YET SUPPORTED.")
		elif self.mode == 1:
			self.log("Running launch. Mode : 1")
			try:
				self.module_checklist()
			except:
				self.log("Hit error in developer mode [mode 1]. While running %s" % (self.__class__.__name__ + ".module_checklist()"),level="CRITICAL")
				self.log(str(sys.exc_info()))
				return False
			else:
				return True
		elif self.mode == 2:
			pass
if __name__ == '__main__':
	launch = launcher(1,"Sword_Smith_Now_logs.log","game_info.json",initial_gui=False)
	launch.load()
