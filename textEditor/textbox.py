from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.codeinput import CodeInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from pygments.lexers import CythonLexer

'''class TextEditor(Widget):
    codeinput = CodeInput(lexer=CythonLexer())

    def on_enter(instance, value):
        print(value)'''

class TextEditorApp(App):

    def build(self):
        codeinput = CodeInput(lexer=CythonLexer())
        boxwhole = BoxLayout()
        label = Label()
        codeinput.bind(text=label.setter("text"))
        boxwhole.add_widget(label)
        boxwhole.add_widget(codeinput)

        return boxwhole


if __name__ == '__main__':
    TextEditorApp().run()
