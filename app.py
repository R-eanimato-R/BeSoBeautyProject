 
import flet as ft
from router import Router
from config import AppConfig
from database import Database
import random
import string
import json
import time

class BeautyApp:
    def __init__(self, page: ft.Page):
        print("Инициализация BeautyApp...")
        self.page = page
        print("Router инициализируется...")
        self.router = Router(self)
        print("Config инициализируется...")
        self.config = AppConfig()
        print("БД инициализируется (lazy)...")
        self._db = None  
        
        self.current_user_id = None
        self.tg_user_data = None
        self.current_master = None
        self.current_client = None
        self.current_space = "client"  
        print("BeautyApp инициализирована успешно")
    
    @property
    def db(self):
        """Ленивая инициализация БД"""
        if self._db is None:
            try:
                self._db = Database()
            except Exception as e:
                print(f"Ошибка инициализации БД: {e}")
                raise
        return self._db
        
    def setup_page(self):
        """Базовая настройка страницы"""
        print("Настройка страницы...")
        self.page.title = "BeautySpace"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.spacing = 0
        self.page.bgcolor = self.config.colors['background']
        self.page.fonts = self.config.fonts
        
 
        try:
            _ = self.db
        except Exception as e:
            print(f"ОШИБКА инициализации БД: {e}")

    def initialize_app(self):
        """
        Главная точка входа.
        Пытается получить данные ТГ, определяет роль и направляет на нужный экран.
        """
        print("Запуск инициализации приложения...")
        
 
 
 
        
        tg_data_str = self.page.client_storage.get("tg_user_data")
        
        if tg_data_str:
            try:
                user_data = json.loads(tg_data_str)
                self.current_user_id = str(user_data.get('id'))
                self.tg_user_data = user_data
                print(f"✅ Авторизован через Telegram: {self.current_user_id} ({user_data.get('first_name')})")
            except Exception as e:
                print(f"❌ Ошибка парсинга данных ТГ: {e}")
                self.current_user_id = self._get_or_generate_user_id()
        else:
            print("⚠️ Данные Telegram не найдены, используем тестовый режим (Dev)")
 
            dev_id = self.page.client_storage.get("dev_user_id")
            if not dev_id:
                dev_id = self._get_or_generate_user_id()
                self.page.client_storage.set("dev_user_id", dev_id)
            self.current_user_id = dev_id

 
        role = self.db.check_user_role(self.current_user_id)
        print(f"Роль пользователя: {role}")

        if role == 'master':
            self.switch_space("master")
        elif role == 'client':
            self.switch_space("client")
        else:
 
 
            first_name = self.tg_user_data.get('first_name', '') if self.tg_user_data else "Гость"
            self.db.get_or_create_client(self.current_user_id, name=first_name)
            self.router.navigate("/welcome")

    def _get_or_generate_user_id(self) -> str:
        random_id = ''.join(random.choices(string.digits, k=6))
        return f"dev_user_{random_id}"
    
    def show_snackbar(self, message: str, color="#FF9EB5"):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()
        
    def switch_space(self, space: str):
        """Переключение между клиентом и мастером"""
        print(f"Switch space: {space}")
        if space in ["client", "master"]:
            self.current_space = space
            
            if space == "master":
                try:
                    self.current_master = self.db.get_or_create_master(self.current_user_id)
 
                    if self.tg_user_data and not self.current_master.get('name'):
                        name = f"{self.tg_user_data.get('first_name', '')} {self.tg_user_data.get('last_name', '')}".strip()
                        username = self.tg_user_data.get('username', '')
                        self.db.update_master_profile(self.current_master['id'], name=name, username=username)
                        self.current_master = self.db.get_master_by_id(self.current_master['id'])
                    
                    self.router.navigate("/master/home")
                except Exception as e:
                    print(f"ОШИБКА загрузки мастера: {e}")
                    self.show_snackbar("Ошибка загрузки профиля")
            
            elif space == "client":
                try:
                    self.current_client = self.db.get_or_create_client(self.current_user_id)
                    self.router.navigate("/client/home")
                except Exception as e:
                    print(f"ОШИБКА загрузки клиента: {e}")

    def get_current_space(self):
        return self.current_space