# Background-Only Crops for Small-Object Detection in Drone Imagery

**A short guidance note**

*Context: object detection on 42 MP drone imagery, very small targets (~12–40 px), tiled into 640×640 crops for YOLO-family and RF-DETR models. The recurring question: what percentage of the training set should be background-only (empty) crops?*

---

## The short answer

**Start at ~10% background-only tiles — not 20% — and make most of them "hard negatives." Then run a small ablation on your own data and let precision/recall decide.**

Two things are true at once here, and it helps to separate them:

1. **There is no peer-reviewed paper that gives an "optimal percentage."** If you couldn't find one, that's because it doesn't exist. Papers report *that* they used background/negative images, rarely a ratio. So anyone quoting a precise number is giving engineering advice, not a citable result.

2. **The most authoritative concrete number comes from the framework authors.** Ultralytics (who maintain YOLO) recommend **roughly 0–10% background images**, and note that COCO — the reference dataset — contains about **1,000 background images, ~1% of the total**. That is the closest thing to a "source" for a percentage, and it is *lower* than the 20–30% figure floating around online.

So your fellow mentor's gut call — *"10%, 20% is too high"* — is actually well aligned with the framework authors' own guidance. Her instinct matches the documented recommendation.

## Why the lower number makes sense for this problem

When a 42 MP image is tiled into 640×640 crops around 12–40 px targets, each **positive** tile is already ~99% background pixels, and every non-object grid cell / anchor is already treated as a negative during training. The model is not starving for "what is *not* an object" — it sees enormous amounts of it in every positive tile.

Pure **background-only** tiles therefore buy you one specific thing: **false-positive reduction** on backgrounds that resemble targets (glint, foam, bright rocks, bird shadows, wakes). A smaller, *smarter* set of those beats a large pile of random empty ocean.

For DETR-family models like RF-DETR there's an extra reason empty scenes help: the architecture has an explicit "no-object" (∅) class in its matching loss, so it directly benefits from images where the correct answer is "nothing here." (See Carion et al. below.)

## What to actually do next

1. **Start at ~10%** background-only tiles (90% containing ≥1 annotated object).
2. **Make the majority of those background tiles hard negatives**, not random empties. The recipe:
   - Train a first-pass model.
   - Run it and save the tiles it *false-positives* on.
   - Add those tiles as background (empty) training images.
   - Retrain. Repeat if needed.
   This is the single biggest lever — bigger than the exact percentage.
3. **Keep the background tiles diverse** — different sea states, altitudes, illumination, glint, foam, substrate. Twenty *different* backgrounds are worth far more than twenty near-identical ocean crops.
4. **Ablate on your own data.** Train at 0% / 5% / 10% / 20% background and compare:
   - Precision, Recall
   - mAP@50 and mAP@50–95
   - **False positives per image** (the metric background tiles are meant to move)
   
   If false positives stay high, nudge the background fraction up. If recall starts dropping, pull it back down. Any number — including the 10% above — is a starting point, not a conclusion.

## References
The Ultralytics documentation was checked directly against their live docs/repository. The three papers are canonical works in the field; the arXiv IDs and DOIs below resolve directly on arxiv.org and the publisher sites.

1. **Ultralytics YOLO Documentation** — recommendation of ~0–10% background images; note that COCO contains ~1,000 background images (~1% of the dataset). Ultralytics Docs, "Tips for Best Training Results" and the Detection Datasets guide.
   <https://docs.ultralytics.com/datasets/detect/> and the model-training tips guide at <https://docs.ultralytics.com/guides/model-training-tips/>
   *(This is the direct source for the percentage question. Note it is framework/engineering guidance, not a peer-reviewed finding.)*

2. **Lin, T.-Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). "Focal Loss for Dense Object Detection" (RetinaNet).** *Proceedings of the IEEE International Conference on Computer Vision (ICCV).*
   arXiv:1708.02002 · DOI: 10.1109/ICCV.2017.324
   *Why it matters: the foundational treatment of foreground/background class imbalance in one-stage detectors — the reason negatives matter and why naive random negatives are weak.*

