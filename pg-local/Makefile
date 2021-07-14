run-db:
	docker run --name local_postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=local_postgres -v ${PWD}/db_data:/var/lib/postgresql/data -d postgres