leaders_number = 12
output_leaderboard = open("Leaderboard", "w")
leaders = ["NAME", "SCORE", "TIME"]
for _ in range(leaders_number):
    leaders.append("UNTITLED")
    leaders.append("0")
    leaders.append("00:00")
for j in range(leaders_number + 1):
    print(leaders[j * 3] + " " * (16 - len(leaders[j * 3])) + leaders[j * 3 + 1] + " " * (
            12 - len(leaders[j * 3 + 1])) + leaders[j * 3 + 2], file=output_leaderboard)
output_leaderboard.close()
