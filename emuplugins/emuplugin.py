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

import threading

class EmuPlugin(threading.Thread):
    """
        Plugin module to interface with a cpu core.
        
            Access to the cpu core should be done via self.cpu.
            
            Signaling a shutdown should be done via raising SystemExit in cpu_ticked().
            
            Implemention should happen within tick(), return tick as often as you like.
            If you do implement a non-returning loop, you must return once self.running is False.
    """
    
    running = True
    cpu = None
    name = "Unknown"
    
    def tick(self):
        """
            Overload this function to implement your plugin
        """
        raise NotImplementedError
    
    def cpu_ticked(self):
        """
            Gets called once per CPU tick
                If you wish to signal a shutdown, raise a SystemExit
        """
        pass
    
    def run(self):
        """
            Gets called once on plugin load and loops until shutdown() is called
        """
        while(self.running):
            self.tick()
    
    def shutdown(self):
        """
            Called when requesting a plugin shutdown
        """
        self.running = False
    
    def __init__(self, cpu):
        self.cpu = cpu
        self.name = self.__class__.__name__
        threading.Thread.__init__(self)
