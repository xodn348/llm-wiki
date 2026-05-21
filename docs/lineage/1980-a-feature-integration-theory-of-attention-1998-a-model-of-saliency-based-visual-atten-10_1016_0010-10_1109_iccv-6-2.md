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

> Feature-integration theory linked attention to basic visual feature maps, which Itti, Koch, and Niebur computationalized as saliency maps for rapid scene analysis.

“A feature-integration theory of attention” framed visual attention as operating over separable basic features before they are bound into coherent objects. That made feature maps a central explanatory unit: attention could be understood as selecting, combining, and prioritizing information distributed across dimensions such as color, orientation, and intensity.

“A model of saliency-based visual attention for rapid scene analysis” took that conceptual lineage into a computational form. Itti, Koch, and Niebur treated bottom-up attention as something that could be modeled through saliency maps derived from basic visual feature maps. In that sense, feature-integration theory enabled the later model by giving a cognitive architecture in which primitive features and attentional selection were already linked; the 1998 work translated that link into a mechanism for rapid scene analysis.

### 1998 → 2004: [A model of saliency-based visual attention for rapid scene analysis](../paper/10_1109_34_730558.md) enables [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md)

> Saliency-based rapid scene analysis reinforced the idea of fast attentional feature selection that Viola-Jones implemented through efficient visual features.

“A model of saliency-based visual attention for rapid scene analysis” helped formalize a computational view of vision in which a scene could be scanned quickly by selecting informative visual features before deeper interpretation. Its saliency framework reinforced the broader idea that attention-like mechanisms can prioritize parts of an image through efficient feature selection rather than exhaustive semantic analysis.

“Robust Real-Time Face Detection” translated that same pressure toward speed into a practical detection system: simple visual features, evaluated efficiently, could guide rapid decisions about whether an image region contained a face. The connection is not that Viola-Jones adopted the saliency model directly, but that both papers sit in a lineage where fast, selective processing became central to computer vision: first as rapid scene analysis, then as real-time object detection through efficient visual features.

### 2004 → 2009: [Robust Real-Time Face Detection](../paper/10_1023_b_visi_0000013087_49260_fb.md) enables [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md)

> Real-time face detection helped establish sliding-window object-detection methodology that PASCAL VOC generalized across visual object classes.

“Robust Real-Time Face Detection” helped make object detection feel like an operational computer-vision problem rather than only an offline recognition task. Its importance in this lineage is methodological: it popularized the idea that a detector could scan an image efficiently with a sliding-window style procedure, evaluating many candidate regions and deciding whether the target object was present.

“The Pascal Visual Object Classes (VOC) Challenge” generalized that detection mindset beyond faces. Instead of treating face detection as a specialized success, VOC framed detection as a benchmarkable problem across multiple visual object classes, with shared datasets and evaluation conventions. In that sense, real-time face detection helped establish a practical detection template, and PASCAL VOC turned the broader question into a common challenge for the field.

### 2009 → 2016: [The Pascal Visual Object Classes (VOC) Challenge](../paper/10_1007_s11263_009_0275_4.md) enables [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](../paper/10_1109_tpami_2016_2577031.md)

> PASCAL VOC standardized object-detection benchmarks and evaluation metrics, giving Faster R-CNN a common dataset and mAP target for measuring region proposal networks.

“The Pascal Visual Object Classes (VOC) Challenge” helped make object detection a comparable, benchmark-driven problem rather than a collection of isolated demos. By standardizing datasets, object categories, annotation conventions, and evaluation through mean average precision, PASCAL VOC gave later detection systems a shared target and vocabulary for progress.

“Faster R-CNN” builds directly in that measurement culture. Its region proposal network was not just a new architectural component; it could be evaluated against a recognized detection benchmark and mAP criterion, making its contribution legible relative to prior proposal-and-classification pipelines. In that sense, PASCAL VOC enabled Faster R-CNN by supplying the common experimental ground on which faster, integrated region proposal methods could be judged.

### 2016 → 2023: [Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](../paper/10_1109_tpami_2016_2577031.md) enables [Segment Anything](../paper/10_1109_iccv51070_2023_00371.md)

> Faster R-CNN's region proposal framing enabled SAM's promptable segmentation pipeline by establishing object localization as a reusable precursor to mask prediction.

*Faster R-CNN* helped make object localization a reusable stage in visual recognition: its region proposal framing separated the problem of finding candidate objects from the downstream task of classifying or refining them. That structure made localization feel less like a bespoke detector trick and more like a general precursor that other vision systems could build on.

*Segment Anything* extends that lineage into promptable segmentation. Instead of treating masks as a fixed output of a closed detector, SAM uses prompts such as points or boxes to guide mask prediction. The enabling connection is that Faster R-CNN established object localization as a modular input to richer visual reasoning, while SAM turns localized user or model prompts into precise segmentation outputs.
