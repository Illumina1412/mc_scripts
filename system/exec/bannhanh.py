from java import JavaClass
import minescript as m
import time



Minecraft = JavaClass("net.minecraft.client.Minecraft")
_mc = Minecraft.getInstance()
_ClickType = JavaClass("net.minecraft.world.inventory.ClickType")


def click_slot(slot_index):
    if _mc.screen is None: return
    menu = _mc.screen.getMenu()
    if menu is None: return
    _mc.gameMode.handleInventoryMouseClick(
        menu.containerId, slot_index, 0, _ClickType.PICKUP, _mc.player
    )

def wait_for_gui(timeout=2.0):
    start = time.time()
    while time.time() - start < timeout:
        if _mc.screen is not None:
            try:
                return _mc.screen.getMenu().slots.size()
            except:
                pass
        time.sleep(0.1)
    return None

def is_at_hub():
    item = _mc.player.getInventory().getItem(4)
    return not item.isEmpty() and str(item.getItem()) == "minecraft:totem_of_undying"

def reconnect():
    m.echo("§e[HUB] Đang ở hub, kết nối lại")
    m.player_press_use(True); time.sleep(0.1); m.player_press_use(False)
    slot_count = wait_for_gui()
    if slot_count is None:
        m.echo("§cKhông mở được GUI."); return
    if slot_count >= 90:
        click_slot(29); time.sleep(1.0)
    time.sleep(1)
    slot_count = wait_for_gui()
    if slot_count is None:
        m.echo("§cKhông mở được GUI."); return
    if slot_count >= 41:
        click_slot(4); time.sleep(3.0)

#  MAIN 

m.echo("§aStart! §7(\\z để dừng)")
time.sleep(2)

count = 0
cycle = 0  

while True:
    if is_at_hub():
        reconnect()
        continue

    count += 1
    cycle += 1
    m.echo(f"§a[#{count}] (cycle {cycle}/5)")

    m.player_press_use(True)
    time.sleep(0.1)
    m.player_press_use(False)

    time.sleep(1.2)
    _mc.player.closeContainer()

    if cycle >= 5:
        cycle = 0
        time.sleep(1)
        m.chat("/bannhanh")
        time.sleep(1)
        _mc.player.closeContainer()
        time.sleep(1)
    else:
        time.sleep(4)