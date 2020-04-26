
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
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from filesystem import FileSystem
import os

import tkinter as tk

cache = {'organisation': None, 'password': None}

class NavBarController:
    fileDropdown = DropDown()
    orgDropdown = DropDown()
    runDropdown = DropDown()

    def setup(self, layout):
        help_btn = Button(text='Help', font_size=14)

        #File Drop down
        self.createFile_btn = Button(text='Create', font_size=14, size_hint_y=None, height=30)
        self.import_btn = Button(text='Import', font_size=14, size_hint_y=None, height=30)
        self.loadFile_btn = Button(text='Load', font_size=14, size_hint_y=None, height=30)
        self.saveFile_btn = Button(text='Save', font_size=14, size_hint_y=None, height=30)

        self.createFile_btn.bind(on_press=TextEditor.create_btn_press)
        self.import_btn.bind(on_press=TextEditor.import_file_btn_press)
        self.loadFile_btn.bind(on_press=TextEditor.load_btn_press)
        self.saveFile_btn.bind(on_press=TextEditor.save_btn_press)

        file_btns = [self.createFile_btn, self.import_btn, self.loadFile_btn, self.saveFile_btn]

        fileDropDownSetup = DropDownController()
        self.fileButton = fileDropDownSetup.setup(NavBarController.fileDropdown, file_btns, "File")
        self.fileButton.size_hint_y = 1

        #Organisaition Dropdown
        self.createOrg_btn = Button(text='Create Org', font_size=14, size_hint_y=None, height=30)
        self.loadOrg_btn = Button(text='Login to Org', font_size=14, size_hint_y=None, height=30)
        self.viewOrg_btn = Button(text='View Org', font_size=14, size_hint_y=None, height=30)

        self.createOrg_btn.bind(on_press=TextEditor.createOrg_btn_press)
        self.loadOrg_btn.bind(on_press=TextEditor.loadOrg_btn_press)
        self.viewOrg_btn.bind(on_press=TextEditor.viewOrg_btn_press)

        org_btns = [self.createOrg_btn, self.loadOrg_btn, self.viewOrg_btn]

        orgDropDownSetup = DropDownController()
        self.orgButton = orgDropDownSetup.setup(NavBarController.orgDropdown, org_btns, "Organisation")
        self.orgButton.size_hint_y = 1

        #Run Dropdown
        self.runBasic_btn = Button(text='Run', font_size=14, size_hint_y=None, height=30)
        self.runWidthArgs_btn = Button(text='Run Args', font_size=14, size_hint_y=None, height=30)
        self.compile_btn = Button(text='Compiles', font_size=14, size_hint_y=None, height=30)

        self.runBasic_btn.bind(on_press=TextEditor.runBasic_btn_press)
        self.runWidthArgs_btn.bind(on_press=TextEditor.runWidthArgs_btn_press)
        self.compile_btn.bind(on_press=TextEditor.compile_btn_press)

        run_btns = [self.runBasic_btn, self.runWidthArgs_btn, self.compile_btn]

        runDropdownSetup = DropDownController()
        self.runBtn = runDropdownSetup.setup(NavBarController.runDropdown, run_btns, "Run")
        self.runBtn.size_hint_y = 1

        # layout.add_widget(self.org_btn)
        btns = [self.fileButton, self.orgButton, self.runBtn, help_btn]

        for btn in btns:
            layout.add_widget(btn)

        btns[0].bind(on_release=NavBarController.fileDropdown.open, on_press=NavBarController.printPressed)
        btns[1].bind(on_release=NavBarController.orgDropdown.open, on_press=NavBarController.printPressed)
        btns[2].bind(on_release=NavBarController.runDropdown.open, on_press=NavBarController.printPressed)
        btns[3].bind(on_press=TextEditor.help_btn_press)



    def printPressed(a):
        print("Press")


class DropDownController():
    def setup(self, dropdown, btns, title):
        for btn in btns:
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        mainbutton = Button(text=title, size_hint=(None, None), height = 14)
        mainbutton.bind(on_release=dropdown.open, on_press=self.printPressed)
        return mainbutton

    def printPressed(self, x):
        print("pressed")

