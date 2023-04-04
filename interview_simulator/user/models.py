# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from interview_simulator.database import (
    Column,
    PkModel,
    db,
    reference_col,
    relationship,
)
from interview_simulator.extensions import bcrypt


class UserFile(PkModel):
    """Resume and Job Description for a user."""

    __tablename__ = "user_files"
    file_name = Column(db.String(128), nullable=False)
    file_content = Column(db.Text, nullable=False)
    upload_date = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="user_files")

    def __init__(self, file_name, file_content, user, **kwargs):
        """
        Initializes a new instance of the UserFile.

        Args:
        - file_name (str): The name of the file.
        - file_content (str): The contents of the file.
        - user (User): The user that uploaded the file.

        Returns:
        - None
        """
        super(UserFile, self).__init__(**kwargs)
        self.file_name = file_name
        self.file_content = file_content
        self.user = user


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """
        Initialize a new instance of Role.

        Args:
        - name (str): The name of the role.

        Returns:
        - None
        """
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """
        Returns a string representation of the Role instance.

        Returns:
        - A string representing the Role instance.
        """
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """
        Returns the hashed password of the User.

        Returns:
        - A string representing the hashed password of the User.
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        Sets the password of the User by generating its hash.

        Args:
        - value (str): The password in plain text that is to be hashed and saved.

        Returns:
        - None
        """
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """
        Verifies whether the password provided matches the hashed password stored for the User.

        Args:
        - value (str): The password in plain text that is to be verified.

        Returns:
        - A boolean value indicating whether the provided password matches the stored hashed password.
        """
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """
        Returns the full name of the User as a string.

        Returns:
        - A string representing the full name of the User.
        """
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """
        Returns a string representation of the User instance.

        Returns:
        - A string representing the User instance.
        """
        return f"<User({self.username!r})>"
