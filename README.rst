osc2
====

osc2 is an object-oriented rewrite of the Open Build Service command line
tool osc.

osc2 was developed in a number of Google Summer of Code (GSoC) projects, and
condensed status reports were given regularly on the Open Build Service
mailing list (http://lists.opensuse.org/opensuse-buildservice/), in 2011 as
"osc code cleanup", and in 2012 as "osc2 client". Additionally more information
about osc2 can be found here http://lizards.opensuse.org/author/marcus_h/.

Primary goals
-------------

Reason why `osc2` was created is that experience with `osc` is less
than stellar. To create new improved tool we set these goals:

- provide consistent invocation and behavior for all commands
- split the code into smaller pieces so it is easier to maintain and extend
- strictly separate command line interface from the main code and code generating output; provide module  so the functionality is available for other scripts
- use reasonable return codes, return non-zero code in case of failure


Development environment
-----------------------

To setup a virtualenvironment to work on `osc2` you need to install the
dependencies from the requirements.txt file.

To install the python libraries you also need the development-packages for the
following libraries:

- libxml2 (in openSUSE: libxml2-devel)
- libxslt (in openSUSE: libxslt-devel)
- openssl (in openSUSE: libopenssl-devel)
- libcurl (in openSUSE: libcurl-devel)

Make sure to set the `PYCURL_SSL_LIBRARY` environment variable before
installing them using `pip`.

.. code:: bash

          export PYCURL_SSL_LIBRARY=openssl
          pip install -r requirements.txt

The binaries to test osc2 can be found in OBS (devel:tools:scm): https://build.opensuse.org/package/show/devel:tools:scm/osc2
