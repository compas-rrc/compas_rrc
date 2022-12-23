# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

* Added `to_configuration` and `to_configuration_primitive` to `compas_rrc.ExternalAxes` and `compas_rrc.RobotJoints`

### Changed

* Changed all instructions to inherit from `BaseInstruction` instead of `ROSMsg`.
* Changed `MoveGeneric` to require new interface arguments on the constructor.

### Fixed

### Deprecated

### Removed

## 1.1.0

### Added

* Prepared github actions for continuous integration
* Added compas plugin for automatic Rhino install

### Changed

### Fixed

### Deprecated

### Removed

## 1.0.0

* Initial version
