def get_num_games(g_id, u_id):
	target = ""
	for g in classification:
		if g_id in classification[g]:
			target = g
			break
	return user[u_id][target]

def get_avg_user_level(g_id):
	level_total = 0
	for u in game_user[g_id]:
		level_total = level_total + user[u]['userLevel']
	return level_total/len(game_user[g_id])

def get_avg_user_playtime(g_id):
	playtime_total = 0
	for u in game_user[g_id]:
		playtime_total = playtime_total + game_user[g_id][u]['total_play_time']
	return playtime_total/len(game_user[g_id])

def get_avg_user_playtime_in_G(g_id):
	playtime_total = 0
	num_user = 0
	target = ""
	for g in classification:
		if g_id in classification[g]:
			target = g
			break
	for all_other_g in classification[target]:
		for u in game_user[all_other_g]:
			playtime_total = playtime_total + game_user[all_other_g][u]['total_play_time']
			num_user = num_user + len(game_user[all_other_g])
	return playtime_total/len(game_user[g_id])

def get_user_playtime(g_id, u_id):
	return game_user[g_id][u_id]['total_play_time']

def get_user_level(u_id):
	return user[u_id]['userLevel']

