import subprocess
from tkinter import *

class PasswordWindow:
	def __init__(self):
		self.root = Tk()
		self.root.title("Docker GUI")
		self.root.geometry('300x175')
		self.show()
		self.root.resizable(width=False, height=False)
		self.root.mainloop()

	def getPass(self):
		if not self.password.get():
			return None
		return self.password.get()

	def submit(self):
		cmd = f"echo {self.getPass()}| sudo -k -S -v"
		length = len(subprocess.getoutput(cmd).split('\n'))
		if length == 1:
			self.root.destroy()
		else:
			self.password_slot.delete(0, len(self.getPass()))
			inc_pass_label = Label(self.root, text="Incorrect Password")
			inc_pass_label.grid()
			self.root.after(2000, inc_pass_label.destroy)

	def toggle(self, value):
		if value.get() == 0:
			self.password_slot = Entry(self.root, textvariable=self.password, show='*')
			self.password_slot.grid(row=0, column=1, pady=5)
		else:
			self.password_slot = Entry(self.root, textvariable=self.password)
			self.password_slot.grid(row=0, column=1, pady=5)

	def show(self):
		show_pass = IntVar()
		self.password = StringVar()

		Label(self.root, text="Root password").grid(row=0, column=0, pady=50)
		Button(self.root, text="Submit", bd=2, bg="#e95420", fg="#090909", command=self.submit).grid(row=1, column=1)
		Checkbutton(self.root, text="Show password", variable=show_pass, onvalue=1, offvalue=0, command=lambda: self.toggle(show_pass)).grid(row=1, column=0)
		self.password_slot = Entry(self.root, textvariable=self.password, show='*')
		self.password_slot.grid(row=0, column=1, pady=5)

if __name__ == "__main__":
	pw = PasswordWindow()
	print(pw.getPass())