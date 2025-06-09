import logging
import json
from typing import Dict

from ontology_dc8f06af066e4a7880a5938933236037.config import ConfigClass
from ontology_dc8f06af066e4a7880a5938933236037.input import InputClass
from ontology_dc8f06af066e4a7880a5938933236037.output import OutputClass
from openfabric_pysdk.context import AppModel, State
from openfabric_pysdk.resource import Resource
from core.stub import Stub

# Configurations for the app
configurations: Dict[str, ConfigClass] = dict()

def config(configuration: Dict[str, ConfigClass], state: State) -> None:
    """
    Stores user-specific configuration data.
    """
    for uid, conf in configuration.items():
        logging.info(f"Saving new config for user with id:'{uid}'")
        configurations[uid] = conf


# ----------- Prompt Enhancer -----------
def expand_prompt(prompt: str) -> str:
    return f"A highly detailed and artistic image of {prompt}, with dramatic lighting and cinematic colors."


# ----------- Save to Memory -----------
def save_to_memory(prompt, enhanced, image_path, model_path):
    record = {
        "original_prompt": prompt,
        "enhanced_prompt": enhanced,
        "image_path": image_path,
        "model_path": model_path
    }
    with open("memory.json", "a") as f:
        f.write(json.dumps(record) + "\n")


# ----------- Main Execution Logic -----------
def execute(model: AppModel) -> None:
    request: InputClass = model.request
    prompt = request.prompt.lower().strip()

    user_config: ConfigClass = configurations.get('super-user', None)
    logging.info(f"User Configurations: {configurations}")

    app_ids = user_config.app_ids if user_config else []
    stub = Stub(app_ids)

    # Default message
    message = ""

    # Predefined conversational responses
    if "hello" in prompt or "hi" in prompt:
        message = "Hello! How can I assist you today?"
    elif "your name" in prompt:
        message = "I'm your friendly AI assistant 🤖!"
    elif "joke" in prompt:
        message = "Why did the developer go broke? Because they used up all their cache! 😂"
    elif "add" in prompt and "and" in prompt:
        try:
            parts = prompt.split("add")[1].split("and")
            num1 = float(parts[0])
            num2 = float(parts[1])
            message = f"The sum is {num1 + num2}"
        except:
            message = "Oops! I couldn't calculate that. Try saying: add 5 and 3"
    else:
        # ------- AI Generation Flow -------
        enhanced_prompt = expand_prompt(prompt)

        # Step 1: Text to Image
        text_to_image_app_id = "f0997a01-d6d3-a5fe-53d8-561300318557"
        image_response = stub.call(
            text_to_image_app_id,
            {'prompt': enhanced_prompt},
            'super-user'
        )
        image_data = image_response.get('result')
        image_path = "generated_image.png"
        with open(image_path, "wb") as f:
            f.write(image_data)

        # Step 2: Image to 3D Model
        image_to_3d_app_id = "69543f29-4d41-4afc-7f29-3d51591f11eb"
        model_response = stub.call(
            image_to_3d_app_id,
            {'image': image_data},
            'super-user'
        )
        model_data = model_response.get('result')
        model_path = "generated_model.glb"
        with open(model_path, "wb") as f:
            f.write(model_data)

        # Save memory
        save_to_memory(prompt, enhanced_prompt, image_path, model_path)

        message = f"✅ 3D model generated for: '{enhanced_prompt}'"

        # Attach 3D model as downloadable file
        model.response.content_reference = Resource(path=model_path)

    # Final response
    response: OutputClass = model.response
    response.message = message