class TextEditor(Widget):
    app_container = ObjectProperty(None)
    nav_container = ObjectProperty(None)
    text_container = ObjectProperty(None)
    text = ""
    organisation = None
    password = None
    codeinput = None

    def on_text(instance, value):
        TextEditor.text = value
        print(value)

    def setup(self):
        width = 500
        height = 500
        Window.size = (width, height)
        Window.bind(on_resize=self.on_window_resize)
        Config.set('graphics', 'resizable', '0')
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

        Window.bind(on_keyboard=self.on_keyboard)

        navBar = NavBarController()
        navBarBtnsContainer = navBar.setup(self.nav_container)

        TextEditor.codeinput = CodeInput(lexer=CythonLexer())
        TextEditor.codeinput.bind(text=TextEditor.on_text)
        TextEditor.codeinput.text = 'start'

        self.text_container.add_widget(TextEditor.codeinput)

    def updateCodeInput(newstring):
        print(newstring)
        TextEditor.codeinput.text = newstring

    def updateCodeInput(newstring):
        print(newstring)
        TextEditor.codeinput.text = newstring

    def on_window_resize(self, window, width, height):
        print("width", width)
        self.app_container.size = width, height
        self.nav_container.size_hint = 500/width * 0.8, 500/height * 0.05
    #navBar = ObjectProperty(None)

    # FILE DROPDOWN EVENTS
    def create_btn_press(instance):
        print("Create")

    def import_file_btn_press(instance):
        print('import file')
        lsd = LoadSaveDialog()
        lsd.show_load()

    def load_btn_press(instance):
        print("Load")

    def save_btn_press(instance):
        print("Save")

    # ORG DROPDOWN EVENTS
    def createOrg_btn_press(instance):
        print("Create Org")
        popup = CreateOrgPopup()
        popup.setup()

    def loadOrg_btn_press(instance):
        print("Load Org")
        popup = PopupInput()
        popup.setup()

    def viewOrg_btn_press(instance):
        print("View Orgs")

    # RUN DROPDOWN EVENTS
    def runBasic_btn_press(instance):
        print("Basic Run")
    def runWidthArgs_btn_press(instance):
        print("Run Args")
    def compile_btn_press(instance):
        print("Compile")

    # HELP BTN PRESS
    def help_btn_press(instance):
        print("Help")

    def save_btn_press(instance):
        pass
        # print('Save')
        # fs = FileSystem()
        # fs.updateFile('finnsFile.enc', TextEditor.text, 'Student Hack', 'test1234')
        # print(TextEditor.text)

    def save(self):
        pass
        # print('Save')
        # fs = FileSystem()
        # fs.updateFile('finnsFile.enc', TextEditor.text, 'Student Hack', 'test1234')
        # print(TextEditor.text)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if 'ctrl' in modifier and codepoint == 's':
            print("Clicked")
            self.save()

    def run_btn_press(instance):
        print('Run')

