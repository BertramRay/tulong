#!/bin/bash
# tulong-server
source tulong/bin/activate
cd tulong-server_/tulong_api
gunicorn app:app -b 0.0.0.0:5000 --daemon
# tulong-client
cd tulong-client_
npm run dev