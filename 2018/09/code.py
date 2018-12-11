class Marble():
    def __init__(self, score):
        self.score = score
        self.next = self
        self.prev = self
 
    def insert_after(self, score):
        marble = Marble(score)
        marble.prev = self
        marble.next = self.next
        self.next.prev = marble
        self.next = marble
        return marble
 
    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.next
 
# bruteforce nobrain
def play(players, last):
    scores = {}
    for i in range(0, players):
        scores[i] = 0
    
    cur_marble = Marble(0)
    cur_player = 0
    for score in range(1, last + 1):
        cur_player = (cur_player + 1) % players
        if score % 23 == 0:
            marble = cur_marble
            for i in range(0, 7):
                marble = marble.prev
            scores[cur_player] += score + marble.score
            cur_marble = marble.remove()
        else:
            cur_marble = cur_marble.next.insert_after(score)
    
    print(max(scores.values()))

players = 459
last = 71320
play(players, last)
play(players, 100 * last)