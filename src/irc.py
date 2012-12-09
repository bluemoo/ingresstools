import time
import datetime
import socket
import utilities

last_check = datetime.datetime.now()
mirror = None

network = 'daemonic.foonetic.net'
port = 6667
irc = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
irc.connect ( ( network, port ) )
print irc.recv ( 4096 )
irc.send ( 'NICK BlueBot\r\n' )
irc.send ( 'USER BlueBot BlueBot BlueBot :BlueBot IRC\r\n' )
irc.send ( 'JOIN #mnresistance\r\n' )
irc.send ( 'PRIVMSG #mnresistance :Hello World.\r\n' )
while True:
    data = irc.recv ( 4096 )
    print data
    if data.find ( 'PING' ) != -1:
        irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )
    if data.find ( '!BlueBot quit' ) != -1:
        irc.send ( "PRIVMSG #mnresistance :Fine, if you don't want me\r\n" )
        irc.send ( 'QUIT\r\n' )
    if data.find ( 'hi BlueBot' ) != -1:
        irc.send ( 'PRIVMSG #mnresistance :I already said hi...\r\n' )
    if data.find ( 'hello BlueBot' ) != -1:
        irc.send ( 'PRIVMSG #mnresistance :I already said hi...\r\n' )
    if data.find ( 'KICK' ) != -1:
        irc.send ( 'JOIN #mnresistance\r\n' )
    if data.find ( 'cheese' ) != -1:
        irc.send ( 'PRIVMSG #mnresistance :WHERE!!!!!!\r\n' )
    if data.find ( 'slaps BlueBot' ) != -1:
        irc.send ( 'PRIVMSG #mnresistance :This is the Trout Protection Agency. Please put the Trout Down and walk away with your hands in the air.\r\n' )
    if data.find ('BlueBot go!') != -1:
        print "Mirroring started"
        irc.send( 'PRIVMSG #mnresistance :Mirroring reporting attacks in the Twin Cities area (Tell me "BlueBot stop" to stop)\r\n')
        mirror = utilities.IngressChatMirror()
        list(mirror.attackgen()) #Skip the first batch
    if data.find('BlueBot stop') != -1:
        print "Mirroring stopped"
        irc.send('PRIVMSG #mnresistance :Stopping attack reporting (Tell me "BlueBot go!" to start)\r\n' )
        mirror = None
        
    if mirror and datetime.datetime.now() - last_check > datetime.timedelta(0,20):
        attacks = list(mirror.attackgen())
        for attack in attacks:
            irc.send('PRIVMSG #mnresistance :' + str(attack)+'\r\n')
        last_check = datetime.datetime.now()
    
    time.sleep(1)