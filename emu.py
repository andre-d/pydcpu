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
import sys

def main():
    print("DCPUEmu")
    try:
        core = DCPUCore()
        plugins = emuplugins.load_plugins(core)
        print("...Running...\nCtrl+C to shutdown")
        while True:
            dt = core.run()
            status = "Running at %.2fMhz" % (1.0/dt)
            sys.stdout.write("\r%s\r%s" % (" "*(len(status)+3), status))
            sys.stdout.flush()
            while core.is_alive():
                pass
            for p in plugins:
                p.cpu_ticked()
    except (KeyboardInterrupt, SystemExit):
        print("\nShutting down")
    
    emuplugins.shutdown_plugins(plugins)
    
    exit()

if __name__ == '__main__':
    main()
