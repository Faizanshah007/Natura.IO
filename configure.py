import sys, os
import subprocess


required_modules = ['requests==2.23.0','protobuf==3.11.3','google-cloud-speech']
if('3.7' in sys.version):
    required_modules.append('PyAudio-0.2.11-cp37-cp37m-win_amd64.whl')
elif('3.8' in sys.version):
    required_modules.append('PyAudio-0.2.11-cp38-cp38-win_amd64.whl')

print("Please wait while we prepare the good stuff !!")

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for module in required_modules:
    install(module)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd() + r'\generated-arena-275816-1b3ad024b77d.json'
