# -*- coding: utf-8 -*-
"""bookfindingalgo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xPvm4snTjjxt_DJPrjJlIURvDHwTv8xf
"""

from numpy import*
#book_in_hand

# books = [Genre  ,Author, 'Year' , 'Index'] 
books = [['005.14', 'PBX', '2011', '123'],
         ['005.14', 'qBX', '2012', '123'],
         ['005.14', 'sBX', '2011', '123'],
         ['005.14', 'uBX', '2011', '123']]
#        [Genre  ,Author, 'Year' , 'Index']
book_in_hand  = ['005.14', 'ubx', '2011', '124']
flag = -1
i_genre = book_in_hand[0] #to insert book
i_writer = book_in_hand[1].lower()
i_year = book_in_hand[2]
i_index = book_in_hand[3]
for book in books:
  genre = book[0]
  writer = book[1].lower()
  year = book[2]
  index = book[3]
  if genre != i_genre:
    flag = -1
    break
  else:
    if i_writer < writer:
      flag = flag+1
      break
    elif i_writer > writer :
      flag = flag+1
      continue
    elif i_writer == writer:
      if i_year < year:
        flag = flag+1
        break
      elif i_year > year:
        flag = flag+1
        continue
      elif i_year == year:
        if i_index > index:
          flag = flag+1
          continue
        if i_index < index:
          flag = flag+1
          break
print(flag)
rows = len(books)-1
print ('Book 1', book_in_hand)
print ('List of Books', books)
if flag == -1:
  print("In wrong rack Move Forward")
elif flag == rows:
  if i_writer < writer:
    print('Insert before\nwriter:: ', writer, '\nyear::',year,'\nindex',index)
  else:
    print('Insert After\nwriter:: ', writer, '\nyear::',year,'\nindex',index)
else:
  print('Insert before\nwriter:: ', books[flag][1], '\nyear::',books[flag][2],'\nindex',books[flag][3])