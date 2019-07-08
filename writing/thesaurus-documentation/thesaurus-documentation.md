# Backend Documentation

This should serve as some basis for the backend of the thesaurus aspect of my senior project!

# Table of Contents

- [Backend Documentation](#Backend-Documentation)
- [Table of Contents](#Table-of-Contents)
- [Schema](#Schema)
  - [ThesaurusEntry](#ThesaurusEntry)
- [Endpoints](#Endpoints)
  - [thesaurus/api/v1](#thesaurusapiv1)
    - [GET](#GET)
      - [Description](#Description)
      - [Success Response](#Success-Response)
  - [thesaurus/api/v1/admin/words](#thesaurusapiv1adminwords)
    - [POST](#POST)
      - [Description](#Description-1)
      - [Headers](#Headers)
      - [Body](#Body)
      - [Requirements](#Requirements)
      - [Error Responses](#Error-Responses)
      - [Success Response](#Success-Response-1)
    - [PUT](#PUT)
      - [Description](#Description-2)
      - [Headers](#Headers-1)
      - [Body](#Body-1)
      - [Requirements](#Requirements-1)
      - [Error Responses](#Error-Responses-1)
      - [Success Response](#Success-Response-2)
    - [DELETE](#DELETE)
      - [Description](#Description-3)
      - [Headers](#Headers-2)
      - [Body](#Body-2)
      - [Requirements](#Requirements-2)
      - [Error Responses](#Error-Responses-2)
      - [Success Response](#Success-Response-3)
  - [thesaurus/api/v1/words/< :WORD >](#thesaurusapiv1words-WORD)
    - [GET](#GET-1)
      - [Description](#Description-4)
      - [Body](#Body-3)
      - [Requirements](#Requirements-3)
      - [Error Responses](#Error-Responses-3)
      - [Success Response](#Success-Response-4)

# Schema

## ThesaurusEntry

This will be the base object for our project with no data outside of the synonyms and antonyms.

```json
{
    "_id": "",
    "word": "",
    "antonyms": {
        "adjective": [],
        "adverb": [],
        "noun": [],
        "verb": []
    },
    "synonyms": {
        "adjective": [],
        "adverb": [],
        "noun": [],
        "verb": []
    }
}
```

_____________________________________

# Endpoints

## thesaurus/api/v1

*Versioning and whatnot*

### GET

#### Description

Small debug/"hello world" endpoint.

#### Success Response

```json
{
    "code": 200,    (OK)
    "message": "Hi! This is the api for Cole Hollant's thesaurus for SPROJ.\nBase entries from words.bighugelabs.com."
}
```

--------------------------------------

## thesaurus/api/v1/admin/words

*Utility endpoints for manipulating the thesaurus collection*

### POST

#### Description

Add entries to the collection!

#### Headers

```json
{
    "adminEmail": "",
    "adminPassword": ""
}
```

#### Body

```json
{
    "word": "",
    "antonyms": {
        "adjective": [],
        "adverb": [],
        "noun": [],
        "verb": []
    },
    "synonyms": {
        "adjective": [],
        "adverb": [],
        "noun": [],
        "verb": []
    }
}
```

#### Requirements

* `adminEmail` and `adminPassword` are valid
* `word`, `antonyms`, and `synonyms` are all non-empty
* `word` is not already present

#### Error Responses

*Admin creds invalid*
```json
{
    "code": 401,    (UNAUTHORIZED)
    "message": "Admin credentials incorrect"
}
```

*Empty fields*
```json
{
    "code": 400,    (BAD REQUEST)
    "message": "Empty fields in request",
    "fields": {
        "word": true || false,
        "antonyms": true || false,
        "synonyms": true || false
    }
}
```

*Word already exists*
```json
{
    "code": 400,    (BAD REQUEST)
    "message": "Word already exists"
}
```

#### Success Response

```json
{
    "code": 201,    (CREATED)
    "message": "Word added",
    "data": {
        "word": ""
    }
}
```

### PUT

#### Description

Update entries in the collection!

#### Headers

```json
{
    "adminEmail": "",
    "adminPassword": ""
}
```

#### Body

```json
{
    "word": "",
    "antonyms": {
        "adjective": [],
        "adverb": [],
        "noun": [],
        "verb": []
    },
    "synonyms": {
        "adjective": [],
        "adverb": [],
        "noun": [],
        "verb": []
    }
}
```

#### Requirements

* `adminEmail` and `adminPassword` are valid
* `word`, `antonyms`, and `synonyms` are all non-empty
* `word` exists in db

#### Error Responses

*Admin creds invalid*
```json
{
    "code": 401,    (UNAUTHORIZED)
    "message": "Admin credentials incorrect"
}
```

*Empty fields*
```json
{
    "code": 400,    (BAD REQUEST)
    "message": "Empty fields in request",
    "data": {
        "word": true || false,
        "antonyms": true || false,
        "synonyms": true || false
    }
}
```

*Word does not already exist*
```json
{
    "code": 400,    (BAD REQUEST)
    "message": "Word does not already exist"
}
```

#### Success Response

```json
{
    "code": 200,    (OK)
    "message": "Word updated",
    "data": {
        "word": ""
    }
}
```

### DELETE

#### Description

Remove entries from the collection!

#### Headers

```json
{
    "adminEmail": "",
    "adminPassword": ""
}
```

#### Body

```json
{
    "word": "",
}
```

#### Requirements

* `adminEmail` and `adminPassword` are valid
* `word` is non-empty
* `word` exists in db

#### Error Responses

*Admin creds invalid*
```json
{
    "code": 401,    (UNAUTHORIZED)
    "message": "Admin credentials incorrect"
}
```

*Empty fields*
```json
{
    "code": 400,    (BAD REQUEST)
    "message": "Word is empty",
}
```

*Word does not already exist*
```json
{
    "code": 400,    (BAD REQUEST)
    "message": "Word does not already exist"
}
```

#### Success Response

```json
{
    "code": 200,    (OK)
    "message": "Word removed",
    "data": {
        "word": ""
    }
}
```

--------------------------------------

## thesaurus/api/v1/words/< :WORD >

*Endpoints for accessing the thesaurus collection*

### GET

#### Description

Access entries in the collection!

#### Body

```json
{
    "word": ""
}
```

#### Requirements

* `word` exists in db
* `word` is non-empty

#### Error Responses

*Word DNE*
```json
{
    "code": 404,    (NOT FOUND)
    "message": "Word not found",
}
```

*Empty fields*
```json
{
    "code": 400,    (BAD REQUEST)
    "message": "Word is empty",
}
```

#### Success Response

```json
{
    "code": 200,    (OK)
    "message": "Success!",
    "data": {
        "word": "",
        "antonyms": {
            "adjective": [],
            "adverb": [],
            "noun": [],
            "verb": []
        },
        "synonyms": {
            "adjective": [],
            "adverb": [],
            "noun": [],
            "verb": []
        }
    }
}
```