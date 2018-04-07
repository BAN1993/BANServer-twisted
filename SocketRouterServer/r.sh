
rm -rf log/*

path=`pwd`

pname=$path/main.py
pid=`ps -ef | grep "[0-9] python $pname" | awk '{print $2}'`
kill $pid

python $path/main.py &

sleep 1
tail -f log/*


