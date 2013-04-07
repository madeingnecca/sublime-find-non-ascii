import sublime
import sublime_plugin


class FindNonAsciiCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        sel = view.sel()

        match = []

        if sel[0].empty():
            match.extend(self.find(view.substr(sublime.Region(0, view.size()))))
        else:
            for region in sel:
                offset = min(region.a, region.b)
                match.extend(self.find(view.substr(region), offset))

        if match:
            sel.clear()
            for r in match:
                sel.add(r)

        # This message will follow ".. selected regions"
        sublime.status_message('({0} non-ascii chars)'.format(len(match)))

    def find(self, text, offset=0):
        regions = []

        for idx, unic in enumerate(text):
            bytes = unic.encode('UTF-8')
            if (len(bytes) > 1):
                pos = offset + idx
                # Create region for a single character.
                regions.append(sublime.Region(pos, pos + 1))

        return regions
