HSV tag color plugin
====================

Intro
-----

This plugins generates tag colors based on the [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV) colorspace. The parameters `saturation` and `value` are configurable, while `hue` is generated from the MD5 sum of the tag.

Installation
------------

the installation is as simple as:

```sh
mkdir -p ~/.config/astroid/plugins/
cd ~/.config/astroid/plugins/
git clone https://github.com/astroidmail/astroid-plugin-hsv-tagcolor
```
...and restart astroid.

Configuration
-------------

You can set the configuration options (in the astroid config: `~/.config/astroid/config`):
```
    "plugins": {
      "hsv_tag_color": {
        "saturation" : 0.5,
        "value" : 0.5 
      }
    }
```

Licensing
---------

GPLv3 or later.

