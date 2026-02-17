#!/bin/bash
# Mission Control Dashboard - Background Service

export PYTHONPATH="/root/.openclaw/workspace/tools/cv-optimizer/src:/root/.openclaw/workspace/tools/cv-optimizer"
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

cd /root/.openclaw/workspace/tools/cv-optimizer

# Log file
LOG="/root/.openclaw/workspace/tools/cv-optimizer/dashboard.log"

# Run server
python3 -c "
import sys
sys.path.insert(0, 'src')
import logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)

from mission_control import app
from werkzeug.serving import make_server
import signal
import sys

def signal_handler(sig, frame):
    print('Shutting down...')
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

srv = make_server('0.0.0.0', 5020, app, threaded=True)
print('Mission Control Dashboard running on http://127.0.0.1:5020/')
sys.stdout.flush()
srv.serve_forever()
" >> "$LOG" 2>&1
