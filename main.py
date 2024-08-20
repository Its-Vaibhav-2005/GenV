import flet as ft
import google.generativeai as genai
import os,dotenv

dotenv.load_dotenv()
apiKey = dotenv.dotenv_values(".env","GEMINI_API")

class Application:
    def __init__(self):
        self.page = None
        self.allResponse = ""
        self.prompts = []
        self.themeMode = ft.IconButton(icon=ft.icons.NIGHTS_STAY, on_click=self.themeModeChanger)
        self.AppBar = ft.AppBar(
            leading_width=50,
            center_title=False,
            actions=[
                self.themeMode
            ],
            title=ft.Text(
                        "Mr.Chat",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        italic=True,
            ),
            bgcolor=ft.colors.SURFACE_VARIANT,


        )
        self.prompt = ft.TextField(
            expand=True,
            autofocus=True,
            shift_enter=True,
            filled=True,
            max_lines=8,
            hint_text="Waiting for your Queries 👀 . . .",
            border_radius=20,
            on_submit=self.geminiOutput,
            min_lines=3,
        )
        self.sendPrompt = ft.IconButton(icon=ft.icons.SEND,on_click=self.geminiOutput)
        # self.microphoneButton = ft.IconButton(icon=ft.icons.MIC)
        self.clearAll = ft.IconButton(icon=ft.icons.DELETE,on_click=self.clearGemini)
        self.outputs = ft.ListView(
            expand=True,
            auto_scroll=True,
            spacing=15,
        )
        self.outputPannel = ft.Container(
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            padding=5,
            expand=True,
            content=self.outputs,
            margin=0
        )

    def themeModeChanger(self,e):
        self.page.theme_mode = (ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT)
        self.themeMode.icon = (ft.icons.NIGHTS_STAY if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.SUNNY)
        
        self.page.update()

    def geminiOutput(self,e):
        prompt = self.prompt.value
        self.allResponse = self.gemini(prompt)
        responseLabel = ft.Markdown(value="", selectable=True, expand=True,)
        
        self.outputs.controls.append(responseLabel)
        self.outputs.controls.append(ft.Divider(thickness=5))
        self.page.update()
        for c in self.allResponse:
            responseLabel.value += c
            self.page.update()
        self.prompt.value = ""
        self.page.update()
    def disableEle(self):
        self.sendPrompt.disabled=True
        self.clearAll.disabled=True
        self.prompt.disabled=True

        self.page.update()
    def enableEle(self):
        self.sendPrompt.disabled = False
        self.clearAll.disabled = False
        self.prompt.disabled = False

        self.page.update()
    def gemini(self,prompt):
        self.disableEle()
        try:
            genai.configure(api_key=apiKey["GEMINI_API"])
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            prompt = f"{self.allResponse} \n {prompt}"
            response = model.generate_content([prompt])
            self.enableEle()
            return response.text
        except:
            self.enableEle()
            return "Try Again !"

    def clearGemini(self,e):
        self.allResponse = ""
        self.outputs.controls.clear()
        self.page.update()

    def main(self, page: ft.Page):
        self.page = page
        self.page.title = "Mr. Chat"
        self.page.theme_mode = "light"
        self.page.theme = ft.Theme(color_scheme_seed="#7F00FF")
        self.page.padding = 10

        # Fonts . . .
        dancingFont = """<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400..700&display=swap">"""


        # App Bar
        self.page.appbar = self.AppBar

        self.page.add(
            self.outputPannel,
            ft.Row(  # Row layout in this prompt is taken and send button is present
                controls=[

                    self.prompt,
                    ft.Column(
                        controls=[
                            self.sendPrompt,
                            self.clearAll
                        ],
                        spacing=2,
                    )
                ],
                spacing=2,
            )
        )
        self.page.update()


if __name__ == "__main__":
    app = Application()
    ft.app(target=app.main,assets_dir="./assets",view=ft.WEB_BROWSER)
