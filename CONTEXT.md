# GOES ABI Contrail Segmentation

This context defines the language for a research problem exploring machine learning methods for contrail segmentation in GOES ABI imagery.

## Language

**Contrail Mask**:
A binary per-pixel mask where a pixel is positive if any contrail is present and negative otherwise. It collapses any overlapping or instance-specific contrail labels into a single contrail/not-contrail target.
_Avoid_: Detection mask, instance mask, operational detection

**GOES ABI Contrail Segmentation**:
The research task of predicting a Contrail Mask from GOES ABI imagery.
_Avoid_: Contrail detection, instance segmentation, MCAST detection

**ABI Patch**:
A fixed-size spatial tile from GOES ABI imagery with matching Contrail Mask pixels. In this research problem, ABI Patch refers to the common sample unit used for both native Google tiles and windows extracted from MIT scenes.
_Avoid_: Scene, chip, crop, tile

**Dataset Source**:
The provenance category of an ABI Patch, either MIT or Google, reflecting that the datasets address the same task but were collected with different methodologies and may differ observably.
_Avoid_: Domain, corpus, data flavor

**Leakage-Safe Split**:
A train/validation split where related ABI Patches from the same scene or source-time provenance do not cross split boundaries. For this research problem, Google's original train/validation provenance is respected and MIT patches are split only by whole scene.
_Avoid_: Random patch split, naive split

**Source-Balanced Sampling**:
A sampling approach where Dataset Sources contribute ABI Patches according to an explicit mixture rather than raw available sample counts. It may be combined with explicit preference for Contrail Mask-positive patches to avoid training distributions dominated by empty background.
_Avoid_: Raw concatenation, natural sampling

**ABI Channel Input**:
Model input drawn from GOES ABI channels, excluding longitude and latitude. Spatial coordinates are not model inputs in this research problem because they encourage route-location priors rather than transferable contrail features.
_Avoid_: MCAST input, raw scene input, geographic input

**Full ABI Channel Input**:
An ABI Channel Input containing GOES ABI channels 1 through 16.
_Avoid_: 19-channel input, all-channel input

**Reflective ABI Input**:
An ABI Channel Input containing GOES ABI channels 1 through 6, whose values are reflectance factors in the training data.
_Avoid_: Visible input, daytime input

**Thermal ABI Input**:
An ABI Channel Input containing GOES ABI channels 7 through 16, whose values are brightness temperatures in the training data.
_Avoid_: Emissive input, infrared input

**Solar Geometry Input**:
Solar zenith angle used as an optional non-ABI-channel input describing illumination geometry.
_Avoid_: SZA channel, solar input

**Learned Channel Mixer**:
A model front-end that learns useful combinations of ABI channels, such as channel reductions or brightness-temperature differences, rather than relying only on fixed hand-engineered composites.
_Avoid_: MCAST features, ash composite

**Baseline Segmenter**:
An existing contrail segmentation model evaluated against the Contrail Mask using the same segmentation metrics as candidate models.
_Avoid_: Operational detector, reference detector

**Artifact Filter**:
Deterministic postprocessing that removes predicted structures known not to be contrails from a predicted Contrail Mask.
_Avoid_: Model correction, label cleanup

**Geographic Feature Filter**:
An Artifact Filter for static geographic structures such as coastlines and rivers that can be mistaken for contrails.
_Avoid_: Static mask, land mask

**Scanline Artifact Filter**:
An Artifact Filter for long, approximately constant ABI-y structures associated with instrument scan artifacts.
_Avoid_: Instrument correction, stripe removal

**Filtered Contrail Mask**:
A predicted Contrail Mask after Artifact Filters have been applied.
_Avoid_: Cleaned detection, postprocessed detection

**Contrail Connectivity Metric**:
A metric that evaluates whether predicted contrail structures remain continuous along their thin linear extent, rather than only measuring area overlap.
_Avoid_: Shape metric, topology score
