import collections
import reaper.preset as rp

class vstipreset():
    def __init__(self, preset_name = "", chunk = None, tags = []) -> None:
        self.preset_name = preset_name
        self.type = "VSTi Preset"
        self.chunk = chunk
        self.tags = tags

    @property
    def properties(self):
        props = collections.OrderedDict()
        props["Preset Name"] = self.preset_name
        props["Type"] = self.type
        props["Plugin Name"] = self.chunk.plugin_name
        props["Tags"] = self.tags
        return props

    def check_filter(self, filter):
        show_name = filter in self.preset_name
        show_plugin = filter in self.chunk.plugin_name
        show_tags = filter in self.tags
        show = show_name or show_tags or show_plugin
        return show

    def load(self):
        rp.load(self.chunk)

    def save(self):
        pass

    def onclick(self):
        pass

    def ondoubleclick(self):
        pass


