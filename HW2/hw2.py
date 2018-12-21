import copy

inp = open("input.txt")


def feasible(arr1, arr2, j):
    for i in range(7):
        if arr1[i] + arr2[i] > j:
            return False
    return True


def add(arr1, arr2):
    arr3 = copy.deepcopy(arr1)
    for i in range(7):
        arr3[i] += arr2[i]
    return arr3


def subtract(arr1, arr2):
    arr3 = copy.deepcopy(arr1)
    for i in range(7):
        arr3[i] -= arr2[i]
    return arr3


def sum(options):
    total = 0
    for option in options:
        for day in option.days:
            total += day

    return total


def value(a):
    sum = 0
    for i in range(len(a)):
        sum += a[i]
    return sum


def better(matrix_sum, current_max):
    sum1 = 0
    sum2 = 0
    for i in range(7):
        sum1 += matrix_sum[i]
        sum2 += current_max[i]
    if sum1 > sum2:
        return True
    return False


def spla_move(spla_options1, lahsa_options1, intersecting_options1, spots_filled1, beds_filled1, total_spots1,
              total_beds1):
    best_lahsa_score = [0, 0, 0, 0, 0, 0, 0]
    best_spla_score = [0, 0, 0, 0, 0, 0, 0]
    id = ""
    total_spla_solution = []

    if len(intersecting_options1) == 0:
        best_spla_score, spla_id, spla_solution_list = DP(spla_options1, spots_filled1, total_spots1)
        best_lahsa_score, lahsa_id, lahsa_solution_list = DP(lahsa_options1, beds_filled1, total_beds1)
        return subtract(best_spla_score, spots_filled1), subtract(best_lahsa_score,
                                                                  beds_filled1), spla_id, spla_solution_list

    for intersecting_option1 in intersecting_options1:
        if feasible(intersecting_option1.days, spots_filled1, total_spots1):
            idx0 = intersecting_options1.index(intersecting_option1)
            intersecting_options1.remove(intersecting_option1)
            spla_days, lahsa_days, lahsa_chosen_ap_id, spla_solution_list = lahsa_move(spla_options1, lahsa_options1,
                                                                                       intersecting_options1,
                                                                                       add(spots_filled1,
                                                                                           intersecting_option1.days),
                                                                                       beds_filled1, total_spots1,
                                                                                       total_beds1)
            intersecting_options1.insert(idx0, intersecting_option1)

            if better(add(spla_days, intersecting_option1.days), best_spla_score):
                total_spla_solution = spla_solution_list
                best_spla_score = add(spla_days, intersecting_option1.days)
                best_lahsa_score = lahsa_days
                id = intersecting_option1.applicantID

    best_DP_spla_score, DP_spla_id, spla_solution_list = DP(spla_options1, spots_filled1, total_spots1)
    if better(subtract(best_DP_spla_score, spots_filled1), best_spla_score):
        total_spla_solution = spla_solution_list
        best_spla_score = best_DP_spla_score
        combined_list = lahsa_options1 + intersecting_options1
        best_lahsa_score, lahsa_id, lahsa_solution_list = DP(combined_list, beds_filled1, total_beds1)
        best_lahsa_score = subtract(best_lahsa_score, beds_filled1)
        id = DP_spla_id

    total_spla_solution.append(id)
    return best_spla_score, best_lahsa_score, id, total_spla_solution


def lahsa_move(spla_options2, lahsa_options2, intersecting_options2, spots_filled2, beds_filled2, total_spots2,
               total_beds2):
    best_lahsa_score = [0, 0, 0, 0, 0, 0, 0]
    best_spla_score = [0, 0, 0, 0, 0, 0, 0]
    id = ""
    total_spla_solution = []

    if len(intersecting_options2) == 0:
        best_spla_score, spla_id, spla_solution_list = DP(spla_options2, spots_filled2, total_spots2)
        best_lahsa_score, lahsa_id, lahsa_solution_list = DP(lahsa_options2, beds_filled2, total_beds2)
        return subtract(best_spla_score, spots_filled2), subtract(best_lahsa_score,
                                                                  beds_filled2), lahsa_id, spla_solution_list

    for intersecting_option2 in intersecting_options2:
        if feasible(intersecting_option2.days, beds_filled2, total_beds2):
            idx0 = intersecting_options2.index(intersecting_option2)
            intersecting_options2.remove(intersecting_option2)

            spla_days, lahsa_days, spla_chosen_ap_id, spla_solution_list = spla_move(spla_options2, lahsa_options2,
                                                                                     intersecting_options2,
                                                                                     spots_filled2,
                                                                                     add(beds_filled2,
                                                                                         intersecting_option2.days),
                                                                                     total_spots2, total_beds2)

            intersecting_options2.insert(idx0, intersecting_option2)

            if better(add(lahsa_days, intersecting_option2.days), best_lahsa_score):
                total_spla_solution = spla_solution_list
                best_lahsa_score = add(lahsa_days, intersecting_option2.days)
                best_spla_score = spla_days
                id = intersecting_option2.applicantID

    best_DP_lahsa_score, DP_lahsa_id, lahsa_solution_list = DP(lahsa_options2, beds_filled2, total_beds2)
    if better(subtract(best_DP_lahsa_score, beds_filled2), best_lahsa_score):
        combined_list = spla_options2 + intersecting_options2
        best_spla_score, spla_id, spla_solution_list = DP(combined_list, spots_filled2, total_spots2)
        best_spla_score = subtract(best_spla_score, spots_filled2)
        best_lahsa_score = best_DP_lahsa_score
        total_spla_solution = spla_solution_list
        id = DP_lahsa_id

    return best_spla_score, best_lahsa_score, id, total_spla_solution


