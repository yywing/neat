# neat

Save HTTP flow and make website structure clear.

## docker

```bash
docker-compose build
# make sure env
dokcer-compose up -d

# run migration
docker exec -it api python manage.py migrate
# create user
docker exec -it api python manage.py createsuperuser
```