

exp1 = re.compile("What (do|does) .* mean")
exp2 = re.compile("What's the (abbreviation|acronym) (for|of) (the)?")
exp3 = re.compile("What is the (abbreviation|acronym) (for|of) (the)?")
exp4 = re.compile("What's the abbreviated (term|form|expression) (used )?(for|of) (the)?")
exp5 = re.compile("What is the abbreviated (term|form|expression) (used )?(for|of) (the)?")
exp6 = re.compile("What's .* an (acronym|abbreviation) (for|of)")
exp7 = re.compile("What is .* an (acronym|abbreviation) (for|of)")
"""
exp8 = re.compile("What's CAPS")
exp9 = re.compile("What is CAPS")
exp10 = re.compile("What (do|does) CAPS stand for")
exp11 = re.compile("What (do|does) CAPS mean")
exp12 = re.compile("What's CAPS an (acronym|abbreviation) (for|of)")
exp13 = re.compile("What is CAPS an (acronym|abbreviation) (for|of)")
"""

exp8 = re.compile(r"What's [A-Z\.]+")
exp9 = re.compile(r"What is [A-Z\.]+")
exp10 = re.compile(r"What (do|does) [A-Z\.]+ stand for")
exp11 = re.compile(r"What (do|does) [A-Z\.]+ mean")
exp12 = re.compile(r"What's [A-Z\.]+ an (acronym|abbreviation) (for|of)")
exp13 = re.compile(r"What is [A-Z\.]+ an (acronym|abbreviation) (for|of)")

exp14 = re.compile("Who")
exp15 = re.compile("Whose")
exp16 = re.compile("Whom")
exp17 = re.compile("Where .* (M|m)ountai(n|ns)")
exp18 = re.compile("Where")
exp19 = re.compile("When")
exp20 = re.compile("Why")
exp21 = re.compile("What (causes|caused)")
exp22 = re.compile("What's (used|known) for")
exp23 = re.compile("What (is|are) (used|known) for")
exp24 = re.compile("What (is|are) .* (composed|made) of")
exp25 = re.compile("What's .* (composed|made) of")
exp26 = re.compile("How do (I|you) say")
exp27 = re.compile("What do you call")
exp28 = re.compile("How is .* defined")
exp29 = re.compile("How long is")
exp30 = re.compile("How much .* weight")
exp31 = re.compile("How much .* weights")
exp32 = re.compile("How much money")
exp33 = re.compile("How much .* cost")
exp34 = re.compile("How much .* rent")
exp35 = re.compile("How much .* (fine|fined)")
exp36 = re.compile("How much .* sell")
exp37 = re.compile("How much .* (spend|spent)")
exp38 = re.compile("How much .* (charge|charged)")
exp39 = re.compile("How much .* (pay|paid)")
exp40 = re.compile("How much .* worth")
exp41 = re.compile("How much .* (tax|taxed)")
exp42 = re.compile("How much .* wage")
exp43 = re.compile("How big")
exp44 = re.compile("How you")
exp45 = re.compile("How (do|does|did)")
exp46 = re.compile("How (is|was|were)")
exp47 = re.compile("How has")
exp48 = re.compile("How can")
exp49 = re.compile("How would")
exp50 = re.compile("How close")
exp51 = re.compile("How successful")
exp52 = re.compile("How effective")
exp53 = re.compile("How come")
exp54 = re.compile("How deep")
exp55 = re.compile("How far")
exp56 = re.compile("How high")
exp57 = re.compile("How tall")
exp58 = re.compile("How large")
exp59 = re.compile("How wide")
exp60 = re.compile("How fast")
exp61 = re.compile("How hot")
exp62 = re.compile("How large")
exp63 = re.compile("How loud")
exp64 = re.compile("How often")
exp65 = re.compile("How long")
exp66 = re.compile("How old")
exp67 = re.compile("How many")
exp68 = re.compile("How much")
exp69 = re.compile("How")


if exp1.search(s) != None:
	out = "DESCRIPTION:DEFINITION"
elif exp2.search(s) != None:
	out = "ABBREVIATION:ABBREVIATION"
elif exp3.search(s) != None:
	out = "ABBREVIATION:ABBREVIATION"
