from SequenceFactory import *

if __name__ == '__main__':
  seq = SequenceFactory()
  seq.readSequencesFromXml()
  print(repr(seq.getNewSequence("cmu850")))
  print(repr(seq.getSequencesXml()))
