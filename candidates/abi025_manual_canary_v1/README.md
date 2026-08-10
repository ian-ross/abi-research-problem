# ABI-025 manual canary

This manually authored Candidate Experiment is a minimal, legitimate test of the ABI Candidate Execution lifecycle. It defines only a small PyTorch model architecture. The trusted provider and Harness retain ownership of data loading, splits, sampling, augmentation, loss, optimization, metrics, Artifact Filters, Baseline Segmenters, execution, and research records.

The canary consumes only the provider-declared `abi_16ch` tensor. Longitude and latitude are not Candidate Experiment inputs. Scientific performance is not the success criterion; complete, reviewable lifecycle evidence is.
