import subprocess

class ImageClient:
	def __init__(self, password):
		self.passwd = password

	def parseImage(self, string):
		params = string.split("  ")
		params = [param.strip() for param in params if param != '']
		return f"{params[0]}:{params[1]}", params[2:]

	def getImages(self):
		self.images = {}
		cmd = f"echo {self.passwd}| sudo -k -S docker images"
		output = subprocess.getoutput(cmd).split('\n')[1:]
		for line in output:
			indentifier, info = self.parseImage(line)
			self.images[indentifier] = info

		return self.images

	def delImage(self, image):
		cmd = f"echo {self.passwd}| sudo -k -S docker rmi {image}"
		subprocess.run(cmd, shell=True)

	def run(self, cmd):
		cmd = f"echo {self.passwd}| " + cmd
		print(cmd)
		# subprocess.getoutput(cmd)

class SettingsClient:
	def __init__(self, password):
		self.passwd = password
		self.networks = {}

	def loginDockerCLI(self, username, password):
		cmd = f"{{ echo {self.passwd}; echo {password}; }}| sudo -k -S docker login --username {username} --password-stdin"
		print(cmd)

	def listNetworks(self):
		def parse(string):
			params = string.split("  ")
			params = [param.strip() for param in params if param != '']
			return params.pop(1), params

		cmd = f"echo {self.passwd}| sudo -k -S docker network ls"
		output = subprocess.getoutput(cmd).split('\n')[1:]
		for line in output:
			name, info = parse(line)
			self.networks[name] = info
		return self.networks

if __name__ == "__main__":
	# print(ImageClient("Admin@123").getImages())
	print(SettingsClient("Admin@123").listNetworks())