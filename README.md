*This project has been created as part of the 42 curriculum by tlair, kcolin, cczerwin, lvan-bre, ael-ghaz.*

# Description

Transcendence is a **group project (4-5 people)** intended to  boost creativity, self-confidence, adaptability and teamwork skills by creating a real-world webapp as a team.

# Instructions

## Dependencies

You will need:

- gnumake
- docker with working docker-compose

TODO: check what version of python, django are installed on the school computers and ensure that our project is compatible.

Present on school computer: (hopefully the same on all PCs)
- Docker 28.1.1
- Docker Compose 2.36.2
- Python 3.10.12
- Django not installed
- node 12.22.9
- npm 8.5.1
- Tailwind 4.2.4
- Vue not installed

## Configuration

TODO: add instructions on how to configure the project

- `cp .env.example .env`
- Change settings as desired

## Running

TODO: add instructions on how to build and start the project

- `make dev`

# Resources

- Django documentation - https://docs.djangoproject.com/en/6.0/
- Vue documentation - https://vuejs.org/guide/introduction
- Vite documentation - https://vite.dev/guide/
- Tailwind documentation - https://tailwindcss.com/docs/installation/using-vite

# Team Information

## tlair - Product owner

Defines the product vision, prioritizes features, and ensures the project meets user needs.
- Maintains the product backlog.
- Makes decisions on features and priorities.
- Validates completed work.
- Communicates with stakeholders (evaluators, peers).

## kcolin - Technical lead

Oversees technical decisions and architecture
- Defines technical architecture.
- Makes technology stack decisions.
- Ensures code quality and best practices.
- Reviews critical code changes.

## lvan-bre - Project manager

Facilitates team coordination and removes obstacles.
- Organizes team meetings and planning sessions.
- Tracks progress and deadlines.
- Ensures team communication.
- Manages risks and blockers.

## ael-ghaz & cczerwin - Developer

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

TODO: add justification for these technical choices

# Database Schema

TODO: add database diagram and description of schema

# Features List

TODO: For each feature, add a subheading with description and who worked on it

# Modules

**All of our modules listed below amount for a total of 23pts**

TODO: for each module, add a justification for the choice, how the module was implemented, and who worked on it

## Web modules (starting on subject page 12)

### Major: Use a framework for both the frontend and backend

TODO: justification

We used Vue + Tailwind for the frontend, and Django for the backend.

We all worked on it.

### Minor: Use a frontend framework

TODO: justification

We used Vue + Tailwind for the frontend.

**lvan-bre** worked on the frontend.

### Minor: Use a backend framework

TODO: justification

We used django for the backend.

**kcolin** worked on the backend.

### Major: Implement realtime features using WebSockets or similar technology

- Real-time updates across clients.
- Hanle connection/disconnection gracefully.
- Efficient message broadcasting.

This module is necessary to implement our collaborative drawing game properly.

**ael-ghaz** and **tlair** worked on this module.

### Major: Allow users to interact with other users

- A **basic chat** system (send/receive messages between users).
- A **profile** system (view user information).
- A **friend** system (add/remove friends, see friends list).

This module is important for the social aspect needed for collaborative oriented projects.

**cczerwin** worked on this module.

### Minor: Use an ORM for the database

This is included in Django features, ORM (Object–relational mapping) helps for every interaction with the database making it easier to use.

**kcolin** worked on this module.

### Minor: Real-time collaborative features (shared workspaces, live editing, collaborative drawing, etc.)

### Minor: Server-Side Rendering (SSR) for improved performance and SEO

SSR was used for pages featuring forms to autocomplete where applicable for exemple the user creation page

**kcoline** worked on this module.

**lvan-bre** worked on this module.

### Minor: File upload and management system

- Support multiple file types (images, documents, etc.).
- Client-side and server-side validation (type, size, format).
- Secure file storage with proper access control.
- File preview functionality where applicable.
- Progress indicators for uploads.
- Ability to delete uploaded files.

This module is useful to add a layering tool for our pixel drawing app, it allows coordination between users willing to cooperate to build one large drawing together.

**tlair** worked on this module.

## Accessibility and Internationalization modules (starting on subject page 13)

### Minor: Support for additional browser

- Full compatibility with at least 2 additional browsers (Firefox, Safari, Edge, etc.).
- Test and fix all features in each browser.
- Document any browser-specific limitations.
- Consistent UI/UX across all supported browsers.

It's important for any kind of website to at least support the most used browsers to maximize our potential reach.

Everyone worked on this module.

## User Management modules (starting on subject page 14)

### Major: Standard user management and authentication

- Users can update their profile information.
- Users can upload an avatar (with a default avatar if none provided).
- Users can add other users as friends and see their online status.
- Users have a profile page displaying their information.

This module pairs with the basic interaction module, here focusing on making the actual profiles.

**cczerwin** and **kcolin** worked on this module.

### Minor: Game statistics and match history (requires a game module)

- Track user game statistics (wins, losses, ranking, level, etc.).
- Display match history (1v1 games, dates, results, opponents).
- Show achievements and progression.
- Leaderboard integration.

TODO: add text like others modules

**ael-ghaz** worked on this module.

## Gaming and user experience modules (starting on subject page 16)

### Major: Implement a complete web-based game where users can play against each other

- The game can be real-time multiplayer (e.g., Pong, Chess, Tic-Tac-Toe, Card games, etc.).
- Players must be able to play live matches.
- The game must have clear rules and win/loss conditions.
- The game can be 2D or 3D.

We have a collaborative drawing guess (Pictionary like), this is the corresponding module.

**ael-ghaz** works on this module.

### Major: Remote players — Enable two players on separate computers to play the same game in real-time

- Handle network latency and disconnections gracefully.
- Provide a smooth user experience for remote gameplay.
- Implement reconnection logic.

We also have a collaborative drawing platform (/r/place like), this is the corresponding module.

**tlair** works on this module.

### Major: Multiplayer game (more than 2 players)

- Support for three or more players simultaneously.
- Fair gameplay mechanics for all participants.
- Proper synchronization across all clients.

*See above modules*

**ael-ghaz** works on this module.

### Minor: Game customization options

- Power-ups, attacks, or special abilities.
- Different maps or themes.
- Customizable game settings.
- Default options must be available.

Before starting a game, different game mode can be selected.

TODO: Add things depending on what we implement in the final game

**ael-ghaz** worked on this module.

### Minor: A gamification system to reward users for their actions

- Implement at least 3 of the following: achievements, badges, leaderboards, XP/level system, daily challenges, rewards.
- System must be persistent (stored in database).
- Visual feedback for users (notifications, progress bars, etc.).
- Clear rules and progression mechanics.

This module helps adding to the collaborative aspect.

**cczerwin** worked on this module.

### Minor: Implement spectator mode for games

- Allow users to watch ongoing games.
- Real-time updates for spectators.
- Optional: spectator chat.

This module can be easily added to the game since we're already synchronizing clients.

**ael-ghaz** and **tlair** worked on this module.

# Individual Contributions

TODO: each time you do something, be it code or management related, add it to this part of the readme!

NB: I added some initial contributions from what I could remember, feel free to add/modify

## tlair

- Created team on the intranet

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

## cczerwin

- Created initial choice of module proposition
- Populated the readme

## lvan-bre

## ael-ghaz

- Setup first team meeting to decide on project roles
