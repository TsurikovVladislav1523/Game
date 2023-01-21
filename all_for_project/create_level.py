def create_level(filename):
    filename = "all_for_project/levels/" + filename + '.txt'
    # filename = filename + '.txt'
    with open(filename, 'r') as file:
        text = file.read()
        level = []
        file.close()
        text = text.split('\n')
        for i in range(len(text)):
            level.append([])
            for j in list(text[i]):
                level[i].append(int(j))
        return level
