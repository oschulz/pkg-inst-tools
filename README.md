Simple Software Package Install System
======================================

This is a simple software package install system based on swmod and GNU make.

Preparations
------------

Put pkg-inst-tools in your software directory, next to the software packages
you want to manage (possibly as a Git submodule).

Make a top-level `GNUmakefile` like this:

    PKG_CONFIG_DIR = packages
    include pkg-inst-tools/share/pkg-inst-tools/GNUmakefile.pkg-inst-tools

Create a directory `packages`, containing one or more package configuration
files, for example `packages/some-program.json`:

{
  "packages": [{
    "name": "some-package",
    "requires": ["some-other-package", "a-third-package"],
    "options": "--with-lib-foo"
  }]
}

The `required` and `options` fields are optional. The value of `options`
is passed on to `swmod instpkg`, internally.


Usage
-----

As pkg-inst-tools is based on swmod, you need to set your swmod install target
module:

    # swmod setinst some-module@some-version

If the packages you want to install depend on each other, you also need to load
your module so that the packages will find each other during installation:

    # swmod load some-module@some-version

Note: If your module directory does not exist yet, `swmod load` will fail. In
this case, just use

    # swmod adddeps none

to create the module directory (with an empty `swmod.deps` file). Of course you
will often need to add some actual module dependencies anyhow.

Now (in the main directory) simply run

    # make install

or, to use multiple threads, something like

    # make -j8 install

The Makefiles will ensure that the individual packages are built and
installed in the right order. All builds are run in `$TMPDIR` (defaulting to
`/tmp`), the package source directories remain unmodified.

You can also install a single package (with it's dependencies) using

    # make install-some-package
