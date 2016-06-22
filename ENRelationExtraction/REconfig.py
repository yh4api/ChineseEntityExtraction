import sys

###
relInput = "ibm_sl_rel"
irrelInput = "ibm_sl_irrel"

relActiveOut = "rel.verb"
irrelActiveOut = "irrel.verb"

relPassiveOut = "rel_p.verb"
irrelPassiveOut = "irrel_p.verb"

### for example this is a "Acquistion" example
targetRelationName = ""

### initial seed, update data in [A, B] format
seed = {}
seed["ibm"] = [
["ibm", "softlayer"],
["IBM", "SoftLayer"],
["ibm", "Thingworx"],
["IBM", "ThingWorx"],
["ibm", "Hughes"]]

