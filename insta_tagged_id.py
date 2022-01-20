# pip3 install --upgrade instaloader
import pandas as pd
from tqdm import tqdm
import instaloader

def tagged_id(name_id):
	L = instaloader.Instaloader(download_pictures = False, download_videos = False, download_video_thumbnails = False,
	                            download_geotags = False, download_comments = False, save_metadata = False)

	# glami : wakeupandmakeup, morphebrushes, influenster
	# travel : beautifuldestinations, Beautifulhotels

	posts = instaloader.Profile.from_username(L.context, name_id).get_posts()

	li = []
	for post in tqdm(posts, desc = "돌리는중: "):
		try:
		    li_star_id = post.caption_mentions
		    sorting = len(li_star_id)
		    if sorting == 0:
		        continue
		    elif sorting == 1:
		    	if li_star_id in li:
		    		continue
		    	else:
		        	li.append(li_star_id[0])
		    else:
		        for i in li_star_id:
		        	if i in li:
		        		continue
		        	else:
		            	li.append(i)
		except:
			continue

	df_star_id = pd.DataFrame(li, columns = ['star_id'])
	main = pd.ExcelWriter(f'/Users/sjpyo/Desktop/{name_id}.xlsx') # pylint: disable=abstract-class-instantiated
	df_star_id.to_excel(main)
	main.save()

	print('FINISH')

if __name__=="__main__":
	tagged_id()