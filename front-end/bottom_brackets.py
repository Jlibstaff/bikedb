import mesop as me

from dataclasses import dataclass

import bottom_brackets

CARD_WIDTH = "95%"
HOME_URL = "/"


@dataclass
class Resource:
  title: str
  description: str
  links: tuple[str]
  img_url: str
  


@dataclass
class Section:
  name: str
  resources: list[Resource]
  icon: str


SECTIONS = [
  Section(
    name="Bottom Brackets",
    icon="star",
    resources=[
      Resource(
        title="Full List",
        description="here's a full list of bottom brackets. Let's add some filters and things here.",
        links=('/components/bottom-brackets'),
        img_url="",
      )
    ],
  ),
]

def scroll_to_section(e: me.ClickEvent):
  me.scroll_into_view(key="section-" + e.key)
  me.state(State).sidenav_menu_open = False


def toggle_theme(e: me.ClickEvent):
  if me.theme_brightness() == "light":
    me.set_theme_mode("dark")
  else:
    me.set_theme_mode("light")


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.stateclass
class State:
  sidenav_menu_open: bool


def toggle_menu_button(e: me.ClickEvent):
  s = me.state(State)
  s.sidenav_menu_open = not s.sidenav_menu_open


def is_mobile():
  return me.viewport_size().width < 640


@me.page(
  title="bikeDB",
  on_load=on_load,
  path="/components/bottom-brackets",
)
def page():
  # Menu bar
  with me.box(style=me.Style(display="flex", height="100%")):
    if is_mobile():
      with me.content_button(
        type="icon",
        style=me.Style(top=6, left=8, position="absolute", z_index=9),
        on_click=toggle_menu_button,
      ):
        me.icon("menu")
      with me.sidenav(
        opened=me.state(State).sidenav_menu_open,
        style=me.Style(
          background=me.theme_var("surface-container-low"),
        ),
      ):
        sidenav()
    else:
      sidenav()
    with me.box(
      style=me.Style(
        background=me.theme_var("surface-container-low"),
        display="flex",
        flex_direction="column",
        flex_grow=1,
      )
    ):
      # Title Bar
      with me.box(
        style=me.Style(
          height=240,
          width="100%",
          padding=me.Padding.all(16),
          display="flex",
          align_items="center",
        ),
      ):
        me.text(
          "bikeDB",
          style=me.Style(
            color=me.theme_var("on-background"),
            font_size=44,
            font_weight=500,
            letter_spacing="0.8px",
            padding=me.Padding(left=36) if is_mobile() else None,
          ),
        )

        # dark mode button
        with me.content_button(
          type="icon",
          style=me.Style(position="absolute", right=4, top=8),
          on_click=toggle_theme,
        ):
          me.icon(
            "light_mode" if me.theme_brightness() == "dark" else "dark_mode"
          )
      
      # Body
      with me.box(
        style=me.Style(
          background=me.theme_var("background"),
          flex_grow=1,
          padding=me.Padding(
            left=32,
            right=32,
            bottom=64,
          ),
          border_radius=16,
          overflow_y="auto",
        )
      ):
        # Sections
        for section in SECTIONS:
          me.text(
            section.name,
            style=me.Style(
              font_size=18,
              font_weight=500,
              padding=me.Padding(top=32, bottom=16),
            ),
            key="section-" + section.name,
          )
          # Tiles
          with me.box(
            style=me.Style(
              display="grid",
              #justify_content="space-around",
              grid_template_columns=f"repeat(auto-fit, minmax({CARD_WIDTH}, 1fr))",
              gap=24,
              margin=me.Margin(
                bottom=24,
              ),
            )
          ):
            for resource in section.resources:
              card(resource)
        
def sidenav():
  with me.box(
    style=me.Style(
      width=216,
      height="100%",
      background=me.theme_var("surface-container-low"),
      padding=me.Padding.all(16),
    )
  ):
    with me.box(
      style=me.Style(
        display="flex", flex_direction="column", margin=me.Margin(top=48)
      )
    ):
      with me.content_button(
        type="icon",
        on_click=lambda e: me.navigate(HOME_URL),
      ):
        with me.box(
          style=me.Style(display="flex", align_items="center", gap=12)
        ):
          me.icon("home")
          me.text(
            "Home",
            style=me.Style(
              font_size=16,
              margin=me.Margin(bottom=4),
            ),
          )
    with me.box(
      style=me.Style(
        padding=me.Padding(top=24),
        display="flex",
        flex_direction="column",
        gap=8,
      ),
    ):
      me.text(
        "Categories",
        style=me.Style(
          font_weight=500,
          letter_spacing="0.4px",
          padding=me.Padding(left=12),
        ),
      )
      for section in SECTIONS:
        with me.box(
          style=me.Style(
            display="flex",
            align_items="center",
            cursor="pointer",
          ),
          on_click=scroll_to_section,
          key=section.name,
        ):
          with me.content_button(type="icon"):
            me.icon(section.icon)
          me.text(section.name)

def card(resource: Resource):
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=12,
      box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
      border_radius=16,
      min_width=CARD_WIDTH,
      max_width=480,
      background=me.theme_var("surface-container-lowest"),
    )
  ):
    me.box(
      style=me.Style(
        background=f"url('{resource.img_url}') center/cover no-repeat",
        cursor="pointer",
        height=200,
        width="100%",
        border_radius=16,
        margin=me.Margin(bottom=8),
      ),
    )
    with me.box(
      style=me.Style(
        padding=me.Padding(left=16),
        display="flex",
        flex_direction="column",
        gap=8,
      ),
      key=resource.links,
      on_click=lambda e: me.navigate(e.key),
    ):
      me.button(
        resource.title, 
        style=me.Style(font_weight="bold"), 
        key=resource.links,
        on_click=lambda e: me.navigate(e.key))
      me.text(resource.description, style=me.Style(height=40))
