import flet as ft
from config import AppConfig

class ServiceCard:
    def __init__(self, service_data, on_click=None):
        self.service_data = service_data
        self.on_click = on_click
        self.config = AppConfig()

    def build(self) -> ft.Control:
        """Build a service card with modern design"""
        title = self.service_data.get('title', 'Услуга')
        description = self.service_data.get('description', 'Описание услуги')
        price = self.service_data.get('price', '0 ₽')
        duration = self.service_data.get('duration', '60 мин')

        card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        width=48,
                        height=48,
                        border_radius=24,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[self.config.colors['primary'], self.config.colors['secondary']]
                        ),
                        content=ft.Icon(name="SPA", size=28, color=self.config.colors['surface']),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        title,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=self.config.colors['text_primary_dark'],
                        expand=True,
                        font_family=self.config.fonts['Poppins']
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(height=12),
                ft.Text(
                    description,
                    size=15,
                    color=self.config.colors['text_secondary'],
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    font_family=self.config.fonts['Poppins']
                ),
                ft.Container(height=20),
                ft.Row([
                    ft.Column([
                        ft.Text(
                            price,
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=self.config.colors['primary'],
                            font_family=self.config.fonts['Poppins']
                        ),
                        ft.Text(
                            duration,
                            size=14,
                            color=self.config.colors['text_secondary'],
                            font_family=self.config.fonts['Poppins']
                        ),
                    ], spacing=4),
                    ft.Container(expand=True),
                    ft.Container(
                        width=48,
                        height=48,
                        border_radius=24,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[self.config.colors['primary'], self.config.colors['secondary']]
                        ),
                        content=ft.Icon(
                            name="ADD_CIRCLE",
                            size=28,
                            color=self.config.colors['surface']
                        ),
                        alignment=ft.alignment.center,
                        on_click=self._on_click,
                        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ],
            spacing=0
            ),
            padding=ft.padding.all(24),
            bgcolor=self.config.colors['glass_bg'],
            border_radius=self.config.sizes['border_radius'] * 2,
            border=ft.border.all(1, self.config.colors['glass_border']),
            blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
            shadow=ft.BoxShadow(blur_radius=30, spread_radius=5, color="#0000001A"),
            on_click=self._on_click,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e, card=card: self._card_hover_effect(e, card)
        )
        return card

    def _card_hover_effect(self, e, card):
        """Effect on hover"""
        if e.data == "true":
            card.shadow = ft.BoxShadow(
                blur_radius=50,
                spread_radius=5,
                color="#0000002A"
            )
            card.border = ft.border.all(2, self.config.colors['primary'])
        else:
            card.shadow = ft.BoxShadow(
                blur_radius=30,
                spread_radius=5,
                color="#0000001A"
            )
            card.border = ft.border.all(1, self.config.colors['glass_border'])
        card.update()

    def _on_click(self, e):
        if self.on_click:
            self.on_click(self.service_data.get('id'))