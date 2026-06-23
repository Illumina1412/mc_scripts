from java import JavaClass
import minescript as m
import time


Minecraft = JavaClass("net.minecraft.client.Minecraft")
_mc = Minecraft.getInstance()
_ClickType = JavaClass("net.minecraft.world.inventory.ClickType")


INVIS_WARN_SECONDS = 30  
INVIS_RTP_SECONDS = 10    


_invis_state = {
    "warned": False,         
    "rtp_done": False,       
    "last_remaining": None,  
}


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
    time.sleep(2)
    m.player_press_use(True); time.sleep(0.1); m.player_press_use(False)
    slot_count = wait_for_gui()
    if slot_count is None:
        m.echo("§cKhông mở được GUI."); return
    if slot_count >= 90:
        click_slot(22); time.sleep(1.0)
    time.sleep(1)
    slot_count = wait_for_gui()
    if slot_count is None:
        m.echo("§cKhông mở được GUI."); return
    if slot_count >= 41:
        click_slot(4); time.sleep(3.0)


def get_invisibility_seconds():
    try:
        effects = list(_mc.player.getActiveEffects().toArray())
        for e in effects:
            if "invisibility" in str(e).lower():
                return e.getDuration() / 20.0
        return None
    except:
        return None


def check_invisibility():
    remaining = get_invisibility_seconds()

    if remaining is None:
        _invis_state["warned"] = False
        _invis_state["rtp_done"] = False
        _invis_state["last_remaining"] = None
        return

    last = _invis_state["last_remaining"]
    if last is not None and remaining > last + 2:
        _invis_state["warned"] = False
        _invis_state["rtp_done"] = False

    _invis_state["last_remaining"] = remaining

    if remaining <= INVIS_RTP_SECONDS and not _invis_state["rtp_done"]:
        m.echo(f"§c[TÀN HÌNH] Hết hiệu lực ({int(remaining)}s)! Đang /rtp lánh đi...")
        _mc.setScreen(None)
        m.chat("/rtp")
        _invis_state["rtp_done"] = True
        _invis_state["warned"] = True
    elif remaining <= INVIS_WARN_SECONDS and not _invis_state["warned"]:
        for _ in range(10):
            m.echo(f"§e[TÀN HÌNH] Còn {int(remaining)}s! Ném thuốc tàn hình ngay!")
        _invis_state["warned"] = True


#  MAIN 

m.echo("§aStart! §7(\\z để dừng)")

while True:
    if is_at_hub():
        reconnect()
        continue

    check_invisibility()
    time.sleep(0.2)