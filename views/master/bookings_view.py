 
import flet as ft
from views.base_view import BaseView
from config import AppConfig

class BookingsView(BaseView):
    def __init__(self, page: ft.Page, app=None):
        self.config = AppConfig()
        self.app = app
        super().__init__(page)
        self.bookings = []
        self.setup_controls()

    def setup_controls(self):
        self._load_bookings()

        header = ft.Container(
            padding=ft.padding.only(top=50, left=10, right=20, bottom=10),
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, on_click=lambda e: self.app.router.navigate("/master/home")),
                ft.Text("Мои записи", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(width=40)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        self.bookings_list = ft.Column(spacing=10, scroll=ft.ScrollMode.HIDDEN)
        self._render_list()

        self.content = ft.Container(
            gradient=ft.LinearGradient(colors=["#FDFBFB", "#FFF0F5"], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
            expand=True,
            content=ft.Column([
                header,
                ft.Container(content=self.bookings_list, expand=True, padding=20)
            ])
        )

    def _load_bookings(self):
        if self.app and self.app.current_master:
            try:
                self.bookings = self.app.db.get_master_bookings(self.app.current_master['id'])
            except:
                self.bookings = []

    def _render_list(self):
        self.bookings_list.controls = []
        if not self.bookings:
            self.bookings_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.EVENT_BUSY, size=50, color=ft.Colors.PINK_200),
                        ft.Text("Записей пока нет", color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=50
                )
            )
            return

        for b in self.bookings:
            status_color = ft.Colors.GREEN if b['status'] == 'confirmed' else ft.Colors.ORANGE
            card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"{b['booking_date']} в {b['booking_time']}", weight=ft.FontWeight.BOLD, size=16),
                        ft.Container(bgcolor=status_color, width=10, height=10, border_radius=5)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Клиент: {b['client_name']}", size=14),
                    ft.Text(f"Услуга: {b.get('service_name', 'Не указана')}", size=14, color=ft.Colors.GREY_600),
                    ft.Text(f"Прим: {b['notes']}", size=12, italic=True, color=ft.Colors.GREY_500) if b['notes'] else ft.Container()
                ])
            )
            self.bookings_list.controls.append(card)

    def build(self):
        return self.content