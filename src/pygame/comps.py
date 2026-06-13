import pygame

from core.eventSystem import EventTarget


class UIElement(EventTarget):
  def __init__(self, x: int, y: int, width: int, height: int) -> None:
    super().__init__()
    # 1. Define geometry using a Rect for clean boundary math
    self.rect = pygame.Rect(x, y, width, height)
    self.style = {}

  def draws(self):
    pass


class UIButton(UIElement):
  def __init__(
    self, x: int, y: int, width: int, height: int, text: str, font_size: int = 24
  ):
    super().__init__(x, y, width, height)
    self.text = text

    # 2. Font configuration
    self.font = pygame.font.SysFont("Arial", font_size, bold=True)

    # 3. Dynamic styling states (No cheap icons, just modern clean lines)
    self.color_normal = (50, 50, 50)  # Dark Gray
    self.color_hover = (70, 70, 70)  # Slightly lighter gray
    self.color_text = (240, 240, 240)  # Off-white
    self.color_border = (100, 100, 100)  # Subtle boundary line

    self.is_hovered = False

  def handle_event(self, event: pygame.event.Event) -> bool:
    """
    Processes mouse interaction.
    Returns True ONLY on a valid mouse click release inside the button bounds.
    """
    # Track where the cursor is currently sitting
    mouse_pos = pygame.mouse.get_pos()
    self.is_hovered = self.rect.collidepoint(mouse_pos)

    # Check for a mouse button release event
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      if self.is_hovered:
        self.dispatch_event("click")
        return True  # Signal that the button action should fire!

    return False

  def draw(self, surface: pygame.Surface):
    """Renders the button base, dynamic hover states, and perfectly centered text."""
    # 1. Pick background color based on hover state
    current_color = self.color_hover if self.is_hovered else self.color_normal

    # 2. Draw the background and a sleek 1px border
    pygame.draw.rect(surface, current_color, self.rect)
    pygame.draw.rect(surface, self.color_border, self.rect, 1)

    # 3. Render and center the text inside the bounding box
    # True flags anti-aliasing for smooth font edges
    text_surface = self.font.render(self.text, True, self.color_text)
    text_rect = text_surface.get_rect()

    # Magically center the text canvas directly over the button canvas center
    text_rect.center = self.rect.center

    # Blit text to screen
    surface.blit(text_surface, text_rect)
