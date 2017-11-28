#!/bin/bash

# $1 Relation after running ner4_.py
# $2 no. of docs of class one
# $3 train file
echo "********************************************************"
echo "*********  Run master.sh with three agruments  *********"
echo "/     arg1 - Relation obtained from ner4_train.py      /"
echo "/     arg2 - No. of docs of class 1                    /"
echo "/     arg3 - The train file used in ner4_train.py      /"
echo "********************************************************"

read -p  "Press any key to continue or ESC to abort ..." -s -n 1 key #-p for promt...  -s not to echo input .. -n reads reutrn after n chars 

echo ''
case $key in
     $'\e') exit 1;;
esac


rm Relmerged.csv 

echo "$1"
python merge.py "$1"

echo "Relations merged"

tmpfile=$(mktemp)

awk -F'\t' '{print $NF}' Relmerged.csv > "$tmpfile"

#echo $variable
sed -i  's/\[//g' "$tmpfile"
sed -i  's/]//g' "$tmpfile"

totaldocs=`wc -l "$3"  | awk '{print $1}'`

rm doc_p

python pearson.py "$totaldocs" "$2" "$3" "$tmpfile"


sed -e 's/$/./' -i doc_p

sed -i -e 's/^/XX\t/' doc_p

awk '{printf "%d\t%s\n", NR, $0}' doc_p >  train_file.txt