def DP(player_options, space_already_used, no_of_spaces):
    if no_of_spaces == 0:
        return [0, 0, 0, 0, 0, 0, 0], 0, []

    player_options_count = len(player_options)

    matrix = [[[0 for i in range(7)] for j in range(no_of_spaces + 1)] for k in range(player_options_count + 1)]

    # find min parking space needed to solve the problem
    min_space_needed = 0
    for i in range(7):
        if space_already_used[i] > min_space_needed:
            min_space_needed = space_already_used[i]

    # base conditions for DP
    for j in range(min_space_needed, no_of_spaces + 1):
        matrix[0][j] = space_already_used

    for i in range(1, player_options_count):
        matrix[i][0] = [0, 0, 0, 0, 0, 0, 0]

    for i in range(1, player_options_count + 1):
        for j in range(min_space_needed,
                       no_of_spaces + 1):
            current_max = matrix[i - 1][j]
            for k in range(0, j):
                if feasible(matrix[i - 1][j - k], player_options[i - 1].days, j):
                    matrix_sum = add(matrix[i - 1][j - k], player_options[i - 1].days)
                    if better(matrix_sum, current_max):
                        current_max = matrix_sum
                        break
            for k in range(2, i):
                if feasible(player_options[i - k].days, player_options[i - 1].days, j):
                    matrix_sum = add(player_options[i - k].days, player_options[i - 1].days)
                    if better(matrix_sum, current_max):
                        current_max = matrix_sum
                        break
            matrix[i][j] = current_max

    # for i in range(0, player_options_count + 1):
    #     print matrix[i]

    dp_solution = []

    # for i in range(player_options_count):
    #     print player_options[i].applicantID, player_options[i].days

    i = player_options_count
    j = no_of_spaces

    while i != 0:
        i_changed = False
        for k in range(j, 0, -1):
            if matrix[i][j] == add(player_options[i - 1].days, matrix[i - 1][k]):
                dp_solution.append(player_options[i - 1].applicantID)
                # print player_options[i - 1].applicantID
                i -= 1
                j = k
                i_changed = True
                break
            if matrix[i][j] == matrix[i - 1][k]:
                i -= 1
                j = k
                i_changed = True
                break
        if not i_changed:
            # print "ye case aata bhi hai"
            for k in range(i - 2, 0, -1):
                if matrix[i][j] == add(player_options[i - 1].days, player_options[k].days):
                    dp_solution.append(player_options[i - 1].applicantID)
                    # print player_options[i - 1].applicantID
                    i = k
                    break

    # print dp_solution
    id = 0
    if len(dp_solution) != 0:
        id = dp_solution[0]
    return matrix[player_options_count][no_of_spaces], id, dp_solution  # logic to send smallest id


class Applicant:

    def __init__(self, applicantID, gender, age, pets, medical_conditions, car, drivers_license, days):
        self.applicantID = applicantID
        self.gender = gender
        self.age = age
        self.pets = pets
        self.medical_conditions = medical_conditions
        self.car = car
        self.drivers_license = drivers_license
        self.days = days


no_of_beds = int(inp.readline().strip())
no_of_parking_spaces = int(inp.readline().strip())

# for testing
# no_of_parking_spaces = 2

L = int(inp.readline().strip())
lahsa_already_chosen_set = []
for x in range(L):
    lahsa_already_chosen_set.append(inp.readline().strip())

