---
title: 'The neighbor-joining method: a new method for reconstructing phylogenetic
  trees.'
doi: 10.1093/oxfordjournals.molbev.a040454
openalex_id: https://openalex.org/W2097706568
year: 1987
venue: Molecular Biology and Evolution
authors: Naruya Saitou, M Nei
citations: 60402
fleming_tier: true
concepts:
- Phylogenetic tree
- Tree (set theory)
- Biology
- Cluster analysis
- Phylogenetic network
- Tree rearrangement
- Computational phylogenetics
- Algorithm
- Mathematics
- Computer science
---

# The neighbor-joining method: a new method for reconstructing phylogenetic trees.

## Why this mattered

Before Saitou and Nei, distance-based phylogenetic reconstruction often forced a tradeoff between speed, realism, and topology: methods such as UPGMA were computationally simple but depended on restrictive assumptions like a molecular clock. Neighbor-joining changed that balance. Starting from a star-like tree and repeatedly joining the pair of operational taxonomic units that minimized total tree length, it produced an unrooted tree with branch lengths without requiring equal rates of evolution across lineages. That made distance phylogenetics far more practical for molecular data, especially as DNA and protein sequence datasets were beginning to expand rapidly.

The importance of the paper was not only that it introduced another tree-building algorithm, but that it made large-scale phylogenetic inference routine. Neighbor-joining was fast enough to be used widely on datasets that were awkward or infeasible for more exhaustive optimality-based methods, while simulations in the paper showed it was competitive with or better than several established alternatives in recovering the correct unrooted tree. This helped shift phylogenetics toward algorithmic, data-intensive reconstruction from molecular distances, supporting comparative genomics, systematics, epidemiology, and evolutionary biology as sequence databases grew.

Its later influence is visible in how often neighbor-joining became the baseline method: a first-pass tree builder, a benchmark for newer algorithms, and a component of many phylogenetic software workflows. Subsequent breakthroughs in maximum likelihood, Bayesian phylogenetics, bootstrapping practices, and genome-scale evolutionary analysis did not replace the conceptual role of Saitou and Nei’s contribution; they built in a field where rapid computational tree reconstruction had become expected. The method’s enormous citation record reflects that it helped turn phylogenetic trees from labor-intensive specialist reconstructions into standard analytical objects across modern biology.

## Abstract

A new method called the neighbor-joining method is proposed for reconstructing phylogenetic trees from evolutionary distance data. The principle of this method is to find pairs of operational taxonomic units (OTUs [= neighbors]) that minimize the total branch length at each stage of clustering of OTUs starting with a starlike tree. The branch lengths as well as the topology of a parsimonious tree can quickly be obtained by using this method. Using computer simulation, we studied the efficiency of this method in obtaining the correct unrooted tree in comparison with that of five other tree-making methods: the unweighted pair group method of analysis, Farris's method, Sattath and Tversky's method, Li's method, and Tateno et al.'s modified Farris method. The new, neighbor-joining method and Sattath and Tversky's method are shown to be generally better than the other methods.


## Related



## Sources

- DOI: [https://doi.org/10.1093/oxfordjournals.molbev.a040454](https://doi.org/10.1093/oxfordjournals.molbev.a040454)
- OpenAlex: [https://openalex.org/W2097706568](https://openalex.org/W2097706568)