from server import db,Course, Professor, Student


a= Professor(name='Natasha' , recapHours=0)
b = Professor(name='Amira' , recapHours=0)
c = Professor(name='Asma' , recapHours=0)
d = Professor(name='Malek' , recapHours=0)
e = Professor(name='Brahim' , recapHours=0)
f = Professor(name='Elizabeth' , recapHours=0)
g = Professor(name='Fadwa' , recapHours=0)
h = Professor(name='Mike' , recapHours=0)
i = Professor(name='Pattie' , recapHours=0)
j = Professor(name='Robert' , recapHours=0)
k = Professor(name='Zied' , recapHours=0)

db.session.add(a)
db.session.add(b)
db.session.add(c)
db.session.add(d)
db.session.add(e)
db.session.add(f)
db.session.add(g)
db.session.add(h)
db.session.add(i)
db.session.add(j)
db.session.add(k)

db.session.commit()
