result_data_path = "/Users/ting-hsin/Downloads/"


resultLIST = []
tmpLIST = []

#剩把pseudoDICT的值叫出來
pseudoLIST = []
targetPseudoLIST = []
High_CDpwLIST = []
Low_CDpwLIST = []
sub_num = "003"
with open (result_data_path + "003_pseudowordsDICT.json", "r", encoding = "utf-8") as jfile:
    pseudoDICT = json.load(jfile)
    pprint(pseudoDICT)

    #print(sub_num)

    targetPseudoLIST.extend(pseudoDICT["The TargetPseudo group_6"])
    High_CDpwLIST.extend(pseudoDICT["High_CD condition pseudowords_3"])
    Low_CDpwLIST.extend(pseudoDICT["Low_CD condition pseudowords_3"])

    print(sub_num, "Target pw : ", targetPseudoLIST)
    print(sub_num, "High-CD pw : ", High_CDpwLIST)
    print(sub_num, "Low-CD pw : ", Low_CDpwLIST) # output: 003 Low-CD pw :  ['vaesow', 'payliy', 'paenliy']    


with open (result_data_path + "003_Reading_task.csv", "r", encoding= 'unicode_escape') as csvfile_reading:  #, "r", encoding = "utf-8")
    readingLIST = csvfile_reading.read().split("\n")
    #pprint(readingLIST)
    #print(type(readingLIST))
    #print(len(readingLIST))
    readingLIST.pop(0)   # exclude the headers
    #print(len(readingLIST))
    
    # exclude the blank row
    readingLIST = LISTblankEraser(readingLIST)
    #print(len(readingLIST))
    #print(readingLIST[0])
    count = 0
    cleaned_LIST = []
    textLIST = []
    
    for row in readingLIST:
        #print(row)
        if ',"[""' in row:
            rawLIST = row.split(',"[""')
        elif ',"[\'' in row:
            rawLIST = row.split(',"[\'')
        else:
            print("Wrong!!!!!!!!!!!!!!!!!! >>>>>",rawLIST)
            print("Wrong_count >>>>>", len(rawLIST))
            
        if len(rawLIST) ==2:
            count +=1
        else:
            print("Wrong!!!!!!!!!!!!!!!!!! >>>>>",rawLIST)
            print("Wrong_count >>>>>", len(rawLIST))
        cleaned_LIST.append(rawLIST)

    print(count)
    #pprint(cleaned_LIST)
    print(len(cleaned_LIST))
    
    count_H = 0
    count_L = 0
    
    text_H_LIST = []
    text_L_LIST = []
    
    for row in cleaned_LIST:
        textLIST = row[1].lower().split(" ")
        #print(textLIST)
        #print(len(textLIST))
        for H_pw in High_CDpwLIST:
            for word in textLIST:
                if H_pw in word:
                    print("High-CD", word)
                    count_H += 1
                    text_H_LIST.append(row)
                else:
                    pass
        for L_pw in Low_CDpwLIST:
            for word in textLIST:
                if L_pw in word:
                    print("Low-CD", word)
                    count_L += 1
                    text_L_LIST.append(row)
                else:
                    pass
    
    #print("count_H", count_H)
    #print("count_L", count_L)
    #print("Text_Hs", text_H_LIST)
    #print(len(text_H_LIST))
    #print("Text_Ls", text_L_LIST)
    #print(len(text_L_LIST))
    ##print(len(readingLIST[0]))
    new_text_H_LIST = []
    new_text_L_LIST = []
    H_ratingDICT = {}
    L_ratingDICT = {}
    
    for row in text_H_LIST:
        rawLIST = row[0].split(",")
        rawLIST.append(row[1])
        new_text_H_LIST.append(rawLIST)
    #print(new_text_H_LIST)
    #print(len(new_text_H_LIST))
    
    for row in text_L_LIST:
        rawLIST = row[0].split(",")
        rawLIST.append(row[1])
        new_text_L_LIST.append(rawLIST)
    #print(new_text_L_LIST)
    #print(len(new_text_L_LIST))
    
    H_ratingDICT = Mean(new_text_H_LIST, 4, "H-CD self-rating")
    L_ratingDICT = Mean(new_text_L_LIST, 4, "L-CD self-rating")
    
    print(H_ratingDICT)
    print(L_ratingDICT)