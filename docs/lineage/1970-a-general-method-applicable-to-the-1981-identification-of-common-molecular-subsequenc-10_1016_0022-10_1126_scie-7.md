---
title: '1970 A general method applicable to the → 1981 Identification of common molecular
  subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped
  BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read alignment → 2015
  Integrative analysis of 111 reference human → 2020 The GTEx Consortium atlas of
  genetic'
length: 6
start_doi: 10.1016/0022-2836(70)90057-4
end_doi: 10.1126/science.aaz1776
---

# 1970 A general method applicable to the → 1981 Identification of common molecular subsequences → 1988 Improved tools for biological sequence comparison. → 1997 Gapped BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read alignment → 2015 Integrative analysis of 111 reference human → 2020 The GTEx Consortium atlas of genetic

_7 papers, 6 `enables` steps._

## Chain

1. **1970** — [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md)
1. **1981** — [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)
1. **1988** — [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)
1. **1997** — [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)
1. **2009** — [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)
1. **2015** — [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md)
1. **2020** — [The GTEx Consortium atlas of genetic regulatory effects across human tissues](../paper/10_1126_science_aaz1776.md)

## Walkthrough

### 1970 → 1981: [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md) enables [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)

> Needleman and Wunsch's dynamic-programming sequence alignment enabled Smith and Waterman's local molecular subsequence alignment method.

Needleman and Wunsch’s 1970 paper supplied a general dynamic-programming framework for comparing amino acid sequences, turning sequence similarity into an optimization problem over possible alignments. Its importance was methodological: it showed that biological sequence comparison could be handled systematically rather than by ad hoc inspection, making alignment a computable object with explicit scoring and recurrence structure.

Smith and Waterman’s 1981 “Identification of common molecular subsequences” built directly on that lineage by adapting dynamic programming to find local similarities: shared subsequences embedded within longer molecular sequences. In that sense, the earlier global sequence-alignment method enabled the later local molecular subsequence alignment method by providing the algorithmic foundation that Smith and Waterman specialized for detecting common regions rather than aligning entire proteins end to end.

### 1981 → 1988: [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md) enables [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)

> Smith-Waterman local alignment defined optimal molecular subsequence matching that FASTA approximated with faster heuristic tools.

“Identification of common molecular subsequences” introduced the Smith-Waterman local alignment framework: a way to define optimal matching regions between biological sequences rather than forcing whole-sequence comparisons. That mattered because it gave the field a rigorous target for what meaningful subsequence similarity should mean.

“Improved tools for biological sequence comparison.” built on that foundation by making sequence comparison more practical at database scale. FASTA did not replace the optimal local-alignment idea; it approximated it with faster heuristics, preserving the core goal of finding biologically relevant local similarities while trading exactness for speed. In that sense, Smith-Waterman supplied the formal standard, and FASTA helped turn that standard into a usable search tool for rapidly growing biological sequence collections.

### 1988 → 1997: [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md) enables [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)

> FASTA's heuristic sequence-comparison strategy helped establish fast database searching that Gapped BLAST and PSI-BLAST extended.

“Improved tools for biological sequence comparison” helped make rapid, heuristic database searching a practical foundation for sequence analysis. By showing how tools such as FASTA could trade exhaustive comparison for efficient, biologically useful search, it established a model in which large sequence databases could be queried quickly enough to become routine scientific infrastructure.

“Gapped BLAST and PSI-BLAST” extended that lineage into a new generation of protein search programs. Its advances built on the same enabling premise captured in the edge label: FASTA’s heuristic sequence-comparison strategy helped establish fast database searching, and BLAST-family methods then expanded that paradigm with gapped alignments and iterative profile-based searching while preserving the central goal of fast, useful database comparison.

### 1997 → 2009: [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md) enables [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)

> Gapped BLAST refined seed-and-extend alignment heuristics, a predecessor to BWT-based short-read aligners that made genome-scale matching faster.

“Gapped BLAST and PSI-BLAST” advanced the practical seed-and-extend style of sequence search: find promising local matches quickly, then extend and score them with more sensitive alignment heuristics. That framing helped establish a central pattern in computational biology: exhaustive biological sequence comparison could be made useful at database scale by combining clever indexing or seeding with selective alignment rather than attempting full dynamic programming everywhere.

“Fast and accurate short read alignment with Burrows–Wheeler transform” carried that lineage into the high-throughput sequencing era. Its BWT-based indexing was a different technical engine, but it addressed the same pressure that Gapped BLAST had helped define: making genome-scale matching fast enough while preserving biologically meaningful alignments. In that sense, Gapped BLAST was a predecessor not because it used BWT, but because it refined the heuristic search tradition that later short-read aligners adapted to much larger read-mapping workloads.

### 2009 → 2015: [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md) enables [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md)

> BWA enabled the reference epigenome project by aligning large ChIP-seq, DNA methylation, and chromatin-accessibility short-read datasets to the human genome.

“Fast and accurate short read alignment with Burrows-Wheeler transform” provided a practical way to map large volumes of short sequencing reads back to the human reference genome. That mattered because epigenomic assays such as ChIP-seq, DNA methylation profiling, and chromatin-accessibility sequencing all begin with reads whose biological meaning depends on where they align in the genome.

The 2015 “Integrative analysis of 111 reference human epigenomes” could therefore build on BWA as part of the computational foundation for producing comparable genome-wide maps across many cell and tissue contexts. In the recorded lineage, BWA enabled the reference epigenome project by aligning these large short-read datasets to the human genome, turning raw sequencing output into genomic signal tracks that could be integrated across epigenomic marks and samples.

### 2015 → 2020: [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md) enables [The GTEx Consortium atlas of genetic regulatory effects across human tissues](../paper/10_1126_science_aaz1776.md)

> Reference epigenome maps provided chromatin annotations used to interpret tissue-specific regulatory effects in the GTEx atlas.

“Integrative analysis of 111 reference human epigenomes” helped establish broad reference maps of human chromatin states across many tissues and cell types. Those maps gave researchers a shared epigenomic context for asking where regulatory DNA was likely active, poised, repressed, or otherwise marked in different biological settings.

That enabled the 2020 GTEx atlas by providing chromatin annotations that could be used to interpret tissue-specific genetic regulatory effects. In GTEx, genetic variants linked to gene regulation across tissues were not just cataloged as associations; they could be placed against reference epigenome maps to help explain why particular regulatory effects appeared in particular tissue contexts.
