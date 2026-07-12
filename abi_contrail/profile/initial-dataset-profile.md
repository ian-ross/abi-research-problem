# Initial ABI dataset profile placeholder

ABI-001 only scaffolds the Research Problem provider. Durable dataset profiling is added by a later backlog task after provider-owned ABI Patch dataset loading and leakage-safe splits exist.

Known intended Dataset Sources:

- MIT full-scene GOES ABI data, later windowed into ABI Patches.
- Google 256 x 256 GOES ABI contrail patches.

Labels will be collapsed to a binary Contrail Mask with `labels != 0` in trusted provider code.
