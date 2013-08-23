
import urllib, re, os, sqlite3

def main():
    import socket, ssl
    
    #some functions to help repetitive task in connect()
    def msg(ircCMD, channel, msg):
        irc.send('%s #%s %s\r\n' % (ircCMD, channel, msg))
    def join(channel):
        irc.send('JOIN #%s \r\n' % channel)
    
    network = 'irc.baconbits.org'
    chan = 'spam2.1'
    port = 16667
    nick = 'SpamCoin'
    
        
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((network,port))
    irc = ssl.wrap_socket(socket)
    irc.send('NICK %s\r\n' % nick)
    print irc.recv(4096)
    irc.send('USER %s %s %s :My bot\r\n' % (nick,nick,nick))
    print irc.recv(4096)
    join(chan)
    print irc.recv(4096)
	
    while True:
        data = irc.recv(4096)
        print data

	if data.find('PING') != -1:
            irc.send('PONG '+data.split()[1]+'\r\n')
	if data.find('!safeword\r\n') != -1:
            irc.send('QUIT\r\n')
            exit()#exits python. 
	if data.find('!registerAll') != -1:
            #grab all users in channel step through them sending to addUser
	if data.find('!register') != -1:
            #input be like !register.UserName would send to addUser
	if data.find('!ban') != -1:
            #!ban.username Takes the name who sent the command checks to see if they have enough money if so bans user.
	if data.find('!kick') != -1:
            #!kick.username Takes the name who sent the command checks to see if they have enough money if so kicks user.
	if data.find('!topic') != -1:
            #!topic.text Takes the name who sent the command checks to see if they have enough money if so creates new topic
            
def createDB():
       
    conn = sqlite3.connect('spamCoin.db')
    cur = conn.cursor()

    #create table to hold Nicks, their money and their multiplier
    cur.execute('''CREATE TABLE IF NOT EXISTS dabank
                 (Nick text, Amount text, multiplier text)''') 

  
    conn.commit()
    cur.close()
    conn.close()

def addUser(Nick, Amount, multiplier):

    try:                            
        users = []
        conn = sqlite3.connect('spamCoin.db')

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM dabank")
        rows = cur.fetchall()
        #if table is empty no clients have been added go ahead and add client. 
            if not rows:
                cur.execute("INSERT INTO dabank VALUES (?, ?, ?)", (Nick, Amount, multiplier)) 

        #Creates a list of all clients then it checks to see if current client is in database if not adds it. if so prints error msg.
            else:
                for row in rows:
                    users.append(row[0])
                        
                if Nick not in users:
                    cur.execute("INSERT INTO dabank VALUES (?, ?, ?)", (Nick, Amount, multiplier))

                else:
                    print "User already in registered in database" 

        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:
            if conn:
                conn.close()
                
#transaction = deposit or withdrawl
#editMultiplier if zero do nothing if postive number increase if negitive number decrease.
    
def update(Nick, transaction, Amount, editMultiplier):
    
    
    try:
        conn = sqlite3.connect('spamCoin.db')

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM dabank")
        rows = cur.fetchall()
                                
        for row in rows:
            if re.match(Nick,row[0]):
                CurrentAmount = row[1]
                CurrentMultiplier = row[2]
                if transaction == 'deposit':
                    money = int(CurrentAmount) + int(Amount)
                if transaction == 'withdrawl':
                    if int(CurrentAmount) < int(Amount):
                        money = int(CurrentAmount) - 40
                        #tell the person to learn math and that 40 were taken away as tax.
                    if int(CurrentAmount) > int(Amount):
                        money = int(CurrentAmount) - int(Amount)
                        #return withdrawl sccuessful
                if editMultiplier != 0:#allows for negitive Multiplier which would get them so far into a deep whole they can never get out.
                    multiplier = int(CurrentMultiplier) + int(editMultiplier)
                else:
                    multiplier = int(CurrentMultiplier)
                    
                cur.execute("UPDATE dabank SET Amount=?, multiplier=? WHERE Nick=?",(money, multiplier, Nick))
                    print row

    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
