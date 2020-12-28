#!/bin/bash
trap kill_batch INT

if [ $1 = "help" ]; then
	echo "./cmd name[string] seed[int] useNodeHash[y/n] roundList[intList]"
	echo "./cmd two-hop-subset 1 y 0 1 2 3"
	echo "./cmd two-hop-subset 1 n 0 1 2 3 4 12 20 28 36 44 52 69 68 76 84 92 100 108"
	exit 0
fi

if [ "$#" -le 3 ]; then
  echo "Error. Argument invalid"
	exit 0
fi

function kill_batch() {
	exit 0
}

name=$1
seed=$2
use_node_hash=$3
record_round="${@:4}"


# run experiment
dirname="${name}_seed${seed}"
dirpath="AnalyseData/$dirname"
mkdir $dirpath
cp config.py $dirpath
# python main.py ${seed} ${use_node_hash} ${record_round}
python testbed.py ${seed} ${dirpath} ${use_node_hash} ${record_round}
retval=$?
if [ "$retval" -ne 0 ]; then
	echo "simulation bug. Exit"
	exit 1
fi	
# mv AnalyseData/*.txt $dirpath

# Calculate it
cd AnalyseData
cal_cmd="./CalculateDelay_batch.py subset ${use_node_hash} ${dirname} ${record_round}"
echo ${cal_cmd}
${cal_cmd}

# Plot it 
plot_cmd="./plot_single.py ${dirname} ${record_round}"
echo ${plot_cmd}
${plot_cmd}
open "${dirname}/${dirname}.png"

