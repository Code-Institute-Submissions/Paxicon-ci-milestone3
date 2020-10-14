# "Bugbears & Bailiffs" - A D&D Fifth Edition Character Vault

The Dungeons and Dragons web-community has been on a massive expansion over the past few years, with playgroups both livestreaming their sessions, releasing episodic content online in the forms of podcasts and vlogs, extensive work from the publisher Wizard's of the Coast to engage fans in dialogue to discuss potential rules-changes and rule-expansions. Sites such as DnDbeyond and roll20.net provide rules and in the latter case full experiences in playing games online.

This Flask web-app is designed to be accessed by subsections of this audience, to provide a secure way of storing character-sheet data online and to access it for quick "checks" (´Dice-throws). More broadly, the app was a way for me to experiment with noSQL, login-auth systems, JWT-token based timed password retrieval, server-side formhandling and a variety of other standard features that should be present and available in a modern web-app.

The project uses several flask-extensions, as the Flask eco-system to a large degrees suffers from a touch too much overconnectedness there's a lot of content in
requirements.txt - All entries will be detailed at the bottom under the "Technologies used" section, with relevant links to documentation.

## Table of contents:

#### 1) Introduction

##### 1.1) UX design

##### 1.2) Features

##### 1.3) Wireframes

##### 1.4) User stories

##### 1.5) What to add in the future?

#### 2) Testing

##### 3) Deployment and installation

##### 3.1) Deployment

##### 3.2) Installation

#### 4) Technologies used

# 1) Introduction

The B&B Character Vault is a web-app using MongoDB and jQuery to produce an interactive character-sheet for Dungeons & Dragons, with included support for basic dice-rolls. I will not expand on the rules
of D&D here, as it is irrelevant to the purpose of the app: demonstrating knowledge of how to use MongoDB in web-development as a NoSQL database-option. The topic was simply selected because the character
sheet provided an interesting schema to try to reproduce in J(B)SON format: a character-sheet is made up of multiple overlapping and interconnected data-points that all interact, much like a JSON-object can nest
multiple objects with their own keys inside.

Being a player of the game, I am also somewhat plugged into the player-community, so designing UX from that point of view made the design interesting to consider. In the following section, I'll discuss the user-stories and intended uses of the site.

## 1.1) UX design

I had three concepts in mind when drawing up the design of the UX for the project. First, I wanted a secure user-auth process, allowing users to administer their own entries and to ensure ownership of database entries were tied directly to users. Second, I wanted a relatively open schema-design since the game rules of D&D by design is modular and expandable. Three, I wanted to include the feature of a simple dice-roller,
to make the sheet an option for gamers who now perhaps play through Discord or other online-means where physical dice might not always be available or accessible the way they would be around a table.

Visually, I went for a "less is more" approach, I wanted unobtrusive and clear access to data over ornate design. I wanted the sheet to be above all-else readable and searchable, making it much faster for the player to get access to the data he's saved.

## 1.2) Features

The app features:

⋅⋅\* _A secure authentication system based on sessioning, built on the Flask-Login extension, that links document-ownership to a users registered account and bars others from deleting it._
..* *A safe way to reset your password and retrieve ownership of your account, using a timed JWT-token method and server-side mailing provided by Flask-mail.*
..\_ *Account management features, such as display-name updating, account deletion with cascading deletion of registered characters if the owner is removed.\*
..\_ _A front-end for adding documents to the database, using the pre-defined "User" and "char" schemas, using the MongoEngine ODM._
..\* _A means of accessing database information through queries, either by ownership (profile.html), sorted alphabetically by collection (characters.html) and to access the data contained in each entry through templates (char_profile.html)_
..\* _A suitable front-end presentation of a character-sheet as you might carry in a none-digital format to a gaming session, complete with jQuery-written javascript to handle dice-rolling and calculating derived statistics._

## 1.2) User stories

.._ *A user would want to keep their sheet stored securely: The user-auth process ensures that only the owner, who created a document in the database, can delete it.*
.._ _A user might want to change their display-name, for a variety of reasons. Profile.html allows the user to manage this aspect of their own account-entry at will._
.._ *A user might want to use this digital representation instead of a paper character sheet. The user can perform most normal 'check' dice-rolls directly with a single click and get their results returned straight away.*
.._ _A user might want to delete a character-sheet, this can be done inside their profile. The user manages his own documents from the profile view._
..\* _A user might want to delete their account. The user is informed that this will delete all their character-entries from the database, before confirming, ensuring transparency in how their data is handled and allows the user to opt-out of the app at any time._

## 1.4) Wireframes

[Wireframe PDF here](wireframes\Milestone 3 - Bugbears & Bailiffs.pdf)

## 1.5) What to add in the future?

I have a lot of items I'd like to add in the future:

..\* _A character-edit button that prepopulates a version of addchar.html for swift, easy editing._
..\* _An admin interface, allowing superusers to perform database actions for all users without the need for accessing Mongo directly._
..\* _A planned feature that had to be cut was allowing players to add their own ability-list and equipment, a highly modular dict-object with nested objects for each entry would have to be added and it was not feasible to complete in time for my deadline. This will be completed post-submission in a separate branch._
