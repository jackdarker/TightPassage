import pygame

def get_images(sheet, frame_indices, size):
    """Get desired images from a sprite sheet image."""
    frames = []
    for cell in frame_indices:
        frame_rect = ((size[0]*cell[0],size[1]*cell[1]), size)
        frames.append(sheet.subsurface(frame_rect))
    return frames
