import flet as ft
from config import AppConfig

class MasterCard:
    def __init__(self, master_data, on_click=None, on_book=None):
        self.master_data = master_data
        self.on_click = on_click
        self.on_book = on_book
        self.config = AppConfig()

    def build(self) -> ft.Control:
        """Build the card as a Container with modern design"""
        name = self.master_data.get('name') or self.master_data.get('user_id') or "Мастер"
        services = self.master_data.get('bio') or "Услуги не указаны"
        location = self.master_data.get('location') or "Город не указан"
        rating = self.master_data.get('rating', 4.5)
        reviews = self.master_data.get('reviews', 0)
        photo_url = self.master_data.get('profile_image_path')

 
        if photo_url:
            photo = ft.Container(
                width=90,
                height=90,
                border_radius=45,
                content=ft.Image(
                    src=photo_url,
                    fit=ft.ImageFit.COVER,
                    border_radius=45,
                ),
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(blur_radius=15, color="#0000002A"),
            )
        else:
            photo = ft.Container(
                width=90,
                height=90,
                border_radius=45,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[self.config.colors['secondary'], self.config.colors['primary']]
                ),
                content=ft.Icon(name="PERSON", size=44, color=self.config.colors['surface']),
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(blur_radius=15, color="#0000002A"),
            )

 
        rating_row = ft.Row([
            ft.Icon(name="STAR", size=18, color=self.config.colors['warning']),
            ft.Text(f"{rating:.1f}", size=16, weight=ft.FontWeight.W_600, color=self.config.colors['text_primary_dark'], font_family=self.config.fonts['Poppins']),
            ft.Text(f"({reviews})", size=14, color=self.config.colors['text_secondary'], font_family=self.config.fonts['Poppins']),
        ], spacing=6, alignment=ft.MainAxisAlignment.CENTER)

        card = ft.Container(
            content=ft.Column([
                photo,
                ft.Container(height=16),
                ft.Text(
                    name,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=self.config.colors['text_primary_dark'],
                    text_align=ft.TextAlign.CENTER,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    font_family=self.config.fonts['Poppins']
                ),
                ft.Container(height=8),
                ft.Text(
                    services,
                    size=14,
                    color=self.config.colors['text_secondary'],
                    text_align=ft.TextAlign.CENTER,
                    max_lines=2,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    font_family=self.config.fonts['Poppins']
                ),
                ft.Container(height=12),
                ft.Row([
                    ft.Icon(name="LOCATION_ON", size=14, color=self.config.colors['accent']),
                    ft.Text(
                        location,
                        size=13,
                        color=self.config.colors['text_secondary'],
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        expand=True,
                        font_family=self.config.fonts['Poppins']
                    )
                ], spacing=6),
                ft.Container(height=16),
                rating_row,
                ft.Container(height=20),
                ft.Container(
                    width=140,
                    height=40,
                    border_radius=self.config.sizes['border_radius'],
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[self.config.colors['primary'], self.config.colors['secondary']]
                    ),
                    content=ft.Text(
                        "Записаться",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=self.config.colors['surface'],
                        font_family=self.config.fonts['Poppins']
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(blur_radius=10, spread_radius=0, color=self.config.colors['primary'] + "80"),
                    on_click=self._on_book_click,
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
            ),
            width=200,
            padding=ft.padding.all(20),
            bgcolor=self.config.colors['glass_bg'],
            border_radius=self.config.sizes['border_radius'] * 2,
            border=ft.border.all(1, self.config.colors['glass_border']),
            blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
            shadow=ft.BoxShadow(blur_radius=30, spread_radius=5, color="#0000001A"),
            on_click=self._on_card_click,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            on_hover=lambda e, card=self: self._card_hover_effect(e, card)
        )
        return card

    def _card_hover_effect(self, e, card):
        """Effect on hover"""
        if e.data == "true":
            card.scale = 1.05
            card.elevation = 10
        else:
            card.scale = 1.0
            card.elevation = 0
        card.update()

    def _on_card_click(self, e):
        if self.on_click:
            self.on_click(self.master_data.get('id'))

    def _on_book_click(self, e):
        e.stop_propagation()
        if self.on_book:
            self.on_book(self.master_data.get('id'))