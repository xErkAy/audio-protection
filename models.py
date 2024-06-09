from dataclasses import dataclass


@dataclass
class Music:
    id: int
    name: str
    password: str
    public_key: bytes
    private_key: bytes


@dataclass
class Person:
    id: int
    full_name: str
    passport: str
    hash: str
