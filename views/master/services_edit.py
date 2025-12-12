 
import flet as ft
from views.base_view import BaseView
from config import AppConfig

class ServicesEditView(BaseView):
    def __init__(self, page: ft.Page, app=None):
        self.config = AppConfig()
        self.app = app
        super().__init__(page)
        self.services = []
        self.setup_controls()

    def setup_controls(self):
        self._load_services()

 
        header = ft.Container(
            padding=ft.padding.only(top=50, left=10, right=20, bottom=10),
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    icon_size=20,
                    icon_color=ft.Colors.BLACK87,
                    on_click=lambda e: self.app.router.navigate("/master/home")
                ),
                ft.Text("Мои услуги", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
 
                ft.Container(
                    content=ft.Icon(ft.Icons.ADD, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.PINK_500,
                    border_radius=15,
                    padding=8,
                    on_click=lambda e: self._open_edit_sheet(None), 
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.4, ft.Colors.PINK_500))
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

 
        self.services_list = ft.Column(spacing=15, scroll=ft.ScrollMode.HIDDEN)
        self._render_list()

 
        self.content = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#FDFBFB", "#FFF0F5"]
            ),
            expand=True,
            content=ft.Column([
                header,
                ft.Container(
                    content=self.services_list,
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=20)
                )
            ], spacing=0)
        )

    def _load_services(self):
        if self.app and self.app.current_master:
            try:
                self.services = self.app.db.get_master_services(self.app.current_master['id'])
            except:
                self.services = []

    def _render_list(self):
        self.services_list.controls = []
        
        if not self.services:
            self.services_list.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Icon(ft.Icons.SPA_OUTLINED, size=50, color=ft.Colors.PINK_200),
                            padding=20,
                            bgcolor=ft.Colors.WHITE,
                            border_radius=50,
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, ft.Colors.PINK_500))
                        ),
                        ft.Container(height=10),
                        ft.Text("Список услуг пуст", size=16, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Text("Нажмите +, чтобы добавить первую услугу", size=12, color=ft.Colors.GREY_400)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=100)
                )
            )
            return

        for s in self.services:
 
            card = ft.Container(
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=20,
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK), offset=ft.Offset(0, 5)),
                content=ft.Row([
 
                    ft.Row([
                        ft.Container(
                            content=ft.Icon(ft.Icons.DIAMOND_OUTLINED, color=ft.Colors.PINK_400, size=24),
                            bgcolor=ft.Colors.PINK_50,
                            padding=10,
                            border_radius=12
                        ),
                        ft.Column([
                            ft.Text(s['name'], weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLACK87),
                            ft.Row([
                                ft.Icon(ft.Icons.ACCESS_TIME, size=12, color=ft.Colors.GREY_500),
                                ft.Text(f"{s['duration_minutes']} мин", size=12, color=ft.Colors.GREY_600),
                                ft.Container(width=5),
                                ft.Icon(ft.Icons.ATTACH_MONEY, size=12, color=ft.Colors.GREY_500),
                                ft.Text(f"{int(s['price'])} ₽", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.BOLD),
                            ], spacing=2)
                        ], spacing=2)
                    ]),
 
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_300)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                on_click=lambda e, srv=s: self._open_edit_sheet(srv),
                animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                on_hover=self._animate_scale
            )
            self.services_list.controls.append(card)

    def _animate_scale(self, e):
        e.control.scale = 0.98 if e.data == "true" else 1.0
        e.control.update()

    def _open_edit_sheet(self, service):
        """Открывает шторку редактирования/создания"""
        is_edit = service is not None
        
 
        name_tf = ft.TextField(
            label="Название услуги", 
            value=service['name'] if is_edit else "",
            border_color="transparent",
            bgcolor=ft.Colors.GREY_50,
            filled=True,
            border_radius=12
        )
        
        price_tf = ft.TextField(
            label="Цена (₽)", 
            value=str(int(service['price'])) if is_edit else "",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color="transparent",
            bgcolor=ft.Colors.GREY_50,
            filled=True,
            border_radius=12,
            width=140
        )
        
        duration_tf = ft.TextField(
            label="Время (мин)", 
            value=str(service['duration_minutes']) if is_edit else "60",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color="transparent",
            bgcolor=ft.Colors.GREY_50,
            filled=True,
            border_radius=12,
            width=140
        )

        description_tf = ft.TextField(
            label="Описание (необязательно)",
            value=service['description'] if is_edit else "",
            multiline=True,
            max_lines=3,
            border_color="transparent",
            bgcolor=ft.Colors.GREY_50,
            filled=True,
            border_radius=12
        )

 
        bs = None

        def save_action(e):
            if not name_tf.value:
                name_tf.error_text = "Введите название"
                name_tf.update()
                return
            
            try:
                price = float(price_tf.value) if price_tf.value else 0
                duration = int(duration_tf.value) if duration_tf.value else 60
                
                if is_edit:
                    self.app.db.update_service(
                        service['id'],
                        name_tf.value,
                        description_tf.value,
                        duration,
                        price
                    )
                    self.show_snackbar("Услуга обновлена", color=ft.Colors.GREEN)
                else:
                    self.app.db.add_service(
                        self.app.current_master['id'],
                        name_tf.value,
                        description=description_tf.value,
                        duration_minutes=duration,
                        price=price
                    )
                    self.show_snackbar("Услуга создана", color=ft.Colors.GREEN)
                
                if bs: self.page.close(bs)
                self._load_services()
                self._render_list()
                self.services_list.update()
                
            except ValueError:
                self.show_snackbar("Цена и время должны быть числами", color=ft.Colors.RED)

        def delete_action(e):
            if not is_edit: return
            self.app.db.delete_service(service['id'])
            if bs: self.page.close(bs)
            self._load_services()
            self._render_list()
            self.services_list.update()
            self.show_snackbar("Услуга удалена", color=ft.Colors.GREY)

 
        bs_content = ft.Container(
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.vertical(top=25),
            content=ft.Column([
                ft.Container(
                    width=40, height=4, bgcolor=ft.Colors.GREY_300, 
                    border_radius=2, margin=ft.margin.only(bottom=20),
                    alignment=ft.alignment.center
                ),
                ft.Text(
                    "Редактирование услуги" if is_edit else "Новая услуга", 
                    size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87
                ),
                ft.Container(height=15),
                name_tf,
                ft.Container(height=10),
                ft.Row([price_tf, duration_tf], spacing=15),
                ft.Container(height=10),
                description_tf,
                ft.Container(height=20),
                
 
                ft.Container(
                    content=ft.Text("Сохранить", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=16),
                    bgcolor=ft.Colors.PINK_500,
                    padding=15,
                    border_radius=15,
                    alignment=ft.alignment.center,
                    on_click=save_action,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, ft.Colors.PINK_500))
                ),
                
 
                ft.Container(
                    content=ft.Text("Удалить услугу", color=ft.Colors.RED_400, size=14),
                    padding=15,
                    alignment=ft.alignment.center,
                    on_click=delete_action,
                    visible=is_edit
                )
            ], tight=True)
        )

        bs = ft.BottomSheet(
            content=bs_content,
            open=True
        )
        self.page.open(bs)

    def build(self):
        return self.content