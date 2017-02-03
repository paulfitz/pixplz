pixplz
======

```
$ pixplz koala
5 images downloaded (1 duds skipped)
$ ls
koala_000000.jpg  koala_000002.jpg  koala_000004.jpg
koala_000001.jpg  koala_000003.jpg
$ pixplz -h
usage: pixplz [-h] [--prefix PREFIX] [--format FORMAT] [--count COUNT]
              term [term ...]

positional arguments:
  term             search term

optional arguments:
  -h, --help       show this help message and exit
  --prefix PREFIX  prefix for downloaded images, _NNNNNN.jpg will be added
  --format FORMAT  format for naming images, for example 'foo/bar%06d.png'
  --count COUNT    target number of images to load (fewer may be loaded)
```

Grabs a few images from ddg to use as casual training data.
After poking around for terms of service, I still don't
know how ddg feels about this.  Will switch to other sources
of public image data if needed.
