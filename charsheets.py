# This file contains the models for the document object, CharacterSheets for Dungeons & Dragons. It is kept separated in this file because of separations
# of concerns, as this is a complex data-object with multiple nested arrays and embedded dicts, it would quickly make app.py unreadable.

from flask_wtf import *
from user import User
from flask_mongoengine import MongoEngine, Document
from flask_mongoengine.wtf import model_form
from wtforms import *
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import *
from wtforms import *
from flask_wtf.form import *
from wtforms.fields.html5 import *
from wtforms.widgets.html5 import *
db = MongoEngine()

# 'Attributes' are a dict of ints that can range from 1 to 20. All characters have a set of Attributes within this range. This will be passed
# to a jQuery script that will then calculate required values based on these database posts. As those values can be modified so frequently
# and are calculated from the base-attribute value, it is preferable to defer the modifier to the FrontEnd to save on r/w operations.


class CharAttributes(db.EmbeddedDocument):
    strength = db.IntField(min_value=1, max_value=20)
    dexterity = db.IntField(min_value=1, max_value=20)
    constitution = db.IntField(min_value=1, max_value=20)
    intelligence = db.IntField(min_value=1, max_value=20)
    wisdom = db.IntField(min_value=1, max_value=20)
    charisma = db.IntField(min_value=1, max_value=20)

# Saves is a list of booleans, represented in HTML as checkboxes. A save in the context of the rules is either true or false. If true, it adds a bonus based on
# proficiency modifier. As the modifier is calculated on the front-end, the database need only pass True or False to the front-end.


class Saves(db.EmbeddedDocument):
    StrSave = db.BooleanField()
    DexSave = db.BooleanField()
    ConSave = db.BooleanField()
    IntSave = db.BooleanField()
    WisSave = db.BooleanField()
    ChaSave = db.BooleanField()

# 'Skills' is a boolean list, represented in HTML as checkboxes. All characters use the list of skills, so it is a separate embedded document like attributes.
# The user will mark a number of skills as 'proficient' and when the data is passed to the front-end, values will be generated using jQuery
# to accurately calculate the exact numeric value based on proficiency. As this number can value based on modifiers, it is not worth writing exact
# numbers into the DB there, you can get accurate data for our purposes knowing just if it is proficient or not.


class Skills(db.EmbeddedDocument):
    Athletics = db.BooleanField()
    Acrobatics = db.BooleanField()
    Sleight = db.BooleanField()
    Stealth = db.BooleanField()
    Arcana = db.BooleanField()
    History = db.BooleanField()
    Investigation = db.BooleanField()
    Nature = db.BooleanField()
    Religion = db.BooleanField()
    AnimalHandling = db.BooleanField()
    Insight = db.BooleanField()
    Medicine = db.BooleanField()
    Perception = db.BooleanField()
    Survival = db.BooleanField()
    Deception = db.BooleanField()
    Intimidation = db.BooleanField()
    Performance = db.BooleanField()
    Persuasion = db.BooleanField()

# 'Armor' at its core represents an integer that theoretically has neither a maximum nor minimum value. However, numerous
# factors can alter armor-class and it is feasible for a user to want to save multiple 'Armor' objects to represent
# different equipment in a game. Therefore, Armor will be accessible through a EmbeddedDocument
# Field of multiple armor-items in
# the DB, which user can add, update or remove from at will. Some of the more basic rules are incorporated for ease-of-use
# in the form of the required boolean-fields.


class Armor(db.EmbeddedDocument):
    Name = db.StringField()
    CharDescription = db.StringField()
    ACValue = db.IntField()
    HeavyArmor = db.BooleanField()
    MediumArmor = db.BooleanField()
    LightArmor = db.BooleanField()
    Shield = db.BooleanField()


# 'Attacks', much like Armor, are a class of what is essentially a collection of ints. An attack roll is a randomized number
# adding the modifier, the modifier being calculated client-side on the front-end, the object needs only save name, description, dice-type
# and defer all other math operations to the JavaScript component.


class Attacks(db.EmbeddedDocument):
    Name = db.StringField()
    Description = db.StringField()
    DmgDie = db.IntField()


class AttackObjs(db.EmbeddedDocument):
    AttacksList = db.EmbeddedDocumentField(Attacks)

# The ClassObj contains name, description and level as well as an embedded list-item classes as "Ability", a catch-all term for character-abilities
# that the user must specify and keep updated themselves. Proficiency is a function of level/4 +1 (Rounded up) and is thus referred to the front-end which handles
# derived stats.


class Abilities(db.EmbeddedDocument):
    Name = db.StringField()
    Description = db.StringField()
    DieType = db.IntField()
    Attribute = FieldList(db.EmbeddedDocumentField(CharAttributes))


class AbilityObjs(db.EmbeddedDocument):
    AbilityList = db.EmbeddedDocumentField(Abilities)


class ClassObj(db.EmbeddedDocument):

    HitDie = db.IntField()
    Abilities = FieldList(db.EmbeddedDocumentField(AbilityObjs))
    AttacksPerRound = db.IntField()


