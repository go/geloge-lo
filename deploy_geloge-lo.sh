#!/bin/bash
CONF=$HOME/.geloge-lo

BASEDIR=`echo $(cd $(dirname $0);pwd)`/geloge-lo

for KEY in `cat $CONF|awk '{print $1}'`; do
  VAL=`fgrep $KEY $CONF | awk '{print $2}'`
  if [ -z $1 ]; then
    echo "convert $KEY to $VAL"
    sed -iold -e "s/$KEY/$VAL/g" $BASEDIR/authtest.py $BASEDIR/authcallbacktest.py 
  else
    echo "revert $VAL to $KEY"
    sed -iold -e "s/$VAL/$KEY/g" $BASEDIR/authtest.py $BASEDIR/authcallbacktest.py 
  fi
done
