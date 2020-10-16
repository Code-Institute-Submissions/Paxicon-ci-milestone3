# "Bugbears & Bailiffs" - A D&D Fifth Edition Character Vault

The Dungeons and Dragons web-community has been on a massive expansion over the past few years, with playgroups both livestreaming their sessions, releasing episodic content online in the forms of podcasts and vlogs, extensive work from the publisher Wizard's of the Coast to engage fans in dialogue to discuss potential rules-changes and rule-expansions. Sites such as DnDbeyond and roll20.net provide rules and in the latter case full experiences in playing games online.

This Flask web-app is designed to be accessed by subsections of this audience, to provide a secure way of storing character-sheet data online and to access it for quick "checks" (´Dice-throws). More broadly, the app was a way for me to experiment with noSQL, login-auth systems, JWT-token based timed password retrieval, server-side formhandling and a variety of other standard features that should be present and available in a modern web-app.

The project uses several flask-extensions, as the Flask eco-system to a large degrees suffers from a touch too much overconnectedness there's a lot of content in
requirements.txt - All entries will be detailed at the bottom under the "Technologies used" section, with relevant links to documentation.

## Table of contents:

1. [Introduction](#1-introduction) \
   1.1) [UX design](#1-1-ux-design) \
   1.2) [Features](#1-2-features) \
   1.3) [User stories](#1-3-user-stories) \
   1.4) [Wireframes](#1-4-wireframes) \
   1.5) [What to add in the future?](#1-5-what-to-add-in-the-future)
2. [Testing & Process](#2-testing-and-process) \
   2.1) [Extensions used](#2-1-extensions-used) \
   2.1.1) [Flask-Login](#2-1-1-flask-login) \
   2.1.2) [Flask-Mongoengine & Flask-WTF](#2-1-2-flask-mongoengine-and-flask-wtf) \
   2.1.3) [Flask-Mail & Py-JWT](#2-1-3-flask-mail-and-py-jwt) \
   2.2) [Version control](#2-2-version-control) \
   2.2.1) [User-Auth](#2-2-1-user-auth) \
   2.2.2) [CRUD-input](#2-2-2-crud-input) \
   2.2.3) [frontend-design](#2-2-3-frontend-design) \
   2.2.4) ['master' branch](#2-2-4-master-branch)
3. [Deployment and installation](#3-deployment-and-installation) \
   3.1) [Deployment](#3-1-deployment) \
   3.2) [Installation](#3-2-installation) \
   3.2.1) [Config variables](#3-2-1-config-variables)
4. [Technologies used](#4-technologies-used)

# 1 Introduction

The B&B Character Vault is a web-app using MongoDB and jQuery to produce an interactive character-sheet for Dungeons & Dragons, with included support for basic dice-rolls. I will not expand on the rules
of D&D here, as it is irrelevant to the purpose of the app: demonstrating knowledge of how to use MongoDB in web-development as a NoSQL database-option. The topic was simply selected because the character
sheet provided an interesting schema to try to reproduce in J(B)SON format: a character-sheet is made up of multiple overlapping and interconnected data-points that all interact, much like a JSON-object can nest
multiple objects with their own keys inside.

Being a player of the game, I am also somewhat plugged into the player-community, so designing UX from that point of view made the design interesting to consider. In the following section, I'll discuss the user-stories and intended uses of the site.

## 1 1 UX design

I had three concepts in mind when drawing up the design of the UX for the project. First, I wanted a secure user-auth process, allowing users to administer their own entries and to ensure ownership of database entries were tied directly to users. Second, I wanted a relatively open schema-design since the game rules of D&D by design is modular and expandable. Three, I wanted to include the feature of a simple dice-roller,
to make the sheet an option for gamers who now perhaps play through Discord or other online-means where physical dice might not always be available or accessible the way they would be around a table.

Visually, I went for a "less is more" approach, I wanted unobtrusive and clear access to data over ornate design. I wanted the sheet to be above all-else readable and searchable, making it much faster for the player to get access to the data he's saved.

## 1 2 Features

The app features:

- _A secure authentication system based on sessioning, built on the Flask-Login extension, that links document-ownership to a users registered account and bars others from deleting it._
- _A safe way to reset your password and retrieve ownership of your account, using a timed JWT-token method and server-side mailing provided by Flask-mail._
- _Account management features, such as display-name updating, account deletion with cascading deletion of registered characters if the owner is removed._
- _A front-end for adding documents to the database, using the pre-defined "User" and "char" schemas, using the MongoEngine ODM._
- _A means of accessing database information through queries, either by ownership (profile.html), sorted alphabetically by collection (characters.html) and to access the data contained in each entry through templates (char_profile.html)_
- _A suitable front-end presentation of a character-sheet as you might carry in a none-digital format to a gaming session, complete with jQuery-written javascript to handle dice-rolling and calculating derived statistics._

## 1 3 User stories

- _A user would want to keep their sheet stored securely: The user-auth process ensures that only the owner, who created a document in the database, can delete it._

- _A user might want to change their display-name, for a variety of reasons. Profile.html allows the user to manage this aspect of their own account-entry at will._

- _A user might want to use this digital representation instead of a paper character sheet. The user can perform most normal 'check' dice-rolls directly with a single click and get their results returned straight away._

- _A user might want to delete a character-sheet, this can be done inside their profile. The user manages his own documents from the profile view._

- _A user might want to delete their account. The user is informed that this will delete all their character-entries from the database, before confirming, ensuring transparency in how their data is handled and allows the user to opt-out of the app at any time._

- _A group of players might want a central, accessible place to store their character sheets inbetween sessions, for sharing. The app allows them to centralize and use the list to compare sheets with each other._

## 1 4 Wireframes

[Wireframe PDF](/wireframes/Milestone-3-Bugbears-and-Bailiffs.pdf)

## 1 5 What to add in the future?

I have a lot of items I'd like to add in the future:

- _A character-edit function that prepopulates a version of addchar.html for swift, easy editing of submitted characters._

- _An admin interface, allowing superusers to perform database actions for all users without the need for accessing Mongo directly._

- _A planned feature that had to be cut was allowing players to add their own ability-list and equipment, a highly modular dict-object with nested objects for each entry would
  have to be added and it was not feasible to complete in time for my deadline. This will be completed post-submission in a separate branch._

# 2 Testing and Process

My general testing process was manual testing, involving friends and colleagues as volunteer-testers. A form was handed to all volunteer-testers, asking them to fill in a small report for any issue that they noted and submit it to me either through Discord or Email. I handled these 'tickets' as they appeared, but in general it mostly involved display-issues that are discussed more in detail in 2.2.3) front-end design.

Since this was my first full-stack project and first experience with Flask, I decided the process would have to be more structured than my approach to the two earlier Milestones. To wit, I first selected my feature-set, then took a look through the Flask extension eco-system to find suitable tasks for what I had in mind. Once my tools were selected, I structured the production and testing work-flow to one section of features at a time and isolated work on them into their own Git branches. Once a feature set was complete and functional enough to move on, I merged to master and branched the next feature-set and so on. Before discussing each branch, I'll begin by discussing the extensions used.

## 2 1 Extensions used

I elected to chose a core set of extensions to provide the features I required: Flask-Login for handling sessions, Flask-Mongoengine as an ODM for handling my calls to Mongo, Flask-WTForm to provide both server-side and frontend validation of forms, Flask-Mail for sending passwords. I'll discuss the testing and implementation process of each below.

### 2 1 1 Flask-Login

[Flask-Login](https://flask-login.readthedocs.io/en/latest/) is a simple extension handling the basic tasks of session-management, but is unopinionated on database choice and design decisions. It is just a simplifying tool for handling logging users in and out and managing a User object. I had written a Flask-Login style User-object early in the process and grew to appreciate the extension, so after the revert I kept the extension to handle this task, while deferring security to werkzeug.

Implementation of the Flask-Login extension was largely straight-forward and uneventful, until I reached the password-reset functionality I had planned. Resetting passwords
kept resulting in invalid passwords, even though it was clear from observing the DB that new hashes of the password were being saved. I debugged by a few print-statements and
eventually found that the password being saved was invariably an empty string. Further trouble-shooting located the issue to a combination of two factors: the way the User-object had been set up using MongoEngine as a Document instead of a DynaMicDocument caused issues with updating values that were not passed through WTF-form validation - But if they were passed to WTF-form, the server-side validation would invariably fail due to the User-object being a strict schema, which caused a write-error because WTF-form passes a validation-key for its CSRF-protection. (I think the lesson here is something about too many cooks and a broth...)

In the end the issue was resolved amicably through redefining the User object as a dynamic object and rewriting the password-reset as a simple "request.form.get" for that view.
I consoled myself that to access that view at all, a user would have had access to a registered email's inbox within the last 60 minutes, so while the code is inelegant in this regard it is still acceptable from a user-security standpoint.

### 2 1 2 Flask-Mongoengine and Flask-WTF

[Flask-Mongoengine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/) and [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) were selected as a package, because of their interoperable features, that is to say Flask-WTF can handle and produce input-forms for database-document style objects created with the Mongoengine schema-model.
This allows for quick prototyping of I/O forms, which was valuable early in the process when I was working to produce many variants on user registration, login and password reset forms.
As the work progressed, I grew to appreciate both extensions more deeply. MongoEngine as an ODM provides structured schema-based approaches to Mongo's document-model, Flask-WTF provides highly customizable form-creation options that lets you pass frontend validation requirements with the object itself (As well as CSS classes and attributes like 'type' and 'label' etc) with integrated server-side validation.

While the bug occured later in the process, as I defined the char-collection, I will add that I did run into issue with using Flask-WTF a little too liberally: When producing prototypes of addchar.html, I iterated over a very long model-object with multiple nested objects called CharInput (Located in charsheets.py) while testing. Due to a mistake I made in the process of defining the embedded documents used to nest several sub-forms, earlier entries in the "char" collection of my database contain upwards of 5 separate csrf_token keys nested in each other.

![Multiple CSRF tokens](/wireframes/csrf_tokens_multiples.png)

This was fixed later in the process, by redefining the sub-forms embedded in CharInput as "Form" objects instead of FlaskForm', a sub-object of the Flask-WTF extension that requires csrf-validation before validation. That is to say, the error occured because the embedded forms were requiring separate validation-tokens. Newly saved entries now only contain the single csrf_token, which I've chosen to save with the database a sort of 'stamp of approval', to ensure all entries have been validated. Older entries to the database do not need updating because the data used for the token is minimal and the user is never aware of the excess keys, nor do they impede functionality of the app.

![Fixed, single CSRF token](/wireframes/csrf_token_singular.png)

Another reason I elected to use Flask-WTF is its security features of escaping input if not otherwise specified. To test this and ensure it was functional, I asked a friend to perform a simplistic javascript XSS-insertion on the /addchar route:
![XSS-test](/wireframes/xss-testing.png)
_(Username cropped to protect the innocent!)_

All entries tested were correctly escaped.

### 2 1 3 Flask-Mail and Py-JWT

[Flask-Mail](https://pythonhosted.org/Flask-Mail/) and [Py-JWT](https://pyjwt.readthedocs.io/en/latest/) were both part of my attempt to provide secure, if basic, user-auth and account management. Flask-Mail provides the ability to send and process emails through Flask and Py-JWT provides JSON web-token encoding. I originally added both of these solely for the password-reset functionality. The flow is as follow:

_User requests a password reset email -> Flask-Mail uses Py-JWT to generate a time-limited token and passes it as an anchor href-argument in a HTML-mail template that is sent to the users registered email -> The user checks their in-box and clicks the link. If the token is active, that is to say the request was made in the last 60 minutes, an input-form is shown for the user to reset their password (If more than 60 minutes have passed, the token is inert and a redirect occurs with flash message) -> The user inputs a new password that is hashed and is logged in -> MongoEngine updates the new password in the User-object. The user can now use their new password to login._

There were no real issues in testing or implementing these two extensions (See under the Flask-Login section to see a bug I thought was caused by the JWT-token, but was actually
unrelated to the mailing process itself) - I simply registered a no-reply adress to a domain I own, got the server port-information, then passed the required configs into my environment variables. I tested the two mailer-forms and concurred they were functional.

![Mail-testing screenshot](/wireframes/about-mail-test.png)

## 2 2 Version control

The work-flow for this project was separated into three separate stages, with a 'master' branch merge at the end of each phase of design.

### 2 2 1 User-Auth

This branch originally began using an extension named [Flask-User](https://flask-user.readthedocs.io/en/latest/), because it contained the tools I needed for a functional user-auth system namely: managing sessions, MongoDB compatibility, pre-integrated form-based password reset and so forth. However it became clear as work progressed that much of Flask-User was not as well-documented as I had hoped and many of its features were implemented in a manner I did not feel were very accessible to customization. In the end, I reverted to a previous version and lost quite a few days of work. I then rewrote the login and auth system as detailed in the section above.

Once I had a functional system that allowed users to login, logout and reset their password automatically, I cleaned up unused extensions and dependencies remaining after Flask-User, updated my requirements.txt and merged to the master.

### 2 2 2 CRUD-input

This branch was where I created the Char object that is used to represent the character-sheet. Designing the document-schema was difficult, due to my own misunderstandings of the extensions used to provide the input (Flask-WTF) and the purpose of the ODM (Flask-MongoEngine) and tried a rigid, Document model, imposing a strict schema. As the design evolved, I realised where I had complicated matters needlessly for myself and a new, better design emerged. I redefined the character-sheet object as follows:

- A Char-object is a dynamic document, not a static document. In the context of using MongoEngine for MongoDB queries, what this means is that the document-schema is more fluid and allows for keys and values to vary between document-instances inside of a collection.

- A Char-object consists of layers. In the outermost layer is a reference to the creating user, with a key of Owner and a value of the users own MongoDB object-ID. At its core, this is the only truly required field: A Char-object must have a direct object-id reference to its user, because to maintain a clean database without dangling references, the Owner key is used to deal with cascading deletion rules.

- The Char-object is defined in charsheet.py in order to maintain code-readability. The nested structure means that the object contains embedded documents, that are also defined in that file as Flask-WTF form-models. The actual user-input is handled by one such form called CharInput, which is saved as a nested object with a key of "content" alongside the Owner in the document.

After redefining the main object with these rules and rewriting the code to be more dynamic, I was able to produce a functional prototype allowing users to add and delete their own characters and administer this from a protected profile page. As mentioned above, to ensure database integrity, cascading deletion rules were set in place and tested: If a user deletes their account from the profile, all Char-objects they are listed as owners of are also deleted. Once I had ensured that creating, reading, updating and deleting documents were all functional, I merged with the master.

### 2 2 3 frontend-design

Once the main backend functions were functional and general proof-of-concept of CRUD was finished, I focused on implementing my visual design. I elected to go for a bright, clean style with a focus on responsiveness and readability, as the app is designed with mobility in mind (A replacement for a paper-document should be as easy to bring with you as a paper document!). While the project began using [Materialize](https://materializecss.com/) as its frontend framework, I switched to [Bootstrap](https://getbootstrap.com/) due to some issues with Flask-WTF's widgets that made the Bootstrap class-based form styling method more appealing. I noticed some slight issues getting the bootstrap-grid to cooperate and responsiveness was lagging behind on smaller screens.

When submitting the project for peer-review, an immensely embarassing bug was uncovered by one of my fellow students: When doing the switch from Materialize to Bootstrap, I had accidentally removed the viewport <meta> tag from base.html! This error was corrected and the responsive design instantly became much more fluid and visually pleasing.

JavaScript was highly limited in the project, by choice. [jQuery](https://jquery.com/) was used to write the script charProfile.js, only used on char_profile.html. The script makes an AJAX-request for a JSON copy of the relevant character-document and uses it to provide interactive dice-rolls as well as to populate certain fields that are derived from other statistics the user has already submitted to the database. The only other JS file is index.js, which provides simple functionality for certain bootstrap components as needed.

### 2 2 4 'master' branch

After merging frontend-design to the main branch, I focused my last week on testing, peer-review and cleaning up extraneous code.

# 3 Deployment and installation

This section summarizes the experience of deploying the app to Heroku, followed by installation instructions including required config-variables.

## 3 1 Deployment

The deployment was not as smooth as I had hoped, due to my own negligence. I had failed to provide a crucial config-variable, port, before deploying which caused the app to crash on load repeatedly. Once I realised my mistake, I manually added a port variable, fixed up the procfile and redeployed and the app has worked since. The only other thing of note is that I used the Heroku github deploy-flow instead of through the CLI, which I've done on minor projects of my own before.

## 3 2 Installation

Requirements to install and run the app locally:

1. Clone the repository and download it locally.
2. Create a file named env.py. This is where you'll store your config-variables when running the code locally.
3. Activate the virtual environment. For windows computers, the simplest way to do so is to type "Scripts/activate" from the command line in the main project folder, this runs a batch-script that activates the virtual environment. For [Mac OS](https://sourabhbajaj.com/mac-setup/Python/virtualenv.html) and Linux([Ubuntu](https://www.liquidweb.com/kb/creating-virtual-environment-ubuntu-16-04/) and [Debian](https://linuxconfig.org/how-to-set-up-a-python-virtual-environment-on-debian-10-buster)), I defer to the documentation
   for Python for those operating systems, beyond the links above.
4. Once env.py is populated with your environment variables, launch a terminal inside the main folder and type: "pip install -r requirements.txt" to install all extensions. Please note that it is _very_ unadvisable to run this command outside of a virtual environment, so ensure you've activate it before the command is issued. Note that this command is for installing and running the app locally on _windows_. If running on Mac OS and Linux, please refer to the links above or the Python/PIP documentation for your OS of choice.
5. Now that all dependencies are installed, launch the app by typing python app.py in the terminal, from the root-folder of the app.

### 3 2 1 Config variables

The following variables must be configured in the environment you're running the app in. If as in our example above you're running the code locally, I recommend you simply create
an env.py file, as in my instructions above.

- 'PORT' = The port used by Flask to serve HTTP requests. For more on configuring environment variables for Flask, please refer to the [documentation](https://flask.palletsprojects.com/en/1.1.x/config/).

- "MONGODB_DB" = The name of the database you're accessing.
- "MONGODB_HOST" = Your MongoDB URI-string.
- "SECRET_KEY" = An alphanumeric/random bit key used to secure multiple security features offered by Flask, as well as Py-JWT. I refer you to Flasks own [documentation](https://flask.palletsprojects.com/en/1.1.x/config/) on how to set it up correctly.

The folllowing config variables are used by the Flask-Mail extension. While any e-mail you can provide proper SMTP-server credentials too will work, I would caution against using gmail and/lr as your mailer, due to security features meant to discourage spam-bots. _Using gmail as your app-mailer will require you to disable two-step verification and other security features!_ For more details and an excellent article, please follow this [link](https://medium.com/analytics-vidhya/send-email-with-gmail-python-and-flask-1810c25cf5f5)

- 'MAIL_SERVER' = An SMTP server URI from your email-provider.
- 'MAIL_PORT' = The port used by your providers server. Refer to your provider to get the correct value for this variable.
- 'MAIL_USERNAME' = Login credentials for your mailer-account.
- 'MAIL_PASSWORD' = Login credentials for your mailer-account.

# 4 Technologies used

As I have discussed the technologies more in depth earlier in the text, during the testing-writeup I will endeavour to just briefly summarize and provide links to documentation.

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) itself provides the web-framework, the Jinja HTML-engine, werkzeug password hashing and the dev-server being used to run the app in its current state.

- [Flask-MongoEngine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/) provides database integration, ODM and some form-generation.

- [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) provides an integrated solution for managing form validation, form-generation and defining MongoEngine compatible schemas.

- [Flask-Mail](https://pythonhosted.org/Flask-Mail/) & [Py-JWT](https://pyjwt.readthedocs.io/en/latest/) provide mailing services as well as a second layer of account-security, crucial to allowing users to self-manage their account..

- [JQuery](https://jquery.com/) and [Bootstrap](https://getbootstrap.com/) provided frameworks for creating visually pleasing designs and interactive elements through JavaScript.

- For writing code, I used primarily Visual Studio Code as my IDE, with version-control handled through the Github CLI and VSC Github integration extension.