S = int(inp.readline().strip())
spla_already_chosen_set = []
for x in range(S):
    spla_already_chosen_set.append(inp.readline().strip())

A = int(inp.readline().strip())

spla_only_set = []
lahsa_only_set = []
intersecting_set = []

spla_parking_space_already_used = [0, 0, 0, 0, 0, 0, 0]
lahsa_beds_already_used = [0, 0, 0, 0, 0, 0, 0]

for x in range(A):
    applicant = inp.readline().strip()
    if spla_already_chosen_set.__contains__(applicant[:5]):
        for i in range(7):
            if applicant[i + 13] == "1":
                spla_parking_space_already_used[i] += 1
        continue
    if lahsa_already_chosen_set.__contains__(applicant[:5]):
        for i in range(7):
            if applicant[i + 13] == "1":
                lahsa_beds_already_used[i] += 1
        continue
    if applicant[10:11] == "N" and applicant[11:12] == "Y" and applicant[12:13] == "Y":
        if applicant[5:6] == "F" and int(applicant[6:9]) > 17 and applicant[9:10] == "N":
            intersecting_set.append(
                Applicant(applicant[:5], applicant[5:6], applicant[6:9], applicant[9:10], applicant[10:11],
                          applicant[11:12], applicant[12:13],
                          [int(applicant[13]), int(applicant[14]), int(applicant[15]),
                           int(applicant[16]), int(applicant[17]), int(applicant[18]), int(applicant[19])]))
        else:
            spla_only_set.append(
                Applicant(applicant[:5], applicant[5:6], applicant[6:9], applicant[9:10], applicant[10:11],
                          applicant[11:12], applicant[12:13],
                          [int(applicant[13]), int(applicant[14]), int(applicant[15]),
                           int(applicant[16]), int(applicant[17]), int(applicant[18]), int(applicant[19])]))
    elif applicant[5:6] == "F" and int(applicant[6:9]) > 17 and applicant[9:10] == "N":
        lahsa_only_set.append(
            Applicant(applicant[:5], applicant[5:6], applicant[6:9], applicant[9:10], applicant[10:11],
                      applicant[11:12], applicant[12:13], [int(applicant[13]), int(applicant[14]), int(applicant[15]),
                                                           int(applicant[16]), int(applicant[17]), int(applicant[18]),
                                                           int(applicant[19])]))

spla, lahsa, id, solution_list = spla_move(spla_only_set, lahsa_only_set, intersecting_set,
                                           spla_parking_space_already_used,
                                           lahsa_beds_already_used, no_of_parking_spaces,
                                           no_of_beds)

spla_only_applicant_ids = {}
lahsa_only_applicant_ids = {}
intersection_only_applicant_ids = {}

# print "spla_only"
for spla_asd in spla_only_set:
    # print spla_asd.applicantID
    spla_only_applicant_ids[spla_asd.applicantID] = spla_asd.days

# print "lahsa only"
for lahsa_asd in lahsa_only_set:
    # print lahsa_asd.applicantID
    lahsa_only_applicant_ids[lahsa_asd.applicantID] = lahsa_asd.days

# print "intersecting only"
for interseting_asd in intersecting_set:
    # print interseting_asd.applicantID
    intersection_only_applicant_ids[interseting_asd.applicantID] = interseting_asd.days

# print "solution list"
# print solution_list

if id in intersection_only_applicant_ids:
    best_id = ""
    best_days = [0, 0, 0, 0, 0, 0, 0]
    for solution_id in solution_list:
        if solution_id in intersection_only_applicant_ids:
            if value(intersection_only_applicant_ids[solution_id]) < value(best_days):
                continue
            else:
                if value(intersection_only_applicant_ids[solution_id]) == value(best_days):
                    if int(solution_id) < int(best_id):
                        best_id = solution_id
                else:
                    best_id = solution_id
                    best_days = intersection_only_applicant_ids[solution_id]
else:
    best_id = "99999"
    best_days = [0, 0, 0, 0, 0, 0, 0]
    for solution_id in solution_list:
        if solution_id in spla_only_applicant_ids:
            if value(spla_only_applicant_ids[solution_id]) < value(best_days):
                continue
            else:
                if value(spla_only_applicant_ids[solution_id]) == value(best_days):
                    if int(solution_id) < int(best_id):
                        best_id = solution_id
                else:
                    best_id = solution_id
                    best_days = spla_only_applicant_ids[solution_id]

# print value(spla)
# print value(lahsa)
# print id
#
# print "best id yeh hai"
# print best_id
out = open("output.txt", "w")
out.write(best_id)
out.close()
