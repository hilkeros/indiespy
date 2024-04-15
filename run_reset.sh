rm -f "db.sqlite3"

# run the migrations
python manage.py makemigrations
python manage.py migrate

#create the superuser
echo "from users.models import CustomUser; CustomUser.objects.create_superuser('hilkeros', 'hilke@redbrickrecords.ch', 'somepassword')" | python manage.py shell
