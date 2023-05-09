        self.change_x = 0
        self.change_y = 0

        # direction = [x, y]
        self.direction = [1, 0] if start[0] < end[0] else [-1, 0]
        self.direction[1] = 1 if start[1] < end[1] else -1
        if self.direction == [1, 0]:
            self.change_x = 1
        elif self.direction == [-1, 0]:
            self.change_x = -1
        if self.direction[1] == 1:
            self.change_y = 1
        elif self.direction[1] == -1:
            self.change_y = -1
        
        #get image
        self.image = pygame.Surface((self.text_surface.get_width(), self.text_surface.get_height()))
        self.image.blit(self.text_surface, (x,y))

        #set colorkey (transparent color)
        self.image.set_colorkey(BLACK)
        self.rect = self.text_surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
            

    def draw(self, screen):
        screen.blit(self.text_surface, self.rect)


    #this is where we tell it how to update the position
    def update(self):
        self.rect.x += self.change_x * self.direction[0]
        self.rect.y += self.change_y * self.direction[1]

        self.rect.x = round(self.rect.x)
        self.rect.y = round(self.rect.y)


        if self.rect.left <= self.start[0] and self.direction[0] == -1:
            self.direction[0] *= -1
        elif self.rect.right >= self.end[0] and self.direction[0] == 1:
            self.direction[0] *= -1
        if self.rect.top <= self.start[1] and self.direction[1] == -1:
            self.direction[1] *= -1
        elif self.rect.bottom >= self.end[1] and self.direction[1] == 1:
            self.direction[1] *= -1