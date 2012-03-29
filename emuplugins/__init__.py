import config
plugins = []
for p in config.plugins:
    plugins.append(__import__('emuplugins.%s'%p.lower(), globals(), locals(), [p], -1).__dict__[p])
