# pip3 install --upgrade instaloader
import instaloader
import re
import pandas as pd
import tqdm.auto as tqdm
import time

def email_search(info):
    if re.search('@[a-z]+.com', info):
        return True
    else:
        return False

def flag_search(info):
    if re.search('[\U0001F1E0-\U0001F1FF]', info):
        return True
    else:
        return False

def usa_search(info):
    if re.search('🇺🇸', info):
        return True
    else:
        return False

def please(start, end):
    L = instaloader.Instaloader()

    li_star = []
    li_followers = []
    li_following = []
    li_explanation = []
    email = []
    flag = []
    usa = []
    crawl_list = pd.read_excel("/Users/sjpyo/Desktop/travel/crawl_monday.xlsx")

    for idx in tqdm.tqdm(range(start, end + 1), desc = '돌리는중'):
        star_id = crawl_list['star_id'][idx]
        print(star_id)
        
        try:
            profile = instaloader.Profile.from_username(L.context, str(star_id))
            followees = profile.followees
            followers = profile.followers
            explanation = profile.biography
            if followers > 100000:
                li_star.append(star_id)
                li_following.append(followees)
                li_followers.append(followers)   
                li_explanation.append(explanation)

                if usa_search(explanation):
                    usa.append('O')
                else:
                    usa.append('X')
                if flag_search(explanation):
                    flag.append('O')
                else:
                    flag.append('X')
                if email_search(explanation):
                    email.append('O')
                else:
                    email.append('X')
            else:
                continue
        except:

            continue
    
    df_starid = pd.DataFrame(li_star, columns = ['star_id'])
    df_followers = pd.DataFrame(li_followers, columns=['followers'])
    df_following = pd.DataFrame(li_following, columns=['following'])
    df_explanation = pd.DataFrame(li_explanation, columns=['info'])
    df_email = pd.DataFrame(email, columns=['email'])
    df_flag = pd.DataFrame(flag, columns=['flag'])
    df_usa = pd.DataFrame(usa, columns=['usa_flag'])

    main_df = pd.concat([df_starid, df_followers], axis = 1)
    main_df = pd.concat([main_df, df_following], axis = 1)
    main_df = pd.concat([main_df, df_explanation], axis = 1)
    main_df = pd.concat([main_df, df_email], axis = 1)
    main_df = pd.concat([main_df, df_flag], axis = 1)
    main_df = pd.concat([main_df, df_usa], axis = 1)


    main = pd.ExcelWriter(f'/Users/sjpyo/Desktop/travel/travel_{start}_{end}.xlsx') # pylint: disable=abstract-class-instantiated
    main_df.to_excel(main)
    main.save()

# for i in range(0, 1312, 500):
please(1000, 1311)