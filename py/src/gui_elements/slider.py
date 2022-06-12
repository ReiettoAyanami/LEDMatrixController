from math import dist
from src.gui_elements.utils import maprange
import pygame
from pygame import gfxdraw
from src.gui_elements.button import Button


class Slider:

    def __init__(self, rect, range = (0,1), rtype = float, main_color = (100,100,100), button_color = (200,200,200), dragging_distance = 1000) -> None:
        
        self.rect = pygame.Rect(rect)
        self.range = range
        self.rtype = rtype
        self.main_color = main_color
        self.button_color = button_color

        self.button_rect = pygame.Rect(self.rect.x,self.rect.y,self.rect.w / 10, self.rect.h * 1.5)
        self.button_rect.centery = self.rect.centery
        self.button_rect.centerx = self.rect.x

        self.dragging = False
        self.dragging_dist = dragging_distance

    def show(self, surface):

        gfxdraw.box(surface, self.rect, self.main_color)
        gfxdraw.rectangle(surface, self.rect, (0,0,0))
        gfxdraw.box(surface, self.button_rect, self.button_color)
        gfxdraw.rectangle(surface, self.button_rect, (0,0,0))

    def update(self, events):
        if events['mouse_pressed']['left'] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.dragging = True
        elif dist(pygame.mouse.get_pos(), self.rect.center) >= self.dragging_dist or not events['mouse_pressed']['left']:
            self.dragging = False
        
        if self.dragging:
            self.button_rect.centerx = pygame.mouse.get_pos()[0]

        if self.button_rect.centerx <= self.rect.x:
            self.button_rect.centerx = self.rect.x
        elif self.button_rect.centerx >= self.rect.right:
            self.button_rect.x = self.rect.right


    def get_value(self):
        return self.rtype(maprange(self.button_rect.x, (self.rect.x - self.button_rect.w // 2, self.rect.right), self.range))