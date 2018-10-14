rm -rf /usr/local/teleserver/*
git clone https://github.com/Dysproz/teleserver.git
chmod 0777 /usr/local/teleserver/*
pkill -f teleserver
nohup /usr/local/teleserver/run.py &
\n
\n
