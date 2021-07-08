# Type: Bool
import os
import sys
import dracula.draw

sys.path.append(os.path.expanduser('~/.config/bspwm/scripts/'))

from wmutils.utils import screen_dim
# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

config.load_autoconfig(False)

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
screen_dims = screen_dim()
mpv_command = 'mpv --slang=en --force-window=immediate --no-terminal --geometry={} --autofit=1280x720 --ytdl-format="bestvideo[height<=?{}][fps<=?30]+bestaudio/best" --x11-name=qutebrowser-youtube --ytdl-raw-options=mark-watched=,cookies="~/Downloads/cookies.txt",embed-subs=,sub-lang=en,write-sub=,write-auto-sub='
mpv_720 = mpv_command.format(
    f'{int(screen_dims["width"]*0.25)}x{int(screen_dims["height"]*0.25)}-0-0',
    '720')
mpv_480 = mpv_command.format(
    f'{int(screen_dims["width"]*0.25)}x{int(screen_dims["height"]*0.25)}-0-0',
    '480')
mpv_360 = mpv_command.format(
    f'{int(screen_dims["width"]*0.25)}x{int(screen_dims["height"]*0.25)}-0-0',
    '360')
mpv_240 = mpv_command.format(
    f'{int(screen_dims["width"]*0.25)}x{int(screen_dims["height"]*0.25)}-0-0',
    '240')
config.bind(';m2', f'hint links spawn tsp {mpv_240} {{hint-url}}')
config.bind(';m3', f'hint links spawn tsp {mpv_360} {{hint-url}}')
config.bind(';m4', f'hint links spawn tsp {mpv_480} {{hint-url}}')
config.bind(';m7', f'hint links spawn tsp {mpv_720} {{hint-url}}')
config.bind(',m2', f'spawn tsp {mpv_240} {{url}};; back')
config.bind(',m3', f'spawn tsp {mpv_360} {{url}};; back')
config.bind(',m4', f'spawn tsp {mpv_480} {{url}};; back')
config.bind(',m7', f'spawn tsp {mpv_720} {{url}};; back')
config.bind(',y', 'spawn mlterm -e youtube-dl --cookies=cookies.txt --all-subs --embed-subs {url};; tab-close')

# dark style sheets
path = os.path.expanduser('~/.config/qutebrowser/Dark-stylesheets/')
stylesheets = ' '.join([os.path.join(path, fn) for fn in os.listdir(path)])
config.bind(',n', 'config-cycle -t content.user_stylesheets %s;; set colors.webpage.bg ""' % stylesheets)
config.bind(',N', 'set content.user_stylesheets " ";; set colors.webpage.bg "white"')
# config.bind(',r', 'spawn --userscript ~/.config/qutebrowser/userscripts/readability-margin')
config.bind(',r', 'spawn --userscript readability-js')
template_keys = ['ia', 'ir', 'im', 'd']
for k in template_keys:
    config.bind(f',c{k}', f'spawn --userscript qute-capture write -k {k}')
config.bind(',or', 'spawn --userscript qute-capture read -H "Interesting Resources"')

# it turns out per-domain settings for content.user-stylesheets is not supported
# config.set('content.user_stylesheets', os.path.join(path, 'gruvbox-all-sites.css'), '*://github.com/*|*://*.stackexchange.com/*|*://stackoverflow.com/*')
# prevent gmail from sending protocol handler confirmation dialogs
config.set('content.register_protocol_handler', True, '*://gmail.com/*')
config.set('content.register_protocol_handler', True, '*://mail.google.com/*')

config.set('content.tls.certificate_errors', 'block')
config.set('content.tls.certificate_errors', 'load-insecurely', '*://mail.westqurna2.com')
config.set('content.notifications.enabled', False)

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

dracula.draw.blood(c)

# tabs positioning
config.set('tabs.position', 'left')
config.set('tabs.padding', {'top':4, 'bottom':4, 'left':3, 'right':3})
config.set('tabs.indicator.width', 1)
config.set('tabs.title.format', '{index}')
config.set('tabs.title.format_pinned', '{index}')
config.set('tabs.width', 26)
config.set('tabs.show', 'multiple')

# allow the last tab to be closed and thus closing the window
c.tabs.last_close = 'close'

c.completion.height = '30%'

# Dark Mode
config.set('colors.webpage.preferred_color_scheme', 'dark')
config.set('colors.webpage.bg', 'black')
config.set('colors.webpage.darkmode.enabled', True)
config.set('colors.webpage.darkmode.policy.images', 'smart')
# Load existing settings made via :set

# config.source('nord.py')

# ad-blocking
config.set('content.blocking.method', 'both')
