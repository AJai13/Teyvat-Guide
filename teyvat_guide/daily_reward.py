import asyncio
import genshin
from telegram import ForceReply
from teyvat_guide.client import client

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# get info about the current daily reward status
def reward_info(update, context):
    signed_in, claimed_rewards = loop.run_until_complete(client.get_reward_info())
    update.message.reply_markdown_v2(
        fr'Signed in: {signed_in} \| Total claimed rewards: {claimed_rewards}',
        reply_markup=ForceReply(selective=True),
    )

    
def claimed_rewards(update, context):
    rewards_list = loop.run_until_complete(client.claimed_rewards())
    message = ''
    for claimed_reward in rewards_list:
        formated_date = claimed_reward.time.__str__().replace('-', '\-').replace('+', '\+')
        message += f"{formated_date}:  {claimed_reward.amount}x {claimed_reward.name}\n\n"

    # enviar mensagem
    update.message.reply_markdown_v2(
        message,
        reply_markup=ForceReply(selective=True),
    )


def claim_daily_reward(update, context):
    try:
        reward = loop.run_until_complete(client.claim_daily_reward())
    except genshin.AlreadyClaimed:
        message = "Daily reward already claimed"
    else:
        message = f"Claimed {reward.amount}x {reward.name}"

    update.message.reply_markdown_v2(
        message,
        reply_markup=ForceReply(selective=True),
    )