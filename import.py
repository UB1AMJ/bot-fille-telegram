import asyncio
import os
from telethon import TelegramClient, events, sync


api_id = 1111
api_hash = ""
bot_token = ""
channel_username = "@xxxx" #телеграмм канал куда будут отправляться файлы 
folder_path = "/1/1/1/" #путь к папке которая будет мониториться кодом


# Нам нужно вручную вызвать «start», если нам нужен явный токен бота
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage())
async def my_event_handler(event):
    pass

async def send_file_to_channel(file_path):

    await client.send_file(channel_username, file_path)


    os.remove(file_path) #Убрать комментарий, чтобы файл удалялся после отправки.

async def monitor_folder():
    sent_files_path = os.path.join(folder_path, 'sented_files.txt') #Файл лога отправленных файлов
    sent_files = []

    if os.path.exists(sent_files_path):
        with open(sent_files_path, 'r') as file:
            sent_files = file.read().splitlines()

    while True:
        files = os.listdir(folder_path)
        xlsx_files = [f for f in files if f.endswith('.csv') and f not in sent_files]#Формат файла для отправки в телеграм

        for file in xlsx_files:
            try:
                await send_file_to_channel(os.path.join(folder_path, file))
                sent_files.append(file)
            except Exception as e:
                print(f"Error sending file {file}: {e}")

        with open(sent_files_path, 'w') as file:
            file.write('\n'.join(sent_files))

        await asyncio.sleep(5)
with client:
    client.loop.create_task(monitor_folder())
    client.run_until_disconnected()
