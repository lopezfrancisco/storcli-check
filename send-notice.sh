#! /bin/bash

mailto="lopez@uci.edu"
errorsto="lopez@uci.edu"
scriptdir="/root/raid_check"
masterfile="$scriptdir/raid.master.txt"
subject="`hostname` RAID check `date +%Y-%m-%d`"
sendemail="n"

dayofweek=`date +%a`
messagesent="$scriptdir/chk-raid-$dayofweek"
if [ ! -f $messagesent ]
then
    touch $messagesent
    # now erase flag from prior day
    priorday=`date -d yesterday +%a`
    messagesent="$scriptdir/chk-raid-$priorday"
    [ -f $messagesent ] && /bin/rm $messagesent
    sendemail="y"
fi

tmpfile="$scriptdir/chk-raid-$$"
$scriptdir/compare.py $masterfile > $tmpfile
if [ $? != 0 ]
then
    # found problems
    mailto="$errorsto"
    subject="`hostname` RAID problems `date +%Y-%m-%d`"
    sendemail="y"
fi

if [ "$sendemail" = "y" ]
then
    mail -s "$subject" $mailto < $tmpfile
fi

/bin/rm $tmpfile
