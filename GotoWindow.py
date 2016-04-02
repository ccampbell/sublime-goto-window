import os
import sublime
import sublime_plugin
from subprocess import Popen, PIPE


class GotoWindowCommand(sublime_plugin.WindowCommand):
    def run(self):
        folders = self._get_folders()

        folders_alone = [x for (x, y) in folders]
        folders_for_list = []
        for folder in folders_alone:
            folders_for_list.append([os.path.basename(folder), folder])

        self.window.show_quick_panel(folders_for_list, self.on_done, 0)

    def on_done(self, selected_index):
        current_index = self._get_current_index()
        if selected_index == -1 or current_index == selected_index:
            return

        folders = self._get_folders()
        window_index = folders[selected_index][1]
        window_to_move_to = sublime.windows()[window_index]

        self.focus(window_to_move_to)

        # OS X and Linux require specific workarounds to activate a window
        # due to this bug:
        # https://github.com/SublimeTextIssues/Core/issues/444
        if sublime.platform() == 'osx':
            self._osx_focus()
        elif sublime.platform() == 'linux':
            self._linux_focus(window_to_move_to)

    def focus(self, window_to_move_to):
        active_view = window_to_move_to.active_view()
        active_group = window_to_move_to.active_group()

        # In Sublime Text 2 if a folder has no open files in it the active view
        # will return None. This tries to use the actives view and falls back
        # to using the active group

        # Calling focus then the command then focus again is needed to make this
        # work on Windows
        if active_view is not None:
            window_to_move_to.focus_view(active_view)
            window_to_move_to.run_command('focus_neighboring_group')
            window_to_move_to.focus_view(active_view)
            return

        if active_group is not None:
            window_to_move_to.focus_group(active_group)
            window_to_move_to.run_command('focus_neighboring_group')
            window_to_move_to.focus_group(active_group)

    def _osx_focus(self):
        name = 'Sublime Text'
        if int(sublime.version()) < 3000:
            name = 'Sublime Text 2'

        # This is some magic. I spent many many hours trying to find a
        # workaround for the Sublime Text bug. I found a bunch of ugly
        # solutions, but this was the simplest one I could figure out.
        #
        # Basically you have to activate an application that is not Sublime
        # then wait and then activate sublime. I picked "Dock" because it
        # is always running in the background so it won't screw up your
        # command+tab order. The delay of 1/60 of a second is the minimum
        # supported by Applescript.
        cmd = """
            tell application "System Events"
                activate application "Dock"
                delay 1/60
                activate application "%s"
            end tell""" % name

        Popen(['/usr/bin/osascript', "-e", cmd], stdout=PIPE, stderr=PIPE)

    # Focus a Sublime window using wmctrl. wmctrl takes the title of the window
    # that will be focused, or part of it.
    def _linux_focus(self, window_to_move_to):
        window_variables = window_to_move_to.extract_variables()

        if 'project_base_name' in window_variables:
            window_title = window_variables['project_base_name']
        elif 'folder' in window_variables:
            window_title = os.path.basename(window_variables['folder'])

        try:
            Popen(["wmctrl", "-a", window_title + ") - Sublime Text"],
                    stdout=PIPE, stderr=PIPE)
        except FileNotFoundError:
            msg = "`wmctrl` is required by GotoWindow but was not found on " \
                  "your system. Please install it and try again."
            sublime.error_message(msg)


    def _get_current_index(self):
        active_window = sublime.active_window()
        windows = sublime.windows()
        current_index = -1
        for i, folder in enumerate(self._get_folders()):
            if windows[folder[1]] == active_window:
                current_index = i
                break

        return current_index

    def _get_folders(self):
        folders = []
        home = os.getenv('HOME')
        for i, window in enumerate(sublime.windows()):
            for folder in window.folders():
                if folder.startswith(home):
                    folder = folder.replace(home, '~')

                folders.append((folder, i))

        return sorted(folders)
