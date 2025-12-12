 
import flet as ft
from views.base_view import BaseView

class PlaceholderView(BaseView):
    def __init__(self, page: ft.Page, app=None, title="В разработке"):
        self.app = app
        self.title_text = title
        super().__init__(page)
        self.content = ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            content=ft.Column([
                ft.Container(padding=ft.padding.only(top=50, left=10), content=ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, on_click=lambda e: self.app.router.navigate("/master/home"))),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center,
                    content=ft.Column([
                        ft.Icon(ft.Icons.CONSTRUCTION, size=60, color=ft.Colors.PINK_300),
                        ft.Text(self.title_text, size=20, weight=ft.FontWeight.BOLD),
                        ft.Text("Этот раздел скоро появится", color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            ])
        )
    def build(self): return self.content

class SubscriptionView(PlaceholderView):
    def __init__(self, page, app): super().__init__(page, app, "Подписка")

class CreativeView(PlaceholderView):
    def __init__(self, page, app): super().__init__(page, app, "Творческий уголок")

class AboutView(PlaceholderView):
    def __init__(self, page, app): super().__init__(page, app, "О приложении")