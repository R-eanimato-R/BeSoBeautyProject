 
import flet as ft

class BaseView:
    def __init__(self, page: ft.Page):
        self.page = page
        
    def build(self) -> ft.Control:
        """Должен возвращать основной контейнер view"""
        raise NotImplementedError("Метод build должен быть реализован в дочернем классе")
    
    def on_swipe(self, direction: str):
        """Обработчик свайпов (пока заглушка)"""
        pass
        
    def show_snackbar(self, message: str, color: str = "#FF9EB5"):
        """Показать уведомление"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()