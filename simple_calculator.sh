#!/usr/bin/env bash

touch operation_history.txt
echo -n > operation_history.txt

echo Welcome to the basic calculator! | tee -a operation_history.txt

while true; do

    echo "Enter an arithmetic operation or type 'quit' to quit:" | tee -a operation_history.txt
    
    read input 
    echo "$input" >> operation_history.txt

    if [[ $input == 'quit' ]]; then
        echo Goodbye! | tee -a operation_history.txt
       
        break
    fi
    
    re='^-?[0-9]+.?[0-9]* [-+*/^] -?[0-9]+.?[0-9]*$'
    
    if [[ "$input" =~ $re ]]; then
        echo $(echo "scale=2; $input" | bc -l) | tee -a operation_history.txt
       
    else
        echo Operation check failed! | tee -a operation_history.txt
   
    fi
done