3. **Carion, N., Massa, F., Synnaeve, G., Usunier, N., Kirillov, A., & Zagoruyko, S. (2020). "End-to-End Object Detection with Transformers" (DETR).** *European Conference on Computer Vision (ECCV).*
   arXiv:2005.12872 · DOI: 10.1007/978-3-030-58452-8_13
   *Why it matters: defines the explicit "no-object" (∅) class in the Hungarian-matching set-prediction loss — the mechanism behind why DETR-family models like RF-DETR benefit from empty/background scenes.*

4. **Shrivastava, A., Gupta, A., & Girshick, R. (2016). "Training Region-Based Object Detectors with Online Hard Example Mining" (OHEM).** *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR).*
   arXiv:1604.03540 · DOI: 10.1109/CVPR.2016.89
   *Why it matters: the standard reference for hard-negative mining — the "run model, harvest false positives, retrain" loop described in step 2 above.*

---

### One-line takeaway for the team

> No paper sets an optimal percentage. The framework authors recommend ~0–10% (COCO is ~1%), so **~10% is a sound starting point — 20% is on the high side** — and the *quality* of the background tiles (hard negatives, diverse) matters more than the exact number. Confirm with a quick 0/5/10/20% ablation on our data.

---

## Appendix: How to run the background-percentage ablation

### What "ablation" means

To *ablate* means to remove. An ablation study is a controlled experiment where you **change one thing at a time and hold everything else fixed**, so any difference in the results can only be caused by that one thing.

The analogy: if you bake the same cake four times and only change the amount of sugar, you learn what sugar does. If you also change the oven temperature and the flour each time, you've learned nothing — you can't tell what caused the difference. Here the "one thing" is the percentage of background-only tiles; everything else stays frozen.

### Turning "10% background" into an ablation

Instead of committing to 10% on faith, train several identical models that differ *only* in their background fraction, then compare.

**Step 1 — Freeze everything except the background count.**
Build one fixed pool of positive tiles (with objects) and one fixed pool of background tiles (ideally hard negatives). Keep these identical across every run:

- the model and its pretrained weights,
- all hyperparameters (learning rate, batch size, epochs, image size, optimizer),
- the augmentation settings and the random seed,
- and — most importantly — a **fixed validation set and a fixed test set that never change**.

If anything other than the background count varies, the experiment is contaminated.

**Step 2 — Make the variants.**
Keep the positive tiles constant and vary only how many background tiles you add. If `P` is your number of positive tiles and you want background to be `X` percent of the *total* training set, the count to add is `B = P · X / (1 − X)`:

| Variant | Background % of total | Background tiles to add |
|---|---|---|
| A | 0% | 0 |
| B | 5% | ≈ 0.053 × P |
| C | 10% | ≈ 0.111 × P |
| D | 20% | 0.25 × P |

**Cleaner design — use nested subsets.** Sample the *largest* background set (the 20% one) first, then take subsets for the smaller conditions, so the 5% tiles are a subset of the 10% tiles, which are a subset of the 20% tiles. That way you change only *how many* backgrounds appear, not *which* ones — removing a hidden confound.

**Step 3 — Train each variant** (four models, A–D) with the identical setup from Step 1.

**Step 4 — Evaluate all four on the same fixed test set** and record the same metrics for each:

- Precision
- Recall
- mAP@50 and mAP@50–95
- **False positives per image** (the metric background tiles are meant to move)

**Step 5 — Read the results.**
Expected pattern: as background % rises, false positives fall and precision climbs — but push it too far and recall starts to drop (the model turns conservative because it sees relatively fewer objects). The winner is the fraction that kills false positives *without* meaningfully hurting recall. That's how you replace "10% because a mentor said so" with "10% because our data showed it."

### Two habits to build in early

- **Run each variant with 2–3 random seeds** (if compute allows) and compare the averages. A single run is noisy — a 0.5 mAP gap between two single runs can just be luck.
- **Make decisions on the validation set; touch the test set only once, at the end**, for the final reported numbers. Repeatedly tuning against the test set quietly makes the comparison meaningless.
