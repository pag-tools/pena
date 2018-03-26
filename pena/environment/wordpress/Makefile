download:
	wp core download --version=4.7 --path=wordpress

config:
	# Check values from the setup.sql file
	wp core config --dbname=wordpress --dbuser=wordpress --dbpass=wordpress --path=wordpress

install:
	wp core install --url=example.com --title="Test Page" --admin_user=user --admin_password=pass --admin_email=example@example.com --skip-email --path=wordpress

serve:
	wp server --path=./wordpress/ --port=8081
