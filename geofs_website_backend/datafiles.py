from typing import TypedDict, Literal
from jsonschema import Draft202012Validator


###############################################
#  Classes for type hinting the dictionaries  #
###############################################

DatafileKeys = Literal[
    "gi_jahrgaenge",
    "gi_praesidienste",
    "gi_termine",
    "gi_rollen",
    "gi_erstiwoche",
    "gi_erstiwochenende",
    "gi_stundenplan",
    "geoloek_praesidienste",
    "geoloek_termine",
]


class Datafile(TypedDict):
    data: str
    template: str
    schema: str
    schema_validator: Draft202012Validator | None


class DatafileDict(TypedDict):
    gi_jahrgaenge: Datafile
    gi_praesidienste: Datafile
    gi_termine: Datafile
    gi_rollen: Datafile
    gi_erstiwoche: Datafile
    gi_erstiwochenende: Datafile
    gi_stundenplan: Datafile
    geoloek_praesidienste: Datafile
    geoloek_termine: Datafile


class Otherfile(TypedDict):
    data: str
    template: str


class OtherfileDict(TypedDict):
    foto_gi: Otherfile
    news_template: Otherfile
    news_readme: Otherfile
    jobs_template: Otherfile
    jobs_readme: Otherfile


######################
#  The dictionaries  #
######################

DATAFILES: DatafileDict = {
    "gi_jahrgaenge": {
        "data": "data/gi/studium/jahrgaenge.json",
        "template": "data_templates/data/gi/studium/jahrgaenge.json",
        "schema": "schemas/jahrgaenge.schema.json",
        "schema_validator": None
    },
    "gi_praesidienste": {
        "data": "data/gi/start/praesidienste.json",
        "template": "data_templates/data/gi/start/praesidienste.json",
        "schema": "schemas/praesidienste.schema.json",
        "schema_validator": None
    },
    "gi_termine": {
        "data": "data/gi/start/termine.json",
        "template": "data_templates/data/gi/start/termine.json",
        "schema": "schemas/termine.schema.json",
        "schema_validator": None
    },
    "gi_rollen": {
        "data": "data/gi/fachschaft/rollen.json",
        "template": "data_templates/data/gi/fachschaft/rollen.json",
        "schema": "schemas/rollen.schema.json",
        "schema_validator": None
    },
    "gi_erstiwoche": {
        "data": "data/gi/erstsemester/erstiwoche.json",
        "template": "data_templates/data/gi/erstsemester/erstiwoche.json",
        "schema": "schemas/erstiwoche.schema.json",
        "schema_validator": None
    },
    "gi_erstiwochenende": {
        "data": "data/gi/erstsemester/erstiwochenende.json",
        "template": "data_templates/data/gi/erstsemester/erstiwochenende.json",
        "schema": "schemas/erstiwochenende.schema.json",
        "schema_validator": None
    },
    "gi_stundenplan": {
        "data": "data/gi/erstsemester/stundenplan.json",
        "template": "data_templates/data/gi/erstsemester/stundenplan.json",
        "schema": "schemas/stundenplan.schema.json",
        "schema_validator": None
    },
    "geoloek_praesidienste": {
        "data": "data/geoloek/praesidienste.json",
        "template": "data_templates/data/geoloek/praesidienste.json",
        "schema": "schemas/praesidienste.schema.json",
        "schema_validator": None
    },
    "geoloek_termine": {
        "data": "data/geoloek/termine.json",
        "template": "data_templates/data/geoloek/termine.json",
        "schema": "schemas/geoloek_termine.schema.json",
        "schema_validator": None
    }
}

OTHER_FILES: OtherfileDict = {
    "foto_gi": {
        "data": "data/gi/fachschaft.jpg",
        "template": "data_templates/data/gi/fachschaft.jpg"
    },
    "news_template": {
        "data": "data/gi/news/2020-12-31_welcome.html",
        "template": "data_templates/data/gi/news/2020-12-31_welcome.html"
    },
    "news_readme": {
        "data": "data/gi/news/readme.txt",
        "template": "data_templates/data/gi/news/readme.txt"
    },
    "jobs_template": {
        "data": "data/gi/jobs/2024-12-31_ifgi.html",
        "template": "data_templates/data/gi/jobs/2024-12-31_ifgi.html"
    },
    "jobs_readme": {
        "data": "data/gi/jobs/readme.txt",
        "template": "data_templates/data/gi/jobs/readme.txt"
    }
}
