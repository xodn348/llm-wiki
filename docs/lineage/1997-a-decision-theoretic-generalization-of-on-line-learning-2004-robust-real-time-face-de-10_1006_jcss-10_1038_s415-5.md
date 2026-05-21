---
title: 1997 A Decision-Theoretic Generalization of On-Line Learning → 2004 Robust
  Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2016 Deep
  Residual Learning for Image Recognition → 2021 Highly accurate protein structure
  prediction with
length: 4
start_doi: 10.1006/jcss.1997.1504
end_doi: 10.1038/s41586-021-03819-2
---

# 1997 A Decision-Theoretic Generalization of On-Line Learning → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2016 Deep Residual Learning for Image Recognition → 2021 Highly accurate protein structure prediction with

_5 papers, 4 `enables` steps._

## Chain

1. **1997** — [A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting](../paper/10_1006_jcss_1997_1504.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2016** — [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)
1. **2021** — [Highly accurate protein structure prediction with AlphaFold](../paper/10_1038_s41586_021_03819_2.md)

## Walkthrough

### 1997 → 2004: [A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting](../paper/10_1006_jcss_1997_1504.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> AdaBoost supplied the boosted cascade classifier training method used by Viola-Jones for real-time face detection.

Freund and Schapire’s 1997 paper framed AdaBoost as a decision-theoretic method for combining many weak learners into a strong predictor through iterative reweighting. That contribution became a practical training recipe: instead of hand-designing one complex classifier, a system could select and weight many simple tests so that difficult examples shaped later stages of learning.

Viola and Jones’s 2004 real-time face detector used that AdaBoost machinery as the training method for its boosted cascade classifiers. In the face-detection setting, AdaBoost helped choose and combine simple visual features into increasingly selective stages, making the cascade architecture viable for fast rejection of non-face regions. Thus, the earlier on-line learning and boosting framework enabled the later detector by supplying the core method for training the classifiers inside the real-time cascade.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Real-time face detection helped establish sliding-window object-detection methodology that PASCAL VOC generalized across visual object classes.

*Robust Real-Time Face Detection* helped make the sliding-window detector a practical, influential template: scan an image at multiple positions and scales, evaluate a learned classifier quickly, and return localized object hypotheses. Its importance was not just that it detected faces, but that it showed how object detection could be framed as efficient, repeatable search over image windows.

*The Pascal Visual Object Classes (VOC) Challenge* generalized that methodological pattern beyond faces. Instead of a single, highly structured category, VOC organized detection and recognition around many everyday visual object classes, shared datasets, and common evaluation. In that lineage, real-time face detection helped establish a working detection paradigm, while PASCAL VOC turned object detection into a broader benchmarked problem for the computer vision community.

### 2009 → 2016: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md)

> PASCAL VOC helped standardize visual-recognition benchmarking and detection tasks that residual networks later improved through very deep convolutional features.

“The Pascal Visual Object Classes (VOC) Challenge” helped turn visual recognition into a shared benchmark culture: common datasets, task definitions, and evaluation settings for classification and object detection. That standardization made progress legible across methods, giving later convolutional-network work a concrete arena in which improved visual features could be compared and understood.

“Deep Residual Learning for Image Recognition” built on this benchmarking landscape by showing how residual connections made very deep convolutional models practical for image recognition. In that lineage, PASCAL VOC did not cause residual networks directly; it helped define the visual-recognition and detection problems that residual networks later advanced through stronger, deeper learned representations.

### 2016 → 2021: [Deep Residual Learning for Image Recognition](../paper/10_1109_cvpr_2016_90.md) enables [Highly accurate protein structure prediction with AlphaFold](../paper/10_1038_s41586_021_03819_2.md)

> Residual networks enabled AlphaFold's very deep neural architectures to propagate pairwise and spatial protein-structure features without optimization collapse.

“Deep Residual Learning for Image Recognition” made very deep neural networks practically trainable by letting layers learn residual transformations while preserving signal flow through shortcut connections. That idea became part of the broader deep learning toolkit for building architectures deep enough to refine complex internal representations without collapsing during optimization.

AlphaFold’s 2021 protein-structure system depended on very deep neural architectures that repeatedly propagated and updated pairwise and spatial features relevant to protein geometry. In that lineage, residual networks enabled the depth needed for those iterative feature transformations: they helped make it feasible to carry structural information through many layers while avoiding the optimization failures that had limited earlier deep models.
