from XmlSequenceReader import *

class Command:
  def __init__(self, cmd, response = ["OK"], waitBeforeNext = 5, timeout = 60):
    self.cmd = cmd
    self.response = response
    self.waitBeforeNext = waitBeforeNext
    self.timeout = timeout

class SequenceFactory:
  def __init__(self):
    radioBand = self.radioBand
    smso = self.smso
    pin = self.pin

    creg020 = self.creg020
    creg20 = self.creg20
    creg1 = self.creg1

    self.sequencesXml = {}
    #self.readSequencesFromXml()
    
    self.sequencesNew = { 
    'cmu850': 
    [ Command(smso(), ["SYSSTART"]),Command(radioBand(4,4)), Command(smso(), ["SYSSTART"]), Command(pin()), 
      Command(radioBand(8,12), creg1()), Command(radioBand(4,4), creg020()),
      Command(radioBand(4,12), creg1())],
    'cmu900': 
    [ Command(smso(), ["SYSSTART"]),Command(radioBand(4,4)), Command(smso(), ["SYSSTART"]), Command(pin()), 
      Command(radioBand(1,3), creg1()), Command(radioBand(4,4), creg020()),
      Command(radioBand(2,3), creg1())]
    }

    self.sequences = { 
    'cmu850': 
    [ radioBand(4,4), smso(), pin(),radioBand(8,12),radioBand(4,4),
    radioBand(4,12)],

    'cmu850_AllowAll': #with Camp?!
    [ radioBand(4,4), smso(), pin(),radioBand(8,15),radioBand(4,4),
    radioBand(2,15)],
 
    'cmu900': 
    [ radioBand(4,4), smso(), pin(),radioBand(1,3),radioBand(4,4),
    radioBand(2,3)],

    'cmu900_AllowAll':#with CAMP?! should camp on 2,2 or 4,4? Another Test Case?
    [ radioBand(2,2), smso(), pin(),radioBand(1,15),radioBand(2,2),
     radioBand(8,15)],
    }

  def readSequencesFromXml(self):
    sequences = XmlSequenceReader("Sequences.xml").getSequences()

    for sequence in sequences:
      self.sequencesXml[sequence.attrib['name']] = []
      sequenceCommands = self.sequencesXml[sequence.attrib['name']]

      commands = list(sequence)
      for command in commands:
        atcmd = self.resolveCommand(command.find("atcmd").text)
        print(repr(atcmd))
        response = command.find("response").text
        print(repr(response))
        waitBeforeNext = command.find("waitBeforeNext").text
        print(repr(waitBeforeNext))
        timeout = command.find("timeout").text
        print(repr(timeout))
        
        if (len(response) == 0) and (len(timeout) == 0) and (len(waitBeforeNext) == 0):
          sequenceCommands.append(Command(atcmd))
          continue
        if (len(timeout) == 0) and (len(waitBeforeNext) == 0):
          sequenceCommands.append(Command(atcmd, response))
          continue
        if (len(timeout) == 0):
          sequenceCommands.append(Command(atcmd, response, waitBeforeNext))
        else:
          sequenceCommands.append(Command(atcmd, response, waitBeforeNext, timeout))
          

      
  def resolveCommand(self, command):
    pass

  def creg(self, code):
    return "+CREG: {0}".format(code)

  def creg1(self):
    return [self.creg(1)]

  def creg20(self):
    return [self.creg(2), self.creg(0)]

  def creg020(self):
    return [self.creg(0), self.creg(2), self.creg(0)]


  def getNewSequence(self, sequenceName):
    return self.sequencesNew[sequenceName]

  def getSequence(self, sequenceName):
    return self.sequences[sequenceName]

  def getAllSequenceNames(self):
    return self.sequences.keys()

  def radioBand(self,preferred, allowed):
    return "at^scfg=Radio/band,{0},{1}".format(preferred, allowed)

  def pin(self,pinValue = 9999):
    return "AT+CPIN={0}".format(pinValue)

  def cmee2(self):
    return "AT+CMEE=2"

  def smso(self):
    return "AT^SMSO"
