# erratacheck

The program in this repository was written to check for OpenBSD errata
and print out any errata added since the previous run.  It should
typically be run from cron so that the output would be emailed to the
user or system administrator.  It could be used as an alternative to
subscribing to the
[OpenBSD announce email list](https://www.openbsd.org/mail.html).

## Prerequisites

`erratacheck` requires [Python 3](https://www.python.org/).  Most
modern operating systems come with Python 3, either as part of the
default install or a separate package.  See your operating system
instructions for how to install it.

## Installation

Installation of `erratacheck` is very simple.  Copy `erratacheck.py`
to some location where you can easily run it.  (I put it in my
personal `bin` directory and remove the `.py` suffix.)  Make sure it
is executable with something like `chmod +x /path/to/erratacheck`.
Finally, put the `erratacheck.ini` file in your home directory.  You
should now be able to run the program.

## Configuration

### erratacheck.ini

The configuration file for the program is very simple.  It contains a
single section, Errata, with three options: url, sequence, and
unixstamp.  These are each described in the following subsections.

#### url

The url setting is the URL for the errata page of your current OpenBSD
release.  You will want to change it as appropriate when you upgrade
OpenBSD.

#### sequence

The sequence setting stores the number of the last patch seen by the
program.  You will want to set this to 0 when/if you ever change the
url setting.  Otherwise, you will not want to touch it.

#### unixstamp

This is a timestamp of the last time that the program was run.  You
will never need to change it.

### crontab

If your account is permitted to schedule programs via `cron` or some
other service, then you should add an entry to run `erratacheck` on
some basis.  Daily or weekly work well depending upon how often you
wish to check for updates.

This is what my `crontab` entry looks like.  It runs the program every
day at 5:00 a.m.:

```
0 5 * * * /home/jason/bin/erratacheck
```

## Author

**Jason Stephenson** - [Sigio](http://www.sigio.com/)

## License

The program is licensed under the [GNU General Public License, Version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html), or (at your option) any later version.
