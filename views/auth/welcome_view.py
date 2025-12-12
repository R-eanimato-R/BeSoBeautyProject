 
import flet as ft
from views.base_view import BaseView
from config import AppConfig

class WelcomeView(BaseView):
    def __init__(self, page: ft.Page, app=None):
        self.config = AppConfig()
        self.app = app
        super().__init__(page)
        self.setup_controls()

    def setup_controls(self):
        """Создание всех элементов интерфейса с современным дизайном 2025"""
 
        self.decorative_shapes = self._create_decorative_shapes()
        
 
        self.title = ft.Container(
            content=ft.Column([
                ft.Container(
                    width=100,
                    height=100,
                    border_radius=50,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[
                            self.config.colors['gradient_start'],
                            self.config.colors['gradient_mid'],
                            self.config.colors['gradient_end']
                        ]
                    ),
                    content=ft.Icon(
                        name="SPA",
                        size=56,
                        color=self.config.colors['surface']
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        blur_radius=30,
                        spread_radius=5,
                        color=self.config.colors['gradient_start'] + "80"
                    )
                ),
                ft.Text(
                    "BeautySpace",
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    color=self.config.colors['text_primary_dark'],
                    font_family=self.config.fonts['Poppins']
                ),
                ft.Text(
                    "Ваш идеальный мастер красоты",
                    size=18,
                    color=self.config.colors['text_secondary'],
                    text_align=ft.TextAlign.CENTER,
                    font_family=self.config.fonts['Poppins']
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
            ),
            margin=ft.margin.only(bottom=30)
        )
        
 
        self.client_card = self._create_role_card(
            icon="PERSON_SEARCH_SHARP",
            title="Я клиент",
            description="Найдите мастера для любых услуг",
            button_color=self.config.colors['client_btn'],
            gradient_colors=[
                self.config.colors['client_btn'],
                self.config.colors['primary']
            ],
            on_click=self.navigate_to_client
        )
        
 
        self.master_card = self._create_role_card(
            icon="PERSON",
            title="Я мастер",
            description="Предоставляйте услуги и находите клиентов",
            button_color=self.config.colors['master_btn'],
            gradient_colors=[
                self.config.colors['master_btn'],
                self.config.colors['secondary']
            ],
            on_click=self.navigate_to_master
        )
        
 
        self.cards_container = ft.ResponsiveRow(
            controls=[self.client_card, self.master_card],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
        
 
        self.footer = ft.Container(
            content=ft.Row([
                ft.Container(
                    width=24,
                    height=24,
                    border_radius=6,
                    border=ft.border.all(2, self.config.colors['primary']),
                    bgcolor=self.config.colors['surface'] + "00",
                    alignment=ft.alignment.center,
                    content=ft.Icon(
                        name="CHECK",
                        size=16,
                        color=self.config.colors['surface'],
                        opacity=0
                    ),
                    on_click=self._toggle_checkbox
                ),
                ft.Text(
                    "Я соглашаюсь с условиями и политикой конфиденциальности",
                    size=14,
                    color=self.config.colors['text_secondary'],
                    expand=True,
                    font_family=self.config.fonts['Poppins']
                )
            ],
            spacing=16,
            alignment=ft.MainAxisAlignment.CENTER
            ),
            margin=ft.margin.only(top=30, bottom=24)
        )
        
 
        self.loading_indicator = ft.ProgressRing(
            width=40,
            height=40,
            stroke_width=4,
            color=self.config.colors['primary'],
            visible=False
        )
        
    def _create_decorative_shapes(self):
        """Создание декоративных элементов фона"""
        shapes = []
 
        colors = [
            self.config.colors['gradient_start'] + "20",
            self.config.colors['gradient_mid'] + "20",
            self.config.colors['gradient_end'] + "20"
        ]
        for i in range(3):
            shape = ft.Container(
                width=200 + i * 100,
                height=200 + i * 100,
                border_radius=100 + i * 50,
                bgcolor=colors[i],
                blur=ft.Blur(30, 30, ft.BlurTileMode.CLAMP),
                top=100 + i * 80,
                left=-50 + i * 150
            )
            shapes.append(shape)
        return shapes
    
    def _create_role_card(self, icon, title, description, button_color, gradient_colors, on_click):
        """Создание карточки роли с glassmorphism эффектом"""
        card = ft.Container(
            content=ft.Column([
                ft.Container(
                    width=100,
                    height=100,
                    border_radius=50,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=gradient_colors
                    ),
                    content=ft.Icon(
                        name=icon,
                        size=48,
                        color=self.config.colors['surface']
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        blur_radius=20,
                        spread_radius=2,
                        color=button_color + "80"
                    )
                ),
                ft.Container(height=24),
                ft.Text(
                    title,
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=self.config.colors['text_primary_dark'],
                    font_family=self.config.fonts['Poppins']
                ),
                ft.Container(height=12),
                ft.Text(
                    description,
                    size=16,
                    color=self.config.colors['text_secondary'],
                    text_align=ft.TextAlign.CENTER,
                    font_family=self.config.fonts['Poppins']
                ),
                ft.Container(height=32),
                ft.Container(
                    width=180,
                    height=56,
                    border_radius=self.config.sizes['border_radius'],
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[button_color, self._adjust_brightness(button_color, 1.2)]
                    ),
                    content=ft.Text(
                        "Начать",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=self.config.colors['surface'],
                        font_family=self.config.fonts['Poppins']
                    ),
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        blur_radius=15,
                        spread_radius=0,
                        color=button_color + "80"
                    ),
                    on_click=on_click,
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
            ),
            width=self.config.sizes['card_width'],
            padding=ft.padding.all(32),
            bgcolor=self.config.colors['glass_bg'],
            border_radius=self.config.sizes['border_radius'] * 2,
            border=ft.border.all(1, self.config.colors['glass_border']),
            blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
            shadow=ft.BoxShadow(
                blur_radius=40,
                spread_radius=5,
                color="#0000001A"
            ),
            animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
        )
        card.on_hover = lambda e: self._card_hover_effect(e, card)
        return card
    
    def _adjust_brightness(self, hex_color, factor):
        """Увеличивает яркость цвета (простой вариант)"""
 
        return hex_color
    
    def _card_hover_effect(self, e, card):
        """Эффект при наведении на карточку"""
        if e.data == "true":
            card.shadow = ft.BoxShadow(
                blur_radius=60,
                spread_radius=10,
                color="#0000002A"
            )
            card.border = ft.border.all(2, self.config.colors['primary'])
        else:
            card.shadow = ft.BoxShadow(
                blur_radius=40,
                spread_radius=5,
                color="#0000001A"
            )
            card.border = ft.border.all(1, self.config.colors['glass_border'])
        card.update()
    
    def _toggle_checkbox(self, e):
        """Переключение чекбокса соглашения"""
        checkbox = e.control
        icon = checkbox.content
        if icon.opacity == 0:
            icon.opacity = 1
            checkbox.bgcolor = self.config.colors['primary']
        else:
            icon.opacity = 0
            checkbox.bgcolor = self.config.colors['surface'] + "00"
        checkbox.update()
    
    def navigate_to_client(self, e):
        """Переход в режим клиента"""
        self._navigate_with_loading("client")
    
    def navigate_to_master(self, e):
        """Переход в режим мастера"""
        self._navigate_with_loading("master")
    
    def _navigate_with_loading(self, space):
        """Навигация с индикатором загрузки"""
        self.loading_indicator.visible = True
        self.page.update()
        
        try:
            if self.app:
                self.app.switch_space(space)
        except Exception as ex:
            print(f"Ошибка при переходе в {space} пространство: {ex}")
            import traceback
            traceback.print_exc()
        finally:
            self.loading_indicator.visible = False
            self.page.update()
    
    def build(self) -> ft.Control:
        """Сборка всего интерфейса"""
        return ft.Container(
            content=ft.Stack([
                *self.decorative_shapes,
                ft.ListView(
                    controls=[
                        ft.Container(height=40),
                        self.title,
                        ft.Container(height=10),
                        self.cards_container,
                        ft.Container(height=10),
                        self.footer,
                        ft.Container(
                            content=self.loading_indicator,
                            alignment=ft.alignment.center
                        )
                    ],
                    expand=True,
                    spacing=0,
                    padding=0,
                )
            ]),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    self.config.colors['background'],
                    self.config.colors['surface_dark'],
                    self.config.colors['background']
                ]
            ),
            padding=20,
            expand=True
        )