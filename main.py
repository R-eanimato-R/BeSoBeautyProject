import flet as ft
import flet.fastapi as flet_fastapi
from fastapi import FastAPI
import uvicorn
import os
import sys
import asyncio

 
from app import BeautyApp

 
async def main(page: ft.Page):
    try:
 
        app = BeautyApp(page)
        app.setup_page()
        
 
 
        loading_screen = ft.Container(
            content=ft.Column([
                ft.ProgressRing(color=ft.Colors.PINK_400),
                ft.Text("Загрузка...", color=ft.Colors.GREY_500)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.WHITE
        )
        page.add(loading_screen)
        page.update()

 
 
        await asyncio.sleep(0.5)
        
 
        try:
 
 
            app.initialize_app()
        except TimeoutError:
            print("⚠️ Client Storage Timeout. Браузер не ответил вовремя.")
 
 
            if not app.current_user_id:
                print("   -> Создаем временного Dev-пользователя.")
                dev_id = app._get_or_generate_user_id()
                app.current_user_id = dev_id
 
                app.db.get_or_create_client(dev_id, name="Dev User")
                app.router.navigate("/welcome")
        except Exception as e:
            print(f"Ошибка логики app: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        page.clean()
        page.add(ft.Text(f"Ошибка запуска: {str(e)}", color="red"))
        page.update()

 
fastapi_app = FastAPI()
fastapi_app.mount("/", flet_fastapi.app(main, assets_dir="assets"))

 
if __name__ == "__main__":
    cert_path = r"C:\Certbot\live\beauty-be.ru-0001\fullchain.pem"
    key_path = r"C:\Certbot\live\beauty-be.ru-0001\privkey.pem"
    is_production = os.path.exists(cert_path) and os.path.exists(key_path)

    if is_production:
        print("PRODUCTION MODE: Запуск через Uvicorn с SSL (Port 443)")
        uvicorn.run(
            "main:fastapi_app", 
            host="0.0.0.0",
            port=443,
            ssl_certfile=cert_path,
            ssl_keyfile=key_path,
            reload=False
        )
    else:
        print("DEV MODE: Запуск через python main.py (Port 8000)")
        ft.app(
            target=main,
            port=8000,
            view=ft.AppView.WEB_BROWSER,
            assets_dir="assets"
        )