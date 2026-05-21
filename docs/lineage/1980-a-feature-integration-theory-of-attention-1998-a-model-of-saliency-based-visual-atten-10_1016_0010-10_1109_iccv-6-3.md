---
title: 1980 A feature-integration theory of attention → 1998 A model of saliency-based
  visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual
  Object Classes (VOC) → 2014 Rich Feature Hierarchies for Accurate Object → 2023
  Segment Anything
length: 5
start_doi: 10.1016/0010-0285(80)90005-5
end_doi: 10.1109/iccv51070.2023.00371
---

# 1980 A feature-integration theory of attention → 1998 A model of saliency-based visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2014 Rich Feature Hierarchies for Accurate Object → 2023 Segment Anything

_6 papers, 5 `enables` steps._

## Chain

1. **1980** — [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md)
1. **1998** — [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2014** — [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md)
1. **2023** — [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

## Walkthrough

### 1980 → 1998: [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md) enables [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)

> Feature-integration theory linked attention to basic visual feature maps, which Itti, Koch, and Niebur computationalized as saliency maps for rapid scene analysis.

“A feature-integration theory of attention” framed visual attention as operating over separable basic features before they are bound into coherent objects. That gave later computational work a clear conceptual substrate: attention could be modeled not just as a vague spotlight, but as a process acting on feature-specific representations.

“A model of saliency-based visual attention for rapid scene analysis” built directly on that lineage by computationalizing feature maps into saliency maps. In the recorded relationship, Treisman and Gelade linked attention to basic visual feature maps; Itti, Koch, and Niebur turned that idea into an explicit model for ranking locations in a scene by visual salience, making rapid attentional selection operational in machine vision terms.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based rapid scene analysis reinforced the idea of fast attentional feature selection that Viola-Jones implemented through efficient visual features.

“A model of saliency-based visual attention for rapid scene analysis” helped frame vision as a process of quickly selecting informative regions and features from a scene, rather than exhaustively interpreting everything at once. Its saliency-based account reinforced the broader idea that efficient visual attention can prioritize candidate locations using relatively simple, fast-computed signals.

“Robust Real-Time Face Detection” translated that attentional logic into an engineering system: instead of modeling biological saliency directly, Viola-Jones used efficient visual features and a cascade to rapidly reject unlikely image regions while focusing computation on promising candidates. In that sense, the 1998 work enabled the 2004 paper conceptually, by strengthening the case for fast feature-driven selection as a practical path toward rapid scene analysis.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Real-time face detection helped establish sliding-window object-detection methodology that PASCAL VOC generalized across visual object classes.

“Robust Real-Time Face Detection” helped make object detection feel like a practical, operational problem: scan an image with a detection window, evaluate candidate regions efficiently, and return localized object hypotheses. Its success around real-time face detection gave the sliding-window paradigm a concrete and influential form, showing how a detector could be trained for a visual category and deployed across image locations and scales.

“The Pascal Visual Object Classes (VOC) Challenge” generalized that methodological frame beyond faces. Rather than treating face detection as a special-purpose achievement, VOC helped turn category-level detection into a shared benchmark problem across many object classes, with common datasets, tasks, and evaluation conventions. In that lineage, Viola-Jones-style real-time detection helped establish the practical template that VOC broadened into a community-wide object-recognition challenge.

### 2009 → 2014: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md)

> PASCAL VOC provided the object-detection benchmark and evaluation protocol on which R-CNN demonstrated region-based CNN detection gains.

The Pascal VOC Challenge made object detection a shared, measurable problem rather than a collection of incomparable demos. By defining benchmark datasets, task structure, and an evaluation protocol, it gave later work a standard arena for asking whether a detector actually improved over prior approaches.

R-CNN’s “Rich Feature Hierarchies” could therefore show its contribution in a historically legible way: applying CNN features to region proposals and evaluating the resulting detector under the PASCAL VOC protocol. VOC enabled the paper’s gains to be understood as advances in object detection itself, not just as performance on a private dataset or idiosyncratic test setup.

### 2014 → 2023: [Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation](../paper/10_1109_cvpr_2014_81.md) enables [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

> R-CNN linked CNN feature extraction with region-level recognition, enabling SAM's use of learned visual features for object-level segmentation masks.

“Rich Feature Hierarchies for Accurate Object Detection and Semantic Segmentation” helped establish the pattern of using deep CNN representations as transferable visual features for region-level understanding. Its R-CNN framing connected learned feature extraction with object proposals and recognition over localized regions, making object-centric interpretation a practical deep-learning pipeline rather than only a classification task.

“Segment Anything” builds in a later era with much larger models and broader training, but it inherits that lineage: segmentation masks depend on learned visual features that support object-level separation in an image. The enabling relationship is not that SAM copies R-CNN’s architecture, but that R-CNN made the CNN-feature-to-region-understanding bridge central to modern vision, helping clear the path for promptable object-level mask generation.
