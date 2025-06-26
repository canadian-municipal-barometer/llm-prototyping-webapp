import os
from shiny import reactive
from shiny.express import input, render, ui
import model_test as mt

with open("base_prompt.txt", "r", encoding="utf-8") as file:
    base_prompt = file.read()

KEY = os.environ["API_KEY"]

with ui.div(class_="text-center mt-4"):
    ui.h1("LLM Prompt Prototyper")

with ui.div(class_="d-flex justify-content-center mt-4"):
    with ui.div(style="width: 50vw;"):  # Set width of the card here

        with ui.navset_card_tab(id="tab"):
            with ui.nav_panel("Input/Output"):
                ui.input_text_area("user_input", "User input:", width="100%")
                with ui.div(class_="d-flex justify-content-end mt-2"):
                    ui.input_action_button(
                        "submit",
                        "Submit",
                        style="width: 20%;",
                    )
                ui.br()
                ui.markdown("Model output:")

                @render.text
                @reactive.event(input.submit)
                def llm_output():
                    base_prompt = {"text": input.base_prompt(), "base_id": 0}
                    prompt = mt.create_full_prompt(
                        prompt=base_prompt, user_input=input.user_input()
                    )
                    response = mt.send_request(
                        prompt=prompt, model="mixtral-8x22b-instruct", api_key=KEY
                    )
                    return response["completion"]

            with ui.nav_panel("Full prompt"):
                ui.input_text_area(
                    "base_prompt",
                    "Modify instructions:",
                    value=base_prompt,
                    width="100%",
                    height="30em",
                )

            with ui.nav_panel("Instructions"):
                ui.markdown(
                    """
                    1. Provide your mock user input on the *Input/Output* page.
                    2. Adjust the prompt's instructions on the *Full prompt* page.
                    3. Use the *Submit* button to send the prompt to the model and diplay its response.
                    """
                )
