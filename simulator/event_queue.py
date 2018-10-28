import heapq

class Event_Queue:
    q = []

    @staticmethod
    def Post(e):
        heapq.heappush(Event_Queue.q, e)

    @staticmethod
    def Get_Earliest():
        if Event_Queue.q == []:
            return None
        return heapq.heappop(Event_Queue.q)

    @staticmethod
    def Str():
        ans = ""
        for i in Event_Queue.q:
            ans += str(i)
            ans += "\n"
        return ans

