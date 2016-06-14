# English Automatic Taxonomy Construction based on Wordnet similarity<br/>
# Inspiration: Taxonomy Construction Using Syntactic Contextual Evidence Sec 2.2.1, String inclusion with Wordnet<br/>
1. Read a list of interesting terms/phrases (salient.csv in my case), use Wordnet to find term-pairs with similarity higher than a threshold (0.25); at the same time, terms not paired (might be because they are adj or v, or because they are not in wordnet) are put in isolated pool.<br/>
2. group similar terms and select representative terms.<br/>
3. group similar group and create hierarchy.<br/>
4. First come first combined, results might differ every time.<br/>

dependency: <br/>
wordnet <br/>
networkx <br/>
