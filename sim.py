import sys
import logging

from simulator.config import *
from simulator.topology import Topology
from simulator.event_queue import Event_Queue


class Sim(Topology):

    def __init__(self, algorithm, topo_file, event_file):
        super().__init__(algorithm)
        self.load_topo(TOPO_PATH + topo_file)
        self.load_event(EVENT_PATH + event_file)
        self.logging.info("\n" + str(self))
        self.send_current_links()
        self.dispatch_event()


    def __str__(self):
        ans = "==== Print Topology ====\n"
        ans += super().__str__()
        ans += "==== Print Event ====\n"
        ans += Event_Queue.Str()
        return ans


    def dispatch_event(self):
        e = Event_Queue.Get_Earliest()
        while e:
            e.dispatch()
            e = Event_Queue.Get_Earliest()


    def load_topo(self, topo_file):
        self.load_event(topo_file)
        self.dispatch_event()


    def load_event(self, file):
        self.load_command_file(file)




def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ROUTE_ALGORITHM:
        sys.stderr.write(USAGE_STR)
        sys.exit(-1)

    s = Sim(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    # Try: python sim.py GENERIC demo.topo demo.event
    # Change logging level to INFO or WARNING, if debug information bothers you
    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, datefmt=LOGGING_DATAFMT)
    main()
