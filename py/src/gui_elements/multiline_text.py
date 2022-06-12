from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
from ctypes import c_char_p
from pygame import Rect, font
from itertools import chain
import pygame
from src.gui_elements.utils import *


class Multiline_Text():


    def __init__(self, font,text:str,pos, color, AA = True,  max_width = 120) -> None:
        
        self.font:pygame.font.SysFont or pygame.font.Font = font
        self.raw_text:str = text
        self.color = color
        self.multiline_text = wrap_multi_line(self.raw_text, font, max_width)
        self.pos = pos
        self.text_surfaces = []
        for string in self.multiline_text:
            self.text_surfaces.append(self.font.render(string, AA,self.color))


        max_length_record = self.text_surfaces[0].get_width()
        total_height = 0
        for s in self.text_surfaces:
            
            total_height += s.get_height()
            max_length_record = max(max_length_record, s.get_width())
            

        self.blit_surf = pygame.Surface((max_length_record, total_height), pygame.SRCALPHA)


        current_y = 0
        for s in self.text_surfaces:
            self.blit_surf.blit(s, (0, current_y))
            current_y += s.get_height()

        
    def get(self):
        return self.blit_surf

    def get_rect(self) -> pygame.Rect:

        return pygame.Rect(self.pos[0], self.pos[1], self.blit_surf.get_width(), self.blit_surf.get_height())