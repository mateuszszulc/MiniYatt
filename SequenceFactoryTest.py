from SequenceFactory import *

if __name__ == '__main__':
  seq = SequenceFactory().readSequencesFromXml()
  print(repr(seq.getSequence("cmu850")))
