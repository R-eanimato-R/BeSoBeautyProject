 
import flet as ft
from views.base_view import BaseView
from config import AppConfig
import datetime
import json

class ClientMasterProfileView(BaseView):
    def __init__(self, page: ft.Page, app=None, master_id: int = None):
        self.config = AppConfig()
        self.app = app
        self.master_id = master_id
        self.master = None
        self.services = []
        self.available_slots = [] 
        super().__init__(page)
        self.setup_controls()

    def setup_controls(self):
 
        try:
            if self.app and self.master_id:
                self.master = self.app.db.get_master_by_id(self.master_id)
                self.services = self.app.db.get_master_services(self.master_id)
 
                self.available_slots = self.app.db.get_available_slots(self.master_id)
        except:
            self.master = None
            self.services = []
            self.available_slots = []

        if not self.master:
            self.content = ft.Container(content=ft.Text("Мастер не найден"))
            return

 
        header = ft.Container(
            padding=ft.padding.only(top=50, left=10, right=20, bottom=20),
            content=ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, on_click=lambda e: self.app.router.navigate("/client/home")),
                ft.Text("Профиль мастера", size=18, weight=ft.FontWeight.BOLD),
                ft.IconButton(icon=ft.Icons.FAVORITE_BORDER, icon_color=ft.Colors.PINK_500)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

 
        img_src = self.master.get('profile_image_path')
        profile_info = ft.Container(
            padding=20,
            content=ft.Column([
                ft.Container(
                    width=100, height=100, border_radius=50,
                    content=ft.Image(src=img_src, fit=ft.ImageFit.COVER) if img_src else ft.Icon(ft.Icons.PERSON, size=50, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.PINK_200, alignment=ft.alignment.center,
                    border=ft.border.all(3, ft.Colors.WHITE),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.2, ft.Colors.PINK_500))
                ),
                ft.Container(height=10),
                ft.Text(self.master.get('name', 'Мастер'), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                ft.Text(self.master.get('location', 'Город не указан'), color=ft.Colors.GREY_600),
                ft.Container(height=15),
                ft.Row([
                    self._build_stat("4.9", "Рейтинг", ft.Icons.STAR, ft.Colors.AMBER),
                    self._build_stat("150+", "Отзывов", ft.Icons.CHAT_BUBBLE, ft.Colors.BLUE),
                    self._build_stat("3 года", "Опыт", ft.Icons.WORK, ft.Colors.GREEN),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )

 
        services_column = ft.Column(spacing=10)
        for s in self.services:
            card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
                content=ft.Row([
                    ft.Column([
                        ft.Text(s['name'], weight=ft.FontWeight.BOLD, size=16),
                        ft.Text(f"{s['duration_minutes']} мин", size=12, color=ft.Colors.GREY_500)
                    ], expand=True),
                    ft.Text(f"{int(s['price'])} ₽", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.PINK_500),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
            services_column.controls.append(card)

 
        fab_book = ft.Container(
            content=ft.Text("Выбрать окошко для записи", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.PINK_500,
            padding=15,
            border_radius=30,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, ft.Colors.PINK_500), offset=ft.Offset(0, 5)),
            on_click=self._open_slots_sheet,
            margin=ft.margin.only(left=20, right=20, bottom=20),
            animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
            on_hover=self._animate_scale
        )

 
        self.content = ft.Stack([
            ft.Container(
                gradient=ft.LinearGradient(colors=["#FDFBFB", "#FFF0F5"], begin=ft.alignment.top_center, end=ft.alignment.bottom_center),
                expand=True,
                content=ft.Column([
                    header,
                    ft.Container(
                        content=ft.Column([
                            profile_info,
                            ft.Container(height=20),
                            ft.Text("Прайс-лист", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                            ft.Container(height=10),
                            services_column,
                            ft.Container(height=100) 
                        ], scroll=ft.ScrollMode.HIDDEN), 
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=20),
                    )
                ], spacing=0)
            ),
            ft.Container(content=fab_book, bottom=0, left=0, right=0)
        ])

    def _build_stat(self, value, label, icon, color):
        return ft.Column([
            ft.Container(content=ft.Icon(icon, color=color, size=20), padding=8, bgcolor=ft.Colors.WHITE, border_radius=10, shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.1, color))),
            ft.Text(value, weight=ft.FontWeight.BOLD, size=14),
            ft.Text(label, size=10, color=ft.Colors.GREY_500)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)

    def _animate_scale(self, e):
        e.control.scale = 0.97 if e.data == "true" else 1.0
        e.control.update()

    def _open_slots_sheet(self, e):
 
        slots_by_date = {}
        for slot in self.available_slots:
            date_str = slot['slot_date']
            if date_str not in slots_by_date:
                slots_by_date[date_str] = []
            slots_by_date[date_str].append(slot)

 
        content_col = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO, height=400)
        
        if not slots_by_date:
            content_col.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.EVENT_BUSY, size=50, color=ft.Colors.GREY_400),
                        ft.Text("Нет свободных окошек", color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=50
                )
            )
        else:
 
            sorted_dates = sorted(slots_by_date.keys())
            
            for date_str in sorted_dates:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d %B") 
                
 
                time_chips = []
                for slot in slots_by_date[date_str]:
 
                    service_ids = json.loads(slot['service_ids'])
                    services_info = self.app.db.get_services_by_ids(service_ids)
                    service_names = ", ".join([s['name'] for s in services_info])
                    
                    chip = ft.Container(
                        content=ft.Column([
                            ft.Text(f"{slot['start_time']}", weight=ft.FontWeight.BOLD, color=ft.Colors.PINK_700),
                            ft.Text(service_names, size=10, color=ft.Colors.GREY_600, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=100, text_align=ft.TextAlign.CENTER)
                        ], spacing=2, alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.PINK_50,
                        border=ft.border.all(1, ft.Colors.PINK_200),
                        border_radius=12,
                        padding=10,
                        on_click=lambda e, s=slot: self._confirm_booking_dialog(s),
                        ink=True
                    )
                    time_chips.append(chip)
                
                date_section = ft.Column([
                    ft.Text(formatted_date, weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK87),
                    ft.Row(time_chips, wrap=True, spacing=10, run_spacing=10)
                ])
                content_col.controls.append(date_section)

        self.bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=ft.border_radius.vertical(top=25),
                content=ft.Column([
                    ft.Container(
                        width=40, height=4, bgcolor=ft.Colors.GREY_300, 
                        border_radius=2, margin=ft.margin.only(bottom=20),
                        alignment=ft.alignment.center
                    ),
                    ft.Text("Выберите время", size=20, weight=ft.FontWeight.BOLD),
                    content_col
                ], tight=True)
            )
        )
        self.page.open(self.bs)

    def _confirm_booking_dialog(self, slot):
 
        service_ids = json.loads(slot['service_ids'])
        services_info = self.app.db.get_services_by_ids(service_ids)
        service_names = ", ".join([s['name'] for s in services_info])
        total_price = sum([s['price'] for s in services_info])

        def book_action(e):
            success = self.app.db.book_slot_transaction(
                slot['id'],
                "Я (Клиент)", 
                "Запись через приложение"
            )
            
            self.page.close(self.confirm_dlg)
            self.page.close(self.bs)
            
            if success:
                self.show_snackbar("Вы успешно записаны!", color=ft.Colors.GREEN)
 
                self.available_slots = self.app.db.get_available_slots(self.master_id)
            else:
                self.show_snackbar("Окошко уже занято", color=ft.Colors.RED)

        self.confirm_dlg = ft.AlertDialog(
            title=ft.Text("Подтверждение записи"),
            content=ft.Column([
                ft.Text(f"Дата: {slot['slot_date']}"),
                ft.Text(f"Время: {slot['start_time']}"),
                ft.Text(f"Услуги: {service_names}"),
                ft.Text(f"Стоимость: {int(total_price)} ₽", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.PINK_500),
            ], tight=True),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.page.close(self.confirm_dlg)),
                ft.ElevatedButton("Записаться", bgcolor=ft.Colors.PINK_500, color=ft.Colors.WHITE, on_click=book_action)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.open(self.confirm_dlg)

    def build(self):
        return self.content