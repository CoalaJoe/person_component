import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'person'

CONF_FIRSTNAME = 'firstname'
CONF_LASTNAME = 'lastname'
CONF_GENDER = 'gender'
CONF_RELATIONSHIPS = 'relationships'
CONF_RELATIONSHIPS_PERSON = 'person'
CONF_RELATIONSHIPS_RELATION = 'relation'

DEFAULT_GENDER = 'undefined'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.All(cv.ensure_list, [{
        vol.Required(CONF_FIRSTNAME): cv.string,
        vol.Required(CONF_LASTNAME): cv.string,
        vol.Optional(CONF_GENDER, default=DEFAULT_GENDER): cv.string,
        vol.Optional(CONF_RELATIONSHIPS):
            vol.All(cv.ensure_list, [{
                vol.Required(CONF_RELATIONSHIPS_PERSON): cv.string,
                vol.Required(CONF_RELATIONSHIPS_RELATION): cv.string,
            }])
    }])
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    persons = []
    for person_data in config.get(DOMAIN):
        person = Person(person_data.get(CONF_FIRSTNAME), person_data.get(CONF_LASTNAME))
        person.gender = person_data.get(CONF_GENDER)
        if person_data.get(CONF_RELATIONSHIPS):
            print(person_data.get(CONF_RELATIONSHIPS))
        persons.append(person)

    for person in persons:
        hass.states.set('person.%s_%s' % (person.firstname, person.lastname), '')
        hass.states.set('person.%s_%s.firstname' % (person.firstname, person.lastname), person.firstname)
        hass.states.set('person.%s_%s.lastname' % (person.firstname, person.lastname), person.lastname)
        hass.states.set('person.%s_%s.gender' % (person.firstname, person.lastname), person.gender)

    return True


class Person():
    """
    Person and possibly something we could use as an user.
    """

    RELATIONSHIPS_STATES = dict(
        CHILD={
            'opposite': 'PARENT'
        },
        PARENT={
            'opposite': 'CHILD'
        },
        PARTNER={
            'opposite': 'PARTNER'
        },
        WIFE={
            'opposite': 'HUSBAND'
        },
        HUSBAND={
            'opposite': 'WIFE'
        }
    )

    def __init__(self, firstname, lastname):
        """
        :param firstname: 
        :param lastname: 
        """
        self._firstname = firstname
        self._lastname = lastname
        self._relationships = []
        self._gender = None

    @property
    def firstname(self):
        return self._firstname

    @property
    def lastname(self):
        return self._lastname

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        """
        :param gender: The good ol' gender question.... Binary?  
        :return: 
        """
        self._gender = gender

    @property
    def relationships(self):
        return self._relationships

    def add_relationship(self, person, type):
        self._relationships.append({person: person, type: type})
