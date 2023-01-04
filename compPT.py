from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty

Window.size = (400,700)
Window.clearcolor = (1, 1, 1, 1)

class StartScreen(Screen):
    pass

class SignUpScreen(Screen): #screen property allows switch between, layout nested inside
    email_info = StringProperty("")

    def on_text_validate_email(self, widget): #function that gets value of email text field when confirm button pressed
        self.text_input_email = widget.text
        print(self.text_input_email)

    def on_text_validate_pw(self, widget):
        self.text_input_pw = widget.text
        print(self.text_input_pw)

    def on_text_validate_target(self, widget):
        self.text_input_target = widget.text
        print(self.text_input_target)

class MainWidget(Widget):
    pass

class SilverWalletsApp(App):
    pass
SilverWalletsApp().run()
