---
title: '1970 A general method applicable to the → 1990 Basic local alignment search
  tool → 1997 Gapped BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read
  alignment → 2015 Integrative analysis of 111 reference human → 2020 The GTEx Consortium
  atlas of genetic'
length: 5
start_doi: 10.1016/0022-2836(70)90057-4
end_doi: 10.1126/science.aaz1776
---

# 1970 A general method applicable to the → 1990 Basic local alignment search tool → 1997 Gapped BLAST and PSI-BLAST: a new → 2009 Fast and accurate short read alignment → 2015 Integrative analysis of 111 reference human → 2020 The GTEx Consortium atlas of genetic

_6 papers, 5 `enables` steps._

## Chain

1. **1970** — [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md)
1. **1990** — [Basic local alignment search tool](../paper/10_1016_s0022_2836_05_80360_2.md)
1. **1997** — [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)
1. **2009** — [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)
1. **2015** — [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md)
1. **2020** — [The GTEx Consortium atlas of genetic regulatory effects across human tissues](../paper/10_1126_science_aaz1776.md)

## Walkthrough

### 1970 → 1990: [A general method applicable to the search for similarities in the amino acid sequence of two proteins](../paper/10_1016_0022_2836_70_90057_4.md) enables [Basic local alignment search tool](../paper/10_1016_s0022_2836_05_80360_2.md)

> Needleman-Wunsch dynamic programming for sequence similarity enabled BLAST's faster heuristic local alignment search.

Needleman and Wunsch’s 1970 paper established dynamic programming as a general way to compare amino acid sequences and identify sequence similarity through an explicit optimization procedure. That gave later computational biology a rigorous baseline: protein sequences could be aligned algorithmically, and similarity search could be framed as a reproducible computational problem rather than a purely manual comparison.

BLAST, introduced in 1990, was enabled by that lineage while changing the practical strategy. Instead of applying full dynamic programming to every possible comparison, it used a faster heuristic approach for local alignment search, preserving the core goal of detecting biologically meaningful sequence similarity while making large-scale database searching more tractable. Thus Needleman-Wunsch supplied the foundational alignment framework that BLAST accelerated and adapted for the expanding sequence databases of molecular biology.

### 1990 → 1997: [Basic local alignment search tool](../paper/10_1016_s0022_2836_05_80360_2.md) enables [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md)

> Original BLAST introduced local heuristic database search, which Gapped BLAST and PSI-BLAST enhanced with gaps and iterative profiles.

“Basic local alignment search tool” established BLAST as a practical heuristic approach for finding local sequence similarities in large databases. By making local database search fast and usable, it created the foundation that later protein-search methods could extend rather than replace.

“Gapped BLAST and PSI-BLAST” built directly on that foundation: Gapped BLAST enhanced the original local-search framework by allowing gaps in alignments, while PSI-BLAST added iterative profile-based searching to detect more remote protein relationships. The 1997 paper is therefore a clear next generation of the 1990 work: it kept BLAST’s core heuristic database-search idea, then expanded what kinds of biologically meaningful similarities the search could capture.

### 1997 → 2009: [Gapped BLAST and PSI-BLAST: a new generation of protein database search programs](../paper/10_1093_nar_25_17_3389.md) enables [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md)

> Gapped BLAST refined seed-and-extend alignment heuristics, a predecessor to BWT-based short-read aligners that made genome-scale matching faster.

“Gapped BLAST and PSI-BLAST” helped establish a practical lineage of database search built around heuristic alignment: find promising local matches, extend them efficiently, and trade exhaustive dynamic programming for speed while preserving useful biological sensitivity. Its gapped seed-and-extend style became part of the common toolkit for thinking about large-scale sequence comparison, especially as databases grew beyond what naive all-against-all alignment could handle.

“Fast and accurate short read alignment with Burrows-Wheeler transform” inherited that pressure point: genome-scale matching needed to become faster still, now for massive numbers of short sequencing reads. BWT-based aligners changed the indexing machinery, but they addressed a problem already shaped by BLAST-era heuristics: rapidly locating candidate matches and refining alignments at scale. In that sense, Gapped BLAST was a predecessor in search strategy, while BWT supplied the next-generation data structure for high-throughput read alignment.

### 2009 → 2015: [Fast and accurate short read alignment with Burrows–Wheeler transform](../paper/10_1093_bioinformatics_btp324.md) enables [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md)

> BWA enabled the reference epigenome project by aligning large ChIP-seq, DNA methylation, and chromatin-accessibility short-read datasets to the human genome.

“Fast and accurate short read alignment with Burrows-Wheeler transform” introduced BWA as a practical way to align large volumes of short sequencing reads to the human reference genome. That capability became part of the basic infrastructure for high-throughput genomics: before biological interpretation, reads from assays such as ChIP-seq, DNA methylation profiling, and chromatin-accessibility experiments had to be placed accurately on the genome.

The 2015 “Integrative analysis of 111 reference human epigenomes” depended on exactly that kind of alignment layer. By enabling large epigenomic short-read datasets to be mapped consistently to the human genome, BWA helped make it possible to compare regulatory marks, methylation patterns, and accessibility profiles across many human tissues and cell types within a shared genomic coordinate system.

### 2015 → 2020: [Integrative analysis of 111 reference human epigenomes](../paper/10_1038_nature14248.md) enables [The GTEx Consortium atlas of genetic regulatory effects across human tissues](../paper/10_1126_science_aaz1776.md)

> Reference epigenome maps provided chromatin annotations used to interpret tissue-specific regulatory effects in the GTEx atlas.

The 2015 integrative analysis of 111 reference human epigenomes helped establish a broad reference framework for reading regulatory DNA through chromatin state. By mapping epigenomic patterns across many human cell and tissue contexts, it gave later genetics studies a way to distinguish likely promoters, enhancers, repressed regions, and other regulatory annotations from raw noncoding sequence.

The 2020 GTEx atlas built on that kind of reference context when interpreting how genetic variation affects gene regulation across human tissues. Its tissue-specific regulatory effects were not just lists of associations; they could be placed against chromatin annotations from reference epigenome maps, helping connect genetic regulatory signals to plausible regulatory elements and tissue-relevant genomic contexts.
