from emuplugins.emuplugin import EmuPlugin
import emuconfig
plugins = []
for p in emuconfig.plugins:
    plugins.append(__import__('emuplugins.%s'%p.lower(), globals(), locals(), [p], -1).__dict__[p])

def load_plugins(*a, **kw):
    if not plugins:
        return plugins
    print("Starting plugins")
    loaded = []
    for p in plugins:
        loaded.append(p(*a, **kw))
    for l in loaded:
        print("Starting plugin %s" % l.name)
        l.start()
    return loaded

def shutdown_plugins(plugins):
    if not plugins:
        return
    print("Shutting down plugins")
    for p in plugins:
        print("Shutting down %s" % p.name)
        p.shutdown()
    
    shutdown = False
    while not shutdown:
        for p in plugins:
            if p.is_alive():
                print("Waiting for plugin %s to shutdown" % p.name)
                continue;
        shutdown = True
