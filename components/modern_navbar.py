import flet as ft
from config import AppConfig

class ModernNavbar:
    def __init__(self, page: ft.Page, current_tab: str = "home", app=None, tabs=None):
        self.page = page
        self.app = app
        self.current_tab = current_tab  # expected to be label lowercased or route
        self.config = AppConfig()
        self.tabs = tabs or self._default_tabs()
        self.setup_controls()

    def _default_tabs(self):
        """Default tabs for client space"""
        return [
            {"icon": "HOME", "label": "Главная", "route": "/client/home"},
            {"icon": "SEARCH", "label": "Поиск", "route": "/client/search"},
            {"icon": "CALENDAR_TODAY", "label": "Записи", "route": "/client/bookings"},
            {"icon": "PERSON", "label": "Профиль", "route": "/client/profile"},
        ]

    def setup_controls(self):
        """Create navbar items with modern design"""
        self.nav_items = []
        for tab in self.tabs:
 
            is_active = (self.current_tab.lower() == tab["label"].lower() or
                         self.current_tab.lower() in tab["route"].lower())
            color = self.config.colors['primary'] if is_active else self.config.colors['text_secondary']
            bgcolor = self._with_opacity(self.config.colors['primary'], 0.15) if is_active else "transparent"

            item = ft.Container(
                content=ft.Column([
                    ft.Icon(tab["icon"], size=30, color=color),
                    ft.Text(tab["label"], size=12, color=color, weight=ft.FontWeight.W_600, font_family=self.config.fonts['Poppins'])
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6
                ),
                padding=ft.padding.symmetric(vertical=12, horizontal=20),
                border_radius=self.config.sizes['border_radius'] * 1.5,
                bgcolor=bgcolor,
                on_click=lambda e, r=tab["route"]: self._navigate(r),
                data=tab["route"],
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )
            item.on_hover = lambda e, it=item: self._item_hover_effect(e, it)
            self.nav_items.append(item)

        self.navbar = ft.Container(
            content=ft.Row(
                controls=self.nav_items,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=16, horizontal=28),
            bgcolor=self.config.colors['glass_bg'],
            border_radius=ft.border_radius.only(top_left=32, top_right=32),
            border=ft.border.all(1, self.config.colors['glass_border']),
            blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
            shadow=ft.BoxShadow(
                blur_radius=40,
                spread_radius=-10,
                color="#0000001A"
            )
        )

    def _with_opacity(self, hex_color, opacity):
        """Convert hex color to rgba string with given opacity (0-1)"""
 
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{opacity})"

    def _item_hover_effect(self, e, item):
        """Effect on hover for navbar items"""
        if e.data == "true":
            item.bgcolor = self._with_opacity(self.config.colors['primary'], 0.2)
            item.shadow = ft.BoxShadow(
                blur_radius=20,
                spread_radius=0,
                color=self.config.colors['primary'] + "40"
            )
        else:
 
            is_active = self._is_item_active(item)
            item.bgcolor = self._with_opacity(self.config.colors['primary'], 0.15) if is_active else "transparent"
            item.shadow = None
        item.update()

    def _is_item_active(self, item):
        """Check if item is active (simplified)"""
 
        return False

    def _navigate(self, route):
        """Navigate to route"""
        if self.app:
            self.app.router.navigate(route)
        else:
            print(f"Навигация: {route}")

    def build(self) -> ft.Control:
        return self.navbar