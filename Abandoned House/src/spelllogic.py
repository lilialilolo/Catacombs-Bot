import asyncio
from farmlogic import farm

# async def pass_turn_dead(self) -> None:
#   """
#   Clicks `pass` while in a battle
#   """
#   await self.mouse.click(300, 300, duration=0.2, delay=0.5)
#   await self.wait(0.5)

async def fight(name, p1, p2, p3, p4):

  hitter_pos = 7 # 6 for 3, 7 for 4
  
  battle = p2.get_battle(name)
  if (name == "mobs"):
    while await battle.loop():
      m_feint = await p1.find_spell('mass-feint')
      if m_feint:
        await m_feint.cast()
      else:
        await p1.pass_turn()

      r_ele = await p2.find_spell('elemental-blade')
      r_sharpen = await p2.find_spell('sharpened-blade')
      if r_ele and r_sharpen:
        e_r_blade = await r_sharpen.enchant(r_ele)
        await e_r_blade.cast(target=hitter_pos)
      else:
        await p2.pass_turn()
      
      ele_blade = await p3.find_spell('elemental-blade')
      if ele_blade:
        await ele_blade.cast(target=hitter_pos)
      else:
        await p3.pass_turn()

      tempest = await p4.find_spell('tempest')
      epic = await p4.find_spell('epic')

      if tempest and epic:
        e_hit = await epic.enchant(tempest)
        await e_hit.cast()
      else:
        await p4.pass_turn()

  ##BOSS BATTLE *epic, intense music, plays intensely and epically*
  elif (name == "trashking"):
    count = 0
    while await battle.loop():
      ########################################################
      ## R1/3
      ########################################################
      if count % 3 == 0:
        m_feint = await p1.find_spell('mass-feint')
        if m_feint:
          await m_feint.cast()
        else:
          await p1.pass_turn()

        r_potent = await p2.find_spell('potent')
        r_feint = await p2.find_spell('feint')
        if r_feint and r_potent:
          e_r_potent = await r_potent.enchant(r_feint)
          await e_r_potent.cast(target=0)
        else:
          await p2.pass_turn()

        r_feint = await p3.find_spell('feint')
        i_potent = await p3.find_spell('potent-item')
        if r_feint and i_potent:
          e_i_potent = await i_potent.enchant(r_feint)
          await e_i_potent.cast(target=0)
        else:
          await p3.pass_turn()

        frenzy = await p4.find_spell('frenzy')

        if frenzy:
          await frenzy.cast()
        else:
          epic = await p4.find_spell('epic')
          tempest = await p4.find_spell('epic')
          if epic and tempest:
            e_hit = await epic.enchant(tempest)
            await e_hit.cast()
          else:
            await p4.pass_turn()

      ########################################################
      ## R2/4
      ########################################################
      elif count % 3 == 1:
        r_ele = await p1.find_spell('elemental-blade')
        i_sharpen = await p1.find_spell('sharpened-blade-item')
        if r_feint and i_sharpen:
          e_i_blade = await i_sharpen.enchant(r_ele)
          await e_i_blade.cast(target=hitter_pos)
        else:
          await p1.pass_turn()

        r_ele = await p2.find_spell('elemental-blade')
        r_sharpen = await p2.find_spell('sharpened-blade')
        if r_ele and r_sharpen:
          e_r_blade = await r_sharpen.enchant(r_ele)
          await e_r_blade.cast(target=hitter_pos)
        else:
          await p2.pass_turn()
        
        ele_blade = await p3.find_spell('elemental-blade')
        if ele_blade:
          await ele_blade.cast(target=hitter_pos)
        else:
          await p3.pass_turn()

        stormlord = await p4.find_spell('storm-lord')
        epic = await p4.find_spell('epic')

        if stormlord and epic:
          e_hit = await epic.enchant(stormlord)
          await e_hit.cast()
        else:
          await p4.pass_turn()
      count +=1



asyncio.run(farm(fight))