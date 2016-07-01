import gi
gi.require_version ('Astroid', '0.1')
gi.require_version ('Gtk', '3.0')
gi.require_version ('WebKit', '3.0')
from gi.repository import GObject, Gtk, Astroid, WebKit

import os, os.path
import sys
import json
import colorsys
import struct
from hashlib import md5

print ("hls-hsv-tag-color: plugin loading..")

class HlsHsvTagColorPlugin (GObject.Object):
  json          = {}
  colorspace    = 'hls'
  saturation    = .5
  lightness     = .5 # hsl
  value         = .5 # hsv
  alpha         = .5

  def do_activate (self):
    self.config = os.getenv ('ASTROID_CONFIG')

    if self.config is not None and os.path.exists (self.config):
      with open (self.config, 'r') as cf:
        self.json = json.load(cf)

    # add configuration options:
    # plugins.hls_hsv_tag_color.colorspace = { 'hls', 'hsv' }
    # plugins.hls_hsv_tag_color.saturation
    # plugins.hls_hsv_tag_color.lightness
    # plugins.hls_hsv_tag_color.value
    # plugins.hls_hsv_tag_color.alpha

    self.plugin_config = self.json.get ('plugins', None)
    if self.plugin_config is not None:
      self.plugin_config = self.plugin_config.get ('hls_hsv_tag_color', None)

    if self.plugin_config is not None:
      self.colorspace = self.plugin_config.get ('colorspace', 'hls')
      self.saturation = self.plugin_config.get ('saturation', .5)
      self.lightness  = self.plugin_config.get ('lightness', .5)
      self.alpha      = self.plugin_config.get ('alpha', .5)

    print ('hls-tag-color: activate, colorspace:', self.colorspace)

  def do_deactivate (self):
    print ('hls-hsv-tag-color: deactivate')

  def do_format_tags (self, bg, tags, selected):
    newtags = []

    # vary hue based on tag md5: saturation and value remain constant.
    for t in tags:
      m = md5 (t.encode('ascii', 'replace')).hexdigest()[-6:]
      m = int (m, 16)

      hue = m / 0xffffff * 1.0

      if self.colorspace == 'hls':
        (r, g, b) = colorsys.hls_to_rgb (hue, self.saturation, self.lightness)
      else:
        (r, g, b) = colorsys.hsv_to_rgb (hue, self.saturation, self.value)

      r = int(r * 255)
      g = int(g * 255)
      b = int(b * 255)
      a = int(self.alpha * 255)

      tc = (r, g, b, a)

      # parse bg color
      (rb, gb, bb) = struct.unpack ('BBB', bytes.fromhex(bg[1:7]))

      # luminocity
      lum = ((self.alpha * r + (1-self.alpha) * rb) * .2126 +
             (self.alpha * g + (1-self.alpha) * gb) * .7152 +
             (self.alpha * b + (1-self.alpha) * bb)  * .0722) / 255.0;

      if lum > 0.5:
        fc = "#000000"
      else:
        fc = "#ffffff"

      newtags.append ((tc, fc, t))

    return newtags

class HlsHsvTagColorIndexPlugin (HlsHsvTagColorPlugin, Astroid.ThreadIndexActivatable):
  thread_index  = GObject.property (type = Gtk.Box)

  def do_activate (self):
    HlsHsvTagColorPlugin.do_activate (self)

  def do_deactivate (self):
    HlsHsvTagColorPlugin.do_deactivate (self)

  def do_format_tags (self, bg, tags, selected):
    tags = HlsHsvTagColorPlugin.do_format_tags (self, bg, tags, selected)

    return "<span size=\"xx-small\"> </span>".join(["<span bgcolor=\"%s\" color=\"%s\"> %s </span>" % (("#%02x%02x%02x%02x" % tc), fc, t) for tc, fc, t in tags])


class HlsHsvTagColorViewPlugin (HlsHsvTagColorPlugin, Astroid.ThreadViewActivatable):
  object = GObject.property (type = GObject.Object)
  thread_view = GObject.property (type = Gtk.Box)
  web_view = GObject.property (type = WebKit.WebView)

  def do_activate (self):
    HlsHsvTagColorPlugin.do_activate (self)

  def do_deactivate (self):
    HlsHsvTagColorPlugin.do_deactivate (self)

  def do_format_tags (self, bg, tags, selected):
    tags = HlsHsvTagColorPlugin.do_format_tags (self, bg, tags, selected)

    def f(tags):
      for t in tags:
        tc, fc, ts = t
        r, g, b, a = tc
        a = a / 255
        yield "<span style=\"background-color: rgba(%d, %d, %d, %.2f); color: %s !important; white-space: pre;\" > %s </span>" % (r, g, b, a, fc, ts)

    return " ".join(f(tags))

