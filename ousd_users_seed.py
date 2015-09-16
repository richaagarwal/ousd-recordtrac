from public_records_portal import db
from public_records_portal.models import Department, User
from public_records_portal.prflask import app
import csv

def create_liaison(name, email, phone, department_name):
	if name != "" and email != "":
		email = email.lower()
		u = User.query.filter(User.email == email).first()
		if not u:
			u = User(alias = name, email = email, phone = phone, is_staff = True)
			db.session.add(u)
			db.session.commit()
		d = Department.query.filter(Department.name == department_name).first()
		if not d:
			d = Department(name = department_name)
			db.session.add(d)
			db.session.commit()
		if not d.primary_contact_id:
			d.primary_contact_id = u.id
			db.session.add(d)
			db.session.commit()

def create_backup_liaison(name, email, phone, department_name):
	if name != "" and email != "":
		email = email.lower()
		u = User.query.filter(User.email == email).first()
		if not u:
			u = User(alias = name, email = email, phone = phone, is_staff = True)
			db.session.add(u)
			db.session.commit()
		d = Department.query.filter(Department.name == department_name).first()
		if not d:
			d = Department(name = department_name)
			db.session.add(d)
			db.session.commit()
		if not d.backup_contact_id:
			d.backup_contact_id = u.id
			db.session.add(d)
			db.session.commit()


print "Creating users..."

userfile = list(csv.reader(open('ousd_liaisons.csv', 'rb'), delimiter='\t'))
for row in userfile:
	department_name = row[0]
	phone = None
	if len(row) > 4:
		phone = row[4]
	create_liaison(row[2], row[3], phone, department_name)
	# Create backup liaisons
	if len(row) > 6:
		phone = None
		if len(row) > 7:
			phone = row[7]
		create_backup_liaison(row[5], row[6], phone, department_name)
	if len(row) > 9:
		phone = None
		if len(row) > 10:
			phone = row[10]
		create_backup_liaison(row[8], row[9], phone, department_name)
	if len(row) > 12:
		phone = None
		if len(row) > 13:
			phone = row[13]
		create_backup_liaison(row[11], row[12], phone, department_name)

print "Finished!"



