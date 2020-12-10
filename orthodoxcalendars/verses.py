# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:30:31 2020

@author: adamisch
"""
import itertools
import pandas as pd
import re

def get_verses(reading):
    """Reading name translated to book, chapter, and verse DataFrame."""
    if reading:
        book_name=[x.strip() for x in re.findall("(^.*?)(?=\d*:)", reading) if x]
        print(book_name)
        if ";" in reading:
                # Acts 6:8-15; 7:1-5, 47-60
            chapter_verses = reading.split(';')
            chapters = [[x.strip() for x in re.findall("(\d+?)(?=:)", y)] 
                    for y in chapter_verses]
            verses =  [x.strip() for x in re.findall("(?<=[:, ])(?<![[a-z]{1}\s)([\d-]+)(?![:\d])", reading)]
            readings_return = pd.DataFrame([book_name, chapters, verses]).T.explode(1).ffill()
            readings_return.rename({0:'b', 1:'c', 2:'v'}, axis=1, inplace=True)
            readings_return['reading'] = reading
            return readings_return
        elif "," in reading:
            # Luke 2:20-21, 40-52
            # Hebrews 12:25-26, 13:22-25
            # Matthew 10:32-33, 37-38, 19:27-30
            chapter_verses = reading.split(',')
            chapters = [[x.strip() for x in re.findall("(\d+?)(?=:)", y)] 
                       for y in chapter_verses]
            verses =  [x.strip() for x in re.findall("(?<=[:, ])(?<![[a-z]{1}\s)([\d-]+)(?![:\d])", reading)]
            ###### WORK IN PROGRESS ###
            chapters_2d = list(itertools.chain(*chapters))
            for i in range(len(chapters)):
                # if it spans multiple books, the verses will show up as single numbers
                # find index of it, and change it in verses
                if len(chapters[i])==2:
                    verses[i] = verses[i]+"-end"
                    verses[i+1] = "1-" + verses[i+1]
            readings_return = pd.DataFrame([book_name, chapters_2d, verses]).T.explode(1).ffill()
            readings_return.rename({0:'b', 1:'c', 2:'v'}, axis=1, inplace=True)
            readings_return['reading'] = reading
            return readings_return
        else:
            # John 10:1-9
            if re.findall('(\d+?)(:)(\d+)(-)(\d+?)(:)(\d+)', reading) != []:
                ### if it spans multiple books, e.g. Luke 21:37-22:8
                chapters = [x.strip() for x in re.findall("(\d+?)(?=:)", reading)]
                # Get first verse, until end
                verses =  [x.strip() for x in re.findall("(?<=[:, ])(?<![[a-z]{1}\s)([\d-]+)(?![:\d])", reading)]
                # Get second verse from same book
                verses[0] = verses[0] + "-end"
                verses[1] = "1-"+verses[1]
            else:
                chapters = [x.strip() for x in re.findall("(\d+?)(?=:)", reading)]
                verses =  [x.strip() for x in re.findall("(?<=[:])([\d-]+)", reading)]
            readings_return = pd.DataFrame([book_name, chapters, verses]).T.ffill()
            readings_return.rename({0:'b', 1:'c', 2:'v'}, axis=1, inplace=True)
            readings_return['reading'] = reading
            return readings_return
    else:
        return None
    
        
def end_verse(book, chapter, n_verses):
     """For readings that span the end of one chapter and the beginning of another"""
     book = int(book)
     chapter = int(chapter)
     end_verse = n_verses[(n_verses['b']==book)&(n_verses['c']==chapter)][0]
     return int(end_verse)
    