# Finally, the char object contains StringFields for name, description, looks, an int-field for level and references to all other documents to embed.


class Char(db.DynamicDocument):

    Name = db.StringField()
    CharClass = db.StringField()
    Subclass = db.StringField()
    Appearance = db.StringField()
    CharDescription = db.StringField()
    ClassObj = FieldList(db.EmbeddedDocumentField(ClassObj))
    AttributeList = FieldList(db.EmbeddedDocumentField(CharAttributes))
    SavesList = FieldList(db.EmbeddedDocumentField(Saves))
    SkillsList = FieldList(db.EmbeddedDocumentField(Skills))
    ArmorObjList = FieldList(db.EmbeddedDocumentField(Armor))
    AttacksList = FieldList(db.EmbeddedDocumentField(Attacks))
    AbilityObjsList = FieldList(db.EmbeddedDocumentField(AbilityObjs))
    Owner = db.ReferenceField(User, reverse_delete_rule=2)

# The following forms is what is passed to the Frontend and Jinja to register new Chars.


class CharAttributesForm(FlaskForm):
    strength = IntegerField('Strength: ')
    dexterity = IntegerField('Dexterity: ')
    constitution = IntegerField('Constitution: ')
    intelligence = IntegerField('Intelligence: ')
    wisdom = IntegerField('Wisdom: ')
    charisma = IntegerField('Charisma: ')


class ClassObjForm(FlaskForm):

    Lvl = IntegerField('Character level: ')
    HitDie = IntegerField('Hit-die: ')
    Abilities = HiddenField(db.EmbeddedDocumentField('Abilities: '))
    AttacksPerRound = IntegerField('Attack per round: ')


class SaveForm(FlaskForm):
    StrSave = BooleanField('Strength saving throw: ',
                           widget=CheckboxInput())
    DexSave = BooleanField('Dexterity saving throw: ',
                           widget=CheckboxInput())
    ConSave = BooleanField('Constitution saving throw: ',
                           widget=CheckboxInput())
    IntSave = BooleanField('Intelligence saving throw: ',
                           widget=CheckboxInput())
    WisSave = BooleanField('Wisdom saving throw: ',
                           widget=CheckboxInput())
    ChaSave = BooleanField('Charisma saving throw: ',
                           widget=CheckboxInput())


class AbilityObjForm(FlaskForm):
    Name = StringField('Ability name: ')


class AbilitiesForm(FlaskForm):
    Name = StringField('Name of ability')
    Description = StringField(' Describe the ability, effects, damage, DCs: ')
    DieType = IntegerField('Enter the primary dice for this ability: ')
    Attribute = FormField(CharAttributes, "Your character attributes: ")
    AbilityObjList = FormField(
        AbilityObjForm, 'Add abilities your character knows here: ')


class SkillsForm(FlaskForm):
    Athletics = BooleanField('Athletics: ',
                             widget=CheckboxInput())
    Acrobatics = BooleanField('Acrobatics: ', widget=CheckboxInput())
    Sleight = BooleanField('Sleight of Hand: ', widget=CheckboxInput())
    Stealth = BooleanField('Stealth: ', widget=CheckboxInput())
    Arcana = BooleanField('Arcana: ', widget=CheckboxInput())
    History = BooleanField('History: ', widget=CheckboxInput())
    Investigation = BooleanField('Investigation: ', widget=CheckboxInput())
    Nature = BooleanField('Nature: ', widget=CheckboxInput())
    Religion = BooleanField('Religon: ', widget=CheckboxInput())
    AnimalHandling = BooleanField('Animal handling: ', widget=CheckboxInput())
    Insight = BooleanField('Insight: ', widget=CheckboxInput())
    Medicine = BooleanField('Medicine: ', widget=CheckboxInput())
    Perception = BooleanField('Perception: ', widget=CheckboxInput())
    Survival = BooleanField('Survival: ', widget=CheckboxInput())
    Deception = BooleanField('Deception: ', widget=CheckboxInput())
    Intimidation = BooleanField('Intimidation: ', widget=CheckboxInput())
    Performance = BooleanField('Performance: ', widget=CheckboxInput())
    Persuasion = BooleanField('Persuasion: ', widget=CheckboxInput())


class CharInput(FlaskForm):
    Name = StringField('Character name: ')
    CharClass = StringField('Character class: ')
    Subclass = StringField('Subclass: ')
    Race = StringField('Race: ')
    Subrace = StringField('Subace: ')
    Appearance = TextAreaField('Appearance: ')
    CharDescription = TextAreaField('Backstory: ')
    ClassObj = FormField(
        ClassObjForm, 'Character class information: ')
    SkillsObjList = FormField(
        SkillsForm, 'Check box for proficient skills: ')
    AttributeList = FormField(
        CharAttributesForm, 'Character attributes: ')
    SavesList = FormField(SaveForm,
                          'Character saves: ', widget=ListWidget())
