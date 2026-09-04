# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

* Bumped minimum supported Python version to 3.9.

### Removed

* Removed support for IronPython 2.7. The library now requires CPython 3.9 or newer.
* Removed the `compas_rrc.__install` plugin used by `python -m compas_rhino.install`. Install into Rhino 8 with `pip` instead.


## [2.0.0] 2024-03-28

### Added

* Added `to_configuration` and `to_configuration_primitive` to `compas_rrc.ExternalAxes` and `compas_rrc.RobotJoints`

### Changed

* Update minimum requirements to `compas_fab > 1.x` and `compas > 2.x`

### Removed

## 1.1.0

### Added

* Prepared github actions for continuous integration
* Added compas plugin for automatic Rhino install

## 1.0.0

* Initial version
