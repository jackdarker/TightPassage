import pygame

def get_images(sheet, frame_indices, size):
    """Get desired images from a sprite sheet image."""
    frames = []
    for cell in frame_indices:
        frame_rect = ((size[0]*cell[0],size[1]*cell[1]), size)
        frames.append(sheet.subsurface(frame_rect))
    return frames

def get_allImages(sheet,size):
    """Get images from a sprite sheet image.
    returns a list of tiles from top left to bottom right
    """
    frames = []
    maxx = sheet.get_width() // size[0]
    maxy = sheet.get_height() // size[1]
    for x in range(0, maxx):
        for y in range(0, maxy):
            frame_rect = ((size[0]*x,size[1]*y), size)
            frames.append(sheet.subsurface(frame_rect))
    return frames

def get_allImagesInDirectory(sheet,size):
    """Get images from a sprite sheet image.
    returns a list of tiles from top left to bottom right
    """
    #todo
    frames = []
    maxx = sheet.get_width() // size[0]
    maxy = sheet.get_height() // size[1]
    for x in range(0, maxx):
        for y in range(0, maxy):
            frame_rect = ((size[0]*x,size[1]*y), size)
            frames.append(sheet.subsurface(frame_rect))
    return frames