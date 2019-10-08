#!/bin/bash

case $1 in
"run")
  msg="Running!"
  docker-compose up -d
  ;;
"build")
  msg="Building!"
  docker-compose build
  ;;
"boot")
  msg="Booting!"
  docker-compose up --build -d
  ;;
"dev")
  msg "Booting and running dev server"
  docker-compose -f docker-dev.yaml up --build -d
  yarn --cwd frontend run dev
  ;;
"stop")
  msg="Stopping!"
  docker-compose stop
  ;;
"restart")
  msg="Removing containers!"
  docker-compose restart
  ;;
"restart")
  msg="Starting backend"
  pushd backend
  go get -u all
  go build
  ./backend
  popd
  ;;
*)
  msg="
  Oops! '$1' is not a valid option:\noptions: \n\trun \n\tbuild \n\tboot \n\tstop \n\tstop \n\trestart"
  ;;
esac

echo -e $msg