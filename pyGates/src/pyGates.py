'''
Created on Apr 15, 2009
Modified and tested on April 24, 2011.
Need to verify that outputs produced by FullAdder and HalfAdder classes are correct

@author: Juan E. Vargas
'''

class Wire(object):
  '''
  This class is more crucial that what it appears. 
  Languages that pass objects by reference hve a less clear semantics when raw values are passed around.
  In order to preserve the "raw value" of the state of a gate's input or output, an explicit reference 
  to the memory where that object is preserved must be maintained and the Wire class provides that mechanism. 
  This is true for Java and Python 
  '''

  def __init__(self):
    "default constructor/initializer"
    self.v = None

  def setValue(self, aValue):
    if aValue == True or aValue == False :
      self.v = aValue

  def setTrue(self):
    self.v = True

  def setFalse(self):
    self.v = False

  def __str__(self):
    return self.name


class Gate(object):

  def __init__(self):
    self.name = ""
    self.type = ""
    self.output = Wire()
    self.inputs = []

  def __str__(self):
    return self.name

  def setName(self, aName):
    self.name = aName

  def setType(self, aType):
    self.type = aType

  def setInputsTrue(self):
    for w in self.inputs :
      w.setTrue()

  def setInputsFalse(self):
    for w in self.inputs :
      w.setFalse()

  def setInput(self, ndx, aValue):
    w = self.inputs[ndx]
    w.setValue( aValue )

  def setInputWire(self, ndx, aWire):
    self.inputs[ndx] = aWire

  def addInputWire(self, aWire):
    self.inputs.append(aWire) 

  def addInput(self, aValue):
    w = Wire( )
    w.setValue( aValue )
    self.inputs.append( w )

    '''
    Connect gets two arguments. Arg1 is the zero-based index of the input list of self gate that gets 
    the output from Gate g. 
    '''
  def connect(self, ndx, aGate):
    if ndx < 0 :
      return
    if ndx > len( self.inputs ) :
      return
    self.inputs[ndx] = aGate.output

  def execute(self):
    if self.validate() == False :
      return False
    # NOT Logic
    # Do not execute when there are more than one input
    if self.type == 'NOT' and len(self.inputs) > 1:
      self.output = None
      return
      # execute if there is only one input
    if self.type == 'NOT' and len(self.inputs) == 1 :
      w = self.inputs[0]
      if ( w.v == False ) :
        self.output.v = True
      if ( w.v == True) :
        self.output.v = False
      return
    # AND Logic
    if self.type == 'AND' and len(self.inputs)== 0 :
      self.output.v = None
      return
    if self.type == 'AND' and len(self.inputs) > 0 :
      sum = 0
      for w in self.inputs :
        sum += w.v
      if sum == len(self.inputs) :
        self.output.v = True
      if sum < len(self.inputs) :
        self.output.v = False
      return
    # OR Logic
    if self.type == 'OR' and len(self.inputs) == 0 :
      self.output.v = None
      return
    if self.type == 'OR' and len(self.inputs) > 0 :
      sum = 0
      for w in self.inputs :
        sum += w.v
      if sum == 0 :
        self.output.v = False
      if sum > 0 :
        self.output.v = True
      return

  def validate(self):
    if (self.type == ''):
      self.output = None
      self.type = 'INVALID'
      return False
    if self.type != 'NOT' and self.type != 'AND' and self.type != 'OR' :
      self.output = None
      self.type = 'INVALID'
      return False
    return True

  def describe (self):
    print 'name=', self.name, 'type=', self.type
    if self.validate() == False :
      return False
    v1= ' '
    for w in self.inputs :
      v1 = v1 + str(w.v) + ' '
    print 'inputs:', v1
    print 'output: ', str(self.output.v)
    print
    
  # End of class Gate()  


  def testNot(self):
    self.setName('testNot')
    self.setType('NOT')
    self.addInput(False)
    self.execute()
    self.describe()
    self.setInput(0, True)
    self.execute()
    self.describe()

  def testAnd(self):
    self.setName('testAnd')
    self.setType('AND')
    self.addInput(False)
    self.execute()
    self.describe()
    self.setInput(0, True)
    self.execute()
    self.describe()

  def testOr(self):
    self.setName('testOr')
    self.setType('OR')
    self.addInput(False)
    self.execute()
    self.describe()
    self.setInput(0, True)
    self.execute()
    self.describe()


class AndGate (Gate):

  def __init__ ( self ) :
    self.init( )

  def init(self) :
    self.name = ''
    self.type = 'AND'
    self.output = Wire()
    self.output.v = None
    self.inputs = [ ]
  #end of class AndGate

class OrGate (Gate):

  def __init__ ( self ) :
    self.init( )

  def init(self) :
    self.name = ''
    self.type = 'OR'
    self.output = Wire ()
    self.output.v = None
    self.inputs = [ ]
  #end of class OrGate


class NotGate (Gate):

  def __init__ ( self ) :
    self.init( )

  def init(self) :
    self.name = ''
    self.type = 'NOT'
    self.output = Wire()
    self.output.v = None
    self.inputs = [ ]
  #end of class NotGate


