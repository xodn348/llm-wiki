---
title: '1970 A general method applicable to the → 1981 Identification of common molecular
  subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped
  BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read alignment → 2020
  Genomic characterisation and epidemiology of 2019'
length: 5
start_doi: 10.1016/0022-2836(70)90057-4
end_doi: 10.1016/s0140-6736(20)30251-8
---

# 1970 A general method applicable to the → 1981 Identification of common molecular subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read alignment → 2020 Genomic characterisation and epidemiology of 2019

_6 papers, 5 `enables` steps._

## Chain

1. **1970** — [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md)
1. **1981** — [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)
1. **1988** — [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)
1. **1997** — [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)
1. **2009** — [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)
1. **2020** — [Genomic characterisation and epidemiology of 2019 novel coronavirus: implications for virus origins and receptor binding](../paper/10_1016_s0140_6736_20_30251_8.md)

## Walkthrough

### 1970 → 1981: [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md) enables [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)

> Needleman and Wunsch's dynamic-programming sequence alignment enabled Smith and Waterman's local molecular subsequence alignment method.

Needleman and Wunsch’s 1970 paper introduced dynamic programming as a general method for comparing amino acid sequences, giving molecular biologists a principled way to compute an optimal alignment rather than relying on ad hoc visual comparison. In historical context, it helped establish sequence alignment as an algorithmic problem with explicit scoring and recurrence structure.

Smith and Waterman’s 1981 paper built directly on that lineage by adapting dynamic-programming alignment to identify common molecular subsequences. The key enabling relationship is that the earlier global sequence-alignment framework made it possible to formulate a local alignment method: instead of aligning two full protein sequences end to end, Smith and Waterman could search for the best shared subsequence region within them.

### 1981 → 1988: [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md) enables [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)

> Smith-Waterman local alignment defined optimal molecular subsequence matching that FASTA approximated with faster heuristic tools.

“Identification of common molecular subsequences” introduced the Smith-Waterman formulation of local sequence alignment: a rigorous way to find optimal matching subsequences within longer molecular sequences. That mattered because biological similarity often appears in conserved regions rather than across entire sequences, so local alignment gave the field a precise computational target for comparing DNA or protein sequences without forcing end-to-end matches.

“Improved tools for biological sequence comparison.” built on that target from a practical direction. FASTA did not replace the optimal Smith-Waterman idea; it approximated the same kind of local molecular subsequence matching with faster heuristic methods suitable for larger database searches. In that lineage, Smith-Waterman defined what an ideal local comparison meant, and FASTA helped make that comparison usable at broader scale.

### 1988 → 1997: [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md) enables [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)

> FASTA's heuristic sequence-comparison strategy helped establish fast database searching that Gapped BLAST and PSI-BLAST extended.

“Improved tools for biological sequence comparison.” helped make large-scale sequence database search practical by showing how heuristic comparison methods could find useful similarities much faster than exhaustive alignment approaches. In that sense, FASTA was part of the shift from sequence alignment as a specialized calculation to database searching as a routine biological tool.

“Gapped BLAST and PSI-BLAST” built on that established fast-search tradition. Its contribution was not simply speed, but a new generation of protein search programs that extended the heuristic database-search model with gapped alignments and iterative profile-based searching. The lineage is therefore direct: FASTA’s heuristic strategy helped establish the feasibility and importance of fast sequence comparison at database scale, and Gapped BLAST/PSI-BLAST advanced that model for more sensitive protein database searches.

### 1997 → 2009: [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md) enables [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)

> Gapped BLAST refined seed-and-extend alignment heuristics, a predecessor to BWT-based short-read aligners that made genome-scale matching faster.

Gapped BLAST and PSI-BLAST advanced the seed-and-extend style of database search: find promising local matches quickly, then spend more alignment effort only where the seed suggests biological relevance. Its importance for later read alignment was not the specific machinery of BLAST, but the practical framing it helped establish: genome-scale sequence comparison required heuristics that preserved useful accuracy while avoiding exhaustive dynamic programming.

BWA’s 2009 Burrows-Wheeler-transform aligner addressed a different workload, mapping many short reads to a reference genome, but it inherited that same computational lineage. The recorded bridge is that Gapped BLAST refined seed-and-extend alignment heuristics, a predecessor to BWT-based short-read aligners that made genome-scale matching faster. BWA replaced BLAST-style indexing with a compact transform-based index, but it pursued the same enabling goal: fast, accurate matching at biological database scale.

### 2009 → 2020: [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md) enables [Genomic characterisation and epidemiology of 2019 novel coronavirus: implications for virus origins and receptor binding](../paper/10_1016_s0140_6736_20_30251_8.md)

> BWT-based short-read alignment enabled rapid mapping of sequencing reads needed to assemble and compare the 2019-nCoV genome.

“Fast and accurate short read alignment with Burrows-Wheeler transform” helped make high-throughput sequencing data practical to use at speed: BWT-based alignment let researchers rapidly map large numbers of short reads back to reference genomes or related sequences. That capability became part of the computational foundation for modern pathogen genomics, where assembling, checking, and comparing viral genomes depends on turning raw sequencing reads into reliable genome-scale evidence.

In the 2020 2019-nCoV characterization paper, researchers needed to reconstruct and compare the newly observed coronavirus genome to reason about epidemiology, origins, and receptor-binding implications. The recorded link is direct: BWT-based short-read alignment enabled the rapid mapping of sequencing reads needed to assemble and compare the 2019-nCoV genome. The earlier alignment method did not itself discover the virus, but it enabled the kind of fast genomic workflow that made such outbreak analysis feasible.
