---
title: 'Bismark: a flexible aligner and methylation caller for Bisulfite-Seq applications'
doi: 10.1093/bioinformatics/btr167
openalex_id: https://openalex.org/W2131374955
year: 2011
venue: Bioinformatics
authors: Felix Krueger, Simon Andrews
citations: 5852
fleming_tier: true
concepts:
- DNA methylation
- Bisulfite sequencing
- Computer science
- Snapshot (computer storage)
- Computational biology
- Methylation
- CpG site
- Context (archaeology)
- Biology
- Genetics
---

# Bismark: a flexible aligner and methylation caller for Bisulfite-Seq applications

## Why this mattered

Before Bismark, whole-genome bisulfite sequencing had made single-base DNA methylation measurement possible, but the analysis was still technically awkward: bisulfite conversion destroys normal C/T symmetry, creating a mapping problem that standard short-read aligners did not solve by themselves. Krueger and Andrews’ contribution was not a new biological theory, but an enabling computational layer: Bismark combined bisulfite-aware alignment with methylation calling in one workflow, using converted read/genome representations and reporting methylation in CpG, CHG, and CHH contexts. That mattered because it turned BS-Seq from a specialist bioinformatics problem into a more routine assay that experimentalists could run, inspect, and interpret soon after sequencing.

The paradigm shift was practical standardization. By supporting single-end and paired-end reads, directional and non-directional libraries, and multiple cytosine sequence contexts, Bismark helped make genome-wide methylation maps comparable across organisms, protocols, and laboratories. Its importance is reflected in its long use as a reference tool for whole-genome and reduced-representation bisulfite sequencing studies: downstream work in cancer epigenomics, plant methylomes, developmental biology, environmental epigenetics, and single-cell methylation methods could treat methylation calls as a scalable data layer rather than a bespoke computational artifact.

Subsequent breakthroughs in epigenomics depended on exactly this kind of infrastructure. Large methylome atlases, differential methylation studies, and integrative analyses linking methylation with chromatin state, transcription, genotype, and disease all required reliable conversion from raw bisulfite reads into base-resolution methylation evidence. Bismark did not discover a new epigenetic mechanism; it made discovery faster and more reproducible by lowering the barrier between sequencing output and interpretable methylomes. Its citation record reflects that role: it became part of the methodological substrate on which modern population-scale and cell-type-resolved DNA methylation research was built.

## Abstract

Abstract Summary: A combination of bisulfite treatment of DNA and high-throughput sequencing (BS-Seq) can capture a snapshot of a cell's epigenomic state by revealing its genome-wide cytosine methylation at single base resolution. Bismark is a flexible tool for the time-efficient analysis of BS-Seq data which performs both read mapping and methylation calling in a single convenient step. Its output discriminates between cytosines in CpG, CHG and CHH context and enables bench scientists to visualize and interpret their methylation data soon after the sequencing run is completed. Availability and implementation: Bismark is released under the GNU GPLv3+ licence. The source code is freely available from www.bioinformatics.bbsrc.ac.uk/projects/bismark/. Contact: felix.krueger@bbsrc.ac.uk Supplementary information: Supplementary data are available at Bioinformatics online.


## Related

- **cite** → [Ultrafast and memory-efficient alignment of short DNA sequences to the human genome](10_1186_gb_2009_10_3_r25.md) — Bismark uses the Bowtie short-read aligner as the core mapping engine for bisulfite-converted sequencing reads.


## Sources

- DOI: [https://doi.org/10.1093/bioinformatics/btr167](https://doi.org/10.1093/bioinformatics/btr167)
- OpenAlex: [https://openalex.org/W2131374955](https://openalex.org/W2131374955)