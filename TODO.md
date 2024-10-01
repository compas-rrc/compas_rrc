# System Interface (WebService) support

- [x] Remove "abb" hard-coded selection in compas_rrc
- [x] Add option to print/see raw result of get/set variable instructions (ie. see the "list of list" output before converting to complex types)
- [x] Decide if we keep or remove raw_data from client-level (replacement of Debug())
- [x] Rename `parse_feedback` to `on_after_receive` across the board
- [ ] Add support for more system instructions:
    - [x] Motor ON/OFF
    - [x] Get Joints
    - [ ] Get Frame/Robtarget/etc
- [ ] Test Alberto's use case from Grasshopper: PP To Main, Start, Stop, Send process code (eg. moving the robot) and in parallel we change some variables (num, speeddata, wobj) using the system interface.

- [ ] Add support for most RAPID types:
    - [ ] [PF] Add decoder/encoders to compas_rrc.compas_types
    - [ ] Add __str__ pretty prints for LoadData and other types with additional info
- [ ] Update documentation
- [ ] Releaseeeeee! 🚀
    - [ ] Create new docker image (compsa-rrc)
    - [ ] Create new docker image for moveit/dfab noetic
- [ ] Fix tests for RAPID lex parser (move to compas_rrc_ros)
