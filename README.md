# django-documentregister
A document registration system built in the Django framework

This project is inspired by working for companies that use google documents and end up with thousands of documents in unstructured folders and no way to reference a particular document.  It is a very simple app built in django that allows you to register a document and receive a document code based on the document type and a numbering system.

e.g. if you are registering a Functional Requirements Document you may get the code FRD00001 which you can then use in the document title on google docs.

I have put the app in Docker so running it in development mode is as easy as

```sh
docker-compose run documentregister setuplocaldb
docker-compose up -d documentregister
```

This is a work in progress and due to using Postgres full text search (I will replace this with elasticsearch eventually) requires django >=1.10
