import mesop as me

ROOT_BOX_STYLE = me.Style(
    background="#e7f2ff",
    height="100%",
    font_family="Inter",
    display="flex",
    flex_direction="column",
)

@me.page(
    path="/components/bottom-brackets",
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
    ],
)
def page():
    with me.box(style=ROOT_BOX_STYLE):
        header()
        with me.box(
            style=me.Style(
                width="min(680px, 100%)",
                margin=me.Margin.symmetric(
                    horizontal="auto",
                    vertical=36,
                ),
            )
        ):
            me.text(
                "Chat with multiple models at once",
                style=me.Style(
                    font_size=20,
                    margin=me.Margin(bottom=24),
                ),
            )
            chat_input()

def header():
    with me.box(
        style=me.Style(
            padding=me.Padding.all(16),
        ),
    ):
        me.text(
            "DuoChat",
            style=me.Style(
                font_weight=500,
                font_size=24,
                color="#3D3929",
                letter_spacing="0.3px",
            ),
        )

def chat_input():
    with me.box(
        style=me.Style(
            border_radius=16,
            padding=me.Padding.all(8),
            background="white",
            display="flex",
            width="100%",
        )
    ):
        with me.box(style=me.Style(flex_grow=1)):
            me.native_textarea(
                placeholder="Enter a prompt",
                style=me.Style(
                    padding=me.Padding(top=16, left=16),
                    outline="none",
                    width="100%",
                    border=me.Border.all(me.BorderSide(style="none")),
                ),
            )
        with me.content_button(type="icon"):
            me.icon("send")