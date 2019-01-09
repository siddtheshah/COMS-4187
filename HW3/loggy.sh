#!/bin/sh

logDir="/var/log"
query= 
func=
start=$(date --iso -d "10 days ago") #default
end=$(date --iso) #default


usage() {
    echo "usage: $loggy [-f func] [--start timeStart] [--end timeEnd] [-q query]"
    echo "  -f       select function"
    echo "  --start  (optional) choose starting time (format: '1 week ago')"
    echo "  --end    (optional) choose ending time (format: '1 day ago')"
    echo "  -h       display help"
    echo "  -q       query"
    exit 1
}

service() {

    res=$(systemctl is-active $query) 
    
    echo "Service is $res"

    echo "Times Started:"
    journalctl -u $query -S $start -U $end --no-pager | grep Started
    echo "Times Stopped:"
    journalctl -u $query -S $start -U $end --no-pager | grep Stopped
}

boots() {
    last reboot --since $start --until $end
    #echo $(pwd)
}

loginFails() {
    aureport -l --failed --summary -i -ts $(date -d $start +"%m/%d/%Y") -te $(date -d $end +"%m/%d/%Y")
}

aptInstalls() {
    #info=zcat $(ls -tr /var/log/apt/history.log.*) 2>/dev/null |   egrep '^(Start-Date:|Commandline:)' |   grep -v aptdaemon |   egrep -B1 '^Commandline:'

    start=$(date -d $start +"%Y-%m-%d")
    #echo $start

    end=$(date -d $end +"%Y-%m-%d")
    #echo $end    
    cat /var/log/apt/history.log |  egrep '^(Start-Date:|Commandline:)' |   grep -v aptdaemon |   egrep -B1 '^Commandline:' > tmp.txt
    
    next=0
    #sed "/$start/, /$end/p"
    while read line;
    do
        # WORKING CODE
        #echo $line
        lineDate=$(echo $line | grep -o "2...-..-..")
        isDate=$(echo $line | grep -o -c "2...-..-..")

        if [ $isDate -eq 1 ];
        then
            #lineDate="$(grep -o "....-..-.." $(pwd)/line.txt)"
            lds=$(date -d "$lineDate" +%s)
            sds=$(date -d "$start" +%s)
            eds=$(date -d "$end" +%s)
            echo $lineDate
            if [ $sds -le $lds ] && [ $lds -le $eds ];
            then
                #echo "First"
                echo $line
                next=1
            fi
            #echo "================== SET HERE ==================="
        elif [ $next -eq 1 ];
        then
            echo $line
        fi

    done<"$(pwd)/tmp.txt"
}

search() {
    journalctl -S $start -U $end | grep $query
}


while [ "$1" != "" ]; do
    case $1 in
        -f )                    shift
                                func=$1
                                ;;
        --start )               shift
                                start=$(date --iso --date "$1")
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        --end )                 shift
                                end=$(date --iso --date "$1")
                                ;;
        -q )                    shift
                                query=$1
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

$func
