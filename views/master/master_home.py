 
import flet as ft
from views.base_view import BaseView
from config import AppConfig

class MasterHomeView(BaseView):
    def __init__(self, page: ft.Page, app=None):
        self.config = AppConfig()
        self.app = app
        super().__init__(page)
        
 
        if self.app and self.app.current_master:
            self.master_data = self.app.current_master
        else:
            self.master_data = {}
        
        self.setup_controls()

    def setup_controls(self):
 
        profile_completion = self.master_data.get('profile_completion_percent', 0) or 0
        is_empty = profile_completion < 30
        
 
        background_blob = ft.Container(
            width=300, height=300,
            bgcolor=ft.Colors.PINK_100,
            border_radius=150,
            shadow=ft.BoxShadow(blur_radius=100, color=ft.Colors.PINK_200, spread_radius=20),
            opacity=0.3,
            top=-100, left=-100,
        )

 
        content_column = ft.Column(
            controls=[
                self._build_app_bar(),
                ft.Container(height=10),
                
 
                self._build_empty_state() if is_empty else self._build_dashboard(),
                
                ft.Container(height=80) # Отступ снизу
            ],
            scroll=ft.ScrollMode.HIDDEN,
            expand=True,
            spacing=0,
        )

 
        switch_btn = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SWAP_HORIZ, color=ft.Colors.PINK_500, size=20),
                ft.Text("Я клиент", color=ft.Colors.PINK_500, weight=ft.FontWeight.BOLD)
            ], spacing=5),
            bgcolor=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=15, vertical=10),
            border_radius=20,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            on_click=lambda e: self.app.switch_space("client"),
            top=50, right=20,
            animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
            on_hover=self._animate_scale
        )

        self.main_container = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#FDFBFB", "#F4F7F6"] # Очень светлый, чистый фон
            ),
            expand=True,
            padding=0,
            content=ft.Stack(
                controls=[
                    background_blob,
                    content_column,
                    switch_btn
                ]
            )
        )

    def _build_app_bar(self):
        """Шапка (без BeBeauty)"""
        return ft.Container(
            padding=ft.padding.only(left=25, right=20, top=60, bottom=10),
            content=ft.Column([
 
                ft.Text(
                    "Твоя студия",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK87,
                    font_family="Poppins"
                ),
                ft.Text(
                    "Управление профилем",
                    size=14,
                    color=ft.Colors.GREY_500,
                    weight=ft.FontWeight.W_500
                )
            ], spacing=2)
        )

    def _build_empty_state(self):
        """Экран для нового мастера"""
        completion = self.master_data.get('profile_completion_percent', 0)
        
        return ft.Container(
            padding=20,
            content=ft.Column([
 
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=24,
                    padding=30,
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK)),
                    content=ft.Column([
                        ft.Icon(ft.Icons.AUTO_AWESOME, size=60, color=ft.Colors.PINK_300),
                        ft.Container(height=15),
                        ft.Text("Добро пожаловать!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87, text_align=ft.TextAlign.CENTER),
                        ft.Container(height=10),
                        ft.Text(
                            "Чтобы клиенты могли записываться к вам, нужно немного рассказать о себе.",
                            size=15, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=25),
                        
 
                        ft.Row([
                            ft.Text("Готовность профиля", size=13, color=ft.Colors.GREY_500),
                            ft.Text(f"{completion}%", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.PINK_500),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ProgressBar(value=completion/100, color=ft.Colors.PINK_400, bgcolor=ft.Colors.PINK_50, bar_height=8, border_radius=4),
                        
                        ft.Container(height=30),
                        
 
                        ft.Container(
                            content=ft.Row([
                                ft.Text("Заполнить профиль", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                                ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE, size=20)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            bgcolor=ft.LinearGradient(colors=[ft.Colors.PINK_400, ft.Colors.PINK_600]),
                            padding=15,
                            border_radius=16,
                            on_click=lambda e: self.app.router.navigate("/master/profile_edit"),
                            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, ft.Colors.PINK_400), offset=ft.Offset(0, 5)),
                            animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                            on_hover=self._animate_scale
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ])
        )

    def _build_dashboard(self):
        """Экран рабочего стола мастера"""
        name = self.master_data.get('name', 'Мастер')
        img_src = self.master_data.get('profile_image_path')
        
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20),
            content=ft.Column([
 
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border_radius=24,
                    padding=20,
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
                    content=ft.Row([
                        ft.Container(
                            width=70, height=70, border_radius=35,
                            content=ft.Image(src=img_src, fit=ft.ImageFit.COVER) if img_src else ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=30),
                            bgcolor=ft.Colors.PINK_200,
                            alignment=ft.alignment.center,
                            border=ft.border.all(3, ft.Colors.WHITE),
                            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.2, ft.Colors.PINK_400))
                        ),
                        ft.Container(width=15),
                        ft.Column([
                            ft.Text(name, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                            ft.Text("Мастер", size=14, color=ft.Colors.GREY_500),
                            ft.Container(height=5),
                            ft.Container(
                                content=ft.Text("Редактировать", size=12, color=ft.Colors.PINK_500, weight=ft.FontWeight.BOLD),
                                on_click=lambda e: self.app.router.navigate("/master/profile_edit")
                            )
                        ], spacing=2, expand=True),
                    ], alignment=ft.MainAxisAlignment.START)
                ),
                
                ft.Container(height=25),
                
 
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LINK, color=ft.Colors.GREY_400, size=16),
                        ft.Text(
                            f"{self.master_data.get('booking_link', 'be.beauty/user')}",
                            size=14, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=10)
                ),

 
                ft.Text("Меню", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Container(height=15),
                self._build_action_grid(),
                
                ft.Container(height=25),
                
 
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.WHITE),
                        ft.Text("Мои записи", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    height=60,
                    gradient=ft.LinearGradient(colors=[ft.Colors.PINK_500, ft.Colors.PURPLE_500]),
                    border_radius=20,
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.3, ft.Colors.PINK_500), offset=ft.Offset(0, 5)),
                    on_click=lambda e: self.app.router.navigate("/master/bookings"),
                    animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                    on_hover=self._animate_scale
                )
            ])
        )

    def _build_action_grid(self):
        """Сетка кнопок"""
        actions = [
            {"icon": ft.Icons.EDIT, "label": "Профиль", "route": "/master/profile_edit", "color": ft.Colors.PINK_50, "icon_color": ft.Colors.PINK_400},
            {"icon": ft.Icons.ADD_CIRCLE_OUTLINE, "label": "Услуги", "route": "/master/services", "color": ft.Colors.PURPLE_50, "icon_color": ft.Colors.PURPLE_400},
            {"icon": ft.Icons.SCHEDULE, "label": "График", "route": "/master/schedule", "color": ft.Colors.TEAL_50, "icon_color": ft.Colors.TEAL_400},
            {"icon": ft.Icons.FAVORITE_BORDER, "label": "Подписка", "route": "/master/subscription", "color": ft.Colors.RED_50, "icon_color": ft.Colors.RED_400},
            {"icon": ft.Icons.PALETTE_OUTLINED, "label": "Портфолио", "route": "/master/creative", "color": ft.Colors.INDIGO_50, "icon_color": ft.Colors.INDIGO_400},
            {"icon": ft.Icons.INFO_OUTLINE, "label": "Инфо", "route": "/about", "color": ft.Colors.BLUE_50, "icon_color": ft.Colors.BLUE_400},
        ]

        items = []
        for action in actions:
            item = ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(action["icon"], color=action["icon_color"], size=26),
                        padding=12,
                        bgcolor=ft.Colors.WHITE,
                        border_radius=16,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK))
                    ),
                    ft.Container(height=8),
                    ft.Text(action["label"], size=13, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=action["color"],
                border_radius=24,
                padding=15,
                aspect_ratio=1, 
                on_click=lambda e, r=action["route"]: self.app.router.navigate(r),
                animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                on_hover=self._animate_scale
            )
            items.append(item)

        return ft.GridView(
            controls=items,
            runs_count=3, # 3 колонки
            child_aspect_ratio=0.85,
            spacing=15,
            run_spacing=15,
            expand=False, 
        )

    def _animate_scale(self, e):
        e.control.scale = 0.95 if e.data == "true" else 1.0
        e.control.update()

    def build(self) -> ft.Control:
        return self.main_container