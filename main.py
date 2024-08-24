import flet as ft
import google.generativeai as genai
import os


apiKey = os.getenv("GEMINI_API")



class Application:
    def __init__(self):
        # Basics . . .
        self.page = None
        self.allResponse = ""
        self.codeTheme = "atom-one-dark"
        self.prompts = []
        self.themeMode = ft.IconButton(icon=ft.icons.SUNNY, on_click=self.themeModeChanger)
        # Main Appbar
        self.AppBar = ft.AppBar(
            leading_width=50,
            center_title=False,
            actions=[
                self.themeMode
            ],
            title=ft.Text(
                        "GenV",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        italic=True,
            ),
            bgcolor=ft.colors.SURFACE_VARIANT,
            adaptive=True,
        )
        # prompt input feild
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
            adaptive=True
        )
        # buttons
        self.sendPrompt = ft.IconButton(icon=ft.icons.SEND,on_click=self.geminiOutput)
        self.clearAll = ft.IconButton(icon=ft.icons.DELETE,on_click=self.clearGemini)
        # inside main Pannel view
        self.outputs = ft.ListView(
            expand=True,
            auto_scroll=True,
            spacing=1,
            adaptive=True
        )
        # main output pannel
        self.outputPannel = ft.Container(
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            padding=5,
            expand=True,
            content=self.outputs,
            margin=0,
            adaptive=True
        )
        # Output Elements inner widgets . . .
        self.responseLabel = ft.Markdown(value="", selectable=True, expand=True,extension_set="gitHubWeb",code_theme="atom-one-dark")



    def themeModeChanger(self,e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.themeMode.icon = (
            ft.icons.NIGHTS_STAY if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.SUNNY
        )
        self.codeTheme = (
                    "atom-one-light" if self.page.theme_mode == ft.ThemeMode.LIGHT else "atom-one-dark"
                )
        for c in self.outputs.controls:
            try:
                c.code_theme = (
                    "atom-one-light" if self.page.theme_mode == ft.ThemeMode.LIGHT else "atom-one-dark"
                )
            except:
                pass
        
        self.page.update()


    def geminiOutput(self,e):
        prompt = self.prompt.value
        self.allResponse = self.gemini(prompt)

        responseLabel = ft.Markdown(value="", selectable=True, expand=True,extension_set="gitHubWeb",code_theme=self.codeTheme)
        queryDisplay = ft.Row(
            expand=True,
            spacing=5,
            controls=[
                ft.CircleAvatar(
                    content=ft.Icon(ft.icons.MAN)
                ),
                ft.Text(value=prompt,text_align=ft.TextAlign.RIGHT,size=24,expand=True)
            ],
        )
        self.outputs.controls.append(queryDisplay)
        self.outputs.controls.append(ft.Divider(thickness=1))
        self.outputs.controls.append(responseLabel)
        self.outputs.controls.append(ft.Divider(thickness=5))
        for c in self.allResponse:
            responseLabel.value += c
            self.page.update()
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
            genai.configure(api_key=apiKey)
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
        self.page.title = "GenV"
        self.page.adaptive = True
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(color_scheme_seed="#7F00FF",)
        self.page.theme.page_transitions.android = ft.PageTransitionTheme.OPEN_UPWARDS
        self.page.padding = 10

        # App Bar
        self.page.appbar = self.AppBar

        self.page.add(
            # ft.SafeArea(
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
            # )
        )
        self.page.update()


if __name__ == "__main__":
    app = Application()
    ft.app(target=app.main,assets_dir="./assets",view=ft.WEB_BROWSER)
