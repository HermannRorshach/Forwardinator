from telethon import TelegramClient, events

from config import CHAT_A_ID, CHAT_B_ID, api_hash, api_id

client = TelegramClient(
    'phone', api_id, api_hash, system_version='4.16.30-vxCUSTOM')


forwarded_messages = {}


@client.on(events.NewMessage(chats=[CHAT_A_ID, CHAT_B_ID]))
async def chat_events(event: events.NewMessage) -> None:
    target_chat = {CHAT_A_ID: CHAT_B_ID, CHAT_B_ID: CHAT_A_ID}[event.chat_id]
    topic_id = getattr(event.message.reply_to, 'reply_to_msg_id', 1)
    print(topic_id, event.message.text)
    if topic_id == 1:
        sender = await event.message.get_sender()
        username = sender.username
        text = event.message.text + f"\n\nДоговориться о сампо: @{username}"
        sent_message = await client.send_message(target_chat, text)
        forwarded_messages[event.message.id] = sent_message.id


@client.on(events.MessageDeleted(chats=[CHAT_A_ID, CHAT_B_ID]))
async def delete_forwarded_message(event: events.MessageDeleted) -> None:
    target_chat = {CHAT_A_ID: CHAT_B_ID, CHAT_B_ID: CHAT_A_ID}[event.chat_id]
    for msg_id in event.deleted_ids:
        if msg_id in forwarded_messages:
            try:
                await client.delete_messages(
                    target_chat, forwarded_messages[msg_id])
                del forwarded_messages[msg_id]
            except Exception as e:
                print(f"Error deleting message: {e}")

client.start()
client.run_until_disconnected()