elif exp4.search(s) != None:
	out = "ABBREVIATION:ABBREVIATION"
elif exp5.search(s) != None:
	out = "ABBREVIATION:ABBREVIATION"
elif exp6.search(s) != None:
	out = "ABBREVIATION:ABBREVIATION"
elif exp7.search(s) != None:
	out = "ABBREVIATION:ABBREVIATION"
elif exp8.search(s) != None:
	out = "ABBREVIATION:EXPANSION"
elif exp9.search(s) != None:
	out = "ABBREVIATION:EXPANSION"
elif exp10.search(s) != None:
	out = "ABBREVIATION:EXPANSION"
elif exp11.search(s) != None:
	out = "ABBREVIATION:EXPANSION"
elif exp12.search(s) != None:
	out = "ABBREVIATION:EXPANSION"
elif exp13.search(s) != None:
	out = "ABBREVIATION:EXPANSION"
elif exp14.search(s) != None:
	out = "HUMAN:INDIVIDUAL"
elif exp15.search(s) != None:
	out = "HUMAN:INDIVIDUAL"
elif exp16.search(s) != None:
	out = "HUMAN:INDIVIDUAL"
elif exp17.search(s) != None:
	out = "LOCATION:MOUNTAIN"
elif exp18.search(s) != None:
	out = "LOCATION:OTHER"
elif exp19.search(s) != None:
	out = "NUMERIC:DATE"
elif exp20.search(s) != None:
	out = "DESCRIPTION:REASON"
elif exp21.search(s) != None:
	out = "DESCRIPTION:REASON"
elif exp22.search(s) != None:
	out = "DESCRIPTION:REASON"
elif exp23.search(s) != None:
	out = "DESCRIPTION:REASON"
elif exp24.search(s) != None:
	out = "ENTITY:SUBSTANCE"
elif exp25.search(s) != None:
	out = "ENTITY:SUBSTANCE"
elif exp26.search(s) != None:
	out = "ENTITY:TERM"
elif exp27.search(s) != None:
	out = "ENTITY:TERM"
elif exp28.search(s) != None:
	out = "DESCRIPTION:DEFINITION"
elif exp29.search(s) != None:
	out = "NUMERIC:DISTANCE"
elif exp30.search(s) != None:
	out = "NUMERIC:WEIGHT"
elif exp31.search(s) != None:
	out = "NUMERIC:WEIGHT"
elif exp32.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp33.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp34.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp35.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp36.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp37.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp38.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp39.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp40.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp41.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp42.search(s) != None:
	out = "NUMERIC:MONEY"
elif exp43.search(s) != None:
	out = "NUMERIC:SIZE"
elif exp44.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp45.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp46.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp47.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp48.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp49.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp50.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp51.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp52.search(s) != None:
	out = "DESCRIPTION:MANNER"
elif exp53.search(s) != None:
	out = "DESCRIPTION:REASON"
elif exp54.search(s) != None:
	out = "NUMERIC:DISTANCE"
elif exp55.search(s) != None:
	out = "NUMERIC:DISTANCE"
elif exp56.search(s) != None:
	out = "NUMERIC:DISTANCE"
elif exp57.search(s) != None:
	out = "NUMERIC:DISTANCE"
elif exp58.search(s) != None:
	out = "NUMERIC:DISTANCE"
elif exp59.search(s) != None:
	out = "NUMERIC:DISTANCE"
elif exp60.search(s) != None:
	out = "NUMERIC:SPEED"
elif exp61.search(s) != None:
	out = "NUMERIC:TEMPERATURE"
elif exp62.search(s) != None:
	out = "NUMERIC:OTHER"
elif exp63.search(s) != None:
	out = "NUMERIC:OTHER"
elif exp64.search(s) != None:
	out = "NUMERIC:OTHER"
elif exp65.search(s) != None:
	out = "NUMERIC:PERIOD"
elif exp66.search(s) != None:
	out = "NUMERIC:PERIOD"
elif exp67.search(s) != None:
	out = "NUMERIC:COUNT"
elif exp68.search(s) != None:
	out = "NUMERIC:COUNT"
elif exp69.search(s) != None:
	out = "DESCRIPTION:MANNER"
