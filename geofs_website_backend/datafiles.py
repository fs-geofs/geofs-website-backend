from typing import Literal, TypedDict

from jsonschema import Draft202012Validator

from .envs import CONTENT_PATH

#############################################
#  Stuff for type hinting the dictionaries  #
#############################################

# defines the names of the keys present in the DATAFILES dictionary (for type hinting)
DatafileKeys = Literal[
    "gremien",
    "gi_jahrgaenge",
    "gi_praesidienste",
    "gi_termine",
    "gi_rollen",
    "gi_erstiwoche",
    "gi_erstiwochenende",
    "gi_stundenplan",
    "geoloek_praesidienste",
    "geoloek_termine",
    "geoloek_erstiwoche_geo",
    "geoloek_erstiwoche_loek",
    "geoloek_erstiwoche_2fb",
    "geoloek_organisation",
]

# defines the names of the keys present in the OTHERFILES dictionary (for type hinting)
OtherfilesKeys = Literal[
    "foto_gi",
    "gi_news_template",
    "gi_news_readme",
    "gi_jobs_template",
    "gi_jobs_readme",
    "foto_geoloek",
    "geoloek_news_template",
    "geoloek_news_readme",
    "geoloek_jobs_template",
    "geoloek_jobs_readme",
]


# defines the values in the DATAFILES dictionary (for type hinting)
class Datafile(TypedDict):
    data: str
    template: str
    schema: str
    schema_validator: Draft202012Validator | None


# defines the values in the OTHERFILES dictionary (for type hinting)
class Otherfile(TypedDict):
    data: str
    template: str


# defines the Keys and Values inside the DATAFILES and OTHERFILES dicts (for type hinting
DatafileDict = dict[DatafileKeys, Datafile]
OtherfileDict = dict[OtherfilesKeys, Otherfile]


######################
#  The dictionaries  #
######################

DATAFILES: DatafileDict = {
    "gremien": {
        "data": f"{CONTENT_PATH}/gremien.json",
        "template": "data_templates/data/gremien.json",
        "schema": "schemas/gremien.schema.json",
        "schema_validator": None,
    },
    "gi_jahrgaenge": {
        "data": f"{CONTENT_PATH}/gi/studium/jahrgaenge.json",
        "template": "data_templates/data/gi/studium/jahrgaenge.json",
        "schema": "schemas/jahrgaenge.schema.json",
        "schema_validator": None,
    },
    "gi_praesidienste": {
        "data": f"{CONTENT_PATH}/gi/start/praesidienste.json",
        "template": "data_templates/data/gi/start/praesidienste.json",
        "schema": "schemas/praesidienste.schema.json",
        "schema_validator": None,
    },
    "gi_termine": {
        "data": f"{CONTENT_PATH}/gi/start/termine.json",
        "template": "data_templates/data/gi/start/termine.json",
        "schema": "schemas/termine.schema.json",
        "schema_validator": None,
    },
    "gi_rollen": {
        "data": f"{CONTENT_PATH}/gi/fachschaft/rollen.json",
        "template": "data_templates/data/gi/fachschaft/rollen.json",
        "schema": "schemas/rollen.schema.json",
        "schema_validator": None,
    },
    "gi_erstiwoche": {
        "data": f"{CONTENT_PATH}/gi/erstsemester/erstiwoche.json",
        "template": "data_templates/data/gi/erstsemester/erstiwoche.json",
        "schema": "schemas/erstiwoche.schema.json",
        "schema_validator": None,
    },
    "gi_erstiwochenende": {
        "data": f"{CONTENT_PATH}/gi/erstsemester/erstiwochenende.json",
        "template": "data_templates/data/gi/erstsemester/erstiwochenende.json",
        "schema": "schemas/erstiwochenende.schema.json",
        "schema_validator": None,
    },
    "gi_stundenplan": {
        "data": f"{CONTENT_PATH}/gi/erstsemester/stundenplan.json",
        "template": "data_templates/data/gi/erstsemester/stundenplan.json",
        "schema": "schemas/stundenplan.schema.json",
        "schema_validator": None,
    },
    "geoloek_praesidienste": {
        "data": f"{CONTENT_PATH}/geoloek/praesidienste.json",
        "template": "data_templates/data/geoloek/praesidienste.json",
        "schema": "schemas/praesidienste.schema.json",
        "schema_validator": None,
    },
    "geoloek_termine": {
        "data": f"{CONTENT_PATH}/geoloek/termine.json",
        "template": "data_templates/data/geoloek/termine.json",
        "schema": "schemas/geoloek_termine.schema.json",
        "schema_validator": None,
    },
    "geoloek_erstiwoche_geo": {
        "data": f"{CONTENT_PATH}/geoloek/erstiwoche_geo.json",
        "template": "data_templates/data/geoloek/erstiwoche_geo.json",
        "schema": "schemas/erstiwoche.schema.json",
        "schema_validator": None,
    },
    "geoloek_erstiwoche_loek": {
        "data": f"{CONTENT_PATH}/geoloek/erstiwoche_loek.json",
        "template": "data_templates/data/geoloek/erstiwoche_loek.json",
        "schema": "schemas/erstiwoche.schema.json",
        "schema_validator": None,
    },
    "geoloek_erstiwoche_2fb": {
        "data": f"{CONTENT_PATH}/geoloek/erstiwoche_2fb.json",
        "template": "data_templates/data/geoloek/erstiwoche_2fb.json",
        "schema": "schemas/erstiwoche.schema.json",
        "schema_validator": None,
    },
    "geoloek_organisation": {
        "data": f"{CONTENT_PATH}/geoloek/organisation.json",
        "template": "data_templates/data/geoloek/organisation.json",
        "schema": "schemas/organisation.schema.json",
        "schema_validator": None,
    },
}

