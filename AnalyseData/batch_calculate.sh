#!/bin/bash
if [ $1 = "help" ]; then
	echo "./batch_cmd repetition_group use_node_hash"
	exit 0
fi

repetition_group=$1
use_node_hash=$2
calculate_method='./CalculateDelay_batch.py'
record_rounds="${@:3}"

for dirname in ./${repetition_group}/* ; do
	# dirpath="${repetition_group}/${dirname}"
	cmd="${calculate_method} subset ${use_node_hash} ${dirname}  ${record_rounds} "
	echo $cmd
	$cmd
done

