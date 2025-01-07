from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import math


class AdvancedScientificCalculatorApp(App):
    def build(self):
        root_widget = BoxLayout(orientation="vertical")
        output_label = Label(size_hint_y=0.75, font_size=50, text="")

        # Advanced button symbols including constants and functions
        button_symbols = (
            "sin", "cos", "tan", "log",
            "π", "e", "sqrt", "exp",
            "7", "8", "9", "+",
            "4", "5", "6", "-",
            "1", "2", "3", "*",
            "0", ".", "(", ")",
            "factorial", "/", "^", "=",
            "Clear"
        )

        button_grid = GridLayout(cols=4, size_hint_y=2)

        for symbol in button_symbols:
            button_grid.add_widget(Button(text=symbol))

        # Function to update label text with button press
        def print_button_text(instance):
            if instance.text == "π":
                output_label.text += str(math.pi)
            elif instance.text == "e":
                output_label.text += str(math.e)
            elif instance.text in ("sin", "cos", "tan", "log", "sqrt", "factorial", "exp", "^"):
                output_label.text += instance.text + "("
            else:
                output_label.text += instance.text

        for button in button_grid.children[::-1]:
            if button.text not in ("Clear", "="):
                button.bind(on_press=print_button_text)

        # Evaluate the result
        def evaluate_result(instance):
            try:
                # Replace symbols with corresponding Python math functions
                expression = output_label.text
                expression = expression.replace("^", "**")
                expression = expression.replace("sqrt", "math.sqrt")
                expression = expression.replace("log", "math.log")
                expression = expression.replace("sin", "math.sin")
                expression = expression.replace("cos", "math.cos")
                expression = expression.replace("tan", "math.tan")
                expression = expression.replace("factorial", "math.factorial")
                expression = expression.replace("exp", "math.exp")
                output_label.text = str(eval(expression))
            except Exception as e:
                output_label.text = "Error!"

        # Clear the label
        def clear_label(instance):
            output_label.text = ""

        # Bind specific buttons
        button_grid.children[1].bind(on_press=evaluate_result)  # "=" button
        button_grid.children[0].bind(on_press=clear_label)      # "Clear" button

        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)
        return root_widget


if __name__ == "__main__":
    AdvancedScientificCalculatorApp().run()
