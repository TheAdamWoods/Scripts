targetCoords = PathFinding.Route()
targetCoords.MaxRetry = 5
targetCoords.UseResync = True
targetCoords.StopIfStuck = False
targetCoords.X = 1415
targetCoords.Y = 1696

if PathFinding.Go(targetCoords):
	anatEvalTarget = 0x00000268
	# Eval Int
	while(Player.GetRealSkillValue('EvalInt') < 100.0):
		Target.Cancel()
		Misc.Pause(50)
		Player.UseSkill('EvalInt')
		Target.WaitForTarget(500)
		Target.TargetExecute(anatEvalTarget)
		Misc.Pause(1000)
	# Anat
	while(Player.GetRealSkillValue('Anatomy') < 100.0):
		Target.Cancel()
		Misc.Pause(50)
		Player.UseSkill('Anatomy')
		Target.WaitForTarget(500)
		Target.TargetExecute(anatEvalTarget)
		Misc.Pause(5000)
	# Spirit Speak
	while(Player.GetRealSkillValue('Spirit Speak') < 100.0):
		Player.UseSkill('Spirit Speak')
		Misc.Pause(1000)
	# Item ID
	_spellbookID = Items.FindByID(0x0EFA, -1, Player.Backpack.Serial)
	while(Player.GetRealSkillValue('Item ID') < 100.0):
		Target.Cancel()
		Misc.Pause(50)
		Player.UseSkill('Item ID')
		Target.WaitForTarget(500)
		Target.TargetExecute(_spellbookID)
		Misc.Pause(1000)
	# Arms Lore
	while(Player.GetRealSkillValue('Arms Lore') < 100.0):
		Target.Cancel()
		Misc.Pause(50)
		Player.UseSkill('Arms Lore')
		Target.WaitForTarget(500)
		Target.TargetExecute(_spellbookID)
		Misc.Pause(1000)
