from sys import flags
from cv2 import randShuffle
from src.gui_elements.multiline_text import Multiline_Text
from src.gui_elements.button import Button
import pygame
import pygame.font
from pygame import gfxdraw
from src.gui_elements.utils import AAfilledRoundedRect
from src.gui_elements.utils import *
import math

pygame.font.init()




class String_Button(Button):

    def __init__(self,rect,text,font = pygame.font.SysFont('Arial',10),value = None, text_color = (255,255,255,255), colors = [(100,100,100),(0,0,0)], outline_colors = [(255,255,255),(0,0,0)], text_offset =  pygame.Vector2(10,5), border_radius = 0, outline_thickness = 0, alpha = 255, text_alpha = 255, show_shadow = False, shadow_size = 20, shadow_color = [0,0,0,10], gradient_direction = 0, max_button_width = 200) -> None:
        super().__init__(rect, None, None)



        self.__text_offset = pygame.Vector2(text_offset)
        self.font =font
        self.text_color = text_color
        self.value = value
        self.border_r = border_radius
        self.outline_thickness = outline_thickness
        self.colors = colors
        self.shadow_updated = False
        self.outline_colors = outline_colors

        self.text = Multiline_Text(self.font, text, (0,0), self.text_color, AA = True, max_width= max_button_width).get() 
        self.text_rect = self.text.get_rect()
        self.rect = pygame.Rect(self.rect.x - self.__text_offset.x - self.outline_thickness, self.rect.y - self.__text_offset.y - self.outline_thickness, self.text_rect.w  + self.__text_offset.x + (self.outline_thickness * 2), self.text_rect.h + self.__text_offset.y + (self.outline_thickness * 2))
        self.text_rect.center =  (self.rect.x + (self.rect.w / 2), self.rect.y + (self.rect.h / 2))
        self.text.set_alpha(text_alpha)
        self.gradient_direction = gradient_direction
        self.__temp_surf = pygame.Surface((self.rect.w,self.rect.h), pygame.SRCALPHA, 32)
        self.__temp_surf.set_alpha(alpha)

        if self.outline_thickness:
            gradient_aaroundedrectangle(self.__temp_surf, (0,0,self.rect.w,self.rect.h),self.outline_colors, self.border_r, gradient_direction)
        gradient_aaroundedrectangle(self.__temp_surf, (self.outline_thickness // 2,self.outline_thickness // 2,self.rect.w - self.outline_thickness,self.rect.h - self.outline_thickness),self.colors, self.border_r, gradient_direction)

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

    def show(self,surface:pygame.Surface):


        if self.outline_thickness:
            gradient_aaroundedrectangle(self.__temp_surf, (0,0,self.rect.w,self.rect.h),self.outline_colors, self.border_r, self.gradient_direction)
        gradient_aaroundedrectangle(self.__temp_surf, (self.outline_thickness // 2,self.outline_thickness // 2,self.rect.w - self.outline_thickness,self.rect.h - self.outline_thickness),self.colors, self.border_r, self.gradient_direction)

        self.shadow = pygame.Surface((self.rect.w + self.SHADOW_OFFSET + self.shadow_size, self.rect.h + self.SHADOW_OFFSET + self.shadow_size), pygame.SRCALPHA)
        self.shadow_rect = pygame.Rect((self.rect.x - self.SHADOW_OFFSET // 2 - self.shadow_size // 2, self.rect.y + self.SHADOW_OFFSET // 2 - self.shadow_size // 2,  self.shadow.get_width(), self.shadow.get_height()))
        self.shadow_rect.center = self.rect.center
        shadow_draw_rect = pygame.Rect(0,0,self.shadow_rect.w - self.SHADOW_OFFSET //2 - self.shadow_size //2, self.shadow_rect.h - self.SHADOW_OFFSET //2 - self.shadow_size //2)
        shadow_draw_rect.center = self.shadow.get_rect().center
        gfxdraw.box(self.shadow, shadow_draw_rect, self.shadow_color)
        self.shadow = BloomNoPremultipliedAlpha(self.shadow)


        if not self.shadow_updated:
            self.shadow_rect.center = self.rect.center
            self.shadow_updated = True

        surface.blit(self.shadow, self.shadow_rect)
        surface.blit(self.__temp_surf, self.rect)
        surface.blit(self.text,self.text_rect)