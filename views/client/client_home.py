 
import flet as ft
from views.base_view import BaseView
from config import AppConfig

class ClientHomeView(BaseView):
    def __init__(self, page: ft.Page, app=None):
        self.config = AppConfig()
        self.app = app
        super().__init__(page)
        self.masters = []
        self.setup_controls()

    def setup_controls(self):
 
        self._load_masters()

 
        self.city_field = ft.TextField(
            hint_text="Город",
            prefix_icon=ft.Icons.LOCATION_ON,
            border_color="transparent",
            bgcolor=ft.Colors.WHITE,
            filled=True,
            border_radius=15,
            content_padding=10,
            text_size=14,
            expand=True,
            on_submit=self._on_search
        )

        self.service_field = ft.TextField(
            hint_text="Услуга (напр. Маникюр)",
            prefix_icon=ft.Icons.SEARCH,
            border_color="transparent",
            bgcolor=ft.Colors.WHITE,
            filled=True,
            border_radius=15,
            content_padding=10,
            text_size=14,
            expand=True,
            on_submit=self._on_search
        )

        search_bar = ft.Container(
            padding=ft.padding.only(top=50, left=20, right=20, bottom=20),
            content=ft.Column([
                ft.Row([
                    ft.Text("BeBeauty", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.PINK_500, font_family="Poppins"),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.SWAP_HORIZ, 
                        icon_color=ft.Colors.PINK_500,
                        tooltip="Я мастер",
                        on_click=lambda e: self.app.switch_space("master")
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(height=10),
                ft.Row([self.city_field, ft.Container(width=10), self.service_field]),
                ft.Container(height=10),
                ft.ElevatedButton(
                    "Найти", 
                    bgcolor=ft.Colors.PINK_500, 
                    color=ft.Colors.WHITE, 
                    width=float("inf"),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=self._on_search
                )
            ])
        )

 
        categories = ["Маникюр", "Педикюр", "Брови", "Ресницы", "Макияж", "Волосы", "Массаж"]
        self.categories_row = ft.Row(
            scroll=ft.ScrollMode.HIDDEN,
            spacing=10,
            controls=[
                ft.Container(
                    content=ft.Text(cat, color=ft.Colors.PINK_600, size=13, weight=ft.FontWeight.W_500),
                    bgcolor=ft.Colors.PINK_50,
                    padding=ft.padding.symmetric(horizontal=15, vertical=8),
                    border_radius=20,
                    on_click=lambda e, c=cat: self._on_category_click(c),
                    animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                    on_hover=self._animate_scale
                ) for cat in categories
            ]
        )
        categories_container = ft.Container(
            content=self.categories_row,
            padding=ft.padding.symmetric(horizontal=20)
        )

 
        self.masters_grid = ft.Column(spacing=15, scroll=ft.ScrollMode.HIDDEN)
        self._render_masters_list()

 
        self.content = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#FDFBFB", "#FFF0F5"]
            ),
            expand=True,
            content=ft.Column([
                search_bar,
                categories_container,
                ft.Container(height=15),
                ft.Container(
                    content=ft.Text("Рекомендации", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                    padding=ft.padding.only(left=20)
                ),
                ft.Container(height=10),
                ft.Container(
                    content=self.masters_grid,
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=20)
                )
            ], spacing=0)
        )

    def _load_masters(self, city="", service=""):
        try:
            self.masters = self.app.db.search_masters(city, service)
        except Exception as e:
            print(f"Search error: {e}")
            self.masters = []

    def _render_masters_list(self):
        self.masters_grid.controls = []
        
        if not self.masters:
            self.masters_grid.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=50, color=ft.Colors.GREY_400),
                        ft.Text("Мастера не найдены", color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=50
                )
            )
            return

        for m in self.masters:
 
            try:
                services = self.app.db.get_master_services(m['id'])
                service_names = [s['name'] for s in services[:3]] 
            except:
                service_names = []

 
            tags = ft.Row(wrap=True, spacing=5, run_spacing=5)
            for s_name in service_names:
                tags.controls.append(
                    ft.Container(
                        content=ft.Text(s_name, size=10, color=ft.Colors.GREY_700),
                        bgcolor=ft.Colors.GREY_100,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=8
                    )
                )

            card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=20,
                padding=15,
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 5)),
                content=ft.Row([
 
                    ft.Container(
                        width=70, height=70, border_radius=35,
                        content=ft.Image(src=m['profile_image_path'], fit=ft.ImageFit.COVER) if m['profile_image_path'] else ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.PINK_200,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(width=15),
 
                    ft.Column([
                        ft.Row([
                            ft.Text(m['name'] or "Мастер", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK87),
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.STAR, size=12, color=ft.Colors.AMBER),
                                    ft.Text("5.0", size=12, weight=ft.FontWeight.BOLD)
                                ], spacing=2),
                                bgcolor=ft.Colors.AMBER_50, padding=4, border_radius=5
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, size=12, color=ft.Colors.GREY_500),
                            ft.Text(m['location'] or "Город не указан", size=12, color=ft.Colors.GREY_500)
                        ], spacing=2),
                        ft.Container(height=5),
                        tags,
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Text("Записаться", color=ft.Colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                            bgcolor=ft.Colors.PINK_500,
                            padding=ft.padding.symmetric(horizontal=20, vertical=8),
                            border_radius=15,
                            alignment=ft.alignment.center,
                            on_click=lambda e, mid=m['id']: self.app.router.navigate(f"/client/master/{mid}")
                        )
                    ], expand=True, spacing=2)
                ], alignment=ft.MainAxisAlignment.START),
                on_click=lambda e, mid=m['id']: self.app.router.navigate(f"/client/master/{mid}"),
                animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                on_hover=self._animate_scale
            )
            self.masters_grid.controls.append(card)

    def _on_search(self, e):
        self._load_masters(self.city_field.value, self.service_field.value)
        self._render_masters_list()
        self.masters_grid.update()

    def _on_category_click(self, category):
        self.service_field.value = category
        self.service_field.update()
        self._on_search(None)

    def _animate_scale(self, e):
        e.control.scale = 0.98 if e.data == "true" else 1.0
        e.control.update()

    def build(self) -> ft.Control:
        return self.content