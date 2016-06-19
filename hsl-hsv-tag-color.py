import gi
gi.require_version ('Astroid', '0.1')
gi.require_version ('Gtk', '3.0')
from gi.repository import GObject, Gtk, Astroid

import os, os.path
import sys
import json
import colorsys
from hashlib import md5

print ("hsl-tag-color: plugin loading..")

class HslTagColorPlugin (GObject.Object, Astroid.ThreadIndexActivatable):
  thread_index  = GObject.property (type = Gtk.Box)

  json          = {}
  saturation    = .5
  lightness     = .5

  def do_activate (self):
    print ('hsl-tag-color: activate')
    self.config = os.getenv ('ASTROID_CONFIG')

    if self.config is not None and os.path.exists (self.config):
      with open (self.config, 'r') as cf:
        self.json = json.load(cf)

    # add configuration options:
    # plugins.hsv_tag_color.saturation
    # plugins.hsv_tag_color.value

    self.plugin_config = self.json.get ('plugins', None)
    if self.plugin_config is not None:
      self.plugin_config = self.plugin_config.get ('hsv_tag_color', None)

    if self.plugin_config is not None:
      self.saturation = self.plugin_config.get ('saturation', .5)
      self.lightness  = self.plugin_config.get ('lightness', .5)

  def do_deactivate (self):
    print ('hsv-tag-color: deactivate')

  def do_format_tags (self, tags):
    newtags = []

    # vary hue based on tag md5: saturation and value remain constant.
    for t in tags:
      m = md5 (t.encode('ascii', 'replace')).hexdigest()[-6:]
      m = int (m, 16)

      hue = m / 0xffffff * 1.0

      (r, g, b) = colorsys.hsv_to_rgb (hue, self.saturation, self.value)

      r = int(r * 255)
      g = int(g * 255)
      b = int(b * 255)

      tc = "#%02x%02x%02x" % (r, g, b)

      # luminocity
      lum = (r * .2126 + g * .7152 + b * .0722) / 255.0;

      if lum > 0.5:
        fc = "#000000"
      else:
        fc = "#ffffff"

      ts = "<span bgcolor=\"%s\" color=\"%s\"> %s </span>" % (tc, fc, t)

      newtags.append (ts)

    return "<span size=\"xx-small\"> </span>".join (newtags)

