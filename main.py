from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from pygments.lexers import PythonLexer
from pygments.lexers import JavaLexer
from pygments.lexers import CppLexer


from kivy.uix.codeinput import CodeInput
from filesystem import FileSystem
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp

from filesystem import FileSystem

from tkinter import filedialog
from tkinter import Tk

class NavBarController:
    def setup(self, layout):
        import_btn = Button(text='Organisation', font_size=14)
        save_btn = Button(text='Run', font_size=14)
        run_btn = Button(text='Help', font_size=14)

        self.createOrg_btn = Button(text='Create Org', font_size=14, size_hint_y=None, height=30)
        self.loadOrg_btn = Button(text='Load Org', font_size=14, size_hint_y=None, height=30)
        self.viewOrg_btn = Button(text='View Org', font_size=14, size_hint_y=None, height=30)

        self.createOrg_btn.bind(on_press=TextEditor.createOrg_btn_press)
        self.loadOrg_btn.bind(on_press=TextEditor.loadOrg_btn_press)
        self.viewOrg_btn.bind(on_press=TextEditor.viewOrg_btn_press)

        org_btns = [self.createOrg_btn, self.loadOrg_btn, self.viewOrg_btn]
        orgDropDownSetup = DropDownController()
        self.org_btn = orgDropDownSetup.setup(org_btns, "Organisation")
        self.org_btn.size_hint_y = 1

        self.createFile_btn = Button(text='Create', font_size=14, size_hint_y=None, height=30)
        self.loadFile_btn = Button(text='Load', font_size=14, size_hint_y=None, height=30)
        self.saveFile_btn = Button(text='Save', font_size=14, size_hint_y=None, height=30)

        self.createFile_btn.bind(on_press=TextEditor.create_btn_press)
        self.loadFile_btn.bind(on_press=TextEditor.load_btn_press)
        self.saveFile_btn.bind(on_press=TextEditor.save_btn_press)

        file_btns = [self.createFile_btn, self.loadFile_btn, self.saveFile_btn]
        fileDropDownSetup = DropDownController()
        self.file_btn = fileDropDownSetup.setup(file_btns, "File")
        self.file_btn.size_hint_y = 1

        btns = [import_btn, save_btn, run_btn]


        layout.add_widget(self.file_btn)
        layout.add_widget(self.org_btn)
        btns = [import_btn, save_btn, run_btn]

        for btn in btns:
            layout.add_widget(btn)

        btns[0].bind(on_press=TextEditor.import_btn_press)
        btns[1].bind(on_press=TextEditor.save_btn_press)
        btns[2].bind(on_press=TextEditor.run_btn_press)

class DropDownController(Widget):
    def setup(self, btns, title):
        print("Done")
        dropdown = DropDown()
        for btn in btns:
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        self.mainbutton = Button(text=title, size_hint=(None, None), height = 14)
        self.mainbutton.bind(on_release=dropdown.open)
        return self.mainbutton

        mainbutton = Button(text='File', size_hint=(None, None))
        print(mainbutton.text)
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        return mainbutton

class TextEditor(Widget):
    app_container = ObjectProperty(None)
    nav_container = ObjectProperty(None)
    text_container = ObjectProperty(None)
    lex = None
    text = ""
    organisation = None
    password = None
    filepath = None

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

        codeinput = CodeInput(lexer=PythonLexer())
        self.choose_lexer()
        codeinput.lexer = TextEditor.lex
        codeinput.bind(text=TextEditor.on_text)

        self.text_container.add_widget(codeinput)

    def choose_lexer(self):
        fs = FileSystem()
        if TextEditor.filepath != None:
            ext = fs.getFileType(TextEditor.filepath)
            if ext == 'py':
                TextEditor.lex = PythonLexer()
            elif ext == 'java':
                TextEditor.lex = JavaLexer()
            elif ext == 'cpp':
                TextEditor.lex = CppLexer()
        else:
            # No extension
            TextEditor.lex = PythonLexer()

    def on_window_resize(self, window, width, height):
        print("width", width)
        self.app_container.size = width, height
        self.nav_container.size_hint = 500/width * 0.8, 500/height * 0.05
    #navBar = ObjectProperty(None)

    # FILE DROPDOWN EVENTS
    def create_btn_press(instance):
        print("Create")

    def load_btn_press(instance):
        print("Load")
        tk = Tk()
        tk.geometry('0x0+0+0')
        filename = filedialog.askopenfilename(title="Select a .enc file", filetypes=("enc files", "*.enc"))
        print(filename)
        tk.destroy()

    def save_btn_press(instance):
        print("Save")

    # ORG DROPDOWN EVENTS
    def createOrg_btn_press(instance):
        print("Create Org")
    def loadOrg_btn_press(instance):
        print("Load Org")
    def viewOrg_btn_press(instance):
        print("View Orgs")

    def org_btn_press(instance):
        print('File')

    def import_btn_press(instance):
        print('import')
        popup = PopupInput()
        popup.setup()

    def popupdismiss(instance):
        print('here')

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
    popup = None

    def set_org(instance, value):
        PopupInput.org = value

    def get_org(self):
        return PopupInput.org

    def set_pas(instance, value):
        PopupInput.pas = value

    def get_pas(self):
        return PopupInput.pas

    def confirm(self):
        pass

    def setup(self):
        layout = BoxLayout(orientation='vertical')
        labelOrg = Label(text='Organisation')
        inputOrg = TextInput(multiline=False)
        labelPas = Label(text='Password')
        inputPas = TextInput(multiline=False)
        button = Button(text='Confirm')
        layout.add_widget(labelOrg)
        layout.add_widget(inputOrg)
        layout.add_widget(labelPas)
        layout.add_widget(inputPas)
        layout.add_widget(button)
        inputOrg.bind(text=PopupInput.set_org)
        inputPas.bind(text=PopupInput.set_pas)
        PopupInput.popup = Popup(title='Enter credentials',
            content=layout, size_hint=(None, None), size=(400, 250))
        PopupInput.popup.open()
        button.bind(on_press=self.confirm_clicked)

    def confirm_clicked(self, x):
        PopupInput.popup.dismiss()
        # validate the credentials
        print(PopupInput.org, PopupInput.pas)
        organisation = PopupInput.org
        password = PopupInput.pas
        fs = FileSystem()
        popup_msg = ""
        err = True
        try:
            fs.getOrganisationKey(organisation, password)
            popup_msg = "Logged in to: "+organisation
            err = False
        except FileNotFoundError:
            # the organisation does not exis
            popup_msg = "Organisation not found!"
        except TypeError:
            # password not provided
            popup_msg = "Password not provided!"
        except ValueError:
            # invalid password
            popup_msg = "Invalid Password!"
        finally:
            layout = BoxLayout(orientation='vertical')
            popup_title = "Error" if err else "Confirmation"
            label = Label(text=popup_msg)
            button = Button(text='Dismiss')
            layout.add_widget(label)
            layout.add_widget(button)
            popup = Popup(title=popup_title,
                content=layout, size_hint=(None, None), size=(400, 250))
            popup.open()
            button.bind(on_press=popup.dismiss)


class MainApp(App):
    def build(self):
        app = TextEditor()
        app.setup()
        return app

if __name__ == '__main__':
    MainApp().run()
