#!/bin/sh

# bash sets the $- variable, and puts 'c' in it if it is a non-interactive
# shell
# For other shells, I assume $- is not available
if [ "$SHELL" = "/bin/bash" ]; then
		if echo $- | grep 'c' >/dev/null; then
				return  #non-interactive
		fi
fi

# Run only in interactive sessions
if [ -n "$PS1" ]; then
    if [ -x /etc/sysconfig/keyboard ]; then
	. /etc/sysconfig/keyboard 2> /dev/null
    fi
    
    if [ -z "$BACKSPACE" ]; then
	# the code for Backspace key is arch-dependent.
	# FIXME: what really returns uname for non-PC machines ???
	case `uname -m`-`uname -p` in
	    i[3456789]86-*) BSNUM=14 ;;
	    *-amiga) BSNUM=65 ;;
	    m68k-atari) BSNUM=14 ;;
	    *-macintosh) BSNUM=51 ;;
	    mips-sun) BSNUM=43 ;;
	    *) BSNUM=999 ;;
	esac

	if [ "$BSNUM" != "999" ]; then
	    BACKSPACE=`dumpkeys 2> /dev/null | grep "^keycode  $BSNUM" | awk '{print $4}'`
	fi
    fi
    
    # BackSpace sends BackSpace
    if [ "$BACKSPACE" = "BackSpace" ]; then
    
	if tty --quiet ; then
	    : #stty erase '^H' &
	fi
    
	# xterm
	if [ "$TERM" = "xterm" -o "$TERM" = "xterm-color" ]; then
	    echo -en '\033[36h'
	fi
    
    # BackSpace sends Delete
    else
    
	if tty --quiet ; then
	    : #stty erase '^?' &
	fi
    
	# xterm
	if [ "$TERM" = "xterm" -o "$TERM" = "xterm-color" ]; then
	    echo -en '\033[36l'
	fi
    fi
    
    # activate keypad on xterm
    if [ "$TERM" = "xterm" -o "$TERM" = "xterm-color" ]; then
	# activate keypad
	echo -en '\033>'
    fi

#fix loadkeys bug. Read KEYBOARD from config and parse to loadkeys

 if ps -f | grep '\-bash' | grep tty > /dev/null
 then
    IFS='='
    while read key value; do
        key=${key// /}
        if [ $key = KEYBOARD ]; then
            value=${value// /}
            /bin/loadkeys -u $value > /dev/null
        fi
    done < /etc/sysconfig/keyboard
 fi

fi

# ugly hack for an ugly bug
#killall -9 stty > /dev/null >& /dev/null
