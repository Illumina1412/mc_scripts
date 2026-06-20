from java import JavaClass
import minescript as m
import time

Minecraft = JavaClass("net.minecraft.client.Minecraft")
_mc = Minecraft.getInstance()
_ClickType = JavaClass("net.minecraft.world.inventory.ClickType")

# ===================== HÀM TIỆN ÍCH =====================

def smooth_turn(target_yaw, target_pitch, steps=35, delay=0.012):
    current_yaw, current_pitch = m.player_orientation()
    yaw_diff = (target_yaw - current_yaw + 180) % 360 - 180
    pitch_diff = target_pitch - current_pitch
    yaw_step = yaw_diff / steps
    pitch_step = pitch_diff / steps
    for _ in range(steps):
        current_yaw = (current_yaw + yaw_step) % 360
        current_pitch += pitch_step
        m.player_set_orientation(current_yaw, current_pitch)
        time.sleep(delay)

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
    m.echo("§e[HUB] Phát hiện totem, đang reconnect...")
    m.player_press_use(True); time.sleep(0.1); m.player_press_use(False)
    slot_count = wait_for_gui()
    if slot_count is None:
        m.echo("§cKhông mở được GUI."); return
    if slot_count >= 90:
        click_slot(29); time.sleep(1.0)
    time.sleep(0.1)
    slot_count = wait_for_gui()
    if slot_count is None:
        m.echo("§cKhông mở được GUI."); return
    if slot_count >= 41:
        click_slot(4); time.sleep(5.0)

# ===================== MAIN =====================

m.echo("§aStart! §7(\\z dừng)")
time.sleep(3)
count=0
while True:
    if is_at_hub():
        reconnect()
        continue
    count += 1
    m.echo(f"§a[#{count}]")
    # if count % 2 ==0:
    #     m.player_press_use(True);   time.sleep(1.2); m.player_press_use(False)
    
    smooth_turn(90, 0 + 4)
    time.sleep(1)
    smooth_turn(90, 0 - 4)
    m.player_press_use(True);   time.sleep(0.9); m.player_press_use(False)
    