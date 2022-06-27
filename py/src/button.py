import imp
import pygame
from pygame import gfxdraw
from src.utils import * 


class Button():
    
    def __init__(self, rect:pygame.Rect or list[int,int,int,int], color:tuple[int,int,int,int] = (100,100,100,255), outline_color:tuple[int,int,int,int] = (255,255,255,255), outline_thickness = 1, corners = {'topleft':0, 'topright':0, 'bottomleft':0, 'bottomright':0}) -> None:
        self.rect = pygame.Rect(rect)
        self.color = color
        self.outline_thickness = outline_thickness
        self.corners = corners
        self.outline_color = outline_color
        self.can_be_clicked = True
        

    def show(self, surface:pygame.Surface) -> None:
        # Box per il contorno
        
        pygame.draw.rect(surface,self.color,self.rect,
                            border_top_left_radius=self.corners.get('topleft'),
                            border_top_right_radius=self.corners.get('topright'),
                            border_bottom_left_radius=self.corners.get('bottomleft'),
                            border_bottom_right_radius=self.corners.get('bottomright'))

        #Rectangle per il fill
        pygame.draw.rect(surface, self.outline_color, self.rect, self.outline_thickness,                            
                            border_top_left_radius=self.corners.get('topleft'),
                            border_top_right_radius=self.corners.get('topright'),
                            border_bottom_left_radius=self.corners.get('bottomleft'),
                            border_bottom_right_radius=self.corners.get('bottomright'))

    
    def set_corners(self,new_corners_radius:int):

        self.corners = new_corners_radius


    def glow(self, surface, color:tuple or pygame.Color):
        gfxdraw.box(surface, self.rect, color)



    def hover(self) -> bool:
        
        return True if self.rect.collidepoint(pygame.mouse.get_pos()) else False



    def on_event(self, event:bool, func = None):
        
        if event and (func is not None):
            return func()

    