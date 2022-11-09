import pygame
from random import uniform, choice

class Player(pygame.sprite.Sprite):
	def __init__(self, is_left_player):
		super().__init__()
		self.image = pygame.Surface((20,100))
		self.image.fill("white")
		self.score = 0

		self.is_left_player = is_left_player
		if self.is_left_player:
			self.controls = [pygame.K_q, pygame.K_z]
			self.rect = self.image.get_rect(center=(50, 200))
		else:
			self.controls = [pygame.K_o, pygame.K_m]
			self.rect = self.image.get_rect(center=(750, 200))

	def update(self):
		speed = 10
		keys = pygame.key.get_pressed()
		if keys[self.controls[0]] and self.rect.top >= 0:
			self.rect.bottom -= speed
		if keys[self.controls[1]] and self.rect.bottom <= 400:
			self.rect.bottom += speed

class Ball(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.size = 18
		self.x = 400
		self.y = 200
		self.image = pygame.Surface((self.size,self.size))
		self.image.fill("white")
		self.rect = self.image.get_rect(center = (self.x,self.y))
		self.init_speed_x = 5
		self.speed_x = choice([self.init_speed_x, -self.init_speed_x])
		self.speed_y = uniform(-2,2)
		self.can_collide_with_ceil = True
		self.can_collide_with_floor = True
		self.can_collide_with_left = True
		self.can_collide_with_right = True
		self.has_hit_player = False
		self.bounce_factor = 4 # lower bounce factor makes the ball bounce more extremely upon hitting player

	def wall_collision(self):
		if self.rect.top <= 0 and self.can_collide_with_ceil:
			self.speed_y = -self.speed_y
			self.can_collide_with_ceil = False
			self.can_collide_with_floor = True
			self.can_collide_with_left = True
			self.can_collide_with_right = True
		if self.rect.bottom >= 400 and self.can_collide_with_floor:
			self.speed_y = -self.speed_y			
			self.can_collide_with_ceil = True
			self.can_collide_with_floor = False
			self.can_collide_with_left = True
			self.can_collide_with_right = True

	def player_collision(self):
		player_collisions = pygame.sprite.spritecollide(self, players, False)
		if player_collisions != []:
			if not self.has_hit_player:
				self.speed_x *= 3
			self.has_hit_player = True
			collision = player_collisions[0]
			if collision.is_left_player and self.can_collide_with_left:
				self.speed_x = -self.speed_x
				self.speed_y = (self.rect.center[1] - collision.rect.center[1])/self.bounce_factor		
				self.can_collide_with_ceil = True
				self.can_collide_with_floor = True
				self.can_collide_with_left = False
				self.can_collide_with_right = True
			if not collision.is_left_player and self.can_collide_with_right:
				self.speed_x = -self.speed_x
				self.speed_y = (self.rect.center[1] - collision.rect.center[1])/self.bounce_factor
				self.can_collide_with_ceil = True
				self.can_collide_with_floor = True
				self.can_collide_with_left = True
				self.can_collide_with_right = False

	def update(self):
		self.wall_collision()
		self.player_collision()
		self.x += self.speed_x
		self.y += self.speed_y
		self.rect.x = self.x
		self.rect.y = self.y

class Game:
	def __init__(self, players, ball):
		self.players = players
		self.ball = ball
		self.left_score = 0
		self.right_score = 0
		self.winner = None

	def reset_game(self):
		self.ball.can_collide_with_ceil = True
		self.ball.can_collide_with_floor = True
		self.ball.can_collide_with_left = True
		self.ball.can_collide_with_right = True
		self.ball.has_hit_player = False
		self.ball.x = 400
		self.ball.y = 200
		self.ball.speed_y = uniform(-2,2)
		self.ball.speed_x = choice([self.ball.init_speed_x, -self.ball.init_speed_x])
		for player in self.players:
			if player.is_left_player:
				player.rect.center = (50,200)
			else:
				player.rect.center = (750,200)

	def scoregoal(self):
		if self.ball.rect.right <= 0:
			self.right_score += 1
			self.reset_game()
		elif self.ball.rect.left >= 800:
			self.left_score += 1
			self.reset_game()
		if self.left_score == 10:
			self.winner = "PLAYER 1"
			self.left_score = 0
		if self.right_score == 10:
			self.winner = "PLAYER 2"
			self.left_score = 0

	def update(self):
		self.scoregoal()

class Button:
	def __init__(self, string, pos, function=lambda: None, size=30, font=None):
		self.font = pygame.font.Font(font, size)
		self.image = self.font.render(string, False, "white")
		self.rect = self.image.get_rect(center = pos)
		self.do_function = function

	def mouse_on(self):
		mouse_pos = pygame.mouse.get_pos()
		return self.rect.collidepoint(mouse_pos)

class Menu:
	def __init__(self, buttons):
		self.buttons = buttons
		self.latest_time = pygame.time.get_ticks()

	def display_loading_screen(self):
		current_time = pygame.time.get_ticks()
		while not (current_time - self.latest_time >= 300):
			current_time = pygame.time.get_ticks()
			background()
			pygame.display.update()
		return

	def display(self):
		mouse_button = pygame.mouse.get_pressed(num_buttons=3)
		for button in self.buttons:
			screen.blit(button.image, button.rect)
			if mouse_button[0] and button.mouse_on():
				self.latest_time = pygame.time.get_ticks()
				self.display_loading_screen()
				return button
	
class GameState:
	def __init__(self):
		self.state = "main menu"
		self.running = True
		self.left_click = False
		self.event = None
		self.pos1 = (500,300)
		self.pos2 = (300,300)
		self.font = "atarifont.ttf"
		def create_main_menu():
			self.quit_button = Button("QUIT", self.pos1, font=self.font)
			self.play_button = Button("PLAY", self.pos2, font=self.font)
			return Menu([self.quit_button, self.play_button])
		self.main_menu = create_main_menu()
		def create_pause_menu():
			self.resume_button = Button("RESUME", self.pos2, size=20, font=self.font)
			self.main_menu_button = Button("MAIN MENU", self.pos1, size=20, font=self.font)
			return Menu([self.resume_button, self.main_menu_button])
		self.pause_menu = create_pause_menu()	

	def play_game(self):
		players.draw(screen)
		players.update()

		ball.draw(screen)
		ball.update()

		# DISPLAY SCOREBOARD
		game.update()
		font = pygame.font.Font(self.font, 30)
		left_score_text = font.render(str(game.left_score), False, "white")
		screen.blit(left_score_text, (350, 50))
		right_score_text = font.render(str(game.right_score), False, "white")
		screen.blit(right_score_text, (450,50))

		# CHECK FOR PAUSE BUTTON
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			self.state = "pause menu"

	def display_main_menu(self):
		game.left_score = 0
		game.right_score = 0
		game.reset_game()
		if game.winner is not None:
			font = pygame.font.Font(self.font, 50)
			announcement = font.render(game.winner + " WIN !", False, "white")
			screen.blit(announcement, announcement.get_rect(center=(400,100)))
		clicked_button = self.main_menu.display()
		if clicked_button == self.play_button:
			game.winner = None
			self.state = "game"
		if clicked_button == self.quit_button:
			self.running = False

	def display_pause_menu(self):
		clicked_button = self.pause_menu.display()
		if clicked_button == self.resume_button:
			self.state = "game"
		if clicked_button == self.main_menu_button:
			self.state = "main menu"

	def manage_states(self):
		if self.state == "main menu":
			self.display_main_menu()
		if self.state == "game":
			self.play_game()
		if self.state == "pause menu":
			self.display_pause_menu()
		if game.winner is not None:
			self.state = "main menu"

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

players = pygame.sprite.Group()
players.add(Player(True))
players.add(Player(False))

ball = pygame.sprite.GroupSingle()
ball.add(Ball())

game = Game(players.sprites(), ball.sprite)
game_state = GameState()


def background():
	bg = pygame.Surface((800,400))
	bg.fill("#0c2112")
	rect = bg.get_rect(center = (400,200))
	screen.blit(bg, rect)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_state.running = False

	if game_state.running:
		background()
		game_state.manage_states()

		pygame.display.update()
		clock.tick(60)
	else:
		break
pygame.quit()   