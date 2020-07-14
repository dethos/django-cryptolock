.. :changelog:

History
-------

Development
+++++++++++

* Challenges are now stored on the database. No longer expire when a new one is
  generated.
* Added initial support for DRF, TokenAuthentication only.


0.1.0 (2020-03-31)
++++++++++++++++++

* Add validation for existing addresses on the signup form
* Add rudimentary BitId support
* Renamed the base auth views to generic names

0.0.2 (2020-01-08)
++++++++++++++++++

* A default ``urls.py`` is provided by the package so can work "out-of-the-box".
* Default location for templates moved to ``django_cryptolock`` folder.
* Update quickstart guide.
* Update instructions to contribute to the project.
* Add ``DJCL`` namespace to all related settings.
* MoneroAddressBackend is now executed when more parameters are added to the
  ``authenticate`` function.

0.0.1 (2019-11-25)
++++++++++++++++++

* First release on PyPI.
