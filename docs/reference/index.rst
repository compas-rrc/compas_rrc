Getting started
===============

``COMPAS RRC`` provides an easy-to-use API to operate robots.
The system relies on 3 components: this library, a ROS RRC driver and
a vendor-specific RRC driver running on the robot controller.

A typical deployment of RRC uses Docker to simplify the setup:

.. image:: ../../images/overview-diagram.png
   :class: img-fluid mb-3

For more details, check the `RRC course repository <https://github.com/compas-rrc/compas_rrc_course>`_.

Hello World
-----------

.. code-block:: python

    import compas_rrc as rrc

    ros = rrc.RosClient()
    ros.run()

    abb = rrc.AbbClient(ros, '/rob1')
    print('Connected.')

    abb.send_and_wait(rrc.PrintText('Welcome to COMPAS_RRC'))

    ros.close()


API Reference
-------------

.. toctree::
   :maxdepth: 2

   concepts
   instructions
   custom_instructions
