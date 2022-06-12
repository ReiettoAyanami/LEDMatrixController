from doctest import set_unittest_reportflags
from turtle import ontimer
from pygame import *
import pygame, cv2 
import numpy as np
from itertools import chain


def maprange(s, a, b):
	(a1, a2), (b1, b2) = a, b
	return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size,SRCALPHA)

    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)


def hexa_to_rgb(s:str):
	conv_s = []
	s = s[1:]
	lookup = "0123456789abcdef"
	s = s.lower()
	for i in range(0,(len(s) - 1),2):
		conv_s.append((lookup.index(s[i])) + ((lookup.index(s[i+1]) * (16))))
	return conv_s


def BloomNoPremultipliedAlpha(canvas: pygame.Surface):
    size = canvas.get_size()
    canvas_color = pygame.surfarray.array2d(canvas)
    canvas_rgba = canvas_color.view(dtype=np.uint8).reshape((*canvas_color.shape, 4))
    newCanvas = pygame.Surface(size, pygame.SRCALPHA)
    cv2.blur(canvas_rgba, ksize=(25, 25), dst=canvas_rgba)

    canvas_rgba[:,:,0:3] = canvas_rgba[:,:,0:3] * 255.0 / canvas_rgba[:,:,[3,3,3]]

    pygame.surfarray.blit_array(newCanvas, canvas_color)
    return newCanvas


def gradient_rectangle_horizontal(surface, rect, colors):

    rect = pygame.Rect(*rect)
            
    rect_surf = pygame.Surface((len(colors), 1), pygame.SRCALPHA)
    
    for i, color in enumerate(colors):
        rect_surf.set_at((i, 0), color)

    rect_surf = pygame.transform.smoothscale(rect_surf, (rect.w, rect.h))

    surface.blit(rect_surf, (rect.x, rect.y))


def gradient_rectangle_vertical(surface, rect, colors):

    rect = pygame.Rect(*rect)
            
    rect_surf = pygame.Surface((1,len(colors)), pygame.SRCALPHA)
    
    for i, color in enumerate(colors):
        rect_surf.set_at((0, i), color)

    rect_surf = pygame.transform.smoothscale(rect_surf, (rect.w, rect.h))

    surface.blit(rect_surf, (rect.x, rect.y))

    


def gradient_aaroundedrectangle_vertical(surface, rect, colors, border_r = .4):

    rect = pygame.Rect(*rect)
    aarect_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    AAfilledRoundedRect(aarect_surf, (0,0,rect.w, rect.h), (255,255,255), border_r)
            
    gradient_rect_surf = pygame.Surface((1,len(colors)), pygame.SRCALPHA)
    
    for i, color in enumerate(colors):
        gradient_rect_surf.set_at((0, i), color)

    gradient_rect_surf = pygame.transform.smoothscale(gradient_rect_surf, (rect.w, rect.h))

    aarect_surf.blit(gradient_rect_surf, (0,0), special_flags=pygame.BLEND_RGB_MULT)

    surface.blit(aarect_surf, (rect.x, rect.y))


def gradient_aaroundedrectangle_horiziontal(surface, rect, colors, border_r = .4):

    rect = pygame.Rect(*rect)
    aarect_surf = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    AAfilledRoundedRect(aarect_surf, (0,0,rect.w, rect.h), (255,255,255), border_r)
            
    gradient_rect_surf = pygame.Surface((len(colors), 1), pygame.SRCALPHA)
    
    for i, color in enumerate(colors):
        gradient_rect_surf.set_at((i, 0), color)

    gradient_rect_surf = pygame.transform.smoothscale(gradient_rect_surf, (rect.w, rect.h))

    aarect_surf.blit(gradient_rect_surf, (0,0), special_flags=pygame.BLEND_RGB_MULT)

    surface.blit(aarect_surf, (rect.x, rect.y))


def gradient_aaroundedrectangle(surface, rect, colors, border_r =.4, gradient_direction = 0):

    if gradient_direction == 0:
        gradient_aaroundedrectangle_horiziontal(surface, rect, colors, border_r)
    else:
        gradient_aaroundedrectangle_vertical(surface, rect, colors,border_r)

def gradient_rectangle(surface, rect, colors, gradient_direction):

    if gradient_direction == 0:
        gradient_rectangle_horizontal(surface, rect, colors)
    else:
        gradient_rectangle_vertical(surface, rect, colors)


def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)