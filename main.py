from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from pygments.lexers import CythonLexer
from kivy.uix.codeinput import CodeInput

class NavBarController(Widget):
    def setup(self, layout):
        org_btn = Button(text='File')
        import_btn = Button(text='Organisation')
        save_btn = Button(text='Run')
        run_btn = Button(text='Help')

        btns = [org_btn, import_btn, save_btn, run_btn]

        layout.add_widget(btns[0])
        layout.add_widget(btns[1])
        layout.add_widget(btns[2])
        layout.add_widget(btns[3])

        btns[0].bind(on_press=NavBarController.org_btn_press)
        btns[1].bind(on_press=NavBarController.import_btn_press)
        btns[2].bind(on_press=NavBarController.save_btn_press)
        btns[3].bind(on_press=NavBarController.run_btn_press)

        numButtons = len(btns)


    def org_btn_press(instance):
        print('File')


    def import_btn_press(instance):
        print('import')

    def save_btn_press(instance):
        print('Save')

    def run_btn_press(instance):
        print('Run')


class TextEditor(Widget):
    app_container = ObjectProperty(None)
    nav_container = ObjectProperty(None)
    text_container = ObjectProperty(None)

    def on_text(self, instance, value):
        self.text = value

    def setup(self):
        self.text = ""
        width = 500
        height = 500
        Window.size = (width, height)
        Window.bind(on_resize=self.on_window_resize)
        Config.set('graphics', 'resizable', '0')

        navBar = NavBarController()
        navBarBtnsContainer = navBar.setup(self.nav_container)

        codeinput = CodeInput(lexer=CythonLexer())
        codeinput.bind(text=self.on_text)
        self.text_container.add_widget(codeinput)

    def on_window_resize(self, window, width, height):
        print("width", width)
        self.app_container.size = width, height
        self.nav_container.size_hint = 500/width * 0.8, 500/height * 0.05
    #navBar = ObjectProperty(None)



class MainApp(App):
    def build(self):
        app = TextEditor()
        app.setup()
        return app

if __name__ == '__main__':
    MainApp().run()
