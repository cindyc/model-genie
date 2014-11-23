from ..base import ArchivableModel

from schematics.types import StringType, NumberType


class Person(ArchivableModel):
    first_name = StringType()
    last_name = StringType()

