import gi
gi.require_version ('Astroid', '0.1')
gi.require_version ('Gtk', '3.0')
from gi.repository import GObject, Gtk, Astroid

print ("hsv-tag-color: plugin loading..")

class HsvTagColorPlugin (GObject.Object, Astroid.ThreadIndexActivatable):
  thread_index  = GObject.property (type = Gtk.Box)

  def do_activate (self):
    print ('hsv-tag-color: activate')

  def do_deactivate (self):
    print ('hsv-tag-color: deactivate')

  def do_format_tags (self, tags):
    print ("got tags: ", tags)

    return ", ".join (tags)

