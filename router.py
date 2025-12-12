 
import flet as ft
from views.auth.welcome_view import WelcomeView
from views.master.master_home import MasterHomeView
from views.master.profile_edit import MasterProfileEditView
 
from views.master.schedule_view import ScheduleView
from views.master.services_edit import ServicesEditView
from views.master.bookings_view import BookingsView
from views.master.placeholders import SubscriptionView, CreativeView, AboutView

class Router:
    def __init__(self, app):
        self.app = app
        self.routes = {
            '/welcome': self._load_welcome_view,
            '/client/home': self._load_client_home,
            '/master/home': self._load_master_home,
            '/master/profile_edit': self._load_master_profile_edit,
            '/master/schedule': self._load_schedule,
            '/master/services': self._load_services,
            '/master/bookings': self._load_bookings,
            '/master/subscription': self._load_subscription,
            '/master/creative': self._load_creative,
            '/about': self._load_about,
            '/help': self._load_about, 
        }
        self.current_route = None
        
    def navigate(self, route: str):
        print(f"Navigate: {route}")
 
        if route.startswith('/client/master/'):
            try:
                master_id = int(route.split('/')[-1])
                self._load_client_master(master_id)
                self.current_route = route
                return
            except Exception as e:
                print(f"Error parsing route {route}: {e}")

        if route in self.routes:
            self.current_route = route
            try:
                self.routes[route]()
                print(f"Маршрут {route} загружен успешно")
            except Exception as e:
                print(f"ОШИБКА при загрузке маршрута {route}: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"Маршрут {route} не найден")
            
    def _load_welcome_view(self):
        self._change_view(WelcomeView(self.app.page, self.app))
    
    def _load_client_home(self):
        from views.client.client_home import ClientHomeView
        self._change_view(ClientHomeView(self.app.page, self.app))
        
    def _load_master_home(self):
        self._change_view(MasterHomeView(self.app.page, self.app))
    
    def _load_master_profile_edit(self):
        self._change_view(MasterProfileEditView(self.app.page, self.app, self.app.current_master))

    def _load_schedule(self):
        self._change_view(ScheduleView(self.app.page, self.app))

    def _load_services(self):
        self._change_view(ServicesEditView(self.app.page, self.app))

    def _load_bookings(self):
        self._change_view(BookingsView(self.app.page, self.app))

    def _load_subscription(self):
        self._change_view(SubscriptionView(self.app.page, self.app))

    def _load_creative(self):
        self._change_view(CreativeView(self.app.page, self.app))

    def _load_about(self):
        self._change_view(AboutView(self.app.page, self.app))

    def _load_client_master(self, master_id):
        from views.client.master_profile import ClientMasterProfileView
        self._change_view(ClientMasterProfileView(self.app.page, self.app, master_id))

    def _change_view(self, view):
        self.app.page.clean()
        self.app.page.add(view.build())
        self.app.page.update()