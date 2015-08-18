# Sublime Goto Window

This package allows you to change between open windows in Sublime Text using a
prompt. It is useful if you have a lot of windows open with different projects
in them and you want to switch without having to press `command ~` over and over again.

## To Install

If you are using Sublime Package Control you can press ``command+shift+p``.  Then select ``Package Control: Install Package`` and choose ``Goto Window``.

Another option is running the following command (this is the OS X version):

```
cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
git clone git@github.com:ccampbell/sublime-goto-window.git GotoWindow
```

## Usage

The default keybinding is

```
super + shift + o
```

After that you will see a menu that looks like this containing all your open
windows in Sublime Text:

![hyog](https://cloud.githubusercontent.com/assets/259316/9324668/72ee20e8-455a-11e5-9f0d-9b89d19764ea.png)

Select an item and that's it!

## Note

There is a bug that prevents this from actually working natively using Sublime
Text.  See https://github.com/SublimeTextIssues/Core/issues/444 for more
information.

I haven't been able to test it on Windows, but I put in a workaround that seems
to work on OS X.
