#!/bin/bash

case $1 in
"start")
  msg="Running!"
  pushd thesaurus
  ./app.sh boot
  popd
  ;;
"stop")
  msg="Building!"
  pushd thesaurus
  /app.sh stop
  popd
  ;;
"restart")
  msg="Booting!"
  pushd thesaurus
  /app.sh stop
  /app.sh boot
  popd
  ;;
*)
  msg="
  Oops! '$1' is not a valid option:\noptions: \n\trun \n\tbuild \n\tboot \n\tstop \n\tstop \n\trestart"
  ;;
esac

echo -e $msg