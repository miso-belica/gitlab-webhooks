#!/bin/bash


prog="python -m glhooks /path/to/your/config.ini"
PROG_USER="glhooks"
RETVAL=0


start () {
        echo "Starting $prog"
        /usr/bin/sudo -u $PROG_USER $prog &
        RETVAL=$?
}

stop () {
        echo "Stopping $prog"
        kilall $prog
        RETVAL=$?
}

restart () {
        stop
        start
}


case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart|reload)
        restart
        ;;
  status)
        RETVAL=$?
        ;;
  *)
        echo "Usage: service glhooks {start|stop|restart|reload}"
        RETVAL=2
        ;;
esac


exit $RETVAL
