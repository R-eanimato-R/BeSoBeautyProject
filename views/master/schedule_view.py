 
import flet as ft
from views.base_view import BaseView
from config import AppConfig
import datetime
import json

class ScheduleView(BaseView):
    def __init__(self, page: ft.Page, app=None):
        self.config = AppConfig()
        self.app = app
        super().__init__(page)
        
 
        self.selected_date = datetime.date.today()
        self.selected_mode = "slots"
        
 
        self.new_slot_start_time = datetime.time(10, 0) 
        self.new_slot_services = [] 
        self.master_services = [] 
        
        self.setup_controls()

    def setup_controls(self):
 
        self._load_master_services()

 
        header = ft.Container(
            padding=ft.padding.only(top=50, left=10, right=20, bottom=10),
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    icon_size=20,
                    icon_color=ft.Colors.BLACK87,
                    on_click=lambda e: self.app.router.navigate("/master/home")
                ),
                ft.Text("График работы", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                ft.Container(width=40)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

 
        self.mode_toggle = ft.Container(
            bgcolor=ft.Colors.PINK_50,
            border_radius=25,
            padding=5,
            content=ft.Row([
                self._build_toggle_btn("По окошкам", "slots"),
                self._build_toggle_btn("По расписанию", "schedule"),
            ], spacing=0)
        )

 
        self.calendar_row = ft.Row(scroll=ft.ScrollMode.HIDDEN, spacing=10)
        self._render_calendar()

 
        self.slots_column = ft.Column(spacing=15, scroll=ft.ScrollMode.HIDDEN)
        self._load_slots_for_date() 

 
        self.txt_start_time = ft.Text(
            self.new_slot_start_time.strftime("%H:%M"), 
            size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87
        )
        self.txt_services_count = ft.Text(
            "Выберите услуги", 
            size=14, color=ft.Colors.BLACK87, 
            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, expand=True
        )
        self.txt_end_time_hint = ft.Text(
            "Время окончания: --:--", 
            size=11, color=ft.Colors.GREY_500
        )

 
        self.add_slot_panel = self._build_add_slot_panel()

 
        self.content = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#FDFBFB", "#FFF0F5"]
            ),
            expand=True,
            content=ft.Stack([
                ft.Column([
                    header,
                    ft.Container(content=self.mode_toggle, alignment=ft.alignment.center, padding=10),
                    ft.Container(content=self.calendar_row, height=90, padding=ft.padding.only(left=20, right=20)),
                    ft.Container(
                        content=ft.Text(f"Расписание на {self.selected_date.strftime('%d.%m')}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                        padding=ft.padding.only(left=25, top=10)
                    ),
                    ft.Container(
                        content=self.slots_column,
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=20)
                    ),
                    ft.Container(height=180) 
                ], spacing=0),
                
                ft.Container(
                    content=self.add_slot_panel,
                    bottom=20, left=20, right=20,
                )
            ])
        )

    def _load_master_services(self):
        if self.app and self.app.current_master:
            try:
                self.master_services = self.app.db.get_master_services(self.app.current_master['id'])
            except:
                self.master_services = []

    def _build_toggle_btn(self, text, mode):
        is_active = self.selected_mode == mode
        return ft.Container(
            content=ft.Text(
                text, 
                color=ft.Colors.WHITE if is_active else ft.Colors.PINK_300,
                weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.Colors.PINK_400 if is_active else ft.Colors.TRANSPARENT,
            border_radius=20,
            on_click=lambda e: self._switch_mode(mode),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            expand=True,
            alignment=ft.alignment.center
        )

    def _switch_mode(self, mode):
        self.selected_mode = mode
        self.mode_toggle.content.controls = [
            self._build_toggle_btn("По окошкам", "slots"),
            self._build_toggle_btn("По расписанию", "schedule"),
        ]
        self.mode_toggle.update()
        self.show_snackbar(f"Режим '{mode}' пока работает одинаково (демо)")

    def _render_calendar(self):
        days = []
        today = datetime.date.today()
        for i in range(14):
            date = today + datetime.timedelta(days=i)
            is_selected = date == self.selected_date
            
            day_name = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"][date.weekday()]
            
            day_container = ft.Container(
                content=ft.Column([
                    ft.Text(day_name, color=ft.Colors.GREY_600 if not is_selected else ft.Colors.PINK_700, size=12, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=ft.Text(str(date.day), weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK if not is_selected else ft.Colors.WHITE),
                        bgcolor=ft.Colors.PINK_500 if is_selected else ft.Colors.WHITE,
                        width=40, height=40,
                        border_radius=20,
                        alignment=ft.alignment.center,
                        border=ft.border.all(1, ft.Colors.PINK_100 if not is_selected else ft.Colors.TRANSPARENT),
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.2, ft.Colors.PINK_500)) if is_selected else None
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
                padding=ft.padding.symmetric(horizontal=5),
                on_click=lambda e, d=date: self._select_date(d),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
            )
            days.append(day_container)
        self.calendar_row.controls = days

    def _select_date(self, date):
        self.selected_date = date
        self._render_calendar()
        self.calendar_row.update()
        self._load_slots_for_date()
        self.slots_column.update()

    def _load_slots_for_date(self):
        self.slots_column.controls = []
        
        if not self.app or not self.app.current_master:
            return

        try:
 
            slots = self.app.db.get_schedule_slots(
                self.app.current_master['id'], 
                self.selected_date.isoformat()
            )
            
            if not slots:
                self.slots_column.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.EVENT_NOTE, size=40, color=ft.Colors.GREY_300),
                            ft.Text("На этот день нет окошек", color=ft.Colors.GREY_500)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        padding=30
                    )
                )
                return

            for slot in slots:
 
                service_ids = json.loads(slot['service_ids'])
                services_info = self.app.db.get_services_by_ids(service_ids)
                
                if services_info:
                    main_service = services_info[0]['name']
                    count_others = len(services_info) - 1
                    desc_text = f"{main_service}"
                    if count_others > 0:
                        desc_text += f" и еще {count_others} услуги"
                else:
                    desc_text = "Услуги удалены"

                is_booked = slot['is_booked'] == 1
                
 
                card = ft.Container(
                    bgcolor=ft.Colors.GREY_100 if is_booked else ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_300 if is_booked else ft.Colors.PINK_100),
                    border_radius=16,
                    padding=15,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)),
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"{slot['start_time']} - {slot['end_time']}", size=18, weight=ft.FontWeight.W_700, color=ft.Colors.BLACK87),
                            ft.Row([
                                ft.Icon(ft.Icons.DELETE_OUTLINE, size=18, color=ft.Colors.RED_300),
                                ft.Text("Удалить", size=12, color=ft.Colors.RED_300)
                            ], spacing=2, visible=not is_booked)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=5),
                        ft.Text(desc_text, size=14, color=ft.Colors.GREY_700),
                        ft.Text("Забронировано" if is_booked else "Свободно", size=12, color=ft.Colors.GREEN_600 if not is_booked else ft.Colors.GREY_500, weight=ft.FontWeight.BOLD)
                    ]),
                    on_click=lambda e, sid=slot['id']: self._delete_slot(sid) if not is_booked else None
                )
                self.slots_column.controls.append(card)

        except Exception as e:
            print(f"Error loading slots: {e}")
            self.show_snackbar("Ошибка загрузки расписания")

    def _delete_slot(self, slot_id):
        try:
            self.app.db.delete_schedule_slot(slot_id)
            self._load_slots_for_date()
            self.slots_column.update()
            self.show_snackbar("Окошко удалено", color=ft.Colors.GREEN)
        except Exception as e:
            print(e)
            self.show_snackbar("Ошибка удаления")

    def _build_add_slot_panel(self):
        """Панель добавления с реальным функционалом"""
        return ft.Container(
            bgcolor=ft.Colors.WHITE,
            border_radius=24,
            padding=20,
            shadow=ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.15, ft.Colors.PINK_500), offset=ft.Offset(0, -5)),
            content=ft.Column([
 
                ft.Container(
                    content=ft.Text("+ Добавить окошко", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.PINK_400,
                    padding=12,
                    border_radius=12,
                    alignment=ft.alignment.center,
                    on_click=self._save_new_slot,
                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.3, ft.Colors.PINK_400), offset=ft.Offset(0, 3)),
                    animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
                    on_hover=self._animate_scale
                ),
                ft.Container(height=15),
                
 
                ft.Row([
                    ft.Column([
                        ft.Text("Время начала", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                        ft.Container(
                            content=ft.Row([
                                self.txt_start_time,
                                ft.Icon(ft.Icons.ACCESS_TIME, size=18, color=ft.Colors.PINK_300)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            border=ft.border.all(1, ft.Colors.GREY_300),
                            border_radius=12,
                            padding=10,
                            width=140,
                            bgcolor=ft.Colors.GREY_50,
                            on_click=self._open_time_picker
                        )
                    ]),
                    ft.Container(width=15),
                    ft.Column([
                        ft.Container(height=20), 
                        self.txt_end_time_hint,
                        ft.Text("*Длительность зависит от услуг", size=10, color=ft.Colors.GREY_400, width=140)
                    ])
                ]),
                
                ft.Container(height=15),
                
 
                ft.Column([
                    ft.Text("Услуги", size=12, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                    ft.Container(
                        content=ft.Row([
                            self.txt_services_count,
                            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=ft.Colors.GREY_500)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=12,
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        on_click=self._open_service_selector
                    )
                ])
            ], spacing=0)
        )

    def _animate_scale(self, e):
        e.control.scale = 0.98 if e.data == "true" else 1.0
        e.control.update()

 
    def _open_time_picker(self, e):
        time_picker = ft.TimePicker(
            confirm_text="Выбрать",
            cancel_text="Отмена",
            error_invalid_text="Неверное время",
            help_text="Выберите время начала",
            on_change=self._on_time_change,
            value=self.new_slot_start_time
        )
 
        self.page.open(time_picker)

    def _on_time_change(self, e):
        self.new_slot_start_time = e.control.value
        self.txt_start_time.value = self.new_slot_start_time.strftime("%H:%M")
        self._recalc_end_time()
        self.add_slot_panel.update()

 
    def _open_service_selector(self, e):
        if not self.master_services:
            self.show_snackbar("Сначала добавьте услуги в профиле", color=ft.Colors.ORANGE)
            return

 
        checkboxes = []
        for s in self.master_services:
 
            is_checked = any(sel['id'] == s['id'] for sel in self.new_slot_services)
            
            cb = ft.Checkbox(
                label=f"{s['name']} ({s['duration_minutes']} мин)",
                value=is_checked,
                data=s, 
                on_change=self._on_service_checkbox_change,
                fill_color=ft.Colors.PINK_400
            )
            checkboxes.append(cb)

 
        bs = ft.BottomSheet(
            content=ft.Container(
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=ft.border_radius.vertical(top=20),
                content=ft.Column([
                    ft.Text("Выберите услуги для слота", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Column(checkboxes, scroll=ft.ScrollMode.AUTO, height=300),
                    ft.Container(height=10),
 
                    ft.ElevatedButton("Готово", bgcolor=ft.Colors.PINK_400, color=ft.Colors.WHITE, width=float("inf"), 
                                      on_click=lambda e: self.page.close(bs))
                ], tight=True)
            )
        )
 
        self.page.open(bs)

    def _on_service_checkbox_change(self, e):
        service = e.control.data
        if e.control.value:
 
            if not any(s['id'] == service['id'] for s in self.new_slot_services):
                self.new_slot_services.append(service)
        else:
 
            self.new_slot_services = [s for s in self.new_slot_services if s['id'] != service['id']]
        
 
        count = len(self.new_slot_services)
        if count == 0:
            self.txt_services_count.value = "Выберите услуги"
        else:
            names = ", ".join([s['name'] for s in self.new_slot_services])
            self.txt_services_count.value = f"{names}"
        
        self._recalc_end_time()
        self.add_slot_panel.update()

    def _recalc_end_time(self):
        if not self.new_slot_services:
            self.txt_end_time_hint.value = "Время окончания: --:--"
            self.txt_end_time_hint.color = ft.Colors.GREY_500
            return

        total_minutes = sum(s['duration_minutes'] for s in self.new_slot_services)
        
 
        start_dt = datetime.datetime.combine(datetime.date.today(), self.new_slot_start_time)
        end_dt = start_dt + datetime.timedelta(minutes=total_minutes)
        
        self.txt_end_time_hint.value = f"Время окончания: {end_dt.strftime('%H:%M')}"
        self.txt_end_time_hint.color = ft.Colors.PINK_500

    def _save_new_slot(self, e):
        if not self.new_slot_services:
            self.show_snackbar("Выберите хотя бы одну услугу", color=ft.Colors.RED)
            return

        total_minutes = sum(s['duration_minutes'] for s in self.new_slot_services)
        start_dt = datetime.datetime.combine(self.selected_date, self.new_slot_start_time)
        end_dt = start_dt + datetime.timedelta(minutes=total_minutes)
        
        service_ids = [s['id'] for s in self.new_slot_services]

        try:
            self.app.db.add_schedule_slot(
                self.app.current_master['id'],
                self.selected_date.isoformat(),
                self.new_slot_start_time.strftime("%H:%M"),
                end_dt.strftime("%H:%M"),
                service_ids
            )
            
            self.show_snackbar("Окошко добавлено!", color=ft.Colors.GREEN)
            
 
            self.new_slot_services = []
            self.txt_services_count.value = "Выберите услуги"
            self._recalc_end_time()
            self.add_slot_panel.update()
            
 
            self._load_slots_for_date()
            self.slots_column.update()
            
        except Exception as ex:
            print(f"Save slot error: {ex}")
            self.show_snackbar("Ошибка сохранения", color=ft.Colors.RED)

    def build(self) -> ft.Control:
        return self.content