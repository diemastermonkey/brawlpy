#!/usr/bin/python3
#
# Brawl: Procgen text DND brawl for Python3
# Use procedural generation to generate heroes, accessed
# by "Id" (seed). Coming soon: They do battle!
#
# Usage: 
#      brawl            Show a random hero, and their seed
#      brawl <seed>     Show (seed) hero. Seed is 0 to 255
# ---------------------------------------------------------
# Names ba bo fa de to ak ko re ro pa ta za ox yo san ma po
# Weapons fist herring staff sword crossbow magic warhammer
# ---------------------------------------------------------
import random;        # For prng
import sys;           # Merely for sys.argv/self. Can be rid?
import re;            # Regex

# Simple string array of attribute mnemonics
aAttributes = ("STR", "DEX", "CON", "INT", "WIS", "CHA");
sSource = ""          # For embedded data

# Brawler class
# ---------------------------------------------------------
class BrawlerType:

  def __init__ (self, argSeed = -1):
    self.iSeed = int(argSeed)              # One mandatory property
    if (self.iSeed > 0):
      random.seed(self.iSeed)
    else:
      random.seed()                        # First true random...
      self.iSeed = random.randint(1,255)   # ...then, small world seed
    self.fnDump()
    return

  def fnDump (self):
    print (self.fnName(), "\t Seed", self.iSeed);
    print ("  Wields", Weapons[self.fnWeapon()]);
    print ("  HP\t", self.fnHP());
    for sAttribute in aAttributes:         # Iterate attribtes
      print (" ", sAttribute, "\t", self.fnAttribute(sAttribute));

    return

  def fnHP (self):                         # Initial HP = Str + Con * 2
    return (self.fnAttribute("STR") + self.fnAttribute("CON") * 2)

  def fnName (self):                         # Procgen name from glob sNames
    random.seed(self.iSeed)
    return "".join(random.sample(Names, 3))  # Python, pfft

  def fnWeapon (self):                       # Procgen weapon from glob sWeapons
    random.seed(self.iSeed)
    return random.randint(0, len(Weapons)-1) # Returns an *index*

  # Procgen DND attribute lte 18, by mnemonic string
  # Each has unique 
  def fnAttribute (self, argAttribute):
    iAttribIndex = aAttributes.index(argAttribute);
    random.seed (self.iSeed + 3 * iAttribIndex); # Unique seed, each
    return (random.randint (8, 18));

# End Brawler class

# fnData: Return list of embedded data by name
def fnData (argName):
  global sSource                           # Again, python wtf
  if len(sSource) < 1:                     # Source unread
    infile = open (sys.argv[0], "r")
    sSource = infile.read()
    infile.close()
  sRecord = re.search ('^# ' + argName + '.*', sSource, re.MULTILINE)
  return sRecord.group(0).split(' ')[2:]   # As list, minus first 2

# Main
# ---------------------------------------------------------
Names = fnData ("Names")
Weapons = fnData ("Weapons")

# Prn init depends on args
if len(sys.argv) < 2:
  Seed = random.randint(0, 63)   # No args? Seed to systime
  print ("Random hero! Also try\n  ", sys.argv[0], "hero_seed_number \n")
else:
  Seed = sys.argv[1]

oHero = BrawlerType (Seed)       # Init dumps hero
  
# Fin
