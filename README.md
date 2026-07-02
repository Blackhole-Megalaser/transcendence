*This project has been created as part of the 42 curriculum by tlair, kcolin, cczerwin, lvan-bre, ael-ghaz.*

[![CI](https://github.com/Blackhole-Megalaser/transcendence/actions/workflows/main.yml/badge.svg)](https://github.com/Blackhole-Megalaser/transcendence/actions/workflows/main.yml)

# Description

Transcendence is a **group project (4-5 people)** intended to  boost creativity, self-confidence, adaptability and teamwork skills by creating a real-world webapp as a team. (*Subject version: 21.1*)

Project Repo link: https://github.com/Blackhole-Megalaser/transcendence

# Instructions

## Dependencies

You will need:

- gnumake
- docker with working docker-compose

<br>

Present on school computer: (hopefully the same on all PCs)
- Docker 28.1.1
- Docker Compose 2.36.2
- Python 3.10.12
- Django not installed
- node 12.22.9
- npm 8.5.1
- Tailwind 4.2.4
- Vue/Vite not installed

## Configuration

- `cp .env.example .env`
- Change settings as desired

Make sure to have the **DEBUG** key set to **False** in production

Note: If the .env file doesn't exist, our makefile create one AND generate a secret key for django (**make .env**)

## Running

To build and start the project you can use either:

- `make`
- `make run`
- `make dev`

Then to reach the website:

- `https://localhost:1443/`
- `https://{server_ip_here}:{port}/`

You can replace localhost with the server ip address to access it from outside.

The default port used is **1443**, you can change that in the **EXTERNAL_PORT** variable in your environment file.

# Resources

- Django documentation - https://docs.djangoproject.com/en/6.0/
- Vue documentation - https://vuejs.org/guide/introduction
- Vite documentation - https://vite.dev/guide/
- Tailwind documentation - https://tailwindcss.com/docs/installation/using-vite

**AI was used to produce graphical assets in this project**

# Team Information

## [tlair](https://github.com/La-Fougere) - Product owner

Defines the product vision, prioritizes features, and ensures the project meets user needs.
- Maintains the product backlog.
- Makes decisions on features and priorities.
- Validates completed work.
- Communicates with stakeholders (evaluators, peers).

## [kcolin](https://github.com/logistic-bot) - Technical lead

Oversees technical decisions and architecture
- Defines technical architecture.
- Makes technology stack decisions.
- Ensures code quality and best practices.
- Reviews critical code changes.

## [lvan-bre](https://github.com/Sellith) - Project manager

Facilitates team coordination and removes obstacles.
- Organizes team meetings and planning sessions.
- Tracks progress and deadlines.
- Ensures team communication.
- Manages risks and blockers.

## [ael-ghaz](https://github.com/ael-ghaz) & [cczerwin](https://github.com/Xblugs) - Developer

- Write code for assigned features.
- Participate in code reviews.
- Test their implementations.
- Document their work.

In addition to their roles, everyone in the team is a developer.

# Project Management

We decided to have a weekly meeting to review where we were at and agree on tasks for the following week.

Our first target was to finish the project on the 31st of may, which would give us 5 weeks.

We used a [google sheet](https://docs.google.com/spreadsheets/d/1-unfSmSeZFW78XxymSvcDQVJqaTeYh-l-Ek2GIyEvls/edit?gid=216360315) to agree which project modules we would implement, and roughly track who would be working on it.

Our communication, when not done in person, was mostly through discord.

# Technical Stack

For the frontend, we decided to go with Vue, Vite and Tailwind.

For the backend, Django was used in combination with a Postgresql database.

Vue is made to be easy to learn and Django because it includes many functions like ORM *(see ORM modules for details)* and can do SSR *(Server Side Rendering)* that we wanted to implement initially before putting it aside to make it easier communicate between the frameworks.

# Database Schema

We have the base User table made by Django internally featuring the user base information such as Username, email, staff status etc.

## User Profile

Each User is associated with one UserProfile that contain its own data:

- the amount of nyancoins (our website currency gotten by placing pixels, used to unlocks colors on the /t/place)
- the amount of placeable pixels
- the maximum amount of pixels that can be had at any time for a given user
- the time to regenerate a pixel to put on the canvas
- the unlocked colors (the base plan was to unlock colors by playing/doing various activities)
- current friends
- currently pending friend requests
- unlocked wordlist

Each wordlist is composed of many word items (simple strings).

We intended to have unlockable word lists for the skribbl game, the models are present in the database but currently there's only one list implemented.

## Skribble

When trying to join a game, the SkribblePlayer models gets populated with the username to have a player required fields to play, they get joined in a SkribbleRoom where the magic happens to manage the game state.

We have:
- the turn count
- the round count
- who is drawing
- the current word to draw/guess
- the word history to not have twice the same word in a game
- the timer for the drawing/turn time
- the scores
- the room code (used to join)
- the room name (visible in the lobby)
- is the game/turn started

## Tplace

For the tplace we store each pixel individually with their coordinates x, y, which user put them, the color used and the data of creation/update.

This is queried in the frontend for the canvas initial load.

# Features List

The project feature a pictionnary-like game (skribl.io like), a collaborative canvas (like reddit /r/place) with associated chatrooms.

# Modules

**All of our modules listed below amount for a total of 26pts**

- Web modules for (9) points
- Accessibility and Internationalization modules for (1) points
- User Management modules for (4) points
- Gaming and user experience modules for (7) points
- Devops modules for (2) points
- Modules of choices for (3) points


## Web modules (starting on subject page 12)

### Major: Use a framework for both the frontend and backend

We used Vue + Tailwind for the frontend, and Django for the backend.

We all worked on this module.

### Minor: Use a frontend framework

We used Vue + Tailwind for the frontend.

**lvan-bre** worked on the main site appearance.<br>
**tlair** worked on the tplace feature.<br>
**ael-ghaz** worked on the skribble feature.

### Minor: Use a backend framework

We used Django for the backend.

**kcolin** and **cczerwin** worked on the backend.

### Major: Implement realtime features using WebSockets or similar technology

- Real-time updates across clients.
- Hanle connection/disconnection gracefully.
- Efficient message broadcasting.

This module is necessary to implement our collaborative drawing game properly.

**cczerwin** worked on this module.<br>
**tlair** worked with it for the tplace.<br>
**ael-ghaz** worked with it for the skribble.

### Major: Allow users to interact with other users

- A **basic chat** system (send/receive messages between users).
- A **profile** system (view user information).
- A **friend** system (add/remove friends, see friends list).

This module is important for the social aspect needed for collaborative oriented projects.

**cczerwin** worked on the chat and friend API.<br>
**lvan-bre** worked on the profile page and friend system.<br>
**ael-ghaz** & **tlair** worked on collaborative features.

### Minor: Use an ORM for the database

This is included in Django features, ORM (Object–relational mapping) helps for every interaction with the database making it easier to use.

**kcolin** worked on this module.

### Minor: Real-time collaborative features (shared workspaces, live editing, collaborative drawing, etc.)

The tplace cover this module, it's a collaborative drawing canvas (/r/place like)

**tlair** && **ael-ghaz** worked on this module.

### Minor: Custom-made design system with reusable components, including a proper color palette, typography, and icons (minimum: 10 reusable components).

Thanks to Vue system, all of our components are re-usable, they react to our theme button as well

**lvan-bre** worked on this module.


## Accessibility and Internationalization modules (starting on subject page 13)

### Minor: Support for additional browser

- Full compatibility with at least 2 additional browsers (Firefox, Safari, Edge, etc.).
- Test and fix all features in each browser.
- Document any browser-specific limitations.
- Consistent UI/UX across all supported browsers.

It's important for any kind of website to at least support the most used browsers to maximize our potential reach.

**Everyone** worked on this module.


## User Management modules (starting on subject page 14)

### Major: Standard user management and authentication

- Users can update their profile information.
- Users can upload an avatar (with a default avatar if none provided).
- Users can add other users as friends and see their online status.
- Users have a profile page displaying their information.

This module pairs with the basic interaction module, here focusing on making the actual profiles.

**cczerwin** and **kcolin** worked on this module.<br>
**lvan-bre** connected the front and made the friendlist and profile page.

### Major: Advanced permissions system

- View, edit, and delete users (CRUD).
- Roles management (admin, user, guest, moderator, etc.).
- Different views and actions based on user role.

Django include an admin view system, an admin user can easily add / edit / delete users

It's possible through this interface to give a staff status or a superuser.
- Staff can access the admin panel and browse the database content
- Superuser can interact with anything add/edit/delete

**cczerwin** and **kcolin** worked on this module.


## Gaming and user experience modules (starting on subject page 16)

### Major: Implement a complete web-based game where users can play against each other

- The game can be real-time multiplayer (e.g., Pong, Chess, Tic-Tac-Toe, Card games, etc.).
- Players must be able to play live matches.
- The game must have clear rules and win/loss conditions.
- The game can be 2D or 3D.

We have a collaborative drawing guess (Pictionary like), this is the corresponding module.

**ael-ghaz** worked on this module.

### Major: Remote players — Enable two players on separate computers to play the same game in real-time

- Handle network latency and disconnections gracefully.
- Provide a smooth user experience for remote gameplay.
- Implement reconnection logic.

We also have a collaborative drawing platform (/r/place like), this is the corresponding module.

**tlair** & **ael-ghaz** worked on this module.

### Major: Multiplayer game (more than 2 players)

- Support for three or more players simultaneously.
- Fair gameplay mechanics for all participants.
- Proper synchronization across all clients.

*See above modules*

**ael-ghaz** & **tlair** worked on this module.

### Minor: Implement spectator mode for games

- Allow users to watch ongoing games.
- Real-time updates for spectators.
- Optional: spectator chat.

This module can be easily added to the game since we're already synchronizing clients.

**tlair** worked on this module.


## Devops modules (starting on subject page 18)

### Major: Backend as microservices

- Design loosely-coupled services with clear interfaces.
- Use REST APIs or message queues for communication.
- Each service should have a single responsibility.

We have each task done in a separate docker container.
- db (postgres database)
- back (Backend with Django)
- front (Frontend with Nginx)
- redis (Websocket cache using Redis)

The thinking part, the backend with Django that manage the API and Websockets.

The Websockets are used in Django through Redis as cache/channel

The database is used by Django and its own api/methods *(ORM)*.

The frontend with Nginx redirect the request either to the backend for api/websocket or to the page corresponding to the url.

The front and the back communicate through Django REST api.

**Everyone** worked on this.

## Modules of choice (starting on subject page 20)

### Major: Implement a custom module that is not listed above.
- The module must be substantial and demonstrate technical complexity.
- You must provide proper justification in your README.md explaining:<br>
&ensp;∗ Why you chose this module.<br>
&ensp;∗ What technical challenges it addresses.<br>
&ensp;∗ How it adds value to your project.<br>
&ensp;∗ Why it deserves Major module status (2 points).<br>
- Taking shortcuts or implementing trivial features will result in rejection.
- Be creative and think outside the box.
- The module should be relevant to your project context.

We choose to add this module for the /t/place, as we introduced a whole entire system of currency, you get nyancoins when placing pixels.

Those coins can be used to upgrade your maximum amount of placeable pixels and/or the time to regenerate one charge. This bring a part of gamification *(not the gamification module)* on top of a canvas with many features.

The /t/place currently doesn't fit the second game module because it doesn't bring a way to win but it took as much work as our skribble game.

**tlair** worked on this module.

### Minor: Same as the major module but smaller in scope and less complex.
- Must still demonstrate technical skill and creativity.
- Should add meaningful value to your project.
- Requires justification in README.md (similar to Major, but for 1 point).

During this projet kcolin added a CI pipeline (Continuous Integration) compose of a few github actions, notably:
- A format check for python files using Ruff
- A linter check for python files using Ruff
- A django integrity check using a Docker on github side
- A docker container integrity check using a Docker on github side

**kcolin** worked on this module.


# Individual Contributions

## tlair

- Created team on the intranet
- Made THE tplace of all time, front & back (one line is not enough to describe all work on this unfortunately)
- Created the website graphical assets with AI
- Installed [font-awesome](https://fontawesome.com/)

## kcolin

- Set up github organisation and project repository
- Influenced technical choice of backend framework
- Setup django project
- Setup .env file loading in django settings for DATABASE_URL
- Create docker-compose.yml with database
- Setup .env file with POSTGRES_* configurations
- Setup dockerfile to create a backend image
- Use docker-compose to run the db and backend
- Enforce health check on db to prevent backend to start too soon
- Worked on the API and did most of the routes
- Created the database models/schema

## cczerwin

- Created initial choice of module proposition
- Populated and updated the readme + docs
- Added ssl termination on nginx
- Configured the websocket server
- Tweaked the dockerfiles / docker compose
- Added aliases in Vue
- Worked on the project folder structure
- Made the base chat and the associated websocket/redis configuration
- Modified how the profile picture are stored (one per user, delete old on modify)
- Worked on the API

## lvan-bre

- Made the base website and it's components
- Added a theme button (light/dark)
- Reworked the chat to have a discord-like appearance

## ael-ghaz

- Setup first team meeting to decide on project roles
- Made THE skribbl.cat game (like the tplace, one line is also not enough to describe all work on this unfortunately)
- Fought against the canvas anti-aliasing and partially won
