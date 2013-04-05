import sublime
import sublime_plugin


class FindNonAsciiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sel = view.sel()
        regions = [r for r in sel]
        is_empty = sel[0].empty()

        sel.clear()

        if is_empty:
            self.find(view.substr(sublime.Region(0, view.size())))
        else:
            for region in regions:
                offset = min(region.a, region.b)
                self.find(view.substr(region), offset)

    def find(self, text, offset=0):
        for idx, unic in enumerate(text):
            bytes = unic.encode('UTF-8')
            if (len(bytes) > 1):
                pos = offset + idx
                self.view.sel().add(sublime.Region(pos, pos + 1))
