import pygame

class Menu:
    def __init__(self, screen, font, title_font, mixer):
        self.screen = screen
        self.font = font
        self.title_font = title_font
        self.mixer = mixer

        # Settings volumes
        self.bgm_volume = 0.5
        self.sfx_volume = 0.5
        self.mixer.music.set_volume(self.bgm_volume)

    def draw_options(self, title, options, selected):
        """Draw a menu with a title and boxed options."""
        self.screen.fill((0, 0, 50))
        title_text = self.title_font.render(title, True, (255, 255, 255))
        self.screen.blit(title_text, (200, 100))

        start_y = 250
        spacing = 70
        for i, text in enumerate(options):
            if i == selected:
                box_color = (255, 255, 0)
                txt_color = (0, 0, 0)
            else:
                box_color = (200, 200, 200)
                txt_color = (0, 0, 0)

            box = pygame.Rect(200, start_y + i * spacing, 400, 50)
            pygame.draw.rect(self.screen, box_color, box, border_radius=10)

            txt = self.font.render(text, True, txt_color)
            txt_rect = txt.get_rect(center=box.center)
            self.screen.blit(txt, txt_rect)

    def main_menu(self):
        """Main menu with Play, Settings, Quit."""
        options = ["Play", "Settings", "Quit"]
        selected = 0
        while True:
            self.draw_options("SPACE SHOOTER", options, selected)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return options[selected].lower()

    def settings_menu(self):
        """Settings menu with volume controls."""
        options = [
            f"BGM Volume: {int(self.bgm_volume*10)}/10",
            f"SFX Volume: {int(self.sfx_volume*10)}/10",
            "Back"
        ]
        selected = 0
        while True:
            # Update dynamic options
            options[0] = f"BGM Volume: {int(self.bgm_volume*10)}/10"
            options[1] = f"SFX Volume: {int(self.sfx_volume*10)}/10"

            self.draw_options("SETTINGS", options, selected)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_LEFT:
                        if selected == 0:
                            self.bgm_volume = max(0, self.bgm_volume - 0.1)
                            self.mixer.music.set_volume(self.bgm_volume)
                        elif selected == 1:
                            self.sfx_volume = max(0, self.sfx_volume - 0.1)
                    elif event.key == pygame.K_RIGHT:
                        if selected == 0:
                            self.bgm_volume = min(1, self.bgm_volume + 0.1)
                            self.mixer.music.set_volume(self.bgm_volume)
                        elif selected == 1:
                            self.sfx_volume = min(1, self.sfx_volume + 0.1)
                    elif event.key == pygame.K_RETURN:
                        if selected == 2:  # Back
                            return "back"

    def game_over_menu(self, score):
        """Game Over menu with Restart, Main Menu, Quit."""
        options = ["Restart Game", "Main Menu", "Quit"]
        selected = 0
        while True:
            self.screen.fill((0, 0, 0))
            title = self.title_font.render("GAME OVER", True, (255, 255, 255))
            self.screen.blit(title, (220, 100))

            score_txt = self.font.render(f"Your Score: {score}", True, (255, 255, 255))
            self.screen.blit(score_txt, (300, 200))

            # Draw options
            start_y = 300
            spacing = 70
            for i, text in enumerate(options):
                if i == selected:
                    box_color = (255, 255, 0)
                    txt_color = (0, 0, 0)
                else:
                    box_color = (200, 200, 200)
                    txt_color = (0, 0, 0)

                box = pygame.Rect(200, start_y + i * spacing, 400, 50)
                pygame.draw.rect(self.screen, box_color, box, border_radius=10)

                txt = self.font.render(text, True, txt_color)
                txt_rect = txt.get_rect(center=box.center)
                self.screen.blit(txt, txt_rect)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return options[selected].lower().replace(" ", "_")
