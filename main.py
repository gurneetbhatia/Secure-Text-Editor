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
from filesystem import FileSystem

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

        btns[0].bind(on_press=TextEditor.org_btn_press)
        btns[1].bind(on_press=TextEditor.import_btn_press)
        btns[2].bind(on_press=TextEditor.save_btn_press)
        btns[3].bind(on_press=TextEditor.run_btn_press)




class TextEditor(Widget):
    app_container = ObjectProperty(None)
    nav_container = ObjectProperty(None)
    text_container = ObjectProperty(None)
    text = ""

    def on_text(instance, value):
        TextEditor.text = value
        print(value)

    def setup(self):
        width = 500
        height = 500
        Window.size = (width, height)
        Window.bind(on_resize=self.on_window_resize)
        Config.set('graphics', 'resizable', '0')

        Window.bind(on_keyboard=self.on_keyboard)

        navBar = NavBarController()
        navBarBtnsContainer = navBar.setup(self.nav_container)

        codeinput = CodeInput(lexer=CythonLexer())
        codeinput.bind(text=TextEditor.on_text)
        self.text_container.add_widget(codeinput)

    def on_window_resize(self, window, width, height):
        print("width", width)
        self.app_container.size = width, height
        self.nav_container.size_hint = 500/width * 0.8, 500/height * 0.05
    #navBar = ObjectProperty(None)

    def org_btn_press(instance):
        print('File')

    def import_btn_press(instance):
        print('import')

    def save_btn_press(instance):
        print('Save')
        fs = FileSystem()
        fs.updateFile('finnsFile.enc', TextEditor.text, 'Student Hack', 'test1234')
        print(TextEditor.text)

    def save(self):
        print('Save')
        fs = FileSystem()
        fs.updateFile('finnsFile.enc', TextEditor.text, 'Student Hack', 'test1234')
        print(TextEditor.text)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if modifier == ['ctrl'] and codepoint == 's':
            print("Clicked")
            self.save()

    def run_btn_press(instance):
        print('Run')



class MainApp(App):
    def build(self):
        app = TextEditor()
        app.setup()
        return app

if __name__ == '__main__':
    MainApp().run()
