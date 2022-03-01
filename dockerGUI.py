from tkinter import *
from dockerClients import ImageClient

class MyImageFrame:
	def __init__(self, master, imageName, imageInfo):
		self.master = master
		self.image = imageName
		self.imageInfo = imageInfo
		self.frame = Frame(master, highlightbackground="black", highlightthickness=1)

	def draw(self):
		Label(self.frame, text=self.image).pack(side=LEFT, padx=10, pady=20)
		buttonFrame = Frame(self.frame)

		Button(buttonFrame, text="Run", bg="#e95420", command=self.run).grid(row=0, column=0, padx=3)
		Button(buttonFrame, text="Info", bg="#e95420", command=self.info).grid(row=0, column=1, padx=3)
		Button(buttonFrame, text="Delete", bg="#e95420", command=self.delete).grid(row=0, column=2, padx=3)

		buttonFrame.pack(side=RIGHT, padx=10, pady=20)
		self.frame.pack(fill='x', padx=5, pady=2, side=TOP)

	def run(self):
		def driver(mode, master):
			master.destroy()
			if mode.get() == "advanced":
				self.advanceRun()
			if mode.get() == "easy":
				self.easyRun()

		flag = StringVar()
		flag.set("easy")
		index = self.image.index(':')
		name = self.image[:index]
		top = Toplevel(self.master)

		element_frame = LabelFrame(top, bg="#ffffff")
		Radiobutton(element_frame, text="Easy setup", variable=flag, value="easy", bg="#ffffff").pack(anchor=W, padx=5)
		Radiobutton(element_frame, text="Advanced Setup", variable=flag, value="advanced", bg="#ffffff").pack(anchor=W, padx=5)
		element_frame.pack(fill=BOTH, expand="yes", padx=10, pady=10)
		Button(top, text="Submit", bg="#e95420", command=lambda: driver(flag, top)).pack(anchor=E, padx=5, pady=5)

		top.geometry("200x120")
		top.title(f"{name} run")
		top.resizable(width=False, height=False)
		top.mainloop()

	def info(self):
		index = self.image.index(':')
		name = self.image[:index]
		tag = self.image[index+1:]
		top = Toplevel(self.master)

		element_frame = LabelFrame(top, bg="#ffffff")
		Label(element_frame, text=f"Tag: {tag}", bg="#ffffff").pack(pady=5)
		Label(element_frame, text=f"Image ID: {self.imageInfo[0]}", bg="#ffffff").pack(pady=5)
		Label(element_frame, text=f"Created: {self.imageInfo[1]}", bg="#ffffff").pack(pady=5)
		Label(element_frame, text=f"Size: {self.imageInfo[2]}", bg="#ffffff").pack(pady=5)
		element_frame.pack(padx=10, pady=10, fill=BOTH, expand="yes")

		top.geometry("250x145")
		top.title(f"{name} info")
		top.resizable(width=False, height=False)
		top.mainloop()

	def delete(self):
		def remove(master, name):
			rs.imageclient.delImage(name)
			rs.refreshScreen()

		index = self.image.index(':')
		name = self.image[:index]
		top = Toplevel(self.master)

		element_frame = Frame(top)
		Label(element_frame, text="This process is irreversible, do you still want to continue ?").pack(side=LEFT, padx=10)
		Button(element_frame, text="Continue", bg="#e95420", command=lambda: remove(top, self.image)).pack(side=RIGHT, padx=10)
		element_frame.pack(fill=BOTH, expand="yes", side=TOP)

		top.geometry("500x80")
		top.title(f"{name} info")
		top.resizable(width=False, height=False)
		top.mainloop()

	def advanceRun(self, valid=True):
		def cancel(master):
			master.destroy()
			self.run()
		def submit(master, cmd):
			if "docker run" in cmd:
				index = cmd.rindex(' ')
				if cmd[index+1:] == self.image:
					master.destroy()
					rs.imageclient.run(cmd)
				else:
					master.destroy()
					rs.imageclient.run(cmd[:index]+' '+self.image)
			else:
				self.advanceRun(valid=False)

		index = self.image.index(':')
		name = self.image[:index]
		top = Toplevel(self.master)

		element_frame = Frame(top)
		Label(element_frame, text="Pass in your docker command:").pack(anchor=W, padx=5, pady=5)
		command_entry = Entry(element_frame)
		command_entry.pack(fill=X, anchor=W, padx=5)
		element_frame.pack(fill=BOTH, expand="yes", padx=10, pady=10)

		buttonFrame = Frame(top)
		Button(buttonFrame, text="Submit", bg="#e95420", command=lambda: submit(top, command_entry.get())).pack(side=RIGHT)
		Button(buttonFrame, text="Cancel", bg="#e95420", command=lambda: cancel(top)).pack(side=RIGHT)
		buttonFrame.pack(anchor=E, padx=10, pady=5)

		if not valid:
			invalid_label = Label(top, text="Invalid Command")
			invalid_label.pack(anchor=W, padx=10, pady=5)
			top.after(2000, invalid_label.destroy)

		top.geometry("500x140")
		top.resizable(width=False, height=False)
		top.title(f"{name} run")
		top.mainloop()

	def easyRun(self):
		def cancel(master):
			master.destroy()
			self.run()
		def submit(master):
			part_cmd = ""
			if name_check.get():
				part_cmd += " --name="+_name.get()
			if net_check.get():
				part_cmd += " --net="+net_name.get()
			if port_check.get():
				_map = []
				_map = port_map.get(1.0, END).split('\n')
				_map = [ports for ports in _map if ports != '']
				part_cmd += " -p "+" -p ".join(_map)
			if vol_check.get():
				_map = []
				_map = vol_map.get(1.0, END).split('\n')
				_map = [vols for vols in _map if vols != '']
				part_cmd += " -v "+" -v ".join(_map)
			cmd = "docker run -dit" + part_cmd + ' ' + self.image
			master.destroy()
			rs.imageclient.run(cmd)

		name_check = StringVar()
		net_check = StringVar()
		port_check = StringVar()
		vol_check = StringVar()

		index = self.image.index(':')
		name = self.image[:index]
		top = Toplevel(self.master)

		name_frame = LabelFrame(top, text="Name")
		Checkbutton(name_frame, text="Name", variable=name_check, onvalue=1, offvalue=0).pack(anchor=W, padx=5)
		Label(name_frame, text="Container Name").pack(side=LEFT, padx=5)
		_name = Entry(name_frame)
		_name.pack(side=RIGHT, padx=5)
		name_frame.pack(anchor=N, fill=BOTH, expand="yes", padx=10, pady=1)

		network_frame = LabelFrame(top, text="Network Setting")
		Checkbutton(network_frame, text="Select Network", variable=net_check, onvalue=1, offvalue=0).pack(anchor=W, padx=5)
		Label(network_frame, text="Network Name").pack(side=LEFT, padx=5)
		net_name = Entry(network_frame)
		net_name.pack(side=RIGHT, padx=5)
		network_frame.pack(anchor=N, fill=BOTH, expand="yes", padx=10, pady=1)

		port_frame = LabelFrame(top, text="Port Mapping")
		Checkbutton(port_frame, text="Map Port(s)", variable=port_check, onvalue=1, offvalue=0).pack(anchor=W, padx=5)
		Label(port_frame, text="Map ports in seperate lines").pack(side=LEFT, padx=5, pady=2)
		port_map = Text(port_frame, width=30, height=5)
		port_map.pack(side=RIGHT, padx=5, pady=2)
		port_frame.pack(anchor=N, fill=BOTH, expand="yes", padx=10, pady=1)

		volume_frame = LabelFrame(top, text = "Volume Mapping")
		Checkbutton(volume_frame, text="Map Volume(s)", variable=vol_check, onvalue=1, offvalue=0).pack(anchor=W, padx=5)
		Label(volume_frame, text="Map volumes in seperate lines").pack(side=LEFT, padx=5, pady=2)
		vol_map = Text(volume_frame, width=30, height=5)
		vol_map.pack(side=RIGHT, padx=5, pady=2)
		volume_frame.pack(anchor=N, fill=BOTH, expand="yes", padx=10, pady=1)

		buttonFrame = Frame(top)
		Button(buttonFrame, text="Submit", bg="#e95420", command=lambda: submit(top)).pack(side=RIGHT)
		Button(buttonFrame, text="Cancel", bg="#e95420", command=lambda: cancel(top)).pack(side=RIGHT)
		buttonFrame.pack(anchor=E, padx=10, pady=5)

		top.geometry("500x500")
		top.resizable(width=False, height=False)
		top.title(f"{name} run")
		top.mainloop()

class RootStructure:
	def __init__(self, master):
		self.master = master
		self.imageclient = ImageClient("Admin@123")
		self.topButtons()
		self.defineLabelFrame()

	def defineLabelFrame(self):
		self.ImageLabelFrame = LabelFrame(self.master, text="Images")
		self.ContainerLabelFrame = LabelFrame(self.master, text="Containers")
		self.SettingsLabelFrame = LabelFrame(self.master, text="Settings")

	def scrollBar(self, master):
		mycanvas = Canvas(master)
		mycanvas.pack(side=LEFT, expand="yes", fill=BOTH)
		myscroll = Scrollbar(master, orient=VERTICAL, command=mycanvas.yview, bg="#ffffff")
		myscroll.pack(side=RIGHT, fill=Y)
		mycanvas.configure(yscrollcommand=myscroll.set)
		mycanvas.bind("<Configure>", lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))
		newFrame = Frame(mycanvas)
		mycanvas.create_window((0,0), window=newFrame, anchor="nw", width=620)
		return newFrame

	def topButtons(self):
		self.frame = Frame(self.master)
		images = Button(self.frame, text="Images", bg="#e95420", height=1, width=10, command=self.showImages).grid(row=0, column=0, padx=10)
		containers = Button(self.frame, text="Containers", bg="#e95420", height=1, width=10, command=self.showContainers).grid(row=0, column=1, padx=10)
		settings = Button(self.frame, text="Settings", bg="#e95420", height=1, width=10, command=self.showSettings).grid(row=0, column=2, padx=10)
		self.frame.pack(pady=20)

	def refreshScreen(self):
		self.master.after(0, self.ImageLabelFrame.destroy)
		self.master.after(0, self.SettingsLabelFrame.destroy)
		self.master.after(0, self.ContainerLabelFrame.destroy)
		self.images = {}
		self.containers = {}
		self.defineLabelFrame()

	def showImages(self):
		self.refreshScreen()
		self.ImageLabelFrame.pack(fill="both", expand="yes", padx=5, pady=2)
		mainFrame = self.scrollBar(self.ImageLabelFrame)
		self.images = self.imageclient.getImages()

		for image, info in self.images.items():
			MyImageFrame(mainFrame, image, info).draw()

	def showContainers(self):
		self.refreshScreen()
		self.ContainerLabelFrame.pack(fill=BOTH, expand="yes", padx=5, pady=2)

	def showSettings(self):
		self.refreshScreen()
		self.SettingsLabelFrame.pack(fill=BOTH, expand="yes", padx=5, pady=2)

		search_frame = LabelFrame(self.SettingsLabelFrame, text="Search Image")
		inner_frame = Frame(search_frame)
		Label(inner_frame, text="Enter Image Name").pack(side=LEFT, padx=10, anchor=N)
		img_name = Entry(inner_frame)
		img_name.pack(side=RIGHT, padx=10, fill=X, expand="yes", anchor=N)
		inner_frame.pack(fill=X, expand="yes")
		Button(search_frame, text="Submit", bg="#e95420").pack(anchor=E, padx=5)
		search_frame.pack(anchor=N, fill=BOTH, expand="yes", padx=10, pady=1)

		element_frame = Frame(self.SettingsLabelFrame, height=200)

		inner_frame = Frame(element_frame)
		create_net_frame = LabelFrame(inner_frame, text="Create Networks")
		Label(create_net_frame, text="Run network Create Command").pack(anchor=W, padx=5, pady=2)
		command_entry = Entry(create_net_frame)
		command_entry.pack(anchor=W, fill = X, padx=5, pady=2)
		Button(create_net_frame, text="Submit", bg="#e95420").pack(anchor=E, padx=5, pady=2)
		create_net_frame.pack(fill=BOTH, expand="yes", padx=10, pady=1, anchor=N)

		pull_frame = LabelFrame(inner_frame, text="Pull image")
		frame1 = Frame(pull_frame)
		Label(frame1, text="Enter Image Name").pack(side=LEFT, padx=5)
		pull_img_name = Entry(frame1)
		pull_img_name.pack(side=RIGHT, fill=X, padx=5)
		frame1.pack(fill=X, expand="yes")
		Button(pull_frame, text="Pull", bg="#e95420").pack(anchor=E, padx=5)
		pull_frame.pack(fill=BOTH, expand="yes", padx=10, pady=1, anchor=N)
		inner_frame.pack(side=LEFT, fill=BOTH, expand="yes", anchor=N)

		inner_frame = Frame(element_frame)
		list_net_frame = LabelFrame(inner_frame, text="List Networks")
		Label(list_net_frame, text="List all available networks").pack(side=LEFT, padx=5, pady=2)
		Button(list_net_frame, text="List", bg="#e95420").pack(side=RIGHT, padx=5, pady=2)
		list_net_frame.pack(anchor=N, fill=BOTH, expand="yes", padx=10, pady=1)

		login_frame = LabelFrame(inner_frame, text="Login DockerHub")
		frame1 = Frame(login_frame)
		Label(frame1, text="Username").pack(side=LEFT, padx=5)
		uname = Entry(frame1)
		uname.pack(side=RIGHT, padx=5, fill=X, expand="yes")
		frame1.pack(fill=X, expand="yes")
		frame2 = Frame(login_frame)
		Label(frame2, text="Password ").pack(side=LEFT, padx=5)
		passwd = Entry(frame2)
		passwd.pack(side=RIGHT, padx=5, fill=X, expand="yes")
		frame2.pack(fill=X, expand="yes")
		Button(login_frame, text="Submit", bg="#e95420").pack(anchor=E, padx=2)
		login_frame.pack(anchor=S, fill=BOTH, expand="yes", padx=10, pady=1)
		inner_frame.pack(side=RIGHT, fill=BOTH, expand="yes")

		element_frame.pack(anchor=N, fill=BOTH, expand="yes")

		inspect_net_frame = LabelFrame(self.SettingsLabelFrame, text="Inspect Networks")
		inner_frame = Frame(inspect_net_frame)
		Label(inner_frame, text="Enter Network Name").pack(side=LEFT, padx=10, pady=2, anchor=N)
		net_name = Entry(inner_frame)
		net_name.pack(side=RIGHT, padx=10, pady=2, fill=X, expand="yes", anchor=N)
		inner_frame.pack(fill=X, expand="yes")
		Button(inspect_net_frame, text="Submit", bg="#e95420").pack(anchor=E, padx=5, pady=2)
		inspect_net_frame.pack(anchor=N, fill=BOTH, expand="yes", padx=10, pady=1)

if __name__ == "__main__":
	root = Tk()
	root.geometry("650x500")
	root.resizable(width=False, height=False)

	rs = RootStructure(root)

	root.mainloop()