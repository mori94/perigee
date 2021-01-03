#!/bin/bash
trap kill_batch INT

if [ $1 = "help" ]; then
	echo "./cmd subcommand[run/complete] name[string] seed[int] useNodeHash[y/n] out_lim[int] roundList[intList]"
	echo "./cmd run two-hop-subset 1 8 y 0 1 2 3"
	echo "./cmd two-hop-subset 1 8 n 0 1 2 3 4 12 20 28 36 44 52 69 68 76 84 92 100 108"
	exit 0
fi

if [ "$#" -le 3 ]; then
  echo "Error. Argument invalid"
	exit 0
fi

function kill_batch() {
	exit 0
}

subcommand=$1
name=$2
seed=$3
out_lim=$4
use_node_hash=$5

record_round="${@:6}"

dirname="${name}_seed${seed}"
dirpath="AnalyseData/$dirname"
mkdir $dirpath
cp config.py $dirpath

# run experiment
if [ ${subcommand} = 'run' ]; then 
	python testbed.py run ${seed} ${dirpath} ${out_lim} ${use_node_hash} ${record_round}
else
	python testbed.py complete_graph ${seed} ${dirpath} ${out_lim} ${use_node_hash} ${record_round}
fi
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
plot_cmd="./plot_single.py ${dirname} ${seed} ${record_round}"
echo ${plot_cmd}
${plot_cmd}
open "${dirname}/${dirname}.png"

