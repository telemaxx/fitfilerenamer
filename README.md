# fitfilerenamer

lezyne fit file rename tool
the LEZYNE SUPER GPS creates fit files with creazy names like:
bcfe453.fit

therefor i made this script

Major Changes From Original Version
-----------------------------------

  * New, hopefully cleaner public API with a clear division between accessible
    and internal parts. (Still unstable and partially complete.)

  * Proper documentation!
    [Available here](http://dtcooper.github.com/python-fitparse/).

  * Unit tests and example programs.

  * **(WIP)** Command line tools (eg a `.FIT` to `.CSV` converter).

  * Component fields and compressed timestamp headers now supported and not
    just an afterthought. Closes issues #6 and #7.