class HalfAdder (object) :
  ''' !!!!  DO NOT create objects like this:
             a = b = c = s = Wire()
    !!!! because all the objects are assigned to the same address !!!!!
  '''

  def __init__ ( self ) :
    self.name = ''
    self.type = 'HalfAdder'
    self.a = Wire()
    self.b = Wire()
    self.c = Wire()
    self.s = Wire() 
    self.a.v = False
    self.b.v = False
    self.s.v = False
    self.c.v = False
    self.a1 = AndGate()
    self.o1 = OrGate()
    self.n1 = NotGate()
    self.a2 = AndGate()
    self.a1.setName('a1')
    self.a2.setName('a2')
    self.o1.setName('o1')
    self.n1.setName('n1')
    self.a1.addInputWire( self.a )
    self.a1.addInputWire( self.b )
    self.o1.setName('o1')
    self.o1.addInputWire( self.a )
    self.o1.addInputWire( self.b )
    self.n1.setName('n1')
    self.n1.addInputWire( self.a1.output )
    self.a2.setName('a2')
    self.a2.addInputWire( self.o1.output )
    self.a2.addInputWire( self.n1.output )
    self.s = self.a2.output
    self.c = self.a1.output

  def setInputs(self, arg1, arg2):
    self.a.v = arg1
    self.b.v = arg2
   
  def execute(self):
    self.o1.execute()
    self.a1.execute()
    self.n1.execute()
    self.a2.execute()

  def describe( self ):
    print 'name=', self.name, 'type=', self.type
    print 'a=', self.a.v, 'b=', self.b.v
    print 's=', self.s.v, 'c=', self.c.v

  def test(self):
    self.setInputs( False, False )
    self.execute()
    self.describe()
    self.setInputs(False, True)
    self.execute()
    self.describe()
    self.setInputs(True, False)
    self.execute()
    self.describe()
    self.setInputs(True, True)
    self.execute()
    self.describe()

  # End of class HaldAdder 


class FullAdder( object ) :

  def __init__ ( self ) :
    self.name = ''
    self.type = 'FullAdder'
    self.a = Wire()
    self.b = Wire()
    self.c = Wire()
    self.s = Wire()
    self.t = Wire()
    self.h1 = HalfAdder()
    self.h2 = HalfAdder()
    self.o1 = OrGate()
    self.h1.name = 'h1'
    self.h2.name = 'h2'
    self.o1.name = 'o1'
    ''' At this point HalfAdders have their internal connections set up,
        therefore instead of adding more input wires, the ones already set
        must be reassigned to the input wires created foe the full adder
    ''' 
    self.h1.a1.setInputWire( 0, self.b )
    self.h1.a1.setInputWire( 1, self.c )
    self.h1.o1.setInputWire( 0, self.b )
    self.h1.o1.setInputWire( 1, self.c )
    self.h2.a1.setInputWire( 0, self.a )
    self.h2.a1.setInputWire( 1, self.h1.s )
    self.h2.o1.setInputWire( 0, self.a )
    self.h2.o1.setInputWire( 1, self.h1.s )
    ''' The full adder or gate needs to get its inputs set up
    '''
    self.o1.addInputWire( self.h2.c )
    self.o1.addInputWire( self.h1.c )
    self.s = self.h2.s
    self.t = self.o1.output

  def setInputs(self, a,b,c):
    self.a.v = a
    self.b.v = b
    self.c.v = c

  def execute(self):
    self.h1.execute()
    self.h2.execute()
    self.o1.execute()

  def describe(self):
    print 'name=', self.name, 'type=', self.type
    print 'a=', self.a.v, 'b=', self.b.v, 'c=', self.c.v
    print 's=', self.s.v, 't=', self.t.v

  def test(self):
    self.setInputs(False, False, False )
    self.execute()
    self.describe()
    self.setInputs(False, False, True)
    self.execute()
    self.describe()
    self.setInputs(False, True, False)
    self.execute()
    self.describe()
    self.setInputs(False, True, True)
    self.execute()
    self.describe()
    self.setInputs(True, False, False )
    self.execute()
    self.describe()
    self.setInputs(True, False, True)
    self.execute()
    self.describe()
    self.setInputs(True, True, False)
    self.execute()
    self.describe()
    self.setInputs(True, True, True)
    self.execute()
    self.describe()
  # end of FullAdder Class


def testGates() :
  g = Gate()
  g.testNot()
  g.testAnd()
  g.testOr()
  g.testAnd()
  g.testOr()
  g.setName('ggg')
  g.setType('OR')
  g.setInputsTrue()
  g.execute()
  g.describe()
  g.setInputsFalse()
  g.execute()
  g.describe()
  g.setName('ggg')
  g.setType('AND')
  g.setInputsTrue()
  g.execute()
  g.describe()
  g.setInputsFalse()
  g.execute()
  g.describe()
  g.setName('ggg')
  g.setType('and')
  g.execute()
  g.describe()
  # end of testGates method

def testConnect():
  a1 = AndGate()
  a1.addInput( False )
  a1.addInput( False)
  a2 = AndGate()
  a2.addInput( True )
  a2.addInput( True )
  o1 = OrGate()
  o1.addInput( False)
  o1.addInput( False)
  o1.execute()
  o1.describe()
  n1 = NotGate()
  n1.addInput(False)
  a2.execute()
  a1.execute()
  o1.connect(0, a1)
  o1.connect(1, a2)
  n1.connect(0, o1)
  o1.execute()
  o1.describe()
  n1.execute()
  n1.describe()
  # End of testConnect() method


def testHalfAdder():
  h1 = HalfAdder()
  h1.test()


def testFullAdder() :
  f1 = FullAdder()
  f1.test()


# testGates()

testHalfAdder()

testFullAdder()

print 'bye bye'

