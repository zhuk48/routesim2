import sys
import traceback

from simulator.config import *
from simulator.event import Event
from simulator.topology import Topology
from simulator.event_queue import Event_Queue


class Sim(Topology):

    def __init__(self, algorithm, topo_file, event_file):
        super().__init__()
        self.algorithm = ROUTE_ALGORITHM[algorithm]
        self.load_topo(TOPO_PATH + topo_file)
        self.load_event(EVENT_PATH + event_file)

        print(self)
        # TODO： 1. Use link_has_been_updated() to init each Node
        # TODO:  2. Process Event


    def __str__(self):
        ans = "==== Print Topology ====\n"
        ans += super().__str__()
        ans += "==== Print Event ====\n"
        ans += Event_Queue.Str()
        return ans


    def load_topo(self, topo_file):
        self.load_event(topo_file)

        e = Event_Queue.Get_Earliest()
        while e:
            e.dispatch()
            e = Event_Queue.Get_Earliest()


    def load_event(self, file):
        try:
            f = open(file)
            for line in f.readlines():
                line = line.strip()
                if line == "" or line[0] == '#':
                    continue

                items = line.split(' ')
                time_stamp = int(items[0])
                event_type = items[1]

                num_args = len(items) - 2
                if event_type == EVENT_TYPE.PRINT:
                    Event_Queue.Post(Event(time_stamp, event_type, self, "".join(items[2:])))
                elif num_args < 0 or num_args > 3:
                    sys.stderr.write(line)
                    raise BufferError
                elif num_args == 0:
                    Event_Queue.Post(Event(time_stamp, event_type, self))
                elif num_args == 1:
                    Event_Queue.Post(Event(time_stamp, event_type, self, int(items[2])))
                elif num_args == 2:
                    Event_Queue.Post(Event(time_stamp, event_type, self, int(items[2]), int(items[3])))
                elif num_args == 3:
                    Event_Queue.Post(Event(time_stamp, event_type, self, int(items[2]), int(items[3]), int(items[4])))

            f.close()

        except IOError as e:
            print("Can not open file " + file)
            print(e)
            sys.exit(-1)

        except BufferError:
            print("File with wrong format " + file)
            sys.exit(-1)

        except Exception as e:
            print("File with wrong format " + file)
            print(e)
            traceback.print_exc()
            sys.exit(-1)


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ROUTE_ALGORITHM.keys():
        sys.stderr.write(USAGE_STR)
        sys.exit(-1)

    s = Sim(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    # Try: python sim.py GENERIC demo.topo demo.event
    main()
