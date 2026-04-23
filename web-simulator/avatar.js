const Avatar = (() => {
    let _config = {};
    let _dictionary = {};
    const _wordSet = new Set();
    let _playingTimeout = null;
    let _stopRequested = false;

    const ready = fetch('avatar.json')
        .then(r => r.json())
        .then(cfg => {
            Object.assign(_config, cfg);
            return fetch(cfg.dictionary || 'dictionary.json');
        })
        .then(r => r.json())
        .then(data => {
            _dictionary = data;
            for (const cat in data) {
                data[cat].forEach(w => _wordSet.add(w));
            }
        });

    function _playSiGML(url) {
        CWASA.playSiGMLURL(new URL(url, window.location.href).href);
    }

    function _findGlosses(input) {
        const tokens = input.trim().split(/\s+/).filter(Boolean);
        const glosses = [];
        for (let i = 0; i < tokens.length; i++) {
            for (let len = 2; len >= 1; len--) {
                if (i + len <= tokens.length) {
                    const candidate = tokens.slice(i, i + len).join(' ');
                    if (_wordSet.has(candidate)) {
                        glosses.push(candidate);
                        i += len - 1;
                        break;
                    }
                }
            }
        }
        return glosses;
    }

    function _playSequentially(glosses, index, callbacks) {
        if (index >= glosses.length || _stopRequested) {
            if (!_stopRequested && callbacks.onDone) callbacks.onDone();
            return;
        }
        _playSiGML('sigml/' + glosses[index] + '.sigml');
        if (callbacks.onSign) callbacks.onSign(glosses[index], index, glosses.length);
        _playingTimeout = setTimeout(() => {
            _playSequentially(glosses, index + 1, callbacks);
        }, _config.signDuration || 1000);
    }

    function sign(text, callbacks = {}) {
        _stopRequested = false;
        const glosses = _findGlosses(text);
        if (glosses.length === 0) {
            if (callbacks.onNoMatch) callbacks.onNoMatch();
            return;
        }
        _playSequentially(glosses, 0, callbacks);
    }

    function stop() {
        _stopRequested = true;
        clearTimeout(_playingTimeout);
    }

    return {
        ready,
        sign,
        stop,
        get config()     { return _config; },
        get dictionary() { return _dictionary; },
        get wordSet()    { return _wordSet; },
    };
})();
