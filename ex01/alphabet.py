import random
import datetime

kurikaesi = 5 #最大繰り返し回数
alpha_all = 10 #最大文字数
alpha_mis = 5 #欠損文字数

def main():
    st = datetime.datetime.now()
    for _ in range(kurikaesi):
        seikai = shutudai()
        w = kaitou(seikai)
        if w == 1:
            break
    ed = datetime.datetime.now()
    print(f"所要時間：{(ed - st).seconds}秒かかったよ")


def shutudai():
    #全アルファベットの文字数
    alpha = [chr(i+65) for i in range(26)]
    alpha_all_des = random.sample(alpha,alpha_all)
    print(f"対象文字：{alpha_all_des}")

    #欠損文字を表示
    alpha_mis_des = random.sample(alpha_all_des,alpha_mis)
    #print(f"欠損文字：{alpha_mis_des}")
    
    #問題表示
    pre_alpha_lis = [r for r in alpha_all_des if r not in alpha_mis_des]
    print(f"表示文字：{pre_alpha_lis}")

    return alpha_mis_des

def kaitou(seikai):
    ans = int(input("欠損文字はいくつある？:"))    
    if ans != alpha_mis:
        print("残念！ 不正解！")
        return 0
    else:
        print("正解！ 具体的な欠損文字は…？")
        for z in range(alpha_mis):
            s = input(f"{z+1}つ目の文字を入力してください：")
            if s not in seikai:
                print("不正解！ またチャレンジしてね")
                return 0
        return 1

if __name__ == "__main__":
    main()