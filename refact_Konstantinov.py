import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __len__(self):
        return math.hypot(self.x, self.y)

    def __add__(self, other):
        return Vec2d(self.x+other.x, self.y+other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
   
    def __sub__(self, other):
        return Vec2d(self.x-other.x, self.y-other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.x -= other.y
        return self

    def __neg__(self):
        return Vec2d(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, int) or isinstance(other, float):
            return Vec2d(self.x * other, self.y * other)
    
    def int_pair(self):
        return int(self.x), int(self.y)

class Polyline:
    def __init__(self, display, points=None, points_speeds=None):
        self.display = display
        self.points = []
        self.speeds = []

        if((points is not None) and (points_speeds is not None)):
            for each_point in points:
                self.points.append(Vec2d(each_point[0], each_point[1]))
            for each_speed in points_speeds:
                self.speeds.append(Vec2d(each_speed[0], each_speed[1]))

    def draw_points(self, width=3, color=(255, 255, 255)):
        self.draw_line(style='points', line_points=self.points, width=width, color=color)

    def draw_line(self, style="points", line_points=[], width=3, color=(255, 255, 255)):
        if style == "line":
            for p_n in range(-1, len(line_points) - 1):
                pygame.draw.line(self.display, color, line_points[p_n].int_pair(),
                                line_points[p_n + 1].int_pair(), width)
        elif style == "points":
            for p in line_points:
                pygame.draw.circle(self.display, color, p.int_pair(), width)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d(self.speeds[p].x, -self.speeds[p].y)

    def add_point(self, point_to_add, speed_to_add):
        self.points.append(Vec2d(point_to_add[0], point_to_add[1]))
        self.speeds.append(Vec2d(speed_to_add[0], speed_to_add[1]))


class Knot(Polyline):
    def __init__(self, display, points=None, points_speeds=None):
        super().__init__(display, points, points_speeds) 

    def get_knot(self, count=0):
        if len(self.points) < 3:
            self.knot_points = []
        else:
            res = []
            for i in range(-2, len(self.points) - 2):
                ptn = []
                ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
                ptn.append(self.points[i + 1])
                ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
                if(count > 0):
                    res.extend(self._get_points(ptn, count))
            self.knot_points = res

    def _get_points(self, vec2d_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self._get_point(vec2d_points, i * alpha))
        return res

    def _get_point(self, vec2d_points, alpha, deg=None):
        if deg is None:
            deg = len(vec2d_points) - 1
        if deg == 0:
            return vec2d_points[0]
        return vec2d_points[deg]*alpha + self._get_point(vec2d_points, alpha, deg - 1)*(1 - alpha)

    def draw_knot(self, width=3, color=(255, 255, 255)):
        super().draw_line(style='line', line_points=self.knot_points, width=width, color=color)

    def set_points(self, count):
        super().set_points()
        self.get_knot(count=count)

    def add_point(self, point_to_add, speed_to_add, count):
        super().add_point(point_to_add, speed_to_add)
        self.get_knot(count=count)

    def pop_point(self, count):
        if(len(self.points)>0 and len(self.speeds)>0):
            self.points.pop()
            self.speeds.pop()
            self.get_knot(count=count)

class KnotDisplay(Knot):
    def __init__(self, display, new_knot=None):
        self.display = display
        self.knot_list = []
        self._max_idx = -1
        self._idx = -1
        if(new_knot is not None):
            self.knot_list.append(new_knot)
            self._max_idx = len(self.knot_list) - 1
            self._idx = self._max_idx

        self._hue = 0
        self._color = pygame.Color(0)

    def add_knot(self, knot_to_add):
        self.knot_list.append(knot_to_add)
        self._max_idx += 1
        self._idx = self._max_idx

    def pop_knot(self):
        if(self._max_idx >= 0):
            self.knot_list.pop(self._idx)
            self._max_idx -= 1
            self._idx = self._max_idx

    def get_next_knot(self):
        if(self._idx + 1)>self._max_idx:
            self._idx = 0
        else:
            self._idx += 1

    def get_max_idx(self):
        return self._max_idx

    def get_current_idx(self):
        return self._idx

    def draw_all(self, count):
        self.display.fill((0, 0, 0))
        if(self._max_idx >= 0):

            self._hue = (self._hue + 1) % 360
            self._color.hsla = (self._hue, 100, 50, 100)

            for each_knot in self.knot_list:
                each_knot.draw_points(color=self._color)
                each_knot.get_knot(count=count)
                each_knot.draw_knot(color=self._color)
        

    def set_all(self, count):
        if(self._max_idx >= 0):
            for each_knot in self.knot_list:
                each_knot.set_points(count=count)

    def draw_knot(self):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].draw_knot(color=self._color)

    def set_points(self, count):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].set_points(count=count)

    def get_knot(self, count):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].get_knot(count=count)

    def draw_points(self):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].draw_points(color=self._color)

    def add_point(self, point_to_add, speed_to_add, count):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].add_point(point_to_add, speed_to_add, count)
    
    def pop_point(self, count):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].pop_point(count)
            if(len(self.knot_list[self._idx].points)==0):
                self.pop_knot()

    def speed_up(self):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].speeds = [each_speed*2 
                                                for each_speed in self.knot_list[self._idx].speeds]

    def speed_down(self):
        if(self._max_idx >= 0):
            self.knot_list[self._idx].speeds = [each_speed*0.5 
                                                for each_speed in self.knot_list[self._idx].speeds]

    def restart_display(self):
        self.knot_list = []
        self._max_idx = -1
        self._idx = -1
        self.display.fill((0, 0, 0))

    def draw_help(self):
        self.display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["d", "Delete the last base point"])

        data.append(["a", "Add a new knot"])
        data.append(["n", "Select the next knot"])
        data.append(["DELETE", "Delete selected knot"])

        data.append(["Num*", "Speed up selected knot"])
        data.append(["Num/", "Speed down selected knot"])

        data.append([str(steps), "Current points"])
        data.append([str(len(self.knot_list)), "Current number of knots"])
        data.append([str(self._idx + 1), "Knot #"])
        data.append([str(len(self.knot_list[self._idx].points)), "Number of basepoints"])

        pygame.draw.lines(self.display, (255, 50, 50, 255), True, [
                        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    knot = Knot(display=gameDisplay)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    knot_display = KnotDisplay(display=gameDisplay, new_knot=knot)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knot_display.restart_display()
                    knot_display.add_knot(knot_to_add=Knot(gameDisplay))
                    pause = True
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

                if event.key == pygame.K_d:
                    knot_display.pop_point(count = steps)
                    if knot_display.get_max_idx() == -1:
                        knot_display.add_knot(knot_to_add=Knot(gameDisplay))
                if event.key == pygame.K_n:
                    knot_display.get_next_knot()
                if event.key == pygame.K_DELETE:
                    knot_display.pop_knot()
                    if knot_display.get_max_idx() == -1:
                        knot_display.add_knot(knot_to_add=Knot(gameDisplay))
                if event.key == pygame.K_a:
                    knot_display.add_knot(knot_to_add=Knot(gameDisplay))
                if event.key == pygame.K_KP_MULTIPLY:
                    knot_display.speed_up()
                if event.key == pygame.K_KP_DIVIDE:
                    knot_display.speed_down()
                

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot_display.add_point(event.pos, (random.random() * 2, random.random() * 2), count = steps)

        knot_display.draw_all(count=steps)
        if not pause:
            knot_display.set_all(count = steps)
        if show_help:
            knot_display.draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)