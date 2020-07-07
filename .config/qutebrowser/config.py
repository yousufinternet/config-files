# Type: Bool
import os
import dracula.draw

# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

c.bindings.key_mappings = {
    'ه': 'i',
    'خ': 'o',
    'ب': 'f',
    '<Ctrl-ر>': '<Ctrl-v>'}

c.editor.command = ['emacsclient', '-a', '""', '-c', '{file}']

# Enable JavaScript.
config.set('content.javascript.enabled', True)

# config.set('content.javascript.enabled', True, 'file://*')
# config.set('content.javascript.enabled', True, 'chrome://*/*')
# config.set('content.javascript.enabled', True, 'qute://*/*')

c.spellcheck.languages = ['en-US']

c.fonts.default_family = ["DejaVu Sans Mono"]
# c.fonts.monospace = '"DejaVu Sans Mono", Monaco, "Bitstream Vera Sans Mono", "Andale Mono", "Courier New", Courier, "Liberation Mono", monospace, Fixed, Consolas, Terminal'

# rofi-pass
config.bind('pi', 'spawn --userscript qute-pass')

# Firefox as a user_agent
# Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0
# config.set('content.headers.user_agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36')
c.content.headers.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

# view youtube vidoes with mpv
# tsp is a task spooler that adds tasks to a queue 

mpv_command = 'mpv --force-window=immediate --no-terminal --geometry=1280x720-0-0 --autofit=1280x720 --ytdl-format="bestvideo[height<=?{}][fps<=?30]+bestaudio/best" --x11-name=qutebrowser-youtube --ytdl-raw-options=mark-watched=,cookies="~/Downloads/cookies.txt"'
mpv_720 = mpv_command.format('720')
mpv_480 = mpv_command.format('480')
config.bind(';m4', f'hint links spawn tsp {mpv_480} {{hint-url}}')
config.bind(';m7', f'hint links spawn tsp {mpv_720} {{hint-url}}')
config.bind(';M', f'hint links spawn tsp {mpv_command} {{hint-url}}')
config.bind(',y', 'spawn konsole -e youtube-dl --all-subs --embed-subs {url};; tab-close')
config.bind(',m', 'spawn tsp mpv --ytdl-format 22 {url};; back')

# dark style sheets
path = os.path.expanduser('~/.config/qutebrowser/Dark-stylesheets/')
stylesheets = ' '.join([os.path.join(path, fn) for fn in os.listdir(path)])
config.bind(',n', 'config-cycle -t content.user_stylesheets %s;; set colors.webpage.bg ""' % stylesheets)
config.bind(',N', 'set content.user_stylesheets " ";; set colors.webpage.bg "white"')
# config.bind(',r', 'spawn --userscript ~/.config/qutebrowser/userscripts/readability-margin')
config.bind(',r', 'spawn --userscript readability-js')

# it turns out per-domain settings for content.user-stylesheets is not supported
# config.set('content.user_stylesheets', os.path.join(path, 'gruvbox-all-sites.css'), '*://github.com/*|*://*.stackexchange.com/*|*://stackoverflow.com/*')
# prevent gmail from sending protocol handler confirmation dialogs
config.set('content.register_protocol_handler', True, '*://gmail.com/*')
config.set('content.register_protocol_handler', True, '*://mail.google.com/*')
config.set('content.ssl_strict', True)
config.set('content.ssl_strict', False, '*://mail.westqurna2.com')
config.set('content.notifications', False)
# Default zoom level
scale_factor = int(os.environ.get('GDK_SCALE', 1))
config.set('zoom.default', '125%' if scale_factor==2 else '100%')

c.url.searchengines = {'DEFAULT': 'https://duckduckgo.com/?q={}',
                       'i': 'https://imdb.com/find?q={}',
                       'r': 'https://reddit.com/r/{}',
                       'g': 'https://google.com/search?q={}',
                       'gt': 'https://github.com/search?q={}',
                       'y': 'https://youtube.com/results?search_query={}',
                       'w': 'https://wiki.archlinux.org/index.php?search={}',
                       'tv': 'http://tv.shabakaty.com/?ch=channel{}',
                       'l': 'http://libgen.is/search.php?req={}'}

# config.set('completion.height', '30%')
# config.set('content.autoplay', False)

# Downloads position, and remove finished after 30 seconds
config.set('downloads.position', 'bottom')
config.set('downloads.remove_finished', 90)

# tabs positioning
config.set('tabs.position', 'left')
config.set('tabs.padding', {'top':1, 'bottom':1, 'left':2, 'right':2})
config.set('tabs.indicator.width', 0)
config.set('tabs.title.format', '{index}')
config.set('tabs.title.format_pinned', '{index}')
config.set('tabs.width', 20)
config.set('tabs.show', 'multiple')

# allow the last tab to be closed and thus closing the window
c.tabs.last_close = 'close'

c.completion.height = '30%'

# Dark Mode
config.set('colors.webpage.prefers_color_scheme_dark', True)
config.set('colors.webpage.bg', 'black')
config.set('colors.webpage.darkmode.enabled', True)
config.set('colors.webpage.darkmode.policy.images', 'smart')

# Load existing settings made via :set

dracula.draw.blood(c)
# config.source('nord.py')
