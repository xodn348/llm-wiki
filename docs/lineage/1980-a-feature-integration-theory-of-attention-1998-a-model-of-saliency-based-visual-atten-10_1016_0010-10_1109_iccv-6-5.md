---
title: '1980 A feature-integration theory of attention → 1998 A model of saliency-based
  visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual
  Object Classes (VOC) → 2016 Faster R-CNN: Towards Real-Time Object Detection → 2023
  Segment Anything'
length: 5
start_doi: 10.1016/0010-0285(80)90005-5
end_doi: 10.1109/iccv51070.2023.00371
---

# 1980 A feature-integration theory of attention → 1998 A model of saliency-based visual attention → 2004 Robust Real-Time Face Detection → 2009 The Pascal Visual Object Classes (VOC) → 2016 Faster R-CNN: Towards Real-Time Object Detection → 2023 Segment Anything

_6 papers, 5 `enables` steps._

## Chain

1. **1980** — [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md)
1. **1998** — [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)
1. **2004** — [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)
1. **2009** — [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)
1. **2016** — [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](../paper/10_1109_tpami_2016_2577031.md)
1. **2023** — [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

## Walkthrough

### 1980 → 1998: [A feature-integration theory of attention](../paper/10_1016_0010_0285_80_90005_5.md) enables [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md)

> Feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception.

“A feature-integration theory of attention” (1980) framed visual attention as the process that binds separately registered features into coherent object perception. That gave later computational accounts a clear conceptual architecture: early vision could be treated as multiple feature-specific representations, while attention selects and integrates what matters for perception.

“A model of saliency-based visual attention for rapid scene analysis” (1998) built on that lineage by turning the idea of separate feature maps into an explicit saliency framework for guiding attention across a scene. In that sense, feature-integration theory enabled saliency models by proposing that attention combines separate feature maps into object perception, making it natural to model visual selection as competition and combination across feature-based maps.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based attention supplied the selective visual-processing idea echoed by cascade-style focus on promising image regions in real-time face detection.

“A model of saliency-based visual attention for rapid scene analysis” (1998) helped formalize a computational idea of selective visual processing: instead of treating every part of a scene as equally relevant, a system can prioritize promising regions for faster analysis. Its saliency framing made attention a concrete image-processing strategy for rapid scene understanding.

“Robust Real-Time Face Detection” (2004) reflects that lineage in a more task-specific engineering form. The cascade detector focuses computation on candidate image regions, quickly rejecting unlikely areas and spending more work only where a face remains plausible. The connection is not a direct reuse of saliency maps, but an enabling idea: efficient vision depends on selective allocation of processing to the most promising parts of the image.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Viola-Jones showed that object categories could be detected efficiently with learned visual features, motivating the benchmarked detection task in Pascal VOC.

“Robust Real-Time Face Detection” helped establish that visual object detection could be framed as a practical learned-feature problem, not just a hand-engineered recognition exercise. Viola-Jones made face detection fast and deployable enough to show that a category-level detector could scan images efficiently and return localized object instances in real time.

That success helped motivate the broader benchmark culture embodied by “The Pascal Visual Object Classes (VOC) Challenge.” Pascal VOC generalized the question from faces to many object categories and made detection a shared, measured task: systems could be compared on common data, categories, and evaluation protocols. In that lineage, Viola-Jones demonstrated the feasibility and importance of efficient learned detection, while Pascal VOC turned object-category detection into a standardized community challenge.

### 2009 → 2016: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](../paper/10_1109_tpami_2016_2577031.md)

> The PASCAL VOC benchmark supplied the object detection evaluation protocol and datasets used to measure Faster R-CNN performance.

“The Pascal Visual Object Classes (VOC) Challenge” helped make object detection a shared, measurable problem rather than a collection of isolated demos. Its benchmark datasets and evaluation protocol gave researchers a common way to train, test, and compare systems on visual object categories, shaping the experimental language used across later detection papers.

“Faster R-CNN” built on that lineage by reporting its region proposal network and detector within the PASCAL VOC evaluation framework. The VOC benchmark did not supply Faster R-CNN’s method, but it supplied the recognized detection setting in which the method’s performance could be measured and compared against prior work.

### 2016 → 2023: [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](../paper/10_1109_tpami_2016_2577031.md) enables [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

> Faster R-CNN's region proposal networks established prompt-like object localization machinery that helped set the detection-to-segmentation lineage leading to Segment Anything.

*Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks* helped make object localization a learned, reusable stage rather than a separate hand-engineered preprocessing step. Its region proposal networks showed that a model could efficiently generate object-focused spatial cues inside a detection pipeline, establishing a practical bridge between “where is the object?” and downstream visual understanding.

That idea forms part of the detection-to-segmentation lineage leading to *Segment Anything*. While SAM is not simply an extension of Faster R-CNN, its promptable segmentation interface depends on the broader historical shift toward using localization signals as actionable inputs for pixel-level prediction. In that sense, Faster R-CNN enabled later work by normalizing prompt-like object localization machinery: boxes, regions, and candidate object locations became central handles for guiding richer visual tasks such as segmentation.
