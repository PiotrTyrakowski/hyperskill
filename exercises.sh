#Create a function that takes either 1, 2, 3 or 0 as arguments. If the argument is 0 then the script should end with the exit command. In other cases, the function should print the respective number and shift arguments with the same amount using the shift command.

function skipper() {
    while(( $1 > 0 )); do
        echo "$1"
        shift "$1"
    done
    exit

}