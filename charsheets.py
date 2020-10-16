# This file contains the models for the document object, CharacterSheets for Dungeons & Dragons. It is kept separated in this file because of separations
# of concerns, as this is a complex data-object with multiple nested arrays and embedded dicts, not to mention subfields for rendering, it would quickly make app.py unreadable.
# The following list of imports various parts of the Flask-MongoEngine and Flask-WTF extensions to make handling database-schema planning and form validation easier,
# as well as some widgets for passing to input fields.

from flask_wtf import *
from user import User
from flask_mongoengine import MongoEngine, Document
from flask_mongoengine.wtf import model_form
from wtforms import *
from wtforms.widgets import ListWidget, CheckboxInput, TableWidget
from wtforms.validators import *
from wtforms import *
from flask_wtf.form import *
from wtforms.fields.html5 import *
from wtforms.widgets.html5 import *

db = MongoEngine()

# This class defines the Char object, the actual document saved to the database. Due to its nature as a DynamicDocument, it does not need to be a stricter schema than this
# and all form-entries are stored as a nested item inside the document labelled "content", the outer layer containing only "content" and "Owner" keys.


class Char(db.DynamicDocument):

    Owner = db.ReferenceField(User, reverse_delete_rule=2)

# Below this polnt are the individual forms that is passed to jinja for rendering and to Flask-WTF for validation on submit.
# All forms given the value of (Form) are contained as nested objects inside the larger CharInput() object, which renders them as part of a single form element.
# Some classes have been commented out, because they are planned for future updates after submission.


class CharAttributesForm(Form):
    class Meta:
        csrf = False
    strength = IntegerField('Strength: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    dexterity = IntegerField('Dexterity: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    constitution = IntegerField('Constitution: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    intelligence = IntegerField('Intelligence: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    wisdom = IntegerField('Wisdom: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    charisma = IntegerField('Charisma: ', [InputRequired(message='Attributes must be entered between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])


class ClassObjForm(Form):
    class Meta:
        csrf = False

    Lvl = IntegerField('Character level: ', [InputRequired(message='Enter a level between 1 and 20!'), NumberRange(
        min=1, max=20, message="This value can only be between 1 and 20!")])
    HitDie = IntegerField('Hit-die: ', [InputRequired(message='This field only takes values between 4 and 12! Enter your class HitDie!'),
                                        NumberRange(min=4, max=12, message="This value can only be between 4 and 12! Enter your class HitDie!")])
    # Abilities is not used currently, but is kept as it is intended to be used for post-submission further work on the app.
    Abilities = HiddenField(db.EmbeddedDocumentField('Abilities: '))
    AttacksPerRound = IntegerField('Attack per round: ', [InputRequired(message='Enter the number of attacks per turn your character can make, unmodified.'), NumberRange(
        min=1, max=10, message="This value can only be between 1 and 10! Consult the Player's Handbook to find your correct attacks-per-round.")])


class SaveForm(Form):
    class Meta:
        csrf = False
    StrSave = BooleanField('Strength saving throw: ')
    DexSave = BooleanField('Dexterity saving throw: ')
    ConSave = BooleanField('Constitution saving throw: ')
    IntSave = BooleanField('Intelligence saving throw: ')
    WisSave = BooleanField('Wisdom saving throw: ')
    ChaSave = BooleanField('Charisma saving throw: ')


# **** IGNORE THE FOLLOWING TWO CLASSES! ****
# They are for a feature I plan to add post-submission and are not to be considered active part of the app at the time of submission. I simply wanted to keep the preparation I had done
# and not have to rewrite it after my grade was finished.

# class AbilityObjForm(Form):
#    class Meta:
#        csrf = False
#    Name = StringField('Ability name: ')


# class AbilitiesForm(Form):
#    class Meta:
#        csrf = False
#    Name = StringField('Name of ability')
#    Description = StringField(' Describe the ability, effects, damage, DCs: ')
#    DieType = IntegerField('Enter the primary dice for this ability: ')
#    Attribute = FormField(CharAttributesForm, "Your character attributes: ")
#    AbilityObjList = FormField(
#        AbilityObjForm, 'Add abilities your character knows here: ')


class SkillsForm(Form):
    class Meta:
        csrf = False
    Athletics = BooleanField('Athletics: ')
    Acrobatics = BooleanField('Acrobatics: ')
    Sleight = BooleanField('Sleight of Hand: ')
    Stealth = BooleanField('Stealth: ')
    Arcana = BooleanField('Arcana: ')
    History = BooleanField('History: ')
    Investigation = BooleanField('Investigation: ')
    Nature = BooleanField('Nature: ')
    Religion = BooleanField('Religon: ')
    AnimalHandling = BooleanField('Animal handling: ')
    Insight = BooleanField('Insight: ')
    Medicine = BooleanField('Medicine: ')
    Perception = BooleanField('Perception: ')
    Survival = BooleanField('Survival: ')
    Deception = BooleanField('Deception: ')
    Intimidation = BooleanField('Intimidation: ')
    Performance = BooleanField('Performance: ')
    Persuasion = BooleanField('Persuasion: ')


class CharInput(FlaskForm):
    Name = StringField('Character name: ', [InputRequired(message='You must provide a name for your new character!'), Length(
        min=1, max=30, message="Character name must be between  and 30 characters long!")])
    CharClass = StringField('Character class: ', [InputRequired(message='You must provide a class!'), Length(
        min=1, max=20, message="Class must be between  and 20 characters long!")])
    Subclass = StringField('Subclass: ', [InputRequired(message='You must provide a subclass!'), Length(
        min=1, max=20, message="Subclass must be between  and 20 characters long!")])
    Race = StringField('Race: ', [InputRequired(message='You must provide a race!'), Length(
        min=1, max=20, message="Race must be between 1 and 20 characters long!")])
    Subrace = StringField('Subrace: ', [InputRequired(message='You must provide a subrace!'), Length(
        min=1, max=20, message="Subrace must be between 1 and 20 characters long!")])
    Appearance = TextAreaField('Appearance: ',  [InputRequired(message='You must provide a short appearance description!'), Length(
        min=1, max=1500, message="Appearance must be between 1 and 1500 characters long!")])
    CharDescription = TextAreaField('Backstory: ', [InputRequired(message='You must provide a short backstory!'), Length(
        min=1, max=2000, message="Backstory must be between 1 and 2000 characters long!")])
    ClassObj = FormField(
        ClassObjForm, 'Character class information: ')
    SkillsObjList = FormField(
        SkillsForm, 'Skills: ')
    AttributeList = FormField(
        CharAttributesForm, 'Character attributes: ')
    SavesList = FormField(SaveForm,
                          'Character saves: ')
