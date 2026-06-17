from java import JavaClass
import minescript as m
import time


Minecraft = JavaClass("net.minecraft.client.Minecraft")
_mc = Minecraft.getInstance()
_ClickType = JavaClass("net.minecraft.world.inventory.ClickType")

MAINTENANCE_INTERVAL = 5

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
        
def has_dolphin_grace():
    try:
        effects = list(_mc.player.getActiveEffects().toArray())
        return any("dolphins_grace" in str(e).lower() for e in effects)
    except:
        return False
    
    
#  MAIN 

m.echo("§aStart! §7(\\z để dừng)")

count=0
while True:
    if is_at_hub():
        reconnect()
        continue
    count += 1 
    m.echo(f"§a[#{count}]")
    
    # m.player_press_forward(True); time.sleep(0.2); m.player_press_forward(False)
    # time.sleep(0.05)
    # m.player_press_forward(True); time.sleep(0.03); m.player_press_forward(False)
    # time.sleep(0.03)
    #.player_press_sprint(True)
    m.player_press_forward(True)  
    time.sleep(6)
    m.player_press_use(True);   time.sleep(1.2); m.player_press_use(False)
    
    while has_dolphin_grace():
        time.sleep(0.2)
    
    m.player_press_forward(False)
    #.player_press_sprint(False)
    time.sleep(0.4)
    m.chat("/home thana")
    maintain=time.time()
    time.sleep(0.04)
    m.player_press_use(True);   time.sleep(1.2); m.player_press_use(False)
    time.sleep(0.05)
    m.player_press_use(True);   time.sleep(1.2); m.player_press_use(False)
    time.sleep(1)
  

    x, y, z = m.player_position()
    while z > 5787:
        #print(f"Vi tri hien tai: Y = {y:.1f}")
        time.sleep(0.2)
        x, y, z = m.player_position()
        if time.time() - maintain >= MAINTENANCE_INTERVAL:
            m.echo("Qua thoi gian dich chuyen")
            time.sleep(0.01)
            m.chat("/home thana")
            maintain=time.time()        
            
    m.player_press_use(True);   time.sleep(0.1); m.player_press_use(False)
 