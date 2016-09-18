#/bin/bash
#usage ./tcpcalc.sh type /path/file ip /path/template
#support type nta ipfix nflow
filename=$2
datatype=$1
ip=$3
template=$4
if [ ! -d ./data ]; then
    mkdir ./data
fi

if [ "$datatype" = "nta" ]; then
    echo "Handle nta file" $filename
    if [ $ip ]; then
        echo "MsgCnt_Client_Sum in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'MsgCnt_Client_Sum' |sed 's/MsgCnt_Client_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "MsgCnt_Server_Sum in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'MsgCnt_Server_Sum' |sed 's/MsgCnt_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "ProcTime_Server_Sum in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'ProcTime_Server_Sum' |sed 's/ProcTime_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "TransTime_Client_Sum in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'TransTime_Client_Sum' |sed 's/TransTime_Client_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "TransTime_Server_Sum in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'TransTime_Server_Sum' |sed 's/TransTime_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Client_Sum in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'NetworkDelay_Client_Sum' |sed 's/NetworkDelay_Client_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Client_Cnt in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'NetworkDelay_Client_Cnt' |sed 's/NetworkDelay_Client_Cnt=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Server_Sum in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'NetworkDelay_Server_Sum' |sed 's/NetworkDelay_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Server_Cnt in $filename is:" `cat $filename|grep $ip|sed 's/\t/\n/g'|grep 'NetworkDelay_Server_Cnt' |sed 's/NetworkDelay_Server_Cnt=//g'|awk '{sum+=$1}END{print sum}'`
    else
        echo "MsgCnt_Client_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'MsgCnt_Client_Sum' |sed 's/MsgCnt_Client_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "MsgCnt_Server_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'MsgCnt_Server_Sum' |sed 's/MsgCnt_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "ProcTime_Server_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'ProcTime_Server_Sum' |sed 's/ProcTime_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "TransTime_Client_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'TransTime_Client_Sum' |sed 's/TransTime_Client_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "TransTime_Server_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'TransTime_Server_Sum' |sed 's/TransTime_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Client_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'NetworkDelay_Client_Sum' |sed 's/NetworkDelay_Client_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Client_Cnt in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'NetworkDelay_Client_Cnt' |sed 's/NetworkDelay_Client_Cnt=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Server_Sum in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'NetworkDelay_Server_Sum' |sed 's/NetworkDelay_Server_Sum=//g'|awk '{sum+=$1}END{print sum}'`
        echo "NetworkDelay_Server_Cnt in $filename is:" `cat $filename|sed 's/\t/\n/g'|grep 'NetworkDelay_Server_Cnt' |sed 's/NetworkDelay_Server_Cnt=//g'|awk '{sum+=$1}END{print sum}'`
    fi
elif [ "$datatype" = "ipfix" ]; then
    echo "Handle ipfix file" $filename
    if [ $template ]; then
        /opt/python27/bin/python ./disp-ipfix/disp-ipfix.pyc $filename --load-template $template --show-all-fields>./data/ipfixtcp.dat
		if [ -f ./data/ipfixtcp.dat ]; then
			echo "transactionCountDelta/MsgCnt in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'transactionCountDelta' |sed 's/transactionCountDelta=//g'|awk '{sum+=$1}END{print sum}'`
			echo "sumTotalRespTime/RespTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumTotalRespTime' |sed 's/sumTotalRespTime=//g'|awk '{sum+=$1}END{print sum}'`
			echo "sumServerRespTime/ProcTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumServerRespTime' |sed 's/sumServerRespTime=//g'|awk '{sum+=$1}END{print sum}'`
			echo "sumTransactionTime/TransactionTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumTransactionTime' |sed 's/sumTransactionTime=//g'|awk '{sum+=$1}END{print sum}'`
			echo "sumServerNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumServerNwkTime' |sed 's/sumServerNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
			echo "sumClientNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumClientNwkTime' |sed 's/sumClientNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
		else 
			echo "Error!File not Exist!"
		fi
    else
		if [ $ip ]; then
			if [[ "$ip" =~ ^(([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$ ]]; then
				/opt/python27/bin/python ./disp-ipfix/disp-ipfix.pyc $filename  --show-all-fields>./data/ipfixtcp.dat
				if [ -f ./data/ipfixtcp.dat ]; then
					echo "transactionCountDelta/MsgCnt in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'transactionCountDelta' |sed 's/transactionCountDelta=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumTotalRespTime/RespTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumTotalRespTime' |sed 's/sumTotalRespTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumServerRespTime/ProcTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumServerRespTime' |sed 's/sumServerRespTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumTransactionTime/TransactionTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumTransactionTime' |sed 's/sumTransactionTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumServerNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumServerNwkTime' |sed 's/sumServerNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumClientNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'sumClientNwkTime' |sed 's/sumClientNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
				else 
					echo "Error!File not Exist!"
				fi
			else 
				/opt/python27/bin/python ./disp-ipfix/disp-ipfix.pyc $filename --load-template $ip --show-all-fields>./data/ipfixtcp.dat
				if [ -f ./data/ipfixtcp.dat ]; then
					echo "transactionCountDelta/MsgCnt in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'transactionCountDelta' |sed 's/transactionCountDelta=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumTotalRespTime/RespTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumTotalRespTime' |sed 's/sumTotalRespTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumServerRespTime/ProcTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumServerRespTime' |sed 's/sumServerRespTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumTransactionTime/TrnasactionTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumTransactionTime' |sed 's/sumTransactionTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumServerNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumServerNwkTime' |sed 's/sumServerNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
					echo "sumClientNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumClientNwkTime' |sed 's/sumClientNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
				else
					echo "Error!File not Exist!"
				fi
			fi
		else
			/opt/python27/bin/python ./disp-ipfix/disp-ipfix.pyc $filename  --show-all-fields>./data/ipfixtcp.dat
			if [ -f ./data/ipfixtcp.dat ]; then
				echo "transactionCountDelta/MsgCnt in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'transactionCountDelta' |sed 's/transactionCountDelta=//g'|awk '{sum+=$1}END{print sum}'`
				echo "sumTotalRespTime/RespTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumTotalRespTime' |sed 's/sumTotalRespTime=//g'|awk '{sum+=$1}END{print sum}'`
				echo "sumServerRespTime/ProcTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumServerRespTime' |sed 's/sumServerRespTime=//g'|awk '{sum+=$1}END{print sum}'`
				echo "sumTransactionTime/TrnasactionTime in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumTransactionTime' |sed 's/sumTransactionTime=//g'|awk '{sum+=$1}END{print sum}'`
				echo "sumServerNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumServerNwkTime' |sed 's/sumServerNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
				echo "sumClientNwkTime/NetworkDelay in ipfixtcp.dat is:" `cat ./data/ipfixtcp.dat|sed 's/,/\n/g'|grep 'sumClientNwkTime' |sed 's/sumClientNwkTime=//g'|awk '{sum+=$1}END{print sum}'`
			else
				echo "Error!File not Exist!"
			fi
		fi
	fi
    
elif [ "$datatype" = "nflow" ]; then
    echo "Handle nflow file" $filename
    if [ $template ]; then
        /opt/python27/bin/python ./disp-nflow/disp-nflow.pyc $filename --load-template $template --show-all-fields>./data/nflowtcp.dat
		if [ -f ./data/nflowtcp.dat ]; then
			echo "connection delay network to-server sum/42087 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42087' |sed 's/RESERVED42087=//g'|awk '{sum+=$1}END{print sum}'`
            echo "connection delay network to-client sum/42084  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42084' |sed 's/RESERVED42084=//g'|awk '{sum+=$1}END{print sum}'`
            echo "connection transaction duration sum/42041  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42041' |sed 's/RESERVED42041=//g'|awk '{sum+=$1}END{print sum}'`
            echo "connection delay response client-to-ser/42077 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42077' |sed 's/RESERVED42077=//g'|awk '{sum+=$1}END{print sum}'`
            echo "connection delay application sum/42074 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42074' |sed 's/RESERVED42074=//g'|awk '{sum+=$1}END{print sum}'`
            echo "connection transaction counter complete/42040 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42040' |sed 's/RESERVED42040=//g'|awk '{sum+=$1}END{print sum}'`
            echo "connection client counter packets retra/42036 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42036' |sed 's/RESERVED42036=//g'|awk '{sum+=$1}END{print sum}'`
		else
			echo "Error!File not Exist!"
		fi
    else
		if [ $ip ]; then
			if [[ "$ip" =~ ^(([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]{1,2}|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$ ]]; then
				/opt/python27/bin/python ./disp-nflow/disp-nflow.pyc $filename --show-all-fields>./data/nflowtcp.dat
				if [ -f ./data/nflowtcp.dat ]; then
					echo "connection delay network to-server sum/42087 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42087' |sed 's/RESERVED42087=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection delay network to-client sum/42084  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42084' |sed 's/RESERVED42084=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection transaction duration sum/42041  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42041' |sed 's/RESERVED42041=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection delay response client-to-ser/42077 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42077' |sed 's/RESERVED42077=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection delay application sum/42074 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42074' |sed 's/RESERVED42074=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection transaction counter complete/42040 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42040' |sed 's/RESERVED42040=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection client counter packets retra/42036 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|grep $ip|sed 's/,/\n/g'|grep 'RESERVED42036' |sed 's/RESERVED42036=//g'|awk '{sum+=$1}END{print sum}'`
				else 
					echo "Error!File not Exist!"
				fi
			else
				/opt/python27/bin/python ./disp-nflow/disp-nflow.pyc $filename --load-template $ip --show-all-fields>./data/nflowtcp.dat
				if [ -f ./data/nflowtcp.dat ]; then
					echo "connection delay network to-server sum/42087 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42087' |sed 's/RESERVED42087=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection delay network to-client sum/42084  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42084' |sed 's/RESERVED42084=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection transaction duration sum/42041  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42041' |sed 's/RESERVED42041=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection delay response client-to-ser/42077 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42077' |sed 's/RESERVED42077=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection delay application sum/42074 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42074' |sed 's/RESERVED42074=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection transaction counter complete/42040 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42040' |sed 's/RESERVED42040=//g'|awk '{sum+=$1}END{print sum}'`
					echo "connection client counter packets retra/42036 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42036' |sed 's/RESERVED42036=//g'|awk '{sum+=$1}END{print sum}'`
				else
					echo "Error!File not Exist!"
				fi
			fi
        else
			/opt/python27/bin/python ./disp-nflow/disp-nflow.pyc $filename --show-all-fields>./data/nflowtcp.dat
			if [ -f ./data/nflowtcp.dat ]; then
				echo "connection delay network to-server sum/42087 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42087' |sed 's/RESERVED42087=//g'|awk '{sum+=$1}END{print sum}'`
				echo "connection delay network to-client sum/42084  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42084' |sed 's/RESERVED42084=//g'|awk '{sum+=$1}END{print sum}'`
				echo "connection transaction duration sum/42041  in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42041' |sed 's/RESERVED42041=//g'|awk '{sum+=$1}END{print sum}'`
				echo "connection delay response client-to-ser/42077 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42077' |sed 's/RESERVED42077=//g'|awk '{sum+=$1}END{print sum}'`
				echo "connection delay application sum/42074 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42074' |sed 's/RESERVED42074=//g'|awk '{sum+=$1}END{print sum}'`
				echo "connection transaction counter complete/42040 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42040' |sed 's/RESERVED42040=//g'|awk '{sum+=$1}END{print sum}'`
				echo "connection client counter packets retra/42036 in nflowtcp.dat is:" `cat ./data/nflowtcp.dat|sed 's/,/\n/g'|grep 'RESERVED42036' |sed 's/RESERVED42036=//g'|awk '{sum+=$1}END{print sum}'`
			else
				echo "Error!File not Exist!"
			fi
		fi
	fi
else 
    echo "File not exist!"
fi
            
