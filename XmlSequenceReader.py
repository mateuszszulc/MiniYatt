import xml.etree.ElementTree as etree

class XmlSequenceReader:

  def __init__(self, filename):
    self.tree = etree.parse('Sequences.xml')
    self.root = self.tree.getroot()
  def getSequences(self):
    return list(self.root)
