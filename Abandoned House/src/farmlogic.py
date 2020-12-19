import os
import sys
import traceback
import atexit

import asyncio
import wizsdk
from wizsdk import Client, register_clients, XYZYaw, unregister_all

__DIR__ = os.path.dirname(os.path.abspath(__file__))

"""
Handler controlling login/client

"""
FIGHT_1 = XYZYaw(x=-11.02, y=-4497.934, z=539.501, yaw=3.137)
INTERMEDIATE_DIALOGUE = XYZYaw(x=57.738, y=-1501.743, z=539.501, yaw=3.216)
FIGHT_2 = XYZYaw(x=-1244.077, y=295.295, z=0.4, yaw=5.085)
FIGHT_2_BATTLE = XYZYaw(x=-134.993, y=-811.772, z=0.4, yaw=3.456)
BELGRIM = XYZYaw(x=-952.787, y=810.977, z=0.4, yaw=2.594)
DOOR = XYZYaw(x=18.129, y=1018.717, z=0.4, yaw=3.108)
KING = XYZYaw(x=-227.956, y=2161.093, z=1.8, yaw=6.083)
KING_BATTLE = XYZYaw(x=-6.862, y=2000.583, z=1.8, yaw=0.0)
  

# HELPER FUNCTIONS
async def teleport_party(players):
  for p in players:
    await p.teleport_to_friend(__DIR__ + "/green_gem.png")

  await players[-1].finish_loading()


async def join_fight(player, delay, run_duration=2):
  await asyncio.sleep(delay)
  await player.send_key("W", run_duration)


async def join_fight_in_order(players, delay_between=0.5, run_duration=1.5):
  await asyncio.gather(*[
    join_fight(player, i * delay_between, run_duration) 
    for i, player in enumerate(players)
  ])


async def go_through_dialogs(players):
  await asyncio.gather(*[
    player.go_through_dialog() 
    for player in players
  ])

async def mass_logout_login(players):
  await asyncio.gather(*[
    player.logout_and_in() 
    for player in players
  ])


async def mass_teleport_to(location, players):
  await asyncio.gather(*[
    player.teleport_to(location)
    for player in players
  ])
    
async def check_all_potions(players):
  for p in players:
    await p.use_potion_if_needed()


async def farm(fight):
  try:
    clients = register_clients(-1,["P1", "P2", "P3", "P4"])
    teammates = clients[1:]
    notHitters = clients[:3]

    p1, p2, p3, p4 = [*clients, None][:4] #""", p3, p4"""
    await asyncio.gather(*[p.activate_hooks() for p in clients])


    while True:
      #sigil
      for p in clients:
        await p.press_x()
      # load?
      await p4.wait(5)
      await p4.finish_loading()

      await mass_teleport_to(FIGHT_1, clients)

      await p1.wait(3)
      await go_through_dialogs(clients)
      await p1.wait(3)

      for p in clients:
        await p.send_key("W", 1)

      await fight("mobs",*clients)
      await go_through_dialogs(clients)

      for p in clients:
        await p.send_key("W", 0.2)

      await p1.teleport_to(INTERMEDIATE_DIALOGUE)
      await go_through_dialogs(clients)
      await mass_teleport_to(FIGHT_2, clients)
      #invincibility
      await p1.wait(5)

      await p1.send_key("W", 1)
      await p1.wait(0.5)
      await p2.teleport_to(FIGHT_2_BATTLE)
      await p2.wait(0.5)
      await p3.teleport_to(FIGHT_2_BATTLE)
      await p3.wait(0.5)
      await p4.teleport_to(FIGHT_2_BATTLE)
      await p4.wait(0.5)

      await fight("mobs",*clients)
      await go_through_dialogs(clients)

      await p1.teleport_to(BELGRIM)
      await p1.press_x()
      await p1.go_through_dialog()

      await mass_teleport_to(DOOR, clients)
      for p in clients:
        await p.send_key("W", 0.2)

      await p1.finish_loading()
      await p1.wait(2)
      await p1.send_key("W", 0.5)
      await go_through_dialogs(clients)

      await p1.send_key("W", 1)
      await p1.wait(0.5)
      await p2.teleport_to(KING_BATTLE)
      await p2.wait(0.5)
      await p3.teleport_to(KING_BATTLE)
      await p3.wait(0.5)
      await p4.teleport_to(KING_BATTLE)
      await p4.wait(0.5)

      await fight("trashking",*clients)
      await check_all_potions(clients)
      await p1.logout_and_in()
      await p2.logout_and_in()
      await p3.logout_and_in()
      await p4.logout_and_in()
      

  except Exception:
    traceback.print_exc()
  finally:
    # ALWAYS UNREGISTER!
    await unregister_all() 







if __name__ == "__main__":
  asyncio.run(farm())