# signum-blockaccouncer
Simple block win announcer for Discord


* Tested on python 3.7
* Install requirements with `pip install -r requirements.txt`
* Edit main.py and fill in your discord webhook url and signum pool url.
* Run main.py with a cronjob or something. It creates a file in the same directory that keeps the most recent block ID to prevent looping trough all wins every time.
