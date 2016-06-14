# reference : Automatically generating Extraction patterns from untagged text, Ellen Rillof
# reference : An introduction to the sundance and the autoslog system, Ellen Rillof and William Phillips


My code took ibm and softlayer for example and training -> retrive other acquisition results.
steps:
0. create your datasets: relevant and irrelevant
1. modify and run a.py to do POS tagging for your target file, which will create a new tmp_pos!

2. modify buildRulesBuy.py (or buildRulesBought.py) to change the seeds
3. run buildRulesBuy.py (or buildRulesBought.py) and save the output to, e.g. XXX_rel, XXX_irrel

4. for unary relation,
   modify input files for vlist
   python LookforCandidate.py

    for a binary relation,
    execute the process for unary relation twice
    modify input files for vlist, such as rel.verb / irrel.verb & python LookforCandidate.py
    then change input for vlist to the cooresponding ones, bought_rel.verb/bought_irrel.verb & python LookforCandidate.py -d
    then the output will include relations binded together.

