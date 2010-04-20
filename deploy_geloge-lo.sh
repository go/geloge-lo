#!/bin/bash
CONF=$HOME/.geloge-lo

BASEDIR=`echo $(cd $(dirname $0);pwd)`/geloge-lo

for KEY in `cat $CONF|awk '{print $1}'`; do
  VAL=`fgrep $KEY $CONF | awk '{print $2}'`
  if [ -z $1 ]; then
    echo "convert $KEY to $VAL"
    sed -i -e "s/$KEY/$VAL/g" $BASEDIR/geloauth/twitter.py
  else
    echo "revert $VAL to $KEY"
    sed -i -e "s/$VAL/$KEY/g" $BASEDIR/geloauth/twitter.py
  fi
done
