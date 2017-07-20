DG2R Update daemon
==================

This script is called everytime there's an USB key plugged in the device. If there's an ``UPDATE.dg2r`` file in it, then
it'll read it, extract it and configure the Armadillo.

:Developer: Yohann Bacha
:Version: 0.1rc1 of 2017-07-18

How to set it up ?
==================
The trigger
-----------

This application isn't a daemon strictly speaking, but is triggered by a service waiting for the mount of a removable
usb device called ``DG2R``.

Thanks to the ``automount``, when the DG2R drive will be mounted, it will start a bash script verifying if the
environment's ready as the specified user. The user MUST be the one logged in, or else the application won't show up.

Of course, this systemd config file should be placed under ``/etc/systemd/system/dg2rupdate.service``.

.. code-block:: yaml

    [Unit]
    Description=Agent de mise à jour DG2R
    Requires=media-<user>-DG2R.mount
    After=media-<user>-DG2R.mount

    [Service]
    Environment=XAUTHORITY=/home/<user>/.Xauthority
    Environment=DISPLAY=:0
    User=<user>
    ExecStart=/usr/local/bin/scan_for_update.sh /media/<user>/DG2R

    [Install]
    WantedBy=media-<user>-DG2R.mount

The auto-mounted key will always be located under ``/media/<user>``, where ``<user>`` is the name of the currently
logged user on the Armadillo.

To enable this new service, and permit him to be triggered on a USB key called DG2R, type the following command
with root privileges :

.. code-block:: bash

    systemctl enable dg2rupdate

You can check if the service is well enabled by typing this :

.. code-block:: bash

    service dg2rupdate status

The launcher
------------

The bash script launching the updater, itself launched by the previous service, is preferably located in
``/usr/local/bin/scan_for_update.sh``. Don't forget to make it executable with ``chmod +x scan_for_update.sh``.

It takes a parameter : the mounted key location. After verifying if a ``UPDATE.dg2r`` exist on it, we finally launch the
updater, which must have been previously installed.

The updater
-----------

This is the biggest piece : the updater. In order to install it, you must have Python 3.5 minimum installed.

If you don't have Python 3.5 on your Armadillo / Raspberry Pi or newer, here's the procedure to install it

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev
    $ wget https://www.python.org/ftp/python/3.5.3/Python-3.5.3.tgz
    $ tar xzvf Python-3.6.0.tgz
    $ cd Python-3.6.0/
    $ ./configure
    $ make
    $ sudo make install

When it's done, you should launch the updater's install :

.. code-block:: bash

    sudo update
    sudo apt-get install libjpeg-dev
    sudo python setup.py install

Once it's finished, you could launch ``dg2r_update_daemon <MOUNTED_PATH>`` from anywhere.
