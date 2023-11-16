from mcdreforged.plugin.server_interface import PluginServerInterface
from mcdreforged.command.builder.tools import SimpleCommandBuilder
from mcdreforged.command.builder.nodes.arguments import Integer, GreedyText
from mcdreforged.command.command_source import CommandSource

# To-Do List 字典
todo_list = {}

def on_load(server: PluginServerInterface, old) -> None:
    global todo_list
    if old is not None:
        todo_list = old.todo_list
        
    builder = SimpleCommandBuilder()
    builder.command("$ todo", show_help)
    builder.command("$ todo list", show_list)
    builder.command("$ todo add <text>", add)
    builder.command("$ todo done <id>", done)
    builder.command("$ todo remove <id>", remove)
    builder.command("$ todo remove_done", remove_done)
    builder.arg("text", GreedyText)
    builder.arg("id", Integer)
    builder.register(server)
    
def show_help(source: CommandSource) -> None:
    source.reply("§aTo-Do List 用法§f")
    source.reply("$ todo                显示 To-Do List 用法")
    source.reply("$ todo list           显示 To-Do List 项")
    source.reply("$ todo add <text>     添加 To-Do 项")
    source.reply("$ todo done <id>      标记 To-Do 项已完成")
    source.reply("$ todo remove <id>    移除 To-Do 项")
    source.reply("$ todo remove_done    移除已完成的 To-Do 项")
    
def show_list(source: CommandSource) -> None:
    if not operation_precheck(source):
        return

    player = source.player
    source.reply("§aTo-Do List 内容§f")
    undone_length = len(todo_list[player][0])
    done_length = len(todo_list[player][1])
    for i in range(undone_length):
        source.reply(f"§a[{i + 1}]§f {todo_list[player][0][i]}")
    for i in range(done_length):
        source.reply(f"§a[{i + undone_length + 1}] §7§m{todo_list[player][1][i]}§f")
    
def add(source: CommandSource, context: dict) -> None:
    if not check_is_player(source):
        return
    
    player = source.player
    text = context["text"]
    if not player in todo_list:
        todo_list[player] = ([], []) # 第一项为未完成列表，第二项为已完成列表
    todo_list[player][0].append(text)
    source.reply("§a已将该项添加到 To-Do List§f")
    
def done(source: CommandSource, context: dict) -> None:
    if not operation_precheck(source):
        return
    
    player = source.player
    id = context["id"]
    undone_length = len(todo_list[player][0])
    if id <= undone_length: # 要标记已完成的项属于未完成项
        text = todo_list[player][0][id - 1]
        del todo_list[player][0][id - 1]
        todo_list[player][1].append(text)
    
    show_list(source)
    
    
def remove(source: CommandSource, context: dict) -> None:
    if not operation_precheck(source):
        return
    
    player = source.player
    id = context["id"]
    undone_length = len(todo_list[player][0])
    if id <= undone_length: # 要删除的项属于未完成项
        del todo_list[player][0][id - 1]
    else: # 要删除的项属于以完成项
        del todo_list[player][1][id - undone_length - 1]
        
    show_list(source)

def remove_done(source: CommandSource) -> None:
    if not operation_precheck(source):
        return
    
    player = source.player
    todo_list[player][1].clear()
    show_list(source)
    
# 检查指令源是否是玩家，并作出相应响应
def check_is_player(source: CommandSource) -> bool:
    if not source.is_player:
        source.reply("§aTo-Do List 仅限玩家使用§f")
        return False
    return True

# 操作前检查
# 检查指令源是否是玩家、To-Do List 是否为空，并作出相应响应
def operation_precheck(source: CommandSource) -> bool:
    if not check_is_player(source):
        return False
    player = source.player
    if not player in todo_list or len(todo_list[player][0]) + len(todo_list[player][1]) == 0:
        source.reply("§aTo-Do List 无内容§f")
        return False
    return True
    