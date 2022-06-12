from operator import ipow
from tkinter.messagebox import RETRY
import py
import pygame
from pygame import gfxdraw
from src.gui_elements.utils import *
from src.gui_elements.button import Button

class Image_Button(Button):

    def __init__(self, rect,image, outline_colors = (255,255,255,255), show_shadow = False, shadow_size = 20, shadow_color = [0,0,0,10], border_radius = 0.4, outline_thickness =  1) -> None:
        super().__init__(rect, None)


        self.rect = pygame.Rect(rect)
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))
        self.border_r = border_radius

        self.image_surface = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        AAfilledRoundedRect(self.image_surface, (0,0, self.rect.w, self.rect.h), (255,255,255), self.border_r)
        self.image_surface.blit(self.image, (0,0), special_flags=pygame.BLEND_RGBA_MIN)





        self.show_shadow = show_shadow
        if outline_thickness:
            self.outline_colors = outline_colors
            self.outline_thickness = outline_thickness
            self.outline_surface = pygame.Surface((self.rect.w + outline_thickness * 2, self.rect.h + outline_thickness * 2), pygame.SRCALPHA)
            gradient_aaroundedrectangle(self.outline_surface, (0,0,self.rect.w + outline_thickness * 2, self.rect.h + outline_thickness * 2), self.outline_colors, border_r= border_radius)


        self.show_shadow = show_shadow
        self.shadow_size = shadow_size
        self.SHADOW_OFFSET = shadow_size * 2
        self.shadow_color = shadow_color

        self.shadow = pygame.Surface((self.rect.w + self.SHADOW_OFFSET + self.shadow_size, self.rect.h + self.SHADOW_OFFSET + self.shadow_size), pygame.SRCALPHA)
        self.shadow_rect = pygame.Rect((self.rect.x - self.SHADOW_OFFSET // 2 - self.shadow_size // 2, self.rect.y + self.SHADOW_OFFSET // 2 - self.shadow_size // 2,  self.shadow.get_width(), self.shadow.get_height()))
        self.shadow_rect.center = self.rect.center
        shadow_draw_rect = pygame.Rect(0,0,self.shadow_rect.w - self.SHADOW_OFFSET //2 - self.shadow_size //2, self.shadow_rect.h - self.SHADOW_OFFSET //2 - self.shadow_size //2)
        shadow_draw_rect.center = self.shadow.get_rect().center
        gfxdraw.box(self.shadow, shadow_draw_rect, self.shadow_color)
        self.shadow = BloomNoPremultipliedAlpha(self.shadow)

    def show(self, surface):
        
        if self.show_shadow:
            surface.blit(self.shadow, self.shadow_rect)
        surface.blit(self.outline_surface, (self.rect.x - self.outline_thickness,self.rect.y - self.outline_thickness))
        surface.blit(self.image_surface, self.rect)


        
        