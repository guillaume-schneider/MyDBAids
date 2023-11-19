from enum import Enum


class AbstractType(Enum):
    ADDRESS = 1
    CURRENCY = 2
    DATE_TIME = 3
    INTERNET = 4
    LOREM = 5
    PERSON = 6
    PHONE_NUMBER = 7
    BOOLEAN = 8
    INT = 9
    FLOAT = 10
    PRIMARY_ID = 11
    AUTO_ID = 12


AbstractTypeFunctionMatch = {
    AbstractType.ADDRESS: "address",
    AbstractType.CURRENCY: "currency",
    AbstractType.DATE_TIME: "date_time",
    AbstractType.INTERNET: "internet",
    AbstractType.LOREM: "lorem",
    AbstractType.PERSON: "person",
    AbstractType.PHONE_NUMBER: "phone_number",
    AbstractType.PRIMARY_ID: "increment_id",
    AbstractType.AUTO_ID: "auto_id"
}
