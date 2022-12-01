from random import randint

from django.templatetags.static import static
from idom import component, hooks, html


@component
def backdrop():
    # TODO: Jump between two images tags for rotating images

    default_backdrop, set_default_backdrop = hooks.use_state(
        f"conreq/backdrop ({randint(1, 200)}).jpg"
    )
    backdrop_selector, set_backdrop_selector = hooks.use_state(1)
    prev_backdrop, set_prev_backdrop = hooks.use_state(None)

    # bg_num, set_bg_num = hooks.use_state(randint(1, 210))
    # async def on_click(_event):
    #     val = bg_num + 1
    #     if val > 210:
    #         val = 1
    #     set_bg_num(val)
    #     print(f"bg_num: {val}")

    return html.div(
        {
            "className": "backdrop-container",
            # "onClick": on_click,
        },
        html.div({"className": "backdrop-tint"}),
        html.img(
            {
                "className": f"backdrop {'opacity-0' if backdrop_selector != 1 else ''}",
                "src": static(default_backdrop),
                "loading": "lazy",
            }
        )
        # html.img(
        #     {
        #         "className": f"backdrop {'opacity-0' if backdrop_selector == 2 else ''}",
        #         "src": prev_backdrop,
        #         "loading": "lazy",
        #     }
        # ),
    )
