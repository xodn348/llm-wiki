---
title: Fast and accurate short read alignment with Burrows–Wheeler transform
doi: 10.1093/bioinformatics/btp324
openalex_id: https://openalex.org/W2103441770
year: 2009
venue: Bioinformatics
authors: Heng Li, Richard Durbin
citations: 62244
fleming_tier: true
concepts:
- Computer science
- Software
- Alignment-free sequence analysis
- Hash table
- Reference genome
- Hybrid genome assembly
- Indel
- Multiple sequence alignment
- Sequence alignment
- DNA sequencing
---

# Fast and accurate short read alignment with Burrows–Wheeler transform

## Why this mattered

_TBD_

## Abstract

MOTIVATION: Many programs for aligning short sequencing reads to a reference genome have been developed in the last 2 years. Most of them are very efficient for short reads but inefficient or not applicable for reads >200 bp because the algorithms are heavily and specifically tuned for short queries with low sequencing error rate. However, some sequencing platforms already produce longer reads and others are expected to become available soon. For longer reads, hashing-based software such as BLAT and SSAHA2 remain the only choices. Nonetheless, these methods are substantially slower than short-read aligners in terms of aligned bases per unit time. RESULTS: We designed and implemented a new algorithm, Burrows-Wheeler Aligner's Smith-Waterman Alignment (BWA-SW), to align long sequences up to 1 Mb against a large sequence database (e.g. the human genome) with a few gigabytes of memory. The algorithm is as accurate as SSAHA2, more accurate than BLAT, and is several to tens of times faster than both. AVAILABILITY: http://bio-bwa.sourceforge.net



## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324)
- OpenAlex: [https://openalex.org/W2103441770](https://openalex.org/W2103441770)