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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp


class NavBarController(Widget):
    def setup(self, layout):
        createFile_btn = Button(text='Create', font_size=14, size_hint_y=None, height=44)
        loadFile_btn = Button(text='Load', font_size=14, size_hint_y=None, height=44)
        saveFile_btn = Button(text='Save', font_size=14, size_hint_y=None, height=44)
        createFile_btn.bind(on_press=TextEditor.create_btn_press)
        loadFile_btn.bind(on_press=TextEditor.load_btn_press)
        saveFile_btn.bind(on_press=TextEditor.save_btn_press)
        file_btns = [createFile_btn, loadFile_btn, saveFile_btn]
        fileDropDownSetup = DropDownController()
        file_btn = fileDropDownSetup.setup(file_btns, "file")

        import_btn = Button(text='Organisation', font_size=14)
        save_btn = Button(text='Run', font_size=14)
        run_btn = Button(text='Help', font_size=14)

        btns = [file_btn, import_btn, save_btn, run_btn]

        for btn in btns:
            layout.add_widget(btn)

        btns[0].bind(on_press=TextEditor.org_btn_press)
        btns[1].bind(on_press=TextEditor.import_btn_press)
        btns[2].bind(on_press=TextEditor.save_btn_press)
        btns[3].bind(on_press=TextEditor.run_btn_press)

class DropDownController(Widget):
    def setup(self, btns, title):
        dropdown = DropDown()
        for btn in btns:
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbutton = Button(text=title, size_hint=(None, None))
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        return mainbutton

class TextEditor(Widget):
    app_container = ObjectProperty(None)
    nav_container = ObjectProperty(None)
    text_container = ObjectProperty(None)
    text = ""
    organisation = None
    password = None

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


    def create_btn_press(instance):
        print("Create")
    def load_btn_press(instance):
        print("Load")
    def save_btn_press(instance):
        print("Save")

    def org_btn_press(instance):
        print('File')

    def import_btn_press(instance):
        print('import')
        PopupInput.setup()

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
        #print("Any Key")
        #print(modifier)
        #print(key)
        #print(codepoint)
        if 'ctrl' in modifier and codepoint == 's':
            print("Clicked")
            self.save()

    def run_btn_press(instance):
        print('Run')

class PopupInput(Widget):
    org = ''
    pas = ''

    def set_org(instance, value):
        PopupInput.org = value

    def get_org(self):
        return org

    def set_pas(instance, value):
        PopupInput.pas = value

    def get_pas(self):
        return pas

    def setup(self):
        layout = BoxLayout(orientation='vertical')
        labelOrg = Label(text='Organisation')
        inputOrg = TextInput(text='Enter Organisation', multiline=False)
        labelPas = Label(text='Password')
        inputPas = TextInput(text='Enter Password', multiline=False)
        button = Button(text='Confirm')
        layout.add_widget(labelOrg)
        layout.add_widget(inputOrg)
        layout.add_widget(labelPas)
        layout.add_widget(inputPas)
        layout.add_widget(button)
        inputOrg.bind(text=PopupInput.set_org)
        inputPas.bind(text=PopupInput.set_pas)
        popup = Popup(title='Enter credentials',
            content=layout, size_hint=(None, None), size=(400, 200))
        popup.open()
        button.bind(on_press=popup.dismiss)

class MainApp(App):
    def build(self):
        app = TextEditor()
        app.setup()
        return app

if __name__ == '__main__':
    MainApp().run()
