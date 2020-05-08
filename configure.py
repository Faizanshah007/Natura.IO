import sys, os
import subprocess

py_executable = ''

for ele in os.listdir(sys.executable.replace(r'\pythonw.exe','')):
	if('.exe' in ele and ele != 'pythonw.exe'):
		py_executable = ele
		break
		
required_modules = ['requests','protobuf','google-cloud-speech']
if('64 bit' in sys.version):
        if('3.7' in sys.version):
            required_modules.append('PyAudio-0.2.11-cp37-cp37m-win_amd64.whl')
        elif('3.8' in sys.version):
            required_modules.append('PyAudio-0.2.11-cp38-cp38-win_amd64.whl')
        elif('3.6' in sys.version):
            required_modules.append('PyAudio-0.2.11-cp36-cp36m-win_amd64.whl')
else:
    print("Use python 3.6 and above - 64 bit. Thank You.")
    sys.exit()

print("Please wait while we prepare the good stuff !!")

def install(package):
    subprocess.check_call([sys.executable.replace('pythonw.exe',py_executable), "-m", "pip", "install", package])

for module in required_modules:
    install(module)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd() + r'\My First Project-2eab4206a67d.json'
