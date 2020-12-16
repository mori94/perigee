#!/bin/bash

rm AnalyseData/*.txt

useNodeHash=$1

record_round="0 2 4 6 8 10 12 14"
for (( i=0; i<=15 ; i++ )); do
	record_round="${record_round} $i"
done

max_round=0
for num in ${record_round}; do
	if [ $num -gt ${max_round} ] ; then
		max_round=$num
	fi
done
echo ${max_round}
exit 0
python main.py 0 $useNodeHash 
cd AnalyseData
./CalculateDelay.py subset $useNodeHash ${record_round}
./plothash.py . ${record_round}

