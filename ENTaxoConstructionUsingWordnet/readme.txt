# English Automatic Taxonomy Construction based on Wordnet similarity
# Inspiration: Taxonomy Construction Using Syntactic Contextual Evidence Sec 2.2.1, String inclusion with Wordnet
1. Read a list of interesting terms/phrases (salient.csv in my case), use Wordnet to find term-pairs with similarity higher than a threshold (0.25); at the same time, terms not paired (might be because they are adj or v, or because they are not in wordnet) are put in isolated pool.
2. group similar terms and select representative terms.
3. group similar group and create hierarchy.
4. For easy and clear visulaization, a term belongs to only ONE group. First come first combined, results might differ every time.

dependency: 
wordnet 
networkx 
d3 is used for visualization
Sofrware Gephi is used to verify if terms are split to strongly connected graph.
