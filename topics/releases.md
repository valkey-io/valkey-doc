---
title: "Valkey releases and versioning"
linkTitle: "Valkey releases"
weight: 4
description: How new versions of Valkey released and supported
aliases:
    - /topics/releases
---

Valkey is usually among the most critical pieces of a software stack.
For this reason, Valkey's release cycle prioritizes highly stable releases at the cost of slower release cycles.

All Valkey releases are published in the [Valkey GitHub repository](https://github.com/valkey-io/valkey/releases).

## Versioning

Valkey stable releases will follow generally `major.minor.patch` [semantic versioning schema](https://semver.org/).
We follow semantic versioning to provide explicit guarantees regarding backward compatibility.

### Patch versions

PATCH versions are released with backwards compatible bug fixes and should not introduce new features.

Upgrading from a previous patch version should be safe and seamless.
It should be safe to run a Valkey cluster with servers running on different patch versions.

PATCH versions may also introduce small improvements such as performance or memory optimizations that don't come with any tradeoffs.

### Minor versions

MINOR version are released with new functionality that is added in a backward compatible manner.
Examples of new functionality include new commands, info fields, or configuration parameters.

Upgrading from a previous minor version should be safe, and will not introduce incompatibilities between servers in the cluster.

**NOTE:** Minor releases may include new commands and data types that can introduce incompatibility between servers in the cluster, but users need to opt-in to these features to cause this type of incompatibility.
For this reason, it is not recommended to run a Valkey cluster with servers running on different minor versions.
Users should also avoid new features until all servers in the cluster have been upgrades.

Commands may also be deprecated in minor versions.
If a command is deprecated, a replacement command or an alternative to using the command will be defined in the same minor version.

### Major versions

MAJOR versions are released with significant functionality that may break backwards compatibility or alter key performance characteristics.
Examples of significant functionality include altering the behavior of an existing command, removing previously deprecated commands, changing the default value of configs, and significant refactoring for performance improvements.

Upgrading from a previous major version is intended to be safe, but should be approached with caution. 
You should carefully read the release notes before performing a major version upgrade.
Major version upgrades do not guarantee backwards compatibility, which means you should always upgrade replicas before upgrading primaries in order to ensure data consistency.

The Valkey community strives to make as few backwards breaking changes as possible.
When breaking changes are required, we will also strive to provide a way to mitigate the impact without incuring downtime to your application.

## Release schedule

The Valkey community strives to release a stable major version once a year.
Stable minor versions are created as needed in between major releases, and we aim to release at least one minor version a year.

### Release candidate

New minor and major versions of Valkey begin by branching off the `unstable` branch as an initial release candidate branch, which take the form *major.minor.patch-R#*.
The first release candidate, or RC1, is released once it can be used for development purposes and for testing the new version.
At this stage, most of the new features and changes in the new version are ready for review, and the version is released for the purpose of collecting the public's feedback.
Subsequent release candidates are released every coupe of weeks, primarily for fixing bugs and refining features based off of user input.

### Stable release

Once development has ended and the feedback for release candidate slows down, it is ready for the final release. 
At this point, the release is marked as stable and is released with "0" as its patch-level version.

Patches are released as needed to fix high-urgency issues, or once a stable version accumulates enough fixes to justify it.

## Support

The latest stable release is always fully supported and maintained.

The Valkey community will provide maintanence support, providing patch releases for bug fixes and all security fixes, for 3 years from when a version was first released.

The Valkey community will also provide extended security security support for the latest minor version of each major version for 5 years from when a version was first released.
The Valkey community will only backport security issues we believe to be possible to exploit, which will be up to the discretion of the TSC.

For contacting the core team on sensitive matters and security issues, please see [SECURITY.md](https://github.com/valkey-io/valkey/blob/unstable/SECURITY.md).

### List of supported versions

| Version | Initial release | Maintenence support end | Extended Security support end |
| -- | -- | -- | -- |
| 7.2 | 2024-04-16 | 2027-04-16 | 2029-04-16 |

## Unstable tree

The unstable development tree of Valkey is located in the `unstable` branch in the [Valkey GitHub repository](https://github.com/valkey-io/valkey).

This branch is the source tree where most of the new features are under development.
`unstable` is not considered production-ready: it may contain critical bugs, incomplete features, and is potentially unstable.

However, we try hard to make sure that even the unstable branch is usable most of the time in a development environment without significant issues.