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

scale_factor = int(os.environ.get('GDK_SCALE', 1))

c.bindings.key_mappings = {
    'ه': 'i',
    'خ': 'o',
    'ب': 'f',
    '<Ctrl-ر>': '<Ctrl-v>'}

c.editor.command = ['emacsclient', '-a', '""', '-c', '{file}']

# Enable JavaScript.
c.content.javascript.enabled = True

# config.set('content.javascript.enabled', True, 'file://*')
# config.set('content.javascript.enabled', True, 'chrome://*/*')
# config.set('content.javascript.enabled', True, 'qute://*/*')

c.spellcheck.languages = ['en-US']

c.fonts.default_family = ["DejaVu Sans Mono"]
# c.fonts.monospace = '"DejaVu Sans Mono", Monaco, "Bitstream Vera Sans Mono", "Andale Mono", "Courier New", Courier, "Liberation Mono", monospace, Fixed, Consolas, Terminal'

# rofi-pass
config.bind('pi', 'spawn --userscript qute-pass')
config.bind('j', 'scroll-px 0 20')
config.bind('k', 'scroll-px 0 -20')

# Firefox as a user_agent
# Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0
# config.set('content.headers.user_agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36')
# c.content.headers.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

# view youtube vidoes with mpv
# tsp is a task spooler that adds tasks to a queue 
screen_dims = screen_dim()
mpv_command = (
    'mpv --slang=en --force-window=immediate --no-terminal'
    ' --geometry={} --autofit=1280x720 '
    '--ytdl-format="bestvideo[height<=?{}][fps<=?30]+bestaudio/best"'
    ' --x11-name=qutebrowser-youtube --ytdl-raw-options=mark-watched='
    ',cookies="~/Downloads/cookies.txt",embed-subs=,sub-lang=en,'
    'write-sub=,write-auto-sub=')
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
config.bind('cc', 'download-clear')
template_keys = ['ia', 'ir', 'im', 'd']
for k in template_keys:
    config.bind(f'c{k}', f'spawn --userscript qute-capture write -k {k}')
config.bind(',or', 'spawn --userscript qute-capture read -H "Interesting Resources"')

# it turns out per-domain settings for content.user-stylesheets is not supported
# config.set('content.user_stylesheets', os.path.join(path, 'gruvbox-all-sites.css'), '*://github.com/*|*://*.stackexchange.com/*|*://stackoverflow.com/*')

# prevent gmail from sending protocol handler confirmation dialogs
config.set('content.register_protocol_handler', True, '*://gmail.com/*')
config.set('content.register_protocol_handler', True, '*://mail.google.com/*')

config.set('content.tls.certificate_errors', 'block')
config.set('content.tls.certificate_errors', 'load-insecurely', '*://mail.westqurna2.com')
config.set('content.notifications.enabled', False)
for url in ['gmail.com', 'mail.westqurna2.com', 'reddit.com', 'mail.zoho.com']:
    config.set('content.notifications.enabled', True, url)

# Default zoom level
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
c.tabs.show = 'switching'
c.tabs.show_switching_delay = 5000

c.completion.height = '30%'

c.confirm_quit = ['downloads']
c.downloads.location.prompt = False

# Dark Mode
config.set('colors.webpage.preferred_color_scheme', 'dark')
config.set('colors.webpage.bg', 'black')
config.set('colors.webpage.darkmode.enabled', True)
config.set('colors.webpage.darkmode.policy.images', 'smart')
# Load existing settings made via :set

# config.source('nord.py')

# ad-blocking
config.set('content.blocking.method', 'both')

# Autosave session
config.set('auto_save.session', True)

config.set('content.javascript.can_access_clipboard', True)
# settings for better performance
config.set('content.autoplay', False)
config.set('content.prefers_reduced_motion', True)
config.set('qt.args', ['ignore-gpu-blocklist', 'enable-gpu-rasterization', 'enable-accelerated-video-decode', 'enable-quic'])
config.set('session.lazy_restore', True)
# Irrelevant to QtWebEngine
# config.set('content.cache.maximum_pages', 6) # see https://webkit.org/blog/427/webkit-page-cache-i-the-basics/

# remove hints on reload
config.set('hints.leave_on_load', True)

# Use ranger as file picker
config.set("fileselect.handler", "external")
config.set("fileselect.single_file.command",
           ['konsole', '-e', 'ranger', '--choosefile', '{}'])
config.set("fileselect.multiple_files.command",
           ['konsole', '-e', 'ranger', '--choosefiles', '{}'])

c.aliases |= {'paywall': "open https://www.google.com/search?q=cache:{url}"}
