import sqlite3


class Database:

    def get_link(self, **kwargs) -> list:
        self._open_connection()
        params = []
        for param in list(kwargs.keys()):
            params.append(f'{param}={kwargs[param]}')
        query = f'SELECT * FROM person_music WHERE {" AND ".join(params)} INNER JOIN person ON person_music.person_id=person.id INNER JOIN music ON person_music.music_id=music.id'
        self._cursor.execute(query)
        result = self._cursor.fetchone()
        self._close_connection()
        return [i for i in result]

    def link_music_to_person(self, music_id: int, person_id: int) -> list:
        self._open_connection()
        self._cursor.execute('''
            INSERT INTO person_music (music_id, person_id) VALUES (?, ?)
        ''', (music_id, person_id,))
        self._connection.commit()
        self._close_connection()

    def is_link_exists(self, full_name: str, passport: str, music_name: str):
        self._open_connection()
        self._cursor.execute('''
            SELECT *
            FROM person_music
            INNER JOIN person ON person_music.person_id=person.id
            INNER JOIN music ON person_music.music_id=music.id
            WHERE person.full_name = ? AND person.passport = ? AND music.name = ?
        ''', (full_name, passport, music_name,))
        result = self._cursor.fetchone()
        self._close_connection()
        return True if result is not None else False

    def is_person_exists(self, hash_: str) -> bool:
        self._open_connection()
        self._cursor.execute('''
            SELECT *
            FROM person
            WHERE hash = ?
        ''', (hash_,))
        result = self._cursor.fetchone()
        self._close_connection()
        return True if result is not None else False

    def is_music_exists(self, name: str) -> bool:
        self._open_connection()
        self._cursor.execute('''
            SELECT *
            FROM music
            WHERE name = ?
        ''', (name,))
        result = self._cursor.fetchone()
        self._close_connection()
        return True if result is not None else False

    def get_person(self, hash_: str) -> list:
        self._open_connection()
        self._cursor.execute('''
            SELECT id, full_name, passport, hash
            FROM person
            WHERE hash = ?
        ''', (hash_,))
        result = self._cursor.fetchone()
        self._close_connection()
        return [i for i in result]

    def get_music(self, name: str) -> list:
        self._open_connection()
        self._cursor.execute('''
            SELECT id, name, password, public_key, private_key
            FROM music
            WHERE name = ?
        ''', (name,))
        result = self._cursor.fetchone()
        self._close_connection()
        return [i for i in result]

    def create_person(self, hash_: str, full_name: str, passport: str):
        self._open_connection()
        self._cursor.execute('''
            INSERT INTO person (hash, full_name, passport) VALUES (?, ?, ?)
        ''', (hash_, full_name, passport,))
        self._connection.commit()
        self._close_connection()

    def add_music(self, name: str, password: str, public_key: bytes, private_key: bytes):
        self._open_connection()
        self._cursor.execute('''
            INSERT INTO music (name, password, public_key, private_key) VALUES (?, ?, ?, ?)
        ''', (name, password, public_key, private_key,))
        self._connection.commit()
        self._close_connection()

    def _open_connection(self):
        self._connection = sqlite3.connect('database.db')
        self._cursor = self._connection.cursor()

    def _close_connection(self):
        self._connection.close()
