#!/usr/bin/env bash

#echo Enter a message:
#read -r string
#echo "$string"

echo Enter an uppercase letter:
read -r letter
echo Enter a key:
read -r number

re1='^[A-Z]$'
re2='^[0-9]$'

#check if two regex match          


if [[ "$letter" =~ $re1 ]] && [[ "$number" =~ $re2 ]]; then
    #change $letter to a ASCII value
    ascii_letter=$(printf "%d\n" "'$letter")
    #add $number to ASCII value
    ascii_letter=$((ascii_letter + number))
    #if ASCII value is greater than 90, subtract 26 from it 
    if [[ $ascii_letter -gt 90 ]]; then
        ascii_letter=$((ascii_letter - 26))
    fi

    
    #change ASCII value to a letter
    letter=$(printf "\x$(printf %x $ascii_letter)")

    echo "$letter"
    #give me more time to check the output  
    sleep 10
    


    

else
    echo Invalid key or letter!
fi