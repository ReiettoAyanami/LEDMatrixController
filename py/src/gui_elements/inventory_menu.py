import pygame
from pygame import Rect
from src.gui_elements.image_button import *
from src.gui_elements.string_button import String_Button

class Inventory_Menu:


    def __init__(self,images:list[pygame.Surface],coords:tuple[int,int] or pygame.Vector2 = pygame.Vector2(0,0),row_length:int = 10, button_dimension:int = 10, button_offset = pygame.Vector2(5,5), trigger_text:str = 'Inventory', color = (0,0,0,50), outline_color = (255,255,255,255), hovering_color = (255,255,255,50)) -> None:
        
        
        self.is_open = False
        self.button_dimension = button_dimension
        self.coords = pygame.Vector2(coords)
        self.row_length = row_length
        self.button_dimension = button_dimension
        self.selected = 0
        self.color = color
        self.outline_color = outline_color
        self.hover_color = hovering_color

        # Convert normal array to bi-dimensional array
        self.board = [[]]
        j = 0
        for i in range(len(images)):

            if i % row_length == 0 and i != 0:
                self.board.append([])
                j += 1 
            
            self.board[j].append(Image_Button(
                (
                    (
                        (i - (row_length * j)) * button_dimension) + (button_offset.x * (i - ((row_length * j)) + 1 )), # for x
                        (j * button_dimension) + (button_offset.y * (j + 1)) + (button_dimension + button_offset.y), # for y
                        button_dimension, button_dimension), 
                        images[i],
                        outline_color = self.outline_color

                    )
                )

        # --- 
        
        
        # Hitboxes exc...

        self.rect = pygame.Rect(
                (
                    self.coords.x,self.coords.y,
                    row_length * button_dimension + (button_offset.x * (row_length + 1)), # for width
                    len(self.board) * button_dimension + (button_offset.y * (len(self.board) + 1)) # for height
                
                ) 
            )

        
        self.rect.y += button_dimension + button_offset.y


        self.trigger_button = String_Button(
                pygame.Rect(
                        self.rect.x, # x
                        self.rect.y - (button_dimension + button_offset.y), # y 
                        self.rect.w, # w
                        (button_dimension  + button_offset.y) # h
                    ), 
                trigger_text , pygame.font.SysFont('arial', button_dimension//2), # font 
                color = self.color, 
                outline_color=self.outline_color
            )

        # ---
    
    def show(self, surface:pygame.Surface):
        
        self.trigger_button.show(surface)
        if self.trigger_button.hover():
                gfxdraw.box(surface, self.trigger_button.rect, self.hover_color)

        if self.is_open:
            gfxdraw.box(surface, self.rect, self.color)
            gfxdraw.rectangle(surface, self.rect, self.color)


            for j in range(len(self.board)):
                for i in range(len(self.board[j])):
                    
                    
                    self.board[j][i].show(surface)
                

                    if self.board[j][i].hover():
                        gfxdraw.box(surface, self.board[j][i].rect, self.hover_color)
                    

    def update(self, events:dict):
        
        o = self.trigger_button.on_event(self.trigger_button.hover() and events.get('mouse_clicked').get('left'), lambda: not self.is_open)
        self.is_open = o if o is not None else self.is_open

        if self.is_open:
            for j in range(len(self.board)):
                for i in range(len(self.board[j])):
                    
                    item_index = self.board[j][i].on_event(self.board[j][i].hover() and events.get('mouse_clicked').get('left'), lambda: (j * self.row_length) + i)

                    self.selected = item_index if item_index is not None else self.selected

                
    def hover(self) -> bool:
        return True if self.rect.collidepoint(pygame.mouse.get_pos()) or self.trigger_button.hover() else False
    
    def get_selected(self):
        return self.selected



    