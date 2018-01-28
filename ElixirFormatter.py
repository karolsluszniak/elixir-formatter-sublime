import os
import sublime
import sublime_plugin
import subprocess
import threading

class ElixirFormatter:
    @staticmethod
    def run(file_name):
        project_root_with_mix = ElixirFormatter.find_project(file_name)
        project_root = project_root_with_mix or os.path.dirname(file_name)
        file_name_rel = file_name.replace(project_root + "/", "")
        blacklisted = ElixirFormatter.check_blacklisted_in_config(project_root, file_name_rel)
        if blacklisted:
            print("ElixirFormatter skipped '{0}' due to :inputs key in '.formatter.exs'".
              format(file_name_rel))
            return

        stdout, stderr = ElixirFormatter.run_command(project_root, ["mix", "format", file_name_rel])
        if stderr != "":
            print("ElixirFormatter catched error running 'mix format':\n{0}".format(stderr))

    @staticmethod
    def find_project(cwd = None):
        cwd = cwd or os.getcwd()
        if cwd == os.path.realpath('/'):
            return None
        elif os.path.exists(os.path.join(cwd, 'mix.exs')):
            return cwd
        else:
            return ElixirFormatter.find_project(os.path.dirname(cwd))

    @staticmethod
    def run_command(project_root, task_args):
        settings = sublime.load_settings('Preferences.sublime-settings')
        env = os.environ.copy()

        try:
            env['PATH'] = os.pathsep.join([settings.get('env')['PATH'], env['PATH']])
        except (TypeError, ValueError, KeyError):
            pass

        if sublime.platform() == "windows":
            launcher = ['cmd', '/c']
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            launcher = []
            startupinfo = None

        process = subprocess.Popen(
            launcher + task_args,
            cwd = project_root,
            env = env,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            startupinfo = startupinfo)

        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')

        return [stdout, stderr]

    check_blacklisted_script_template = """
      file = \"[[file]]\"
      formatter = \".formatter.exs\"
      with true <- File.exists?(formatter),
           {formatter_opts, _} <- Code.eval_file(formatter),
           {:ok, inputs} <- Keyword.fetch(formatter_opts, :inputs) do
        IO.puts("Check result: #{file in Enum.flat_map(inputs, &Path.wildcard/1)}")
      end
    """

    @staticmethod
    def check_blacklisted_in_config(project_root, file_name):
        if not os.path.isfile(os.path.join(project_root, ".formatter.exs")):
            return

        script = ElixirFormatter.check_blacklisted_script_template.replace("[[file]]", file_name)
        stdout, stderr = ElixirFormatter.run_command(project_root, ["elixir", "-e", script])
        return "Check result: false" in stdout

class ElixirFormatterFormatFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name = self.view.file_name()
        extension = os.path.splitext(file_name)[1][1:]
        syntax = self.view.settings().get("syntax")
        if extension in ["ex", "exs"] or "Elixir" in syntax:
            threading.Thread(target=ElixirFormatter.run, args=(file_name,)).start()

class ElixirFormatterEventListeners(sublime_plugin.EventListener):
    @staticmethod
    def on_post_save(view):
        view.run_command("elixir_formatter_format_file")