OTHER_FILES: OtherfileDict = {
    "foto_gi": {
        "data": f"{CONTENT_PATH}/gi/fachschaft.jpg",
        "template": "data_templates/data/gi/fachschaft.jpg",
    },
    "gi_news_template": {
        "data": f"{CONTENT_PATH}/gi/news/2020-12-31_welcome.html",
        "template": "data_templates/data/gi/news/2020-12-31_welcome.html",
    },
    "gi_news_readme": {
        "data": f"{CONTENT_PATH}/gi/news/readme.txt",
        "template": "data_templates/data/gi/news/readme.txt",
    },
    "gi_jobs_template": {
        "data": f"{CONTENT_PATH}/gi/jobs/2024-12-31_ifgi.html",
        "template": "data_templates/data/gi/jobs/2024-12-31_ifgi.html",
    },
    "gi_jobs_readme": {
        "data": f"{CONTENT_PATH}/gi/jobs/readme.txt",
        "template": "data_templates/data/gi/jobs/readme.txt",
    },
    "foto_geoloek": {
        "data": f"{CONTENT_PATH}/geoloek/fachschaft.jpg",
        "template": "data_templates/data/geoloek/fachschaft.jpg",
    },
    "geoloek_news_template": {
        "data": f"{CONTENT_PATH}/geoloek/news/2020-12-31_welcome.html",
        "template": "data_templates/data/geoloek/news/2020-12-31_welcome.html",
    },
    "geoloek_news_readme": {
        "data": f"{CONTENT_PATH}/geoloek/news/readme.txt",
        "template": "data_templates/data/geoloek/news/readme.txt",
    },
    "geoloek_jobs_template": {
        "data": f"{CONTENT_PATH}/geoloek/jobs/2024-12-31_institute.html",
        "template": "data_templates/data/geoloek/jobs/2024-12-31_institute.html",
    },
    "geoloek_jobs_readme": {
        "data": f"{CONTENT_PATH}/geoloek/jobs/readme.txt",
        "template": "data_templates/data/geoloek/jobs/readme.txt",
    },
}
