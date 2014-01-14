=======================
GitLab webhooks handler
=======================

This is simple server (receiver) for `GitLab's <http://gitlab.org/>`_ webhooks feature.

Installation
------------

Make sure you have `Python <http://www.python.org/>`_ 2.6+/3.2+ properly installed (`Windows <http://docs.python-guide.org/en/latest/starting/install/win/>`_/`Linux <http://docs.python-guide.org/en/latest/starting/install/linux/>`_). Then just type ``[sudo] pip install glhooks`` in your favorite shell. Now you have *glhooks* installed so you can run it like this ``python -m glhooks <path_to_config_file>...``. You can find skeleton for the configuration file in `git repository <https://github.com/miso-belica/gitlab-webhooks>`_ in ``config/config.ini``.

I recommend `Supervisor <http://supervisord.org/>`_ or similar application to run the *glhooks* server. Install it via ``[sudo] apt-get install supervisor``. You can find the example of *Supervisor* configuration file for *glhooks* in `git repository <https://github.com/miso-belica/gitlab-webhooks>`_ in ``config/glhooks.conf``. But you can just create some shell script and copy it into ``/etc/init.d/`` (example in `git repository <https://github.com/miso-belica/gitlab-webhooks>`_ in ``config/glhooks.sh``).

Next step is to generate a SSH key **without the passphrase**: ``ssh-keygen -b 4096 -t rsa``. Then add the generated SSH **public key** to your GitLab account. If you have multiple SSH keys in ``$HOME/.ssh/`` you probably has to create file ``$HOME/.ssh/config``. You can find the example file in `git repository <https://github.com/miso-belica/gitlab-webhooks>`_ in ``config/config.ssh``.

Finally add the hook ``http://server.example.com:8000/`` into your project webhooks at GitLab.


Updating
--------

When you change at least one of the configuration files you has to restart *glhooks* server by ``[sudo] supervisorctl restart glhooks`` or ``[sudo] service glhooks restart``.


Contributing
------------
Feel free to `send a pull request <https://github.com/miso-belica/gitlab-webhooks/pulls>`_ or to `report an issue <https://github.com/miso-belica/gitlab-webhooks/issues>`_.
