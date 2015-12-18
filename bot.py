#!/usr/bin/python3

# #laingame IRC bot
# Copyright (C) 2015 #laingame Contributors
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

# imports
#########
import time
import socket


# configuration variables
#########################
# server and channel to join:
server = "irc.freenode.net"
channel = "#laingame"

# bot nick:
botNick = "BattleAI"

# bot password (REDACT BEFORE PUBLISHING):
password = ""

# almighty overlords able to use privileged commands:
owners = ["MrDetonia","cyber-user","roniz"]

# if bot is running:
running = True


# common functions
##################
# send to IRC:
def ircSend(msg):
    print("STATUS - Sending: " + msg)
    ircSock.send(bytes(msg + "\n", "UTF-8"))

# send message to channel:
def ircChanSend(msg):
    ircSend("PRIVMSG " + channel + " :" + msg)


# response functions
####################
# respond to .bots query:
def res_bots():
    ircChanSend("BattleAI is operational.")

# respond to .ping with sender's nick:
def res_ping():
    ircChanSend(sender + " attempted communication. Incident will be logged.")

# OWNERS ONLY
# quit server and kill bot:
def res_quit():
    ircSend("QUIT : BattleAI terminated.")
    global running
    running = False


# command -> function dispatcher
################################
commands = {
    '.bots'     : res_bots,
    '.ping'     : res_ping,
    }

# owners only
owner_commands = {
    '.quit'     : res_quit,
    }

# main procedure
################
# connect to server:
ircSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircSock.connect((server, 6667))
ircSend("USER " + botNick + " " + botNick + " " + botNick + " :connected")
ircSend("NICK " + botNick)
time.sleep(3)

# identify with NickServ:
ircSend("NICKSERV :IDENTIFY " + password + "\r")
time.sleep(3)

# join channel:
ircSend("JOIN " + channel)

# message retrieval/response loop:
while running:
    # clear readBuf and retrieve bytes:
    readBuf = ""
    readBuf = readBuf + ircSock.recv(2048).decode("UTF-8")

    # split up bytes into seperate messages:
    temp = str.split(readBuf, "\n")

    # pop a message and get details:
    readBuf = temp.pop()
    get_time = int(time.strftime("%M"))
    get_sec = int(time.strftime("%S"))
    time.sleep(1)

    # parse messages and act accordingly
    for line in temp:
        # show line in shell
        print("STATUS - received: " + line)

        # always check if we are still running:
        if running == False:
            break

        # sanitise input:
        line = str.rstrip(line)
        line = str.split(line)

        try:
            # respond to PINGs:
            if line[0] == "PING":
                ircSend("PONG " + line[1] + "\r")

            # handle channel messages:
            if line[1] == "PRIVMSG":
                # get sender nick:
                sender = ""
                for char in line[0]:
                    if char == "!": break
                    if char != ":": sender += char

                msg = (line[3])[1:]

                if msg in commands:
                    commands[msg]()
                elif msg in owner_commands and sender in owners:
                    owner_commands[msg]()

        except IndexError:
            pass

print("bot finished execution")
