---
title: '1970 A general method applicable to the → 1981 Identification of common molecular
  subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped
  BLAST and PSI-BLAST: a new → 2011 Accelerated Profile HMM Searches → 2022 ColabFold:
  making protein folding accessible to'
length: 5
start_doi: 10.1016/0022-2836(70)90057-4
end_doi: 10.1038/s41592-022-01488-1
---

# 1970 A general method applicable to the → 1981 Identification of common molecular subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped BLAST and PSI-BLAST: a new → 2011 Accelerated Profile HMM Searches → 2022 ColabFold: making protein folding accessible to

_6 papers, 5 `enables` steps._

## Chain

1. **1970** — [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md)
1. **1981** — [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)
1. **1988** — [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)
1. **1997** — [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)
1. **2011** — [Accelerated Profile HMM Searches](../paper/10_1371_journal_pcbi_1002195.md)
1. **2022** — [ColabFold: making protein folding accessible to all](../paper/10_1038_s41592_022_01488_1.md)

## Walkthrough

### 1970 → 1981: [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md) enables [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)

> Needleman and Wunsch's dynamic-programming sequence alignment enabled Smith and Waterman's local molecular subsequence alignment method.

Needleman and Wunsch’s 1970 paper introduced dynamic programming as a general way to compare amino acid sequences, turning protein similarity search into a rigorous alignment problem rather than an ad hoc visual or heuristic comparison. Its importance was methodological: it showed how biological sequence relationships could be formalized as an optimization problem over possible alignments.

Smith and Waterman’s 1981 “Identification of common molecular subsequences” built directly on that lineage by adapting dynamic-programming sequence alignment to the local case: finding the best matching subsequences rather than forcing comparison across entire molecules. In that sense, the earlier global alignment method enabled the later local molecular subsequence alignment method by providing the computational framework that Smith and Waterman specialized for detecting shared regions within longer sequences.

### 1981 → 1988: [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md) enables [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)

> Smith-Waterman local alignment defined optimal molecular subsequence matching that FASTA approximated with faster heuristic tools.

“Identification of common molecular subsequences” (1981) introduced the Smith-Waterman local alignment framework: a dynamic-programming way to define an optimal match between molecular subsequences rather than forcing whole-sequence comparison. That gave biological sequence comparison a precise target: find the best local similarity under an explicit scoring scheme.

“Improved tools for biological sequence comparison.” (1988) built on that target by making sequence search more practical at database scale. FASTA did not replace the Smith-Waterman definition of optimal local subsequence matching; it approximated the same kind of relationship with faster heuristic tools, trading exhaustive optimality for speed while preserving the central idea that biologically meaningful similarity often lies in local aligned regions.

### 1988 → 1997: [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md) enables [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)

> FASTA's heuristic sequence-comparison strategy helped establish fast database searching that Gapped BLAST and PSI-BLAST extended.

“Improved tools for biological sequence comparison.” sits in the lineage of making sequence search practical at database scale. By presenting FASTA’s heuristic sequence-comparison strategy, the 1988 work helped establish the idea that biologically useful similarity searches could be made fast enough for routine exploration of growing protein and nucleotide databases, rather than relying only on exhaustive comparison.

“Gapped BLAST and PSI-BLAST” extended that same practical search tradition into a new generation of protein database programs. Its contribution belongs downstream of FASTA’s demonstrated heuristic approach: it kept the emphasis on rapid database searching while adding more powerful search behavior, including gapped alignment handling and iterative profile-based searching, to make protein similarity detection more effective within the same expanding-database context.

### 1997 → 2011: [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md) enables [Accelerated Profile HMM Searches](../paper/10_1371_journal_pcbi_1002195.md)

> PSI-BLAST popularized iterative profile-based homology detection, directly motivating faster profile HMM search methods.

*Gapped BLAST and PSI-BLAST* helped shift sequence search from single-query similarity toward iterative, profile-based homology detection. By repeatedly using detected homologs to refine a position-specific profile, PSI-BLAST made the practical value of profiles clear: they could reveal more remote evolutionary relationships than a one-pass pairwise search, while remaining usable at database scale.

That success created pressure for the next generation of profile methods. Profile HMMs offered a richer probabilistic framework for representing sequence families, but their broader use depended on making searches fast enough for large protein databases. *Accelerated Profile HMM Searches* follows naturally from that lineage: PSI-BLAST popularized the core workflow and demand for iterative profile-based homology detection, directly motivating faster methods for searching with profile HMMs.

### 2011 → 2022: [Accelerated Profile HMM Searches](../paper/10_1371_journal_pcbi_1002195.md) enables [ColabFold: making protein folding accessible to all](../paper/10_1038_s41592_022_01488_1.md)

> Accelerated profile HMM search made large-scale homolog detection practical, supporting ColabFold's fast retrieval of sequence information for structure prediction.

“Accelerated Profile HMM Searches” strengthened a key upstream step in protein bioinformatics: finding homologous sequences quickly enough for large databases to be useful in practice. By making profile HMM search more practical at scale, it helped turn remote-homology detection and sequence-profile construction into routine infrastructure rather than a bottleneck.

ColabFold later built on that kind of infrastructure for accessible protein structure prediction. Its usefulness depended not only on neural folding models, but also on quickly retrieving relevant sequence information for many users and many targets. In that lineage, accelerated profile HMM search enabled the broader ecosystem of fast homolog detection that ColabFold could rely on to make sequence-informed structure prediction feel immediate and widely usable.
