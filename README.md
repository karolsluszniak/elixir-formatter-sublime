# Elixir Formatter for Sublime Text

**Sublime Text plugin for integration with the official Elixir Formatter.**

Features:

- detects if you're editing an Elixir file (by extension or current syntax) and invokes the [mix
  format] task upon saving it
- detects the root directory of a Mix project and invokes the task from it to respect the project's
  formatting rules
- respects the `:inputs` key in `.formatter.exs` file by skipping files that are excluded by defined
  patterns
- formats Elixir files even when they're not in a Mix project or when the `.formatter.exs` file is
  missing
- reports `mix format` errors to the Sublime Text console for troubleshooting
- works out of the box without extra configuration

## Installation

Please use [Package Control] to install the linter plugin. This will ensure that the plugin will be
updated when new versions are available. If you want to install from source so you can modify the
source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette] and type `install`. Among the commands you
   should see `Package Control: Install Package`. If that command is not highlighted, use the
   keyboard or mouse to select it. There will be a pause of a few seconds while Package Control
   fetches the list of available plugins.

1. When the plugin list appears, type `elixir formatter`. Among the entries you should see
   `ElixirFormatter`. If that entry is not highlighted, use the keyboard or mouse to select it.

[mix format]: https://hexdocs.pm/mix/master/Mix.Tasks.Format.html
[Package Control]: https://sublime.wbond.net/installation
[Command Palette]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
