import asyncio
import genshin
from telegram import ForceReply
from teyvat_guide.client import client

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Definição das coisa
def get_weapons():
    weapons = loop.run_until_complete(client.get_calculator_weapons())
    weapon_names = []
    for weapon in weapons:
        weapon_names.append(weapon.name)

    return weapon_names


def get_chars():
    characters = loop.run_until_complete(client.get_calculator_characters())
    char_names = []
    for char in characters:
        char_names.append(char.name)

    return char_names


def get_artifacts():
    artifacts = loop.run_until_complete(client.get_calculator_artifacts())
    artifact_names = []
    for artifact in artifacts:
        artifact_names.append(artifact.name)

    return artifact_names


# cada uma recebe uma lista de nomes dos respectivos weapons, chars e artifacts.
WEAPONS = get_weapons()
ARTIFACTS = get_artifacts()
CHARS = get_chars()


# Execução da coisa
def character_calculator(update, context):
    # Representando um input
    # Chiquinha 0 90 <- personagem 
    # Zé-do-caxão 89 90 <- personagem 
    # Manamune 0 30 <- weapon
    # maldição-de-inaros 0 30 <- artifact
    user_input = update.message.text.split(" ")
    given_name = user_input[0].replace("|", " ")
    min_level = user_input[1]
    max_level = user_input[2]
    
    if given_name in CHARS:
        characters = loop.run_until_complete(
            client.get_calculator_characters(query=given_name)
        )  # nome do personagem vem do usuário
        message = ""
        cost = loop.run_until_complete(
            client.calculator().set_character(
                characters[0].id, current=min_level, target=max_level
            )
        )
        for consumable in cost.character:
            message += f"{consumable.name}:  {consumable.amount}x \n\n"

        # enviar mensagem
        update.message.reply_markdown_v2(
            message,
            reply_markup=ForceReply(selective=True),
        )
        
    elif given_name in WEAPONS:
        weapons = loop.run_until_complete(
            client.get_calculator_weapons(query=given_name)
        )  # nome do personagem vem do usuário
        message = ""
        cost = loop.run_until_complete(
            client.calculator().set_weapon(
                weapons[0].id, current=min_level, target=max_level
            )
        )
        for consumable in cost.weapon:
            message += f"{consumable.name}:  {consumable.amount}x \n\n"

        # enviar mensagem
        update.message.reply_markdown_v2(
            message,
            reply_markup=ForceReply(selective=True),
        )

    elif given_name in ARTIFACTS:
        artifacts = loop.run_until_complete(client.get_calculator_artifacts())  # nome do personagem vem do usuário
        current_artifact = None
        for artifact in artifacts:
            if given_name == artifact.name:
                current_artifact = artifact
        
        message = ""

        # Temos um artefato
        if current_artifact:
            cost = loop.run_until_complete(
                client.calculator().add_artifact(
                    current_artifact.id, current=min_level, target=max_level
                )
            )
            
            for artifact in cost.artifacts:
                for consumable in artifact.list:
                    message += f"{consumable.name}:  {consumable.amount}x \n\n"

        else:
            message = "Not found"

        # enviar mensagem
        update.message.reply_markdown_v2(
            message,
            reply_markup=ForceReply(selective=True),
        )

    else:
        update.message.reply_markdown_v2(
            "Not a character, not a weapon and not an artifact",
            reply_markup=ForceReply(selective=True)
        )