class CreateOrgPopup(Widget):
    org = ''
    pas = ''
    popup = None

    def set_org(instance, value):
        CreateOrgPopup.org = value

    def get_org(self):
        return CreateOrgPopup.org

    def set_pas(instance, value):
        CreateOrgPopup.pas = value

    def get_pas(self):
        return CreateOrgPopup.pas

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
        inputOrg.bind(text=CreateOrgPopup.set_org)
        inputPas.bind(text=CreateOrgPopup.set_pas)
        CreateOrgPopup.popup = Popup(title='Enter credentials for new Organisation',
            content=layout, size_hint=(0.6, 0.6))
        CreateOrgPopup.popup.open()
        button.bind(on_press=self.confirm_clicked)
        print('here1')

    def confirm_clicked(self, x):
        CreateOrgPopup.popup.dismiss()
        # validate the credentials
        print(CreateOrgPopup.org, CreateOrgPopup.pas)
        organisation = CreateOrgPopup.org
        password = CreateOrgPopup.pas

        fs = FileSystem()
        # first check if an organisation with this name already exists
        popup_msg = ""
        err = False
        try:
            if(len(password) == 0):
                raise ValueError()
            fs.getOrganisationKey(organisation, password)
            popup_msg = "Organisation already exists!"
            err = True
        except FileNotFoundError:
            # the organisation does not exist
            fs.createOrganisation(organisation, password)
            cache['organisation'] = organisation
            cache['password'] = password
            popup_msg = "Organisation created successfully!"
        except ValueError:
            err = True
            popup_msg = "Please provide a password!"
        finally:
            layout = BoxLayout(orientation='vertical')
            popup_title = "Error" if err else "Confirmation"
            label1 = Label(text=popup_title)
            label = Label(text=popup_msg)
            button = Button(text='Dismiss')
            layout.add_widget(label)
            layout.add_widget(button)
            popup = Popup(title=popup_title,
                content=layout, size_hint=(None, None), size=(400, 250))
            popup.open()
            button.bind(on_press=popup.dismiss)



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
            cache['organisation'] = organisation
            cache['password'] = password
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
            label1 = Label(text=popup_title)
            label = Label(text=popup_msg)
            button = Button(text='Dismiss')
            layout.add_widget(label)
            layout.add_widget(button)
            popup = Popup(title=popup_title,
                content=layout, size_hint=(None, None), size=(400, 250))
            popup.open()
            button.bind(on_press=popup.dismiss)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class LoadSaveDialog(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    #text_input = ObjectProperty(None)
    string = ""
    file_to_load = None
    org = ''
    pas = ''
    popup = None

    def set_org(instance, value):
        LoadSaveDialog.org = value

    def get_org(self):
        return LoadSaveDialog.org

    def set_pas(instance, value):
        LoadSaveDialog.pas = value

    def get_pas(self):
        return LoadSaveDialog.pas

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        LoadSaveDialog.file_to_load = filename
        with open(os.path.join(path, filename[0])) as stream:
            LoadSaveDialog.string= stream.read()

        print(path, filename)
        # ask the user for organisation name and password
        if (cache['organisation'] != None):
            # the user is logged in to an org
            organisation = cache['organisation']
            password = cache['password']
            if ext != 'enc':
                # the file needs to be encrypted first
                print('here3')
                fs.createFile(filename[0], organisation, password)
                print(TextEditor.codeinput.text)
                TextEditor.updateCodeInput(LoadSaveDialog.string)
                print(TextEditor.codeinput.text)
                print(LoadSaveDialog.string)
            else:
                print(fs.readFile(filename, organisation, password))
                TextEditor.codeinput.text = fs.readFile(filename, organisation, password)
        else:
            # the user needs to be prompted to login first
            popup_msg = "Please login to an organisation first!"
            layout = BoxLayout(orientation='vertical')
            popup_title = "Error"
            label1 = Label(text=popup_title)
            label = Label(text=popup_msg)
            button = Button(text='Dismiss')
            layout.add_widget(label1)
            layout.add_widget(label)
            layout.add_widget(button)
            popup = Popup(title=popup_title,
                content=layout, size_hint=(0.6, 0.6))
            popup.open()
            button.bind(on_press=popup.dismiss)

        self.dismiss_popup()

    '''def confirm_clicked(self, x):
        LoadSaveDialog.popup.dismiss()
        filename = LoadSaveDialog.file_to_load
        # validate the credentials
        #print(PopupInput.org, PopupInput.pas)
        organisation = PopupInput.org
        password = PopupInput.pas
        fs = FileSystem()
        popup_msg = ""
        err = True
        try:
            print('here2')
            fs.getOrganisationKey(organisation, password)
            popup_msg = "Logged in to: "+organisation
            err = False
            ext = filename[0].split('.')[-1]
            print('here1')
            print(LoadSaveDialog.string)
            if ext != 'enc':
                # the file needs to be encrypted first
                print('here3')
                fs.createFile(filename[0], organisation, password)
                print(TextEditor.codeinput.text)
                TextEditor.updateCodeInput(LoadSaveDialog.string)
                print(TextEditor.codeinput.text)
                print(LoadSaveDialog.string)
            else:
                print(fs.readFile(filename, organisation, password))
                TextEditor.codeinput.text = fs.readFile(filename, organisation, password)
        except FileNotFoundError:
            # the organisation does not exis
            popup_msg = "Organisation not found!"
        except TypeError as e:
            # password not provided
            print(e.print_tb())
            popup_msg = "Password not provided!"
        except ValueError:
            # invalid password
            popup_msg = "Invalid Password!"
        finally:
            #if err:
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
            print("Done")'''

    def save(self, path, filename):
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()

ref = None
class MainApp(App):
    def build(self):
        app = TextEditor()
        ref = app
        app.setup()
        return app

Factory.register('LoadSaveDialog', cls=LoadSaveDialog)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    MainApp().run()
