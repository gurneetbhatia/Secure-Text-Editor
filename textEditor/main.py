from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.core.window import Window

class NavBarController(Widget):
    def setup(self, width, height, btns, bk):
        btns[0].bind(on_press=NavBarController.org_btn_press)
        btns[1].bind(on_press=NavBarController.import_btn_press)
        btns[2].bind(on_press=NavBarController.save_btn_press)
        btns[3].bind(on_press=NavBarController.run_btn_press)

        numButtons = len(btns)
        btnWidth = width/numButtons
        btnHeight = height/20

        for index, btn in enumerate(btns):
            btn.width = btnWidth
            btn.height = btnHeight
            btn.y = height - btnHeight
            btn.x = 0 + index*btnWidth

        bk.sizex = width
        bk.sizey = btnHeight
        bk.posy = height - btnHeight
        bk.posx = 0


    def org_btn_press(instance):
        print('Organisation')

    def import_btn_press(instance):
        print('import')

    def save_btn_press(instance):
        print('Save')

    def run_btn_press(instance):
        print('Run')


class TextEditor(Widget):
    org_btn = ObjectProperty(None)
    import_btn = ObjectProperty(None)
    save_btn = ObjectProperty(None)
    run_btn = ObjectProperty(None)
    nav_bar_bk = ObjectProperty(None)
    def setup(self):
        width = 500
        height = 500
        Window.size = (width, height)
        NavBtns = [self.org_btn, self.import_btn, self.save_btn, self.run_btn]
        NavBar = NavBarController()
        NavBar.setup(width, height, NavBtns, self.nav_bar_bk)






    #navBar = ObjectProperty(None)

class MainApp(App):
    def build(self):
        app = TextEditor()
        app.setup()
        return app

if __name__ == '__main__':
    MainApp().run()
