rm -rf outlog
mkdir outlog

players=0
if [ ! -n "$1" ] ;then  
	echo "r.sh - test 1 player"
	players=1
else
	echo "r.sh - test $1 players"
	players=$1
fi

times=100
if [ ! -n "$2" ] ;then  
	echo "r.sh - test 100 times"
	times=100
else
	echo "r.sh - test $2 times"
	times=$2
fi

for((now=1;now<=$players;now++)) ;do
	python pushtest.py test$now $times 1>>outlog/"test"$now"_"$times".log" 2>>outlog/"test"$now"_"$times".log" &
done
