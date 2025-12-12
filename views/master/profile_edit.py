 
import flet as ft
import threading
import json
import urllib.request
import urllib.parse
from views.base_view import BaseView
from config import AppConfig

class MasterProfileEditView(BaseView):
    def __init__(self, page: ft.Page, app=None, master_data=None):
        self.config = AppConfig()
        self.app = app
        self.master_data = master_data or {}
        super().__init__(page)
        
 
        self.location_suggestions = []
        self.selected_services = self._parse_services(self.master_data.get('bio', ''))
        self.all_services = self._get_beauty_services()
        
 
        self._search_timer = None
        
        self.setup_controls()

    def _parse_services(self, bio: str):
        """Извлечь список услуг из строки"""
        if not bio:
            return []
        text = bio.replace('•', ',').strip()
        parts = [p.strip() for p in text.split(',') if p.strip()]
        return parts

    def _get_beauty_services(self):
        """Полный список популярных бьюти-услуг"""
        return [
            "Маникюр", "Педикюр", "Наращивание ногтей", "Гель-лак", "Аппаратный маникюр",
            "Классический маникюр", "Европейский маникюр", "SPA-маникюр", "Дизайн ногтей",
            "Стрижка волос", "Окрашивание волос", "Мелирование", "Балаяж", "Омбре",
            "Карвинг", "Укладка волос", "Вечерняя причёска", "Свадебная причёска",
            "Мужская стрижка", "Женская стрижка", "Детская стрижка", "Кератиновое выпрямление",
            "Ламинирование волос", "Ботокс для волос", "Нанопластика", "Биозавивка",
            "Эпиляция воском", "Шугаринг", "Лазерная эпиляция", "Электроэпиляция",
            "Эпиляция нитью", "Чистка лица", "Ультразвуковая чистка лица", "Атравматичная чистка",
            "Химический пилинг", "Лазерный пилинг", "Микродермабразия", "Альгинатная маска",
            "Массаж лица", "Гуаша массаж", "Бьюти-массаж", "Лимфодренажный массаж",
            "Коррекция бровей", "Окрашивание бровей", "Ламинирование бровей", "Татуаж бровей",
            "Наращивание ресниц", "Ламинирование ресниц", "Окрашивание ресниц", "Кератиновое ламинирование ресниц",
            "Перманентный макияж", "Татуаж губ", "Татуаж век", "Татуаж стрелки",
            "Солярий", "Автозагар", "Обёртывание", "Антицеллюлитное обёртывание",
            "Массаж тела", "Расслабляющий массаж", "Спортивный массаж", "Тайский массаж",
            "Ароматерапия", "Рефлексотерапия", "Криотерапия", "Прессотерапия",
            "Миостимуляция", "RF-лифтинг", "Ультразвуковой лифтинг", "Фотоомоложение",
            "Биоревитализация", "Мезотерапия", "Плазмолифтинг", "Контурная пластика",
            "Ботокс", "Диспорт", "Филлеры", "Нитевой лифтинг",
            "Пирсинг", "Татуировка", "Удаление татуировки", "Перманентный татуаж",
            "Уход за кожей", "Уход за телом", "Уход за волосами", "Уход за ногтями",
            "SPA-процедуры", "Банные процедуры", "Хаммам", "Сауна",
            "Йога", "Фитнес", "Стретчинг", "Пилатес",
            "Нутрициология", "Диетология", "Косметология", "Трихология",
            "Подология", "Ортопедия", "Подиатрия", "Реабилитация",
            "Арт-терапия", "Музыкальная терапия", "Цветотерапия", "Ароматерапия",
            "Аюрведа", "Китайская медицина", "Тибетская медицина", "Натуропатия",
        ]

    def setup_controls(self):
 
        self.main_container = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#FDFBFB", "#F4F6F7"]
            ),
            expand=True,
            padding=0,
            content=ft.Column(
                controls=[
                    self._build_app_bar(),
                    ft.Container(
                        expand=True,
                        padding=ft.padding.symmetric(horizontal=20),
                        content=ft.Column(
                            scroll=ft.ScrollMode.HIDDEN,
                            controls=[
                                self._build_avatar_section(),
                                ft.Container(height=20),
                                self._build_form_section(),
                                ft.Container(height=100), # Место для скролла
                            ]
                        )
                    )
                ],
                spacing=0
            )
        )

 
        self.fab_save = ft.Container(
            content=ft.Text("Сохранить изменения", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.PINK_500,
            padding=15,
            border_radius=30,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.4, ft.Colors.PINK_500), offset=ft.Offset(0, 5)),
            on_click=self._on_save_click,
            margin=ft.margin.only(left=20, right=20, bottom=20),
            animate_scale=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
            on_hover=self._animate_scale
        )

    def _build_app_bar(self):
        return ft.Container(
            padding=ft.padding.only(top=50, left=10, right=10, bottom=10),
            content=ft.Row([
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    icon_size=20,
                    icon_color=ft.Colors.BLACK87,
                    on_click=self._on_back_click
                ),
                ft.Text("Редактирование", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.BLACK87),
                ft.Container(width=40) # Для центровки
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

    def _build_avatar_section(self):
        img_src = self.master_data.get('profile_image_path')
        
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Stack([
                ft.Container(
                    width=120, height=120,
                    border_radius=60,
                    border=ft.border.all(4, ft.Colors.WHITE),
                    shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                    content=ft.Image(src=img_src, fit=ft.ImageFit.COVER) if img_src else 
                            ft.Container(bgcolor=ft.Colors.PINK_100, content=ft.Icon(ft.Icons.PERSON, size=60, color=ft.Colors.WHITE), alignment=ft.alignment.center),
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.CAMERA_ALT, size=18, color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.BLACK87,
                    padding=8,
                    border_radius=20,
                    border=ft.border.all(2, ft.Colors.WHITE),
                    bottom=0, right=0,
                    on_click=self._on_change_photo_click
                )
            ])
        )

    def _build_form_section(self):
 
        self.name_field = self._create_text_field("Имя", self.master_data.get('name', ''), ft.Icons.PERSON_OUTLINE)
        self.location_field = self._create_text_field("Адрес", self.master_data.get('location', ''), ft.Icons.LOCATION_ON_OUTLINED, on_change=self._on_location_change)
        
 
        self.location_suggestions_col = ft.Column(spacing=0)
        self.location_dropdown = ft.Container(
            content=self.location_suggestions_col,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            padding=5,
            margin=ft.margin.only(top=5)
        )

 
        self.services_field = ft.TextField(
            hint_text="Например: Маникюр",
            border=ft.InputBorder.NONE,
            text_size=16,
            content_padding=10,
            on_change=self._on_service_input_change,
            on_submit=lambda e: self._add_service_from_input(),
            expand=True
        )
        
        services_container = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SEARCH, color=ft.Colors.GREY_400),
                self.services_field,
                ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.PINK_500, on_click=lambda e: self._add_service_from_input())
            ]),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=10),
            border=ft.border.all(1, ft.Colors.GREY_200)
        )

        self.services_suggestions_col = ft.Column(spacing=0)
        self.services_dropdown = ft.Container(
            content=self.services_suggestions_col,
            visible=False,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            padding=5
        )
        
        self.services_chips_wrap = ft.Row(wrap=True, spacing=8, run_spacing=8)
        self._refresh_service_chips()

 
        self.social_fields = {
            'instagram': self._create_social_field("Instagram", self.master_data.get('instagram', ''), "https://cdn-icons-png.flaticon.com/512/1384/1384063.png"),
            'telegram': self._create_social_field("Telegram", self.master_data.get('telegram', ''), "https://cdn-icons-png.flaticon.com/512/2111/2111646.png"),
            'tiktok': self._create_social_field("TikTok", self.master_data.get('tiktok', ''), "https://cdn-icons-png.flaticon.com/512/3046/3046121.png"),
            'youtube': self._create_social_field("YouTube", self.master_data.get('youtube', ''), "https://cdn-icons-png.flaticon.com/512/1384/1384060.png"),
        }

        return ft.Column(
            controls=[
                self._section_header("Личные данные"),
                self.name_field,
                ft.Container(height=10),
                self.location_field,
                self.location_dropdown,
                
                ft.Container(height=20),
                self._section_header("Услуги"),
                services_container,
                self.services_dropdown,
                ft.Container(height=10),
                self.services_chips_wrap,
                
                ft.Container(height=20),
                self._section_header("Контакты"),
                ft.Column(list(self.social_fields.values()), spacing=10)
            ],
            spacing=0
        )

    def _create_text_field(self, label, value, icon, on_change=None):
        return ft.TextField(
            label=label,
            value=value,
            prefix_icon=icon,
            border_color="transparent",
            bgcolor=ft.Colors.WHITE, # Белый фон для четкости
            filled=True,
            border_radius=12,
            text_size=16,
            content_padding=15,
            on_change=on_change,
            color=ft.Colors.BLACK87,
            label_style=ft.TextStyle(color=ft.Colors.GREY_600)
        )

    def _create_social_field(self, hint, value, icon_src):
        return ft.Container(
            content=ft.Row([
                ft.Image(src=icon_src, width=24, height=24),
                ft.TextField(
                    value=value,
                    hint_text=hint,
                    border=ft.InputBorder.NONE,
                    height=40,
                    text_size=15,
                    content_padding=ft.padding.only(bottom=2),
                    expand=True
                )
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=ft.padding.symmetric(horizontal=10),
            border=ft.border.all(1, ft.Colors.GREY_200)
        )

    def _section_header(self, text):
        return ft.Container(
            content=ft.Text(text, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
            margin=ft.margin.only(bottom=10, left=5)
        )

    def _animate_scale(self, e):
        e.control.scale = 0.97 if e.data == "true" else 1.0
        e.control.update()

 
    def _on_service_input_change(self, e):
        query = e.control.value.strip().lower()
        self.services_suggestions_col.controls.clear()
        if not query:
            self.services_dropdown.visible = False
            self.page.update()
            return

        matches = [s for s in self.all_services if query in s.lower() and s not in self.selected_services][:5]
        if matches:
            for service in matches:
                self.services_suggestions_col.controls.append(
                    self._create_dropdown_item(service, lambda e, s=service: self._add_service(s))
                )
            self.services_dropdown.visible = True
        else:
            self.services_dropdown.visible = False
        self.page.update()

    def _create_dropdown_item(self, text, on_click):
        return ft.Container(
            content=ft.Text(text, size=15, color=ft.Colors.BLACK87),
            padding=12,
            on_click=on_click,
            on_hover=lambda e: self._on_dropdown_hover(e),
            bgcolor=ft.Colors.TRANSPARENT,
            border_radius=8
        )

    def _on_dropdown_hover(self, e):
        e.control.bgcolor = ft.Colors.GREY_100 if e.data == "true" else ft.Colors.TRANSPARENT
        e.control.update()

    def _add_service(self, service_name):
        if service_name and service_name not in self.selected_services:
            self.selected_services.append(service_name)
            self._refresh_service_chips()
            self.services_field.value = ""
            self.services_dropdown.visible = False
            self.page.update()

    def _add_service_from_input(self):
        val = self.services_field.value.strip()
        if val: self._add_service(val)

    def _remove_service(self, service_name):
        if service_name in self.selected_services:
            self.selected_services.remove(service_name)
            self._refresh_service_chips()
            self.page.update()

    def _refresh_service_chips(self):
        self.services_chips_wrap.controls = [
            ft.Container(
                content=ft.Row([
                    ft.Text(s, color=ft.Colors.PINK_700, size=13, weight=ft.FontWeight.W_500),
                    ft.Icon(ft.Icons.CLOSE, size=14, color=ft.Colors.PINK_400)
                ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                bgcolor=ft.Colors.PINK_50,
                border_radius=20,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border=ft.border.all(1, ft.Colors.PINK_100),
                on_click=lambda e, s=s: self._remove_service(s)
            ) for s in self.selected_services
        ]

 
    def _on_location_change(self, e):
        query = e.control.value.strip()
        if self._search_timer: self._search_timer.cancel()
        if len(query) < 2:
            self.location_dropdown.visible = False
            self.page.update()
            return
        self._search_timer = threading.Timer(0.5, self._fetch_location_suggestions, args=[query])
        self._search_timer.start()

    def _fetch_location_suggestions(self, query):
        """Запрос к API Yandex Suggest"""
        suggestions = []
        try:
            url = "https://suggest-maps.yandex.ru/v1/suggest"
            params = {
                'apikey': 'f2680357-6408-4059-b72c-ce34f45a4b31',
                'text': query,
                'lang': 'ru',
                'results': 5,
                'print_address': 1,
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
            }
            req = urllib.request.Request(
                f"{url}?{urllib.parse.urlencode(params)}",
                headers=headers
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.load(response)
                if 'results' in data:
                    for item in data['results']:
                        title = item.get('title', {}).get('text', '')
                        subtitle = item.get('subtitle', {}).get('text', '')
                        display = f"{title}, {subtitle}" if subtitle else title
                        if len(display) > 60:
                            display = display[:57] + '...'
                        suggestions.append(display)
        except Exception as e:
            print(f"API Error: {e}")
            suggestions = self._get_static_suggestions(query)
        
        self._update_location_dropdown_ui(suggestions)

    def _get_static_suggestions(self, query: str):
        cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Сочи", "Краснодар"]
        return [c for c in cities if query.lower() in c.lower()]

    def _update_location_dropdown_ui(self, suggestions):
        self.location_suggestions_col.controls.clear()
        if suggestions:
            for loc in suggestions:
                self.location_suggestions_col.controls.append(
                    self._create_dropdown_item(loc, lambda e, l=loc: self._select_location(l))
                )
            self.location_dropdown.visible = True
        else:
            self.location_dropdown.visible = False
        self.page.update()

    def _select_location(self, location):
        self.location_field.value = location
        self.location_dropdown.visible = False
        self.page.update()

 
    def _on_back_click(self, e):
        if self.app: self.app.router.navigate("/master/home")

    def _on_change_photo_click(self, e):
        self.show_snackbar("Смена фото пока недоступна", color=ft.Colors.ORANGE)

    def _on_save_click(self, e):
        name = self.name_field.value
        location = self.location_field.value
        
        if not name or not location:
            self.show_snackbar("Заполните имя и адрес!", color=ft.Colors.RED_400)
            return

        socials = {k: v.content.controls[1].value for k, v in self.social_fields.items()}
        bio = ", ".join(self.selected_services)

        if self.app and self.app.current_master:
            try:
 
                self.app.db.update_master_profile(
                    self.app.current_master['id'],
                    name=name, location=location, bio=bio, **socials
                )
                
 
 
                current_db_services = self.app.db.get_master_services(self.app.current_master['id'])
                existing_names = [s['name'] for s in current_db_services]

 
                for service_name in self.selected_services:
                    if service_name not in existing_names:
                        print(f"Добавляю новую услугу: {service_name}")
                        self.app.db.add_service(
                            self.app.current_master['id'],
                            name=service_name,
                            price=0, # Цена по умолчанию, мастер потом изменит
                            duration_minutes=60 # Время по умолчанию
                        )

 
                updated = self.app.db.get_master_by_id(self.app.current_master['id'])
                if updated: self.app.current_master = updated
                
                self.show_snackbar("Профиль и услуги сохранены!", color=ft.Colors.GREEN_400)
                self.app.router.navigate("/master/home")
            except Exception as ex:
                print(f"Save error: {ex}")
                self.show_snackbar("Ошибка сохранения", color=ft.Colors.RED)
        else:
            self.show_snackbar("Данные валидны (Демо)", color=ft.Colors.GREEN_400)

    def build(self) -> ft.Control:
        return ft.Stack([
            self.main_container,
            ft.Container(content=self.fab_save, bottom=0, left=0, right=0)
        ], expand=True)