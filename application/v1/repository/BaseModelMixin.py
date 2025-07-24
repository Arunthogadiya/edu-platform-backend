class BaseModelMixin:
    """
    A mixin that provides methods to serialize to/from JSON,
    update attributes from a dict, and standard __repr__, __eq__, and __hash__ implementations.
    """

    def to_json(self):
        """
        Return a dictionary representation of the model instance.
        Iterates over the table columns defined in the SQLAlchemy model.
        """
        return {col: getattr(self, col) for col in self.__table__.columns.keys()}

    @classmethod
    def from_json(cls, json_data):
        """
        Create an instance of the model from a dictionary (JSON).
        
        :param json_data: Dictionary containing keys that match the model's columns.
        :return: An instance of the model with attributes set from the dict.
        """
        instance = cls()
        for col in cls.__table__.columns.keys():
            if col in json_data:
                setattr(instance, col, json_data[col])
        return instance

    def update_from_dict(self, data_dict):
        """
        Update the model instance's attributes from a dictionary.
        
        :param data_dict: Dictionary with keys matching the model's columns.
        """
        for key, value in data_dict.items():
            if key in self.__table__.columns.keys():
                setattr(self, key, value)

    def __repr__(self):
        """
        Provide a simple string representation of the model instance.
        Shows the class name and the primary key.
        """
        pk = getattr(self, 'id', None)
        return f"<{self.__class__.__name__} id={pk}>"

    def __eq__(self, other):
        """
        Define equality: two instances are equal if they are of the same type and have the same primary key.
        """
        if isinstance(other, self.__class__):
            return getattr(self, 'id', None) == getattr(other, 'id', None)
        return False

    def __hash__(self):
        """
        Provide a hash based on the model's class and primary key.
        This makes the model usable in sets and as dict keys.
        """
        return hash((self.__class__, getattr(self, 'id', None)))
