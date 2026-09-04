# Main concepts

The API of `COMPAS RRC` is minimal and very easy to understand.

## Communication methods

The primary way to interact with robots is using the client classes. They allow
four different ways of communication:

* **Send**: The method [`AbbClient.send`][compas_rrc.AbbClient.send] allows
  streaming commands without blocking or waiting for feedback.
* **Send & Wait**: The method
  [`AbbClient.send_and_wait`][compas_rrc.AbbClient.send_and_wait] sends an
  instruction and waits for feedback from the robot.
* **Send & Wait in the future**: Using the return value of the method
  [`AbbClient.send`][compas_rrc.AbbClient.send] allows to defer the waiting to a
  future point in time.
* **Send & Subscribe**: The method
  [`AbbClient.send_and_subscribe`][compas_rrc.AbbClient.send_and_subscribe] can
  activate a streaming service on the robot that will stream feedback at a
  regular interval.

The corresponding classes are documented in [Clients](api/clients.md).

## Transports

`COMPAS RRC` does not talk to ROS directly. Instructions are
[`compas_eve`](https://compas.dev/compas_eve) messages, and
[`AbbClient`][compas_rrc.AbbClient] publishes them over a `compas_eve`
*transport*. ROS is the transport used in practice, but it is not the only one
the client can use.

=== "ROS"

    ```python
    import compas_rrc as rrc

    ros = rrc.RosClient()
    ros.run()

    abb = rrc.AbbClient(ros, '/rob1')
    ```

=== "MQTT"

    ```python
    import compas_rrc as rrc
    from compas_eve.mqtt import MqttTransport

    transport = MqttTransport('broker.example.com')

    abb = rrc.AbbClient(transport, '/rob1')
    ```

!!! note

    Choosing a transport on the Python side only settles one half of the
    connection. The driver on the other end has to speak the same one, and
    `compas_rrc_driver` is a ROS node.

[`RosClient`][compas_rrc.RosClient] is a `compas_eve` ROS transport that also
exposes the `roslibpy` methods RRC scripts have always called, so existing code
keeps working unchanged.

## Robot joints and external axes

The following example shows how to retrieve, update and send the robot joints
and external axes:

```python
# Get joints
robot_joints, external_axes = abb.send_and_wait(rrc.GetJoints())

# Print received values
print(robot_joints, external_axes)

# Change any value and move to new position
robot_joints.rax_1 += 15
done = abb.send_and_wait(rrc.MoveToJoints(robot_joints, external_axes, 100, rrc.Zone.FINE))
```

### ::: compas_rrc.RobotJoints

### ::: compas_rrc.ExternalAxes

## Debugging instructions

Wrapping any instruction in a [`Debug`][compas_rrc.Debug] allows to get raw
access to the output values:

```python
# Get joints
raw_debug_output = abb.send_and_wait(rrc.Debug(rrc.GetJoints()))

# Print received values
print(raw_debug_output)
```

### ::: compas_rrc.Debug
