---
title: 1980 A feature-integration theory of attention → 1998 A model of saliency-based
  visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual
  Object Classes (VOC) → 2016 Deep Residual Learning for Image Recognition → 2021
  Highly accurate protein structure prediction with
length: 5
start_doi: 10.1016/0010-0285(80)90005-5
end_doi: 10.1038/s41586-021-03819-2
---

# 1980 A feature-integration theory of attention → 1998 A model of saliency-based visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2016 Deep Residual Learning for Image Recognition → 2021 Highly accurate protein structure prediction with

_6 papers, 5 `enables` steps._

## Chain

1. **1980** — [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md)
1. **1998** — [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2016** — [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)
1. **2021** — [Highly accurate protein structure prediction with AlphaFold](../paper/10_1038_s41586_021_03819_2.md)

## Walkthrough

### 1980 → 1998: [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md) enables [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)

> Feature-integration theory linked attention to basic visual feature maps, which Itti, Koch, and Niebur computationalized as saliency maps for rapid scene analysis.

Treisman and Gelade’s **“A feature-integration theory of attention”** framed visual attention around the problem of combining basic visual features into coherent percepts. Its key historical contribution, for this lineage, was to make attention depend on separable feature representations: color, orientation, and other basic dimensions could be treated as organized feature maps that attention helps bind and select.

Itti, Koch, and Niebur’s **“A model of saliency-based visual attention for rapid scene analysis”** took that conceptual architecture into computational form. The 1998 model did not merely cite attention as a general capacity; it operationalized the feature-map idea as saliency maps that could guide rapid visual selection in scenes. In that sense, feature-integration theory enabled the later model by turning attention into a feature-based selection problem that could be formalized algorithmically.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based rapid scene analysis reinforced the idea of fast attentional feature selection that Viola-Jones implemented through efficient visual features.

“A model of saliency-based visual attention for rapid scene analysis” helped formalize a computational view of vision in which scenes could be filtered quickly through feature-based attentional selection. Its saliency framing emphasized that not all visual information needs equal processing: simple visual features can guide rapid prioritization of likely relevant regions.

“Robust Real-Time Face Detection” followed a different engineering path, but the connection is in that shared commitment to speed through selective visual computation. Viola-Jones implemented efficient visual features and a staged detection process to make face finding practical in real time. In this lineage, saliency-based rapid scene analysis reinforced the broader idea that fast, feature-driven selection could turn dense visual input into tractable decisions, which Viola-Jones embodied in a robust detection system.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Real-time face detection helped establish sliding-window object-detection methodology that PASCAL VOC generalized across visual object classes.

“Robust Real-Time Face Detection” helped make object detection feel like a practical, repeatable visual-recognition problem rather than a purely offline recognition exercise. Its historical importance lies in the sliding-window framing: scan an image at many positions and scales, score candidate regions, and turn local classifier responses into detections. That methodology became a template for thinking about detection systems.

“The Pascal Visual Object Classes (VOC) Challenge” broadened that template from faces to many everyday object categories. In the lineage captured by the edge label, Viola-Jones-style real-time face detection helped establish the operational pattern that VOC then generalized: evaluate detectors across visual object classes, not just one specialized category. VOC did not merely inherit a face detector; it inherited and standardized the broader detection problem setting that such systems made visible.

### 2009 → 2016: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)

> PASCAL VOC helped standardize visual-recognition benchmarking and detection tasks that residual networks later improved through very deep convolutional features.

“The Pascal Visual Object Classes (VOC) Challenge” helped make visual recognition a shared, measurable problem: common datasets, task definitions, and evaluation protocols for classification, detection, and related vision benchmarks. That standardization gave the field a clearer way to compare methods and track progress on object-centric recognition rather than only on isolated lab datasets.

“Deep Residual Learning for Image Recognition” later advanced this trajectory by showing how very deep convolutional networks could be trained more effectively and used as stronger feature extractors for recognition tasks. In that lineage, PASCAL VOC did not cause residual learning directly; it helped define the benchmark culture and detection problems that residual networks would later improve through deeper visual representations.

### 2016 → 2021: [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md) enables [Highly accurate protein structure prediction with AlphaFold](../paper/10_1038_s41586_021_03819_2.md)

> Residual networks enabled AlphaFold's very deep neural architectures to propagate pairwise and spatial protein-structure features without optimization collapse.

“Deep Residual Learning for Image Recognition” made it practical to train much deeper neural networks by using residual connections, so representations could be refined across many layers without the optimization collapse that had limited earlier architectures. Although developed for visual recognition, that design principle became part of the broader deep learning toolkit for building networks that repeatedly update structured feature maps.

AlphaFold depended on that kind of depth-friendly architecture. Protein structure prediction requires propagating and refining pairwise relationships and spatial constraints across many interacting residues, not just making a shallow local prediction. Residual networks therefore helped enable AlphaFold’s very deep neural architectures to carry protein-structure features through many transformations while preserving trainability, connecting a breakthrough in image-recognition optimization to a later breakthrough in scientific modeling.
