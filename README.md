*This project has been created as part of the 42 curriculum by tlair, kcolin, cczerwin, lvan-bre, ael-ghaz.*

[![CI](https://github.com/Blackhole-Megalaser/transcendence/actions/workflows/main.yml/badge.svg)](https://github.com/Blackhole-Megalaser/transcendence/actions/workflows/main.yml)

# Description

Transcendence is a **group project (4-5 people)** intended to boost creativity, self-confidence, adaptability and teamwork skills by creating a real-world webapp as a team. (*Subject version: 21.1*)

Project Repo link: https://github.com/Blackhole-Megalaser/transcendence

The final project is centered around two multiplayer experiences:

- **t/place**, a collaborative canvas inspired by r/place.
- **Scribbl.cat**, a real-time drawing and guessing game inspired by scribbl.io.

Around those games we also built authentication, profiles, friends, chat, real-time updates, Dockerized deployment, HTTPS, CI and a small economy based on nyancoins.

# Instructions

## Dependencies

You will need:

- gnumake
- docker with working docker compose
- a browser that accepts a local self-signed certificate for development

<br>

The project runtime is containerized, so the host does not need to have Django, Node, Redis or Postgres installed for the normal workflow.

Current container stack:

- Backend: Python 3.14, Django 6.0.5, Django REST Framework 3.17.1, Channels 4 and Daphne 4
- Frontend build: Node 22, Vue 3.5, Vite 8, Tailwind 4, Pinia 3
- Frontend server: Nginx with HTTPS
- Database: PostgreSQL 18
- Realtime/cache: Redis

Present on school computer at the beginning of the project: (hopefully the same on all PCs)

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

Make sure to have the **DEBUG** key set to **False** in production.

Note: If the .env file doesn't exist, our makefile creates one and generates a secret key for Django (**make .env**).

## Running

To build and start the project you can use either:

- `make`
- `make run`
- `make dev`

Then to reach the website:

- `https://localhost:1443/`
- `https://{server_ip_here}:{port}/`

You can replace localhost with the server IP address to access it from outside.

The default port used is **1443**, you can change that in the **EXTERNAL_PORT** variable in your environment file.

Useful local endpoints:

- Frontend: `https://localhost:1443/`
- Backend API through Nginx: `https://localhost:1443/api/` (set DEBUG=True in `.env` for a better experience)

The official FT_CAT instance is accessible for everyone at https://ft.lien.cat

# Resources

- Django documentation - https://docs.djangoproject.com/en/6.0/
- Django REST Framework documentation - https://www.django-rest-framework.org/
- Django Channels documentation - https://channels.readthedocs.io/
- Vue documentation - https://vuejs.org/guide/introduction
- Vite documentation - https://vite.dev/guide/
- Tailwind documentation - https://tailwindcss.com/docs/installation/using-vite
- Pinia documentation - https://pinia.vuejs.org/
- Font Awesome documentation - https://fontawesome.com/

## AI Usage

AI was used in different ways for this projects:

- **tlair**: Used it to generate image assets and to generate and understand code.
- **kcolin**: Used it as a search engine and to find some toy examples on how to use various django-rest-framework features.
- **lvan-bre**: Used it for debugging, as a search engine mostly because Vue's documentation is bad and to find some design ideas.
- **ael-ghaz**: Used it as a search engine and to learn with code structure examples.
- **cczerwin**: Used it to search for specific Django cases and to get code structure examples and to convert from a language to another.

# Team Information

## [tlair](https://github.com/La-Fougere) - Product owner

Defines the product vision, prioritizes features, and ensures the project meets user needs.

- Maintains the product backlog.
- Makes decisions on features and priorities.
- Validates completed work.
- Communicates with stakeholders (evaluators, peers).

## [kcolin](https://github.com/logistic-bot) - Technical lead

Oversees technical decisions and architecture.

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

Our first target was to finish the project on the 31st of May, which gave us 5 weeks. After this date we updated our planned modules list to finish the 2nd or 3rd of July.

We used a [google sheet](https://docs.google.com/spreadsheets/d/1-unfSmSeZFW78XxymSvcDQVJqaTeYh-l-Ek2GIyEvls/edit?gid=216360315) to agree which project modules we would implement, and roughly track who would be working on it.

Our communication, when not done in person, was mostly through Discord.

# Technical Stack

For the frontend, we decided to go with Vue, Vite and Tailwind. Pinia is used for frontend state management and persisted state, and Font Awesome is used for icons.

For the backend, Django is used in combination with Django REST Framework, Django Channels, Daphne, Redis and a PostgreSQL database.

Vue was chosen because it is easy to learn and fast to iterate with. Django was chosen because it includes many useful features like ORM *(see ORM modules for details)*, authentication, admin panel, migrations and a clean way to expose APIs.

The production-like local setup is split into containers:

- `db`: PostgreSQL database.
- `back`: Django backend, REST API and websocket handling through Daphne/ASGI.
- `front`: Nginx server serving the built Vue app and HTTPS entrypoint.
- `redis`: channel layer/cache used by websockets and chat history.

The frontend and backend communicate through the Django REST API and websocket endpoints. Nginx is responsible for serving the frontend and routing API/websocket traffic to the backend.

# Database Schema

[![DB Schema](https://raw.githubusercontent.com/Blackhole-Megalaser/transcendence/refs/heads/main/docs/db_diagram.svg)](https://raw.githubusercontent.com/Blackhole-Megalaser/refs/heads/main/docs/db_diagram.svg)
 
We have the base User table made by Django internally, featuring the user base information such as username, email, staff status, password hash and permissions.

## User Profile

Each User is associated with one UserProfile that contains its own data:

- The amount of nyancoins (our website currency gained by placing pixels, used to unlock colors on t/place)
- The amount of currently placeable pixels
- The maximum amount of pixels that can be held at any time for a given user
- The time needed to regenerate a pixel to put on the canvas
- Unlocked colors
- Current friends
- Pending friend requests
- Unlocked wordlists
- Profile image/avatar
- Last seen timestamp used for online status

Each wordlist is composed of many word items (simple strings).

We intended to have unlockable wordlists for the Scribbl game. The models and API exist, and the project currently ships with the useful base wordlist needed for the game.

## Scribbl

Scribbl is built around rooms, players, turns and an authoritative backend state.

When a user joins a game, a ScribblPlayer is created for this room and attached to a ScribblRoom. The room then manages the full game state:

- room code (used to join)
- room name (visible in the lobby)
- host player
- joined players
- current drawer
- current word to draw/guess
- word history to avoid repeating the same word in a game
- max rounds selected by the host
- current round and turn counters
- timer start and end data
- game started/finished flags
- turn started flag
- per-player scores
- per-turn found/guessed status

The backend exposes endpoints for room creation, join, leave, configuration, game start, random word choices, turn start, state retrieval, guessing, ending a turn and replaying a finished game.

The guess endpoint is authoritative: wrong guesses can still be sent to chat, correct guesses are detected server-side and return a game event instead of leaking the word in chat.

The scoring rule follows the expected scribbl.io-like behavior:

- a player who does not find the word before the timer ends scores 0
- the first correct guess can score around 200 points
- the last correct guess can score around 50 points
- intermediate guesses decrease according to elapsed timer progress
- the drawer only scores if at least one player found the word
- if the drawer leaves before the end of the turn, no point is awarded for that turn

## Tplace

For t/place we store each pixel individually with:

- coordinates `x` and `y`
- the user who placed it
- the color used
- creation/update timestamps

The canvas is queried by the frontend for the initial load, then updated in real time through websocket messages.

The canvas was expanded to a 2000x2000 grid. Pixel coordinates are protected by a unique constraint to avoid duplicated positions.

Tplace also includes progression data through the UserProfile:

- pixel regeneration delay
- maximum pixel capacity
- unlocked colors
- nyancoins

There are API endpoints for placing pixels, retrieving the full canvas, checking pixel regeneration, buying upgrades and unlocking colors.

# API and Realtime Notes

## User and social API

The backend includes routes for:

- signup/login/logout
- current user information (`/api/users/me/`)
- profile detail and update
- avatar/profile image upload
- email change
- friend requests
- accepting/refusing/removing friends
- friend list with profile image and online/last seen information

The API returns clearer conflict and validation errors for cases like duplicate usernames, duplicate friend requests, already existing friendships and invalid usernames.

## Chat and websockets

The project uses websocket consumers and Redis for real-time messages.

Chat messages support room targeting, so the same chat component can be used for different game rooms. Chat history is sent on connection and cached through Redis.

Profile pictures and user information are attached to chat messages on the frontend side to make the chat feel closer to the rest of the social UI.

## Tplace realtime

Tplace uses REST for the initial canvas data and websocket events for live pixel updates.

The frontend supports:

- fullscreen canvas interaction
- zoom and pan
- keyboard shortcuts
- color palette and unlocked colors
- eyedropper tool
- pixel placement feedback
- mobile/touch interactions
- anti-aliasing fixes for crisp pixel art
- upgrade UI for pixel capacity and regeneration speed

## Scribbl realtime

Scribbl uses backend state endpoints plus websocket synchronization for the drawing canvas and chat.

The frontend supports:

- room creation and join flow
- lobby state
- start game action from the host
- drawing canvas synchronization
- chat bound to a room code
- drawing tools, color palette, bucket/fill, undo/redo and touch input
- word choices and selected word startup flow
- redirects when a player is not part of a room anymore

# Features List

The project features:

- a Pictionary-like multiplayer game (Scribbl.cat)
- a collaborative canvas (/t/place)
- user accounts and profile pages
- profile pictures
- online/last seen status
- friend requests and friend list
- real-time chat
- gamification with nyancoins and unlockable t/place upgrades
- HTTPS local deployment through Nginx
- CI checks for the backend and project health

# Modules

**All of our modules listed below amount for a total of 26pts**

- Web modules for (9) points
- Accessibility and Internationalization modules for (1) point
- User Management modules for (4) points
- Gaming and user experience modules for (7) points
- Devops modules for (2) points
- Modules of choices for (3) points

| Module Name                                                        | Status | Points | Bonus | Validated |
| :----------------------------------------------------------------- | :----- | :----- | :---- | :-------- |
| **Web Modules**                                                    |        |        |       |           |
| Use a framework for both frontend and backend                      | Major  | 2      |       |           |
| Use a frontend framework                                           | Minor  | 1      | Bonus |           |
| Use a backend framework                                            | Minor  | 1      | Bonus |           |
| Implement realtime features using WebSockets or similar technology | Major  | 2      |       |           |
| Allow users to interact with other users                           | Major  | 2      |       |           |
| Use an ORM for the database                                        | Minor  | 1      |       |           |
| Real-time collaborative features                                   | Minor  | 1      |       |           |
| Custom-made design system with reusable components                 | Minor  | 1      | Bonus |           |
| **Accessibility and Internationalization Modules**                 |        |        |       |           |
| Support for additional browsers                                    | Minor  | 1      |       |           |
| **User Management Modules**                                        |        |        |       |           |
| Standard user management and authentication                        | Major  | 2      |       |           |
| Advanced permissions system                                        | Major  | 2      |       |           |
| **Gaming and User Experience Modules**                             |        |        |       |           |
| Implement a complete web-based game                                | Major  | 2      |       |           |
| Remote players (Real-time gameplay on separate computers)          | Major  | 2      |       |           |
| Multiplayer game (More than 2 players)                             | Major  | 2      |       |           |
| Implement spectator mode for games                                 | Minor  | 1      | Bonus |           |
| **Devops Modules**                                                 |        |        |       |           |
| Backend as microservices                                           | Major  | 2      | Bonus |           |
| **Modules of Choice**                                              |        |        |       |           |
| Custom module: Currency system (Nyancoins/Gamification)            | Major  | 2      | Bonus |           |
| CI pipeline implementation                                         | Minor  | 1      | Bonus |           |
| **Total Points**                                                   |        | 28     |       |           |

## Web modules (starting on subject page 12)

### Major: Use a framework for both the frontend and backend

We used Vue + Tailwind for the frontend, and Django for the backend.

We all worked on this module.

### Minor: Use a frontend framework

We used Vue + Tailwind for the frontend, with Vite as the build tool and Pinia for state.

**lvan-bre** worked on the main site appearance and reusable components.<br>
**tlair** worked on the t/place feature and its frontend interactions.<br>
**ael-ghaz** worked on the Scribbl game.

### Minor: Use a backend framework

We used Django and Django REST Framework for the backend.

**kcolin**, **cczerwin** and **tlair** worked on backend routes, models, websocket integration and game APIs.

### Major: Implement realtime features using WebSockets or similar technology

- Real-time updates across clients.
- Handle connection/disconnection gracefully.
- Efficient message broadcasting.

This module is necessary to implement our collaborative drawing tools properly.

**cczerwin** worked on the websocket/chat infrastructure.<br>
**tlair** worked with it for t/place.<br>
**ael-ghaz** worked with it for Scribbl.

### Major: Allow users to interact with other users

- A **chat** system (send/receive messages between users).
- A **profile** system (view user information, avatars and status).
- A **friend** system (add/remove friends, see friends list, manage requests).

This module is important for the social aspect needed for collaborative-oriented projects.

**cczerwin** worked on the chat, friend API and user/profile API routes.<br>
**lvan-bre** worked on the profile page, friend UI and frontend integration.<br>
**ael-ghaz** & **tlair** worked on collaborative game features.

### Minor: Use an ORM for the database

This is included in Django features. ORM (Object-relational mapping) helps for every interaction with the database by making it easier and safer to use.

**kcolin** worked on the initial models and schema.<br>
**ael-ghaz**, **cczerwin** and **tlair** extended the schema for game and profile features.

### Minor: Real-time collaborative features (shared workspaces, live editing, collaborative drawing, etc.)

The t/place canvas and Scribbl drawing canvas cover this module.

**tlair** and **ael-ghaz** worked on this module.

### Minor: Custom-made design system with reusable components, including a proper color palette, typography, and icons (minimum: 10 reusable components)

Thanks to Vue, most of our UI is component-based and reusable. The UI reacts to our theme button and uses shared layout/components across pages.

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
- Users can manage friend requests.

This module pairs with the basic interaction module, here focusing on making the actual profiles.

**cczerwin** and **kcolin** worked on the backend part of this module.<br>
**lvan-bre** connected the front and made the friendlist and profile page.

### Major: Advanced permissions system

- View, edit, and delete users (CRUD).
- Roles management (admin, user, guest, moderator, etc.).
- Different views and actions based on user role.

Django includes an admin view system. An admin user can easily add/edit/delete users and project data.

It's possible through this interface to give a staff status or a superuser status.

- Staff can access the admin panel and browse the database content.
- Superuser can interact with anything: add/edit/delete.

We also added admin-oriented helpers during development, including a command to grant nyancoins for testing t/place progression.

**cczerwin**, **kcolin** and **tlair** worked on this module.

## Gaming and user experience modules (starting on subject page 16)

### Major: Implement a complete web-based game where users can play against each other

- The game can be real-time multiplayer (e.g., Pong, Chess, Tic-Tac-Toe, Card games, etc.).
- Players must be able to play live matches.
- The game must have clear rules and win/loss conditions.
- The game can be 2D or 3D.

We have a collaborative drawing and guessing game, Pictionary-like, this is the corresponding module.

**ael-ghaz** worked on the frontend game experience.<br>
**kcolin** started the backend room/game API.<br>
**tlair** finalized the backend API, scoring and turn flow.

### Major: Remote players - Enable two players on separate computers to play the same game in real-time

- Handle network latency and disconnections gracefully.
- Provide a smooth user experience for remote gameplay.
- Implement reconnection logic.

We have both a collaborative drawing game and a collaborative drawing platform (/r/place-like), this is the corresponding module.

**tlair** & **ael-ghaz** worked on this module.

### Major: Multiplayer game (more than 2 players)

- Support for three or more players simultaneously.
- Fair gameplay mechanics for all participants.
- Proper synchronization across all clients.

Scribbl rooms support more than two players, host-controlled game start, multiple rounds and turn rotation. Tplace also supports all connected users interacting with the same shared canvas but may not be considered as a game by the subject.

**ael-ghaz**, **tlair** and **kcolin** worked on this module.

### Minor: Implement spectator mode for games

- Allow users to watch ongoing games.
- Real-time updates for spectators.
- Optional: spectator chat.

This module is technically implemented in the t/place (but may not be considered as a game by the subject).

**tlair** worked on this module.

## Devops modules (starting on subject page 18)

### Major: Backend as microservices

- Design loosely-coupled services with clear interfaces.
- Use REST APIs or message queues for communication.
- Each service should have a single responsibility.

We have each task done in a separate docker container.

- `db` (Postgres database)
- `back` (Backend with Django, REST API, ASGI and websockets)
- `front` (Frontend with Nginx and HTTPS)
- `redis` (Websocket channel layer/cache)

The thinking part is the backend with Django, which manages the API and websockets.

Websockets are used in Django through Redis as cache/channel layer.

The database is used by Django and its own APIs/methods *(ORM)*.

The frontend with Nginx redirects the request either to the backend for API/websocket traffic or to the page corresponding to the URL.

The front and the back communicate through Django REST API and websocket messages.

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

We choose to add this module for the t/place, as we introduced a whole currency system, you get nyancoins when placing pixels.

Those coins can be used to upgrade your maximum amount of placeable pixels and/or the time to regenerate one pixel. This bring a part of gamification *(not the gamification module)* on top of a canvas with many features.

The t/place currently doesn't fit the second game module because it doesn't bring a way to win but it took as much work as our skribble game.

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

This section was refreshed from the merged branch history and commit history. Branch prefixes were used as attribution hints when the original author was less obvious.

## tlair

- Created the team on the intranet.
- Made THE t/place of all time, front & back (one line is still not enough to describe all work on this unfortunately).
- Created the website graphical assets with AI.
- Installed and configured [font-awesome](https://fontawesome.com/).
- Integrated t/place with its backend API and websocket updates.
- Reworked t/place into a fullscreen interactive canvas with dragging, zoom, menu behavior and mobile/touch support.
- Expanded t/place to a 2000x2000 canvas.
- Added canvas quality fixes: crisp pixel rendering, anti-aliasing handling and input precision improvements.
- Added t/place tools and UX: eyedropper, keybinds, better palette behavior and responsive canvas controls.
- Added t/place progression/upgrades: max pixels, pixel regeneration delay, unlocked colors, nyancoin spending and an admin command to get nyancoins.
- Finalized the Scribbl backend API: host permissions, configurable max rounds, minimum players, room state, replay, turn lifecycle, guessing and end-turn behavior.

## kcolin

- Set up GitHub organisation and project repository.
- Influenced the technical choice of backend framework.
- Set up the Django project.
- Set up `.env` loading in Django settings for database and application configuration.
- Created `docker-compose.yml` with database support.
- Set up `.env` with `POSTGRES_*` configurations.
- Set up Dockerfiles and backend image creation.
- Used docker compose to run the database and backend services.
- Enforced database health checks to prevent the backend from starting too soon.
- Added backend dependency management and project structure.
- Added Django models/schema foundations for users, profiles, colors, wordlists, pixels and Scribbl rooms.
- Added migrations and database constraints, including unique t/place pixel positions.
- Added core user API routes: signup, login/logout, current user, user detail and avatar/profile image support.
- Added initial t/place API: place pixel, retrieve full canvas, pixel regeneration and timezone-aware regeneration.
- Added wordlist API and random word endpoints used by Scribbl.
- Added initial Scribbl backend API: room creation, room list/detail, join room, leave room, start game, get random words and start turn.
- Added cleanup/fixes for empty Scribbl rooms and multi-player room crashes.
- Worked on CI, Django checks, ruff/linting, Docker buildx and development shell/tooling.

## cczerwin

- Created the initial choice of module proposition.
- Populated and updated the README + docs during the project.
- Added SSL termination on Nginx and support for HTTPS on the local entrypoint.
- Configured the websocket server stack with ASGI/Daphne and Redis.
- Tweaked the Dockerfiles, docker compose services, volumes and deploy settings.
- Added aliases in Vue and helped with the project folder structure.
- Made the base chat and the associated websocket/Redis configuration.
- Added chat history, room-aware chat behavior and profile picture support in chat messages.
- Worked on websocket routing and moved websocket setup into the main backend routing.
- Added friend API routes and friendlist API views.
- Added request validation for friend requests: prevent duplicates, prevent requests to existing friends and return clearer error messages.
- Added email change route.
- Added profile image URL and last-seen data to friend-related API responses.
- Added middleware/model changes for online status and last seen tracking.
- Improved signup/user validation errors, including username conflicts and ASCII-related checks.
- Modified how profile pictures are stored (one per user, delete old one on modification).
- Worked on admin redirection and backend route polish.
- Worked on API fixes and deployment/debugging support throughout the project.

## lvan-bre

- Made the base website and its wonderful components.
- Set up and iterated on the Vue/Vite/Tailwind frontend structure.
- Added Pinia/persisted state usage for frontend user/session state.
- Added a theme button (light/dark).
- Built shared layout components such as page wrappers, navigation, sidebar/profile UI and reusable buttons/inputs.
- Built and polished the home page, login page, signup page, terms/privacy pages and error pages.
- Added frontend validation for forbidden usernames, password requirements, password similarity and form errors.
- Added profile page UI, profile update flow, profile image display and hover/profile widgets.
- Added frontend support for friend requests, friend list, add-friend flow and friend request handling.
- Connected friend-related frontend flows to backend endpoints and local/session state.
- Added online/login status refresh in the frontend.
- Reworked the chat to have a Discord-like appearance.
- Improved chat visuals, adaptive/mobile layout and message formatting with profile pictures.
- Added UI polish around game cards, game info, icons and nyancoin display.

## ael-ghaz

- Set up the first team meeting to decide on project roles.
- Made THE Scribbl.cat game (like t/place, one line is also not enough to describe all work on this unfortunately).
- Built the Scribbl frontend game canvas and an amazing drawing experience.
- Added drawing tools and gameplay controls: brush, eraser-like behavior, bucket/fill, palette, undo/redo and cursor feedback.
- Fought against canvas anti-aliasing and partially won.
- Added touch/tactile support for the drawing canvas.
- Added Scribbl websocket canvas synchronization and chat integration.
- Added chat history handling for Scribbl rooms.
- Added lobby flow: create room, join room, leave room, room code usage and start game button.
- Added frontend redirects around room/game state, especially when a user is not in the room anymore.
- Connected game start and room code flow to backend APIs.
- Added word choice flow: retrieve 3 words, select one word and start the turn.
- Worked on Scribbl assets, UI polish and gameplay page structure.
