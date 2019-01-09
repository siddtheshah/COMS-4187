
To run loggy.sh:

sh loggy.sh [args]

"usage: $loggy [-f func] [--start timeStart] [--end timeEnd] [-q query]"
"  -f       select function"
"  --start  (optional) choose starting time (format: '1 week ago')"
"  --end    (optional) choose ending time (format: '1 day ago')"
"  -h       display help"
"  -q       query"

functions include:

service
boots                       Note: doesn't require a query
aptInstalls                 Note: doesn't require a query
loginFails                  Note: requires that auditd is installed
search                      Note: wildcard character is "."


examples:

sh loggy.sh -f service --start "3 days ago" --end "1 day ago" -q snapd
sh loggy.sh -f search --start "3 days ago" --end "1 day ago" -q fun.s


