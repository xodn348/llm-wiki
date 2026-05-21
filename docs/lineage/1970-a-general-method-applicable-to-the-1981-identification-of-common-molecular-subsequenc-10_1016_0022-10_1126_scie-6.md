---
title: '1970 A general method applicable to the → 1981 Identification of common molecular
  subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped
  BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read alignment → 2015
  Mutational landscape determines sensitivity to PD-1'
length: 5
start_doi: 10.1016/0022-2836(70)90057-4
end_doi: 10.1126/science.aaa1348
---

# 1970 A general method applicable to the → 1981 Identification of common molecular subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read alignment → 2015 Mutational landscape determines sensitivity to PD-1

_6 papers, 5 `enables` steps._

## Chain

1. **1970** — [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md)
1. **1981** — [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)
1. **1988** — [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)
1. **1997** — [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)
1. **2009** — [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)
1. **2015** — [Mutational landscape determines sensitivity to PD-1 blockade in non–small cell lung cancer](../paper/10_1126_science_aaa1348.md)

## Walkthrough

### 1970 → 1981: [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md) enables [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)

> Needleman and Wunsch's dynamic-programming sequence alignment enabled Smith and Waterman's local molecular subsequence alignment method.

Needleman and Wunsch’s 1970 paper introduced a general dynamic-programming method for comparing amino acid sequences, giving molecular biologists a principled way to search for sequence similarities rather than relying on ad hoc visual inspection. Its key historical role was methodological: it showed that sequence comparison could be formulated as an optimization problem over possible alignments.

Smith and Waterman’s 1981 paper built on that lineage by adapting dynamic programming to identify common molecular subsequences locally. In the recorded relationship, Needleman and Wunsch’s dynamic-programming sequence alignment enabled Smith and Waterman’s local molecular subsequence alignment method: the later work shifted the emphasis from aligning whole sequences to finding the most meaningful shared subsequences within them.

### 1981 → 1988: [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md) enables [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)

> Smith-Waterman local alignment defined optimal molecular subsequence matching that FASTA approximated with faster heuristic tools.

“Identification of common molecular subsequences” (1981) introduced the Smith-Waterman formulation of optimal local alignment: a way to identify the best-matching regions between biological sequences rather than forcing whole-sequence comparisons. That mattered because molecular similarity often appears as conserved subsequences, domains, or motifs, and the paper gave the field a rigorous dynamic-programming baseline for what “best local match” meant.

“Improved tools for biological sequence comparison.” (1988) built on that conceptual target by making sequence comparison faster and more practical at database scale. FASTA did not replace the optimality idea with a new biological claim; it approximated the Smith-Waterman local-alignment objective with heuristic tools that could search large collections efficiently. In that sense, the 1981 work defined the matching problem clearly, and the 1988 work helped make that problem usable for routine biological discovery.

### 1988 → 1997: [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md) enables [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)

> FASTA's heuristic sequence-comparison strategy helped establish fast database searching that Gapped BLAST and PSI-BLAST extended.

“Improved tools for biological sequence comparison.” sits in the lineage of making sequence homology search practical at database scale. FASTA’s heuristic strategy showed that biological sequences could be compared quickly enough to support routine searching against growing sequence collections, while still preserving the core goal of finding meaningful similarity.

“Gapped BLAST and PSI-BLAST” extended that fast-search tradition into a new generation of protein database search programs. Its contribution was not a rejection of the earlier heuristic turn, but a refinement of the same practical agenda: faster, more sensitive ways to search large biological databases. In that sense, FASTA helped establish the computational and methodological template that Gapped BLAST and PSI-BLAST built on: rapid sequence comparison as an everyday engine for biological discovery.

### 1997 → 2009: [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md) enables [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)

> Gapped BLAST refined seed-and-extend alignment heuristics, a predecessor to BWT-based short-read aligners that made genome-scale matching faster.

Gapped BLAST and PSI-BLAST helped define a practical pattern for large-scale biological sequence search: use heuristics to find promising local matches, then extend and refine them instead of attempting exhaustive alignment everywhere. Its gapped alignment improvements made the seed-and-extend style more effective for protein database search, showing how carefully engineered approximations could preserve useful biological signal while making database-scale matching feasible.

The 2009 Burrows-Wheeler short-read aligner addressed a different pressure point: mapping massive numbers of short DNA reads to large genomes. Its BWT-based indexing was not simply another BLAST variant, but it inherited the same lineage of thinking: fast search depends on narrowing the candidate space before detailed alignment. In that sense, Gapped BLAST’s refined seed-and-extend heuristics were an important predecessor to later genome-scale aligners that made high-throughput matching faster.

### 2009 → 2015: [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md) enables [Mutational landscape determines sensitivity to PD-1 blockade in non–small cell lung cancer](../paper/10_1126_science_aaa1348.md)

> BWA short-read alignment enabled accurate tumor sequencing and mutation-burden estimation used to link mutational landscape with PD-1 sensitivity.

“Fast and accurate short read alignment with Burrows-Wheeler transform” introduced BWA as a practical way to align large volumes of short sequencing reads accurately and efficiently. That capability became part of the core infrastructure for next-generation sequencing studies, including tumor sequencing workflows where reads must be mapped reliably before variants can be called.

By 2015, studies such as “Mutational landscape determines sensitivity to PD-1 blockade in non-small cell lung cancer” depended on accurate tumor sequencing and mutation-burden estimation to connect genomic features with immunotherapy response. In that lineage, BWA did not provide the immunological interpretation itself; it enabled the read-alignment layer that made mutation detection and mutational-landscape analysis sufficiently dependable for linking tumor mutation patterns with sensitivity to PD-1 blockade.
