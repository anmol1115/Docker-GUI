from tkinter import *

class MyImageFrame:
	def __init__(self, master, ImageName):
		self.image = ImageName
		self.frame = Frame(master, highlightbackground="black", highlightthickness=1)

	def draw(self):
		Label(self.frame, text=self.image).pack(side=LEFT, padx=10, pady=20)
		buttonFrame = Frame(self.frame)

		Button(buttonFrame, text="Run", bg="#e95420", command=self.run).grid(row=0, column=0, padx=3)
		Button(buttonFrame, text="Info", bg="#e95420").grid(row=0, column=1, padx=3)
		Button(buttonFrame, text="Delete", bg="#e95420").grid(row=0, column=2, padx=3)

		buttonFrame.pack(side=RIGHT, padx=10, pady=20)
		self.frame.pack(fill='x', padx=5, pady=2, side=TOP)

	def run(self):
		print(self.image)

class RootStructure:
	def __init__(self, master):
		self.master = master
		self.images = []
		self.containers = []
		self.topButtons()
		self.defineLabelFrame()

	def defineLabelFrame(self):
		self.ImageLabelFrame = LabelFrame(self.master, text="Images", bg="#ffffff")
		self.ContainerLabelFrame = LabelFrame(self.master, text="Containers", bg="#ffffff")

	def topButtons(self):
		self.frame = Frame(self.master)
		images = Button(self.frame, text="Images", bg="#e95420", height=1, width=10, command=self.showImages).grid(row=0, column=0, padx=10)
		containers = Button(self.frame, text="Containers", bg="#e95420", height=1, width=10, command=self.showContainers).grid(row=0, column=1, padx=10)
		self.frame.pack(pady=20)

	def showImages(self):
		self.master.after(0, self.ContainerLabelFrame.destroy)
		self.master.after(0, self.ImageLabelFrame.destroy)
		self.defineLabelFrame()
		self.ImageLabelFrame.pack(fill="both", expand="yes", padx=5, pady=2)

		for i in range(3):
			self.images.append(MyImageFrame(self.ImageLabelFrame, str(i)))

		for i in range(3):
			self.images[i].draw()


	def showContainers(self):
		self.master.after(0, self.ImageLabelFrame.destroy)
		self.master.after(0, self.ContainerLabelFrame.destroy)
		self.defineLabelFrame()
		self.ContainerLabelFrame.pack(fill="both", expand="yes", padx=5, pady=2)

if __name__ == "__main__":
	root = Tk()
	root.geometry("650x500")
	root.resizable(width=False, height=False)

	rs = RootStructure(root)

	root.mainloop()