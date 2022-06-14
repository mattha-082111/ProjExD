import random

q_1 = "サザエの旦那の名前は？"
q_2 = "カツオの妹の名前は？"
q_3 = "タラオはカツオから見てどんな関係？"

q_1_ans = ["マスオ","ますお"]
q_2_ans = ["ワカメ","わかめ"]
q_3_ans = ["甥","おい","甥っ子","おいっこ"]

r = random.randint(0,2)

def main():
    seikai = shutudai()
    kaitou(seikai)

def shutudai():
    Ques = [q_1,q_2,q_3]
    print("問題：")
    print(Ques[r])
    return Ques[r]

def kaitou(seikai):
    Ques_ans = [q_1_ans,q_2_ans,q_3_ans]
    ans = input("答えは？？:")
    if ans in Ques_ans[r]:
        print("正解!")
    else:
        print("残念!")
        
if __name__ == "__main__":
    main() 
