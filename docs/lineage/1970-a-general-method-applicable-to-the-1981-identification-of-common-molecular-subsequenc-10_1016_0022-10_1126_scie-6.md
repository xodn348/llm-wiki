---
title: 1970 A general method applicable to the → 1981 Identification of common molecular
  subsequences → 1988 Improved tools for biological sequence comparison. → 2009 Fast
  and accurate short read alignment → 2015 Integrative analysis of 111 reference human
  → 2020 The GTEx Consortium atlas of genetic
length: 5
start_doi: 10.1016/0022-2836(70)90057-4
end_doi: 10.1126/science.aaz1776
---

# 1970 A general method applicable to the → 1981 Identification of common molecular subsequences → 1988 Improved tools for biological sequence comparison. → 2009 Fast and accurate short read alignment → 2015 Integrative analysis of 111 reference human → 2020 The GTEx Consortium atlas of genetic

_6 papers, 5 `enables` steps._

## Chain

1. **1970** — [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md)
1. **1981** — [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)
1. **1988** — [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)
1. **2009** — [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)
1. **2015** — [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md)
1. **2020** — [The GTEx Consortium atlas of genetic regulatory effects across human tissues](../paper/10_1126_science_aaz1776.md)

## Walkthrough

### 1970 → 1981: [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md) enables [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md)

> Needleman-Wunsch dynamic programming for pairwise sequence alignment enabled Smith-Waterman local alignment to identify conserved molecular subsequences.

Needleman and Wunsch’s 1970 paper supplied a general dynamic-programming framework for comparing two protein sequences end to end. Its importance was methodological: it made sequence similarity a computable alignment problem, where possible residue matches, mismatches, and gaps could be evaluated systematically rather than by ad hoc visual comparison.

Smith and Waterman’s 1981 “Identification of common molecular subsequences” built directly on that lineage by adapting the dynamic-programming idea toward local alignment. Instead of seeking the best overall alignment across two full sequences, the later method identified high-scoring conserved subsequences within them. In that sense, Needleman-Wunsch enabled Smith-Waterman by establishing the pairwise alignment machinery that could be specialized for finding shared molecular regions.

### 1981 → 1988: [Identification of common molecular subsequences](../paper/10_1016_0022_2836_81_90087_5.md) enables [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md)

> Smith-Waterman introduced local sequence alignment, which FASTA approximated efficiently for rapid database similarity searches.

“Identification of common molecular subsequences” introduced the Smith-Waterman formulation of local sequence alignment: a way to identify the best-matching subsequences between biological sequences rather than forcing an end-to-end comparison. That mattered because biological similarity is often local, reflecting conserved domains, motifs, or regions within otherwise divergent sequences.

“Improved tools for biological sequence comparison.” built on that intellectual foundation by making local-similarity search practical at database scale. FASTA approximated the kind of local alignment Smith-Waterman defined, using efficient heuristics to rapidly find candidate similarities before refinement. In that sense, Smith-Waterman supplied the rigorous alignment objective, while FASTA translated the objective into a faster tool for routine biological sequence database searches.

### 1988 → 2009: [Improved tools for biological sequence comparison.](../paper/10_1073_pnas_85_8_2444.md) enables [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)

> FASTA advanced fast heuristic sequence comparison, motivating the speed-accuracy tradeoff later pushed much further by BWA's Burrows-Wheeler short-read indexing.

“Improved tools for biological sequence comparison.” sits in the lineage as an early demonstration that biological sequence search could be made practical by heuristic comparison rather than exhaustive alignment alone. Through FASTA, it advanced a speed-accuracy tradeoff: find biologically useful similarities quickly enough to support routine database-scale analysis, while preserving enough alignment signal to remain scientifically meaningful.

“Fast and accurate short read alignment with Burrows–Wheeler transform” pushed that same pressure point into the sequencing era. By 2009, short-read data made speed and scale central constraints, and BWA answered with Burrows-Wheeler indexing rather than the FASTA-style heuristic search strategy. The enabling relationship is conceptual and methodological: FASTA helped establish fast approximate sequence comparison as a core computational biology problem, motivating later systems like BWA to drive the speed-accuracy balance much further for short-read alignment.

### 2009 → 2015: [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md) enables [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md)

> BWA enabled efficient alignment of high-throughput sequencing reads used to build Roadmap Epigenomics chromatin, methylation, and transcriptome maps.

Li and Durbin’s 2009 BWA paper helped make short-read sequencing data practically usable at scale by providing a fast, accurate way to align high-throughput reads to the human reference genome. That alignment step is foundational: before chromatin accessibility, histone marks, DNA methylation, or RNA-derived signals can be compared across tissues and cell types, the reads must first be placed reliably on the genome.

The 2015 Roadmap Epigenomics integrative analysis depended on exactly that kind of sequencing infrastructure. BWA enabled efficient alignment of the high-throughput sequencing reads used to build the project’s chromatin, methylation, and transcriptome maps, turning many experiments across many reference epigenomes into genome-coordinate data that could be integrated and compared.

### 2015 → 2020: [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md) enables [The GTEx Consortium atlas of genetic regulatory effects across human tissues](../paper/10_1126_science_aaz1776.md)

> The Roadmap Epigenomics reference maps enabled GTEx to interpret tissue-specific eQTLs through chromatin states and regulatory annotations.

*Integrative analysis of 111 reference human epigenomes* provided a broad reference framework for reading the noncoding genome across many human tissues and cell types. By organizing chromatin states and regulatory annotations into tissue-aware maps, the Roadmap Epigenomics work made it easier to connect genetic variation with the regulatory contexts in which variants might act.

That foundation enabled *The GTEx Consortium atlas of genetic regulatory effects across human tissues* to interpret tissue-specific eQTLs not just as statistical associations between genotype and expression, but as signals embedded in annotated regulatory landscapes. In historical terms, Roadmap helped supply the epigenomic vocabulary, while GTEx applied it at scale to genetic regulation across tissues. The enabling relationship is therefore direct: reference chromatin maps made GTEx’s tissue-specific regulatory interpretations more biologically grounded.
