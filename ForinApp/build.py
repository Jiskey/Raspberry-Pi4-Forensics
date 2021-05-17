#build.py runs and installs all required packages and tools
#Run with 'sudo python3 build.py'

import os

print('Starting...')
os.system('sudo pip3 install click')
os.system('sudo pip3 install simple_term_menu')
os.system('sudo pip3 install pytest')
os.system('sudo apt-get -y install dc3dd')
os.system('sudo apt-get -y install dcfldd')
os.system('sudo apt-get -y install foremost')
os.system('sudo apt-get -y install scalpel')
os.system('sudo apt-get -y install testdisk') #photorec
os.system('sudo apt-get -y install sleuthkit')
os.system('sudo apt-get -y install pdf-parser')
os.system('sudo apt-get -y install pdf-id')
os.system('sudo apt-get -y install hashcat')

input('Done. Press Any button to continue.')
os.system('clear')