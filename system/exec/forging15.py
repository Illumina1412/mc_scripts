from java import JavaClass
import minescript as m
import time


Minecraft = JavaClass("net.minecraft.client.Minecraft")
_mc = Minecraft.getInstance()
_ClickType = JavaClass("net.minecraft.world.inventory.ClickType")

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
def get_level():
    return int(str(_mc.player.experienceLevel))

def get_anvil_cost():
    try:
        menu = _mc.screen.getMenu()
        cls = menu.getClass()
        while cls and "class_1703" not in cls.getName():
            cls = cls.getSuperclass()
        f = cls.getDeclaredField("field_29559")
        f.setAccessible(True)
        return int(str(f.get(menu).getInt(0)))
    except:
        return anvil_cost

def shift_click_slot(slot_index):
    if _mc.screen is None: return
    menu = _mc.screen.getMenu()
    _mc.gameMode.handleInventoryMouseClick(
        menu.containerId, slot_index, 0, _ClickType.QUICK_MOVE, _mc.player
    )

def click_slot(slot_index):
    if _mc.screen is None: return
    menu = _mc.screen.getMenu()
    _mc.gameMode.handleInventoryMouseClick(
        menu.containerId, slot_index, 0, _ClickType.PICKUP, _mc.player
    )

def wait_for_gui(timeout=4.0):
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
    time.sleep(2)
    m.player_press_use(True); time.sleep(0.1); m.player_press_use(False)
    slot_count = wait_for_gui()
    if slot_count is None:
        m.echo("§cKhông mở được GUI."); return
    if slot_count >= 90:
        click_slot(22); time.sleep(1.0)
    elif slot_count >= 41:
        click_slot(4); time.sleep(4.0)
    #_mc.setScreen(None)
    
def has_anvil():
    block = str(m.getblock(*ANVIL_POS)).lower()
    return "anvil" in block
 
def place_anvil():
    m.press_key_bind("key.hotbar.5", True); time.sleep(0.05)
    m.press_key_bind("key.hotbar.5", False)
    time.sleep(0.1)
    m.player_press_use(True); time.sleep(0.1); m.player_press_use(False)
    time.sleep(0.2)
    m.press_key_bind("key.hotbar.3", True); time.sleep(0.1)
    m.press_key_bind("key.hotbar.3", False)
    m.echo("§aĐã đặt đe!")

# ===================== MAIN =====================
ANVIL_POS = (50691, -47, 2424)
anvil_cost = 15
count = 0
last_count_time = time.time()
m.echo(f"§aReady! Cost={anvil_cost}")
base_yaw, base_pitch = -1,5

while True:
    if time.time() - last_count_time > 30:
        m.echo("§e[STUCK] Di chuyển phải...")
        m.player_press_right(True); time.sleep(2); m.player_press_right(False)
        last_count_time = time.time()
        continue

    if is_at_hub():
        reconnect(); continue

    if get_level() < anvil_cost:
        time.sleep(0.02)
        continue
    pos = m.player_position()
    if int(pos[1]) == -48:
        count += 1
        last_count_time = time.time()
        m.echo(f"§a[#{count}]")

        m.player_press_left(True);  time.sleep(0.6);  m.player_press_left(False)
        if not has_anvil():
            place_anvil()
            
        m.player_press_use(True);   time.sleep(0.05);  m.player_press_use(False)
        time.sleep(0.2)

        shift_click_slot(7); time.sleep(0.1)
        shift_click_slot(6); time.sleep(0.05)

        if _mc.screen is not None:
            _mc.screen.keyPressed(259, 0, 0)
        time.sleep(0.05)

        # if count % 10 == 0:
        #     new_cost = get_anvil_cost()
        #     if 0 < new_cost <= 33:
        #         anvil_cost = new_cost
        #         m.echo(f"§eCost cập nhật: {anvil_cost}")

        shift_click_slot(2); time.sleep(0.1)

        _mc.player.closeContainer()
        time.sleep(0.1)

        m.player_press_right(True); time.sleep(0.9);   m.player_press_right(False)
        time.sleep(0.1)
