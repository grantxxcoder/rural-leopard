class Player:
    def __init__(self):
        self.move(0, 0)
        self.jump_tokens = 0

    def inc_jump(self):
        self.jump_tokens += 1
    
    def has_jump(self):
        return self.jump_tokens > 0
    
    def dec_jump(self):
        if self.has_jump:
            self.jump_tokens -= 1

    def get_jumps(self):
        return self.jump_tokens
    
    def get_pos(self):
        return self.x, self.y
    
    def move(self, x, y):
        self.x = x
        self.y = y