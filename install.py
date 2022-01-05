import os

if os.path.isfile('requirements.txt'):
    os.system('pip3 install -r requirements.txt')
    od.system('sudo apt-get install python3-tk')
    os.system("sudo apt install wkhtmltopdf")
else:
    print ("File not exist, make sure requirements.txt exist in the cwd")