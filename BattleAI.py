#!/usr/bin/python3

# #laingame IRC bot 'BattleAI'
# Derived from RussianBot by Lance Brignoni
# Copyright (C) 2015 #laingame
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see http://www.gnu.org/licenses/

import sys
import socket
import time

# Server and channel to join:
server = "irc.freenode.net"
channel = "#laingame"

# Bot Nick, 'BattleAI' is registered with NickServ, you can use other nicks for testing:
botnick = "BattleAI"

# Password goes here (REDACT BEFORE PUBLISHING ANYWHERE):
password = ""

# Almighty overlords able to use privileged commands like '.quit':
owners = ["MrDetonia","cyber-user","roniz"]

#join channel
def joinchan(chan):
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))

#The two first lines are used to connect to the server through port 6667 which is the most used irc-port.
#The third line sends the username, realname etc.
#The fourth line assigns a nick to the bot, and the last line then joins the configured channel.
#all bytes must be converted to utf-8
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667))
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :connected\n", "UTF-8"))
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8"))
time.sleep(3)

# Identify with NickServ
ircsock.send(bytes("NICKSERV :IDENTIFY %s\r\n" % password, "UTF-8"))
time.sleep(3)
joinchan(channel)

while True:
    readbuffer = ""
    readbuffer = readbuffer+ircsock.recv(2048).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    print(readbuffer) #prints incoming messages
    readbuffer=temp.pop( )
    get_time = int(time.strftime("%M"))
    get_sec = int(time.strftime("%S"))
    time.sleep(1)

    # Messages that can be sent to server/channel
    def sendmsg(chan , msg):
        ircsock.send(bytes("PRIVMSG "+ chan +" :"+ msg +"\n", "UTF-8"))
    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)
        try:
            # Respond to server PINGs
            if(line[0] == "PING"):
                ircsock.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))

            # Channel messages
            if(line[1] == "PRIVMSG"):
                #get name of player
                sender = ""
                for char in line[0]:
                    if(char == "!"):
                        break
                    if(char != ":"):
                        sender += char

                # .bots - responds to a generic .bots query
                if(line[3] == ":.bots"):
                    msg = "BattleAI is 100% operational. [Python] ALPHA VERSION"
                    ircsock.send(bytes("PRIVMSG "+ channel +" :"+ msg +"\n", "UTF-8"))

                # .ping - respond to pings with the pingers nick
                if(line[3] == ":.ping"):
                    msg = "WARNING: " + sender + " attempted communication. This incident will be logged."
                    ircsock.send(bytes("PRIVMSG " + channel +" :"+ msg +"\n", "UTF-8"))

                # .quit - OWNER ONLY, quits the server and kills the bot process
                if(line[3] == ":.quit" and sender in owners):
                    ircsock.send(bytes("QUIT : BattleAI shut down.\n", "UTF-8"))
                    sys.exit(0)


        except IndexError:
            pass

