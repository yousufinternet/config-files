function onPauseChange (prop, enabled) {
    if (enabled) {
        mp.set_property('fullscreen', 'no')
    }
}

mp.observe_property('pause', 'bool', onPauseChange)
