#remember to load pickle file: review.p
def get_total_review_g(g_id):
    count = 0
    for each in review:
        if review[each]['game_id'] == g_id:
            count = count + 1
    #print('{0} : {1} '.format(g_id,count))
    return count


def get_total_review_u(u_id):
    count = 0
    for each in review:
        if review[each]['user_id'] == u_id:
            count = count + 1
    #print('{0} : {1} '.format(u_id,count))
    return count
