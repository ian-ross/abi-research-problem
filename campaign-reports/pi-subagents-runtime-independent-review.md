# Pi-subagents runtime independent review

## Conclusion

A fresh-context read-only review found no blocker. The diagnosis, package-manager repair, and smoke evidence addressed the delegated-agent runtime failure without changing scientific policy or launching training.

## Verified evidence

- **Root cause:** The preserved pre-repair runner failure reports `MODULE_NOT_FOUND` for `typebox/compile`, originating from `pi-subagents/src/runs/shared/structured-output.ts`. The affected installation used a package release whose detached runner depended on an optional TypeBox peer.
- **Package-manager-owned repair:** The managed root manifest and lockfile record `pi-subagents` and its production TypeBox dependency with registry integrity metadata. TypeBox exports `./compile` to its built module. The repair does not rely on `NODE_PATH`, symlinks, or a patched package file.
- **Structured-output validation:** Run `feae7b2d-5175-4229-9029-2c0def79d988` completed a schema-bound delegate step with exit code 0 and the required structured success object.
- **Ordinary delegation:** A new parent process loaded the repaired package and launched a fresh ordinary `delegate` child successfully.
- **Fresh-context path:** This independent reviewer launched successfully and completed read-only inspection, providing additional evidence that ordinary fresh-context delegation works.
- **Scientific scope:** No Candidate Run, training, provider policy, or research configuration changed as part of the repair.

## Review limit

The review inspected the installed package metadata, preserved failure evidence, lockfile, and completed smoke artifacts. It did not launch scientific work.
