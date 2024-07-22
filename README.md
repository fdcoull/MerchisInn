# MerchisInn

## Installation
From project directory, run:
mkdir var
touch merchisinn.db
touch etc/key.cfg
python3 init_db.py
python3 init_key.py

Then to generate a key, open the python3 terminal and type the following:
import os
os.urandom(24)

Then copy the string output to your etc/key.cfg secret_key line

From here, just run the app using:
flask --app app run --host=0.0.0.0 --port=8080

