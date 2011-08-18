class SequenceFactory:
  def __init__(self):
    radioBand = self.radioBand
    smso = self.smso
    pin = self.pin
    
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
