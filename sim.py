import sys
import logging

from simulator.config import *
from simulator.topology import Topology, Get_Time
from simulator.event_queue import Event_Queue


class Sim(Topology):

    def __init__(self, algorithm, topo_file, event_file, step='NORMAL'):
        super().__init__(algorithm, step)
        self.load_topo(TOPO_PATH + topo_file)
        self.load_event(EVENT_PATH + event_file)
        self.dump_sim()
        self.send_current_links()
        self.dispatch_event(self.step)

    def __str__(self):
        ans = "==== Print Topology ====\n"
        ans += super().__str__()
        ans += "==== Print Event ====\n"
        ans += Event_Queue.Str()
        return ans

    def dump_sim(self):
        self.logging.info("DUMP_SIM at Time %d\n" % Get_Time() + str(self))

    def dispatch_event(self, step='NORMAL'):
        e = Event_Queue.Get_Earliest()
        while e:
            e.dispatch()
            if step == STEP_COMMAND[1]:
                self.logging.info(str(e))
                self.wait()
            e = Event_Queue.Get_Earliest()

    def load_topo(self, topo_file):
        self.load_event(topo_file)
        self.dispatch_event()

    def load_event(self, file):
        self.load_command_file(file)

    def print_comment(self, comment):
        self.logging.info('Time: %d, Comment: %s' % (Get_Time(), comment))


def main():
    if len(sys.argv) < 4 or len(sys.argv) > 5 or sys.argv[1] not in ROUTE_ALGORITHM:
        sys.stderr.write(USAGE_STR)
        sys.exit(-1)

    step = 'NORMAL'
    if len(sys.argv) == 5:
        if sys.argv[4] not in STEP_COMMAND:
            sys.stderr.write(USAGE_STR)
            sys.exit(-1)
        else:
            step = sys.argv[4]

    s = Sim(sys.argv[1], sys.argv[2], sys.argv[3], step)


if __name__ == '__main__':
    # Try: python sim.py GENERIC demo.topo demo.event
    # Change logging level from DEBUG to INFO or WARNING, if DEBUG information bothers you
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT, datefmt=LOGGING_DATAFMT)
    main()
