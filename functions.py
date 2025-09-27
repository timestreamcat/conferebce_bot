from data import answers_made_easy

print('Это модуль functions')

def math(data):
    sum = 0
    d = [data[f'step_{i}'] for i in range (3,8)]
    for i in d:
        if i in answers_made_easy:
            sum += answers_made_easy[i]
        else: sum += int(i)

    routine_hour = 4.33*(sum)
    if data['step_2'] in answers_made_easy:
        hour = answers_made_easy[data['step_2']]
    else: hour = int(data['step_2'])

    if data['step_1'] in answers_made_easy:
        payment = answers_made_easy[data['step_1']]
    else: payment = int(data['step_1'])
    sell_hour = payment//(hour*4.33+1)

    return [routine_hour, round((sell_hour*routine_hour),2)]