#Seq44_88_315 = {'start' : (4,4), 'command' : (8,8) }

#command = {'comand' : (4,4), 'expected' : (8,8), 'timeout' : 5 }

class TestingSequence:
    def __init__(self, command, expected, timeout):
        self.command = command
        self.expected = expected
        self.timeout = timeout
        #self.delay = delay


class Sequence:
    def __init__(self, init_band, first_band, second_band):
        self.seq = []

				#INIT
        self.seq.append(TestingSequence("AT^SMSO", "SYSTART", 0)) #0 czeka bezwzl
        self.seq.append(TestingSequence(init_band, "OK", 2))
        self.seq.append(TestingSequence("AT^SMSO", "SYSTART", 3))

        self.seq.append(TestingSequence("AT+CPIN=2","CREG 0;CREG 2;CREG 0", 3))

        self.seq.append(TestingSequence(first_band, "OK", 3))
        self.seq.append(TestingSequence("", "CREG 5", 10))

        self.seq.append(TestingSequence(second_band, "OK", 3))
        self.seq.append(TestingSequence("", "CREG 5", 10))

    def play(self):
        while ( len(self.seq) > 0 ) :
            next = self.seq.pop(0)
            print(next.command)
            
class SequencePlayer:
    def __init__(self, socket, seq):
        self.socket = socket
        self.seq = seq
        self.play()
    def play(self):
        self.socket.write(seq.command)
				try 
				{
					sleep(5)
          print("nie dostalem danych")
				}
        catch
        {
            print("Obsluga danych")

        }
    def dataReceived(self):
        #....

        # teraz czekaj na timeout lub na sygnal w zaleznosci od tego,
        # co bedzie wczesniej


