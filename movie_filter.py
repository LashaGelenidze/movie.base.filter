import sqlite3
import matplotlib.pyplot as plt
conn=sqlite3.connect("movies.sqlite3")
cursor=conn.cursor()
# 1.ფუნქცია აბრუნებს ხაზს მითითებული წლის და აუდიენციის მიხედვით
def select_movies(dropping, rating):
    cursor.execute("SELECT * FROM movies WHERE year>=? AND movie_rated=?", (dropping, rating))
    conn.commit()
    return cursor.fetchone()


drop_year=int(input("შეიყვანეთ სასურველი წელი: "))
rated=str(input("შეიყვანეთ სასურველი რეიტინგი(PG, PG-13, R, G): "))
print(select_movies(drop_year,rated))

# ფუნქცია შეტანილი მონაცემების მიხედვით დაამატებს ხაზს
def insert_movies(movie_name, year, audience, lasting, genre, drop_date, rate, raters, review):
    cursor.execute("INSERT INTO movies (name, year, movie_rated, run_length, genres, release_date, rating, num_raters, num_reviews) VALUES (?,?,?,?,?,?,?,?,?)",
                   (movie_name,year,audience,lasting,genre,drop_date,rate,raters,review))
    conn.commit()

movie_name=str(input("შეიყვანეთ სახელი: "))
year=int(input("შეიყვანეთ წელი: "))
audience=str(input("შეიყვანეთ აუდიენცია(PG, PG-13, R, G): "))
lasting=str(input("შეიყვანეთ ხანგრძლივობა: "))
genre=str(input("შეიყვანეთ ჟანრი: "))
drop_date=str(input("შეიყვანეთ ზუსტი გამოშვების თარიღი: "))
rate=int(input("შეიყვანეთ შეფასება: "))
raters=int(input("შეიყვანეთ შემფასებელთა რაოდენობა: "))
review=int(input("შეიყვანეთ რამდენმა მიმოიხილა: "))
insert_movies(movie_name,year,audience,lasting,genre,drop_date,rate,raters,review)

# ფუნქცია მითითებული ფილმის სახელის მიხედვით შეცვლის რეიტინგს
def update_movies(rate, movie):
    cursor.execute('UPDATE movies SET rating=? WHERE name=?', (rate,movie))
    conn.commit()

rate=int(input("შეიყვანეთ შეფასება: "))
movie=str(input("შეიყვანეთ სახელი: "))
update_movies(rate,movie)

# ფუნქცია მითითებული რეიტინგის მიხედვით შლის შესაბამის ხაზებს
def delete_mivies(rate):
    cursor.execute("DELETE FROM movies WHERE rating=?", (rate,))
    conn.commit()

rate=int(input("შეიყვანეთ შეფასება: "))
delete_mivies(rate)

# ფუნქცია განსაზღვრავს ფილმების პროცენტულ რაოდენობას მათთვის განკუთვნილი აუდიენციის მიხედვით
def count_rated_movie(for_audience):
    return cursor.execute("SELECT count(*) FROM movies WHERE movie_rated=?", (for_audience,)).fetchone()[0]

c_for_PG=count_rated_movie('PG')
c_for_PG_13=count_rated_movie('PG-13')
c_for_R=count_rated_movie('R')
c_for_G=count_rated_movie('G')
all_of_them=c_for_PG+c_for_PG_13+c_for_R+c_for_G
print(all_of_them)

def movie_ratio(sum,part):
    return part/sum*100
p_for_PG=movie_ratio(all_of_them, c_for_PG)
p_for_PG_13=movie_ratio(all_of_them, c_for_PG_13)
p_for_R=movie_ratio(all_of_them, c_for_R)
p_for_G=movie_ratio(all_of_them, c_for_G)
print(p_for_PG, p_for_PG_13, p_for_R, p_for_G)



# მონაცემები გამოისახება pie chart-ის საშუალებით
labels=['PG აუდიენციისთვის','PG-13 აუდიენციისთვის','R აუდიენციისთვის','G აუდიენციისთვის']
sizes=[p_for_PG, p_for_PG_13, p_for_R, p_for_G]

fig, ax=plt.subplots()
ax.pie(sizes, labels=labels, autopct='%.f1%%')
plt.title("ფილმების განაწილება აუდიენციის მიხედვით")
plt.show()

# მონაცემები გამოისახება bar chart-ის საშუალებით
labels=['PG','PG-13','R','G']
bar_labels=['red','blue','green','orange']
bar_colors=['tab:red','tab:blue','tab:green','tab:orange']
plt.bar(labels, sizes, label=bar_labels, color=bar_colors)
plt.show()

# ეს ფუნქცია აჩვენებს თუ რამდენი ფილმი გამოვიდა 2008-დან 2019-ის ჩათვლით
def movie_quantity(exact_year):
    return cursor.execute("SELECT count(*) FROM movies WHERE year=?", (exact_year,)).fetchone()[0]

c_2008=movie_quantity(2008)
c_2009=movie_quantity(2009)
c_2010=movie_quantity(2010)
c_2011=movie_quantity(2011)
c_2012=movie_quantity(2012)
c_2013=movie_quantity(2013)
c_2014=movie_quantity(2014)
c_2015=movie_quantity(2015)
c_2016=movie_quantity(2016)
c_2017=movie_quantity(2017)
c_2018=movie_quantity(2018)
c_2019=movie_quantity(2019)
print(c_2008, c_2009 , c_2010, c_2011, c_2012, c_2013, c_2014, c_2015, c_2016, c_2017, c_2018, c_2019)
conn.close()

# plot-ის საშუალებით გამოისახება თუ როგორ შეიცვალა 2008-დან 2019-ის ჩათვლით გამოსულ ფილმთა რაოდენობა
x_points=[2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
y_points=[c_2008, c_2009 , c_2010, c_2011, c_2012, c_2013, c_2014, c_2015, c_2016, c_2017, c_2018, c_2019]
plt.plot(x_points, y_points)
plt.show()