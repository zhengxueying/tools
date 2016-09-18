#/bin/bash
#usage ./value.sh type /path/file /path/template
#support type wflow nta ipfix nflow
datatype=$1
filename=$2
template=$3
if [ ! -d ./data ]; then
    mkdir ./data
fi
if [ "$datatype" = "wflow" ]; then
    echo "Handle wflow file"
    /opt/python27/bin/python ./disp-wflow/disp-wflow.pyc $filename --show-all-fields >./data/wflow.dat
    if [ -f ./data/wflow.dat ]; then
        echo "PktCnt_Sum in wflow is:" `cat ./data/wflow.dat|sed 's/,/\n/g'|grep 'PktCnt_Sum' |sed 's/PktCnt_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "PktLen_Sum in wflow is:" `cat ./data/wflow.dat|sed 's/,/\n/g'|grep 'PktLen_Sum' |sed 's/PktLen_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "ConnCount60s in wflow is:" `cat ./data/wflow.dat|grep 'FlowSide=0'|sed 's/,/\n/g'|grep 'ConnCount60s' |sed 's/ConnCount60s=//g'|awk '{sum+=$1}END{print sum}'`
    else
        echo "Wflow file not exist"
    fi
elif [ "$datatype" = "nta" ]; then
    echo "Handle nta file" $filename
    echo "PktCnt_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'PktCnt_Sum' |sed 's/PktCnt_Sum=//g'|awk '{sum+=$1}END{print sum}'`
    echo "PktLen_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'PktLen_Sum' |sed 's/PktLen_Sum=//g'|awk '{sum+=$1}END{print sum}'`
	echo "FlowDir=0,PktCnt_Sum in $filename is:" `cat $filename|grep 'FlowDir=0'|sed 's/\t/\n/g'|grep 'PktCnt_Sum' |sed 's/PktCnt_Sum=//g'|awk '{sum+=$1}END{print sum}'`
	echo "FlowDir=1,PktCnt_Sum in $filename is:" `cat $filename|grep 'FlowDir=1'|sed 's/\t/\n/g'|grep 'PktCnt_Sum' |sed 's/PktCnt_Sum=//g'|awk '{sum+=$1}END{print sum}'`
    echo "FlowDir=0,PktLen_Sum in $filename is:" `cat $filename|grep 'FlowDir=0'|sed 's/\t/\n/g'|grep 'PktLen_Sum' |sed 's/PktLen_Sum=//g'|awk '{sum+=$1}END{print sum}'`
    echo "FlowDir=1,PktLen_Sum in $filename is:" `cat $filename|grep 'FlowDir=1'|sed 's/\t/\n/g'|grep 'PktLen_Sum' |sed 's/PktLen_Sum=//g'|awk '{sum+=$1}END{print sum}'`
    echo "ConnCount60s in $filename is:" `cat $filename|grep 'FlowSide=0'|sed 's/\t/\n/g'|grep 'ConnCount60s' |sed 's/ConnCount60s=//g'|awk '{sum+=$1}END{print sum}'`
elif [ "$datatype" = "ipfix" ]; then
    echo "Handle ipfix file"
    if [ $template ]; then
        /opt/python27/bin/python ./disp-ipfix/disp-ipfix.pyc $filename --load-template $template>./data/ipfix.dat
    else
        /opt/python27/bin/python ./disp-ipfix/disp-ipfix.pyc $filename>./data/ipfix.dat
    fi
    if [ -f ./data/ipfix.dat ]; then
        echo $filename
        echo "Total PktCnt_Sum in ipfix is:" `cat ./data/ipfix.dat|sed 's/,/\n/g' |grep 'packetDeltaCount'|sed 's/packetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "Total PktLen_Sum in ipfix is:" `cat ./data/ipfix.dat|sed 's/,/\n/g' |grep 'octetDeltaCount'|sed 's/octetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`              
        echo "flowDirection=0&PktCnt_Sum in ipfix is:" `cat ./data/ipfix.dat|grep 'flowDirection=0'|sed 's/,/\n/g' |grep 'packetDeltaCount'|sed 's/packetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "flowDirection=0&PktLen_Sum in ipfix is:" `cat ./data/ipfix.dat|grep 'flowDirection=0'|sed 's/,/\n/g' |grep 'octetDeltaCount'|sed 's/octetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "flowDirection=1&PktCnt_Sum in ipfix is:" `cat ./data/ipfix.dat|grep 'flowDirection=1'|sed 's/,/\n/g' |grep 'packetDeltaCount'|sed 's/packetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "flowDirection=1&PktLen_Sum in ipfix is:" `cat ./data/ipfix.dat|grep 'flowDirection=1'|sed 's/,/\n/g' |grep 'octetDeltaCount'|sed 's/octetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
    else
        echo "ipfix file not exist"
    fi
    #else
     #   echo "Need ipfix template!"
    #fi
elif [ "$datatype" = "nflow" ]; then
    echo "Handle nflow file"
    if [ $template ]; then
        /opt/python27/bin/python ./disp-nflow/disp-nflow.pyc $filename --load-template $template>./data/nflow.dat
	else
		/opt/python27/bin/python ./disp-nflow/disp-nflow.pyc $filename>./data/nflow.dat
	fi
    if [ -f ./data/nflow.dat ]; then
        echo $filename
        echo "Total PktCnt_Sum in nflow is:" `cat ./data/nflow.dat|sed 's/,/\n/g' |grep 'packetDeltaCount'|sed 's/packetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "Total PktLen_Sum in nflow is:" `cat ./data/nflow.dat|sed 's/,/\n/g' |grep 'octetDeltaCount'|sed 's/octetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'` 
        echo "flowDirection=0&PktCnt_Sum in nflow is:" `cat ./data/nflow.dat|grep 'flowDirection=0'|sed 's/,/\n/g' |grep 'packetDeltaCount'|sed 's/packetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "flowDirection=0&PktLen_Sum in nflow is:" `cat ./data/nflow.dat|grep 'flowDirection=0'|sed 's/,/\n/g' |grep 'octetDeltaCount'|sed 's/octetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "flowDirection=1&PktCnt_Sum in nflow is:" `cat ./data/nflow.dat|grep 'flowDirection=1'|sed 's/,/\n/g' |grep 'packetDeltaCount'|sed 's/packetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
        echo "flowDirection=1&PktLen_Sum in nflow is:" `cat ./data/nflow.dat|grep 'flowDirection=1'|sed 's/,/\n/g' |grep 'octetDeltaCount'|sed 's/octetDeltaCount=//g'|awk '{sum+=$1}END{print sum}'`
    else
        echo "nflow file not exist"
    fi
    
else
    echo "Type not support"
fi
