# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from dcpucore import DCPUCore
import emuplugins

def load_plugins(plugins, core):
    if not plugins:
        return plugins
    print("Starting plugins")
    loaded = []
    for p in plugins:
        loaded.append(p(core))
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

def main():
    try:
        plugins = emuplugins.plugins
        core = DCPUCore()
        plugins = load_plugins(plugins, core)
        running = True

        while True:
            running = core.run()
            while core.is_alive():
                pass
            for p in plugins:
                p.cpu_ticked()
    except (KeyboardInterrupt, SystemExit):
        print("Shutting down")
    
    shutdown_plugins(plugins)
    
    exit()

if __name__ == '__main__':
    main()
