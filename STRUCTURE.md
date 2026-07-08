# Herd Wise Structure Report

## Overview

Herd Wise appears to be an early-stage Django application for livestock and farm record management. The core idea is to help a farm manager organize animals, groups of animals, and custom record templates for tracking day-to-day operations such as health, breeding, production, and other farm events.

The project is still in an MVP / prototype phase, but the data model and app structure already point toward a more complete farm-management platform.

---

## Product Direction

From the current codebase, the site is being shaped around these goals:

- Manage farms and their associated users.
- Organize animals into groups and track individual animals.
- Support custom livestock record schemas so different types of records can be created dynamically.
- Provide a portal-style experience for searching and viewing farm data.
- Grow into a polished, multi-user farm operations dashboard.

The planning notes and templates suggest a UI direction that is more dashboard-like and modern, with a base layout, theme switching, and a portal-oriented navigation pattern.

---

## Tech Stack

The site is built with:

- Python and Django 6.0.4
- Django Allauth for authentication and signup
- Tailwind CSS with DaisyUI-style theming
- Alpine.js for interactive UI behavior
- PostgreSQL in Docker for production-style deployment
- SQLite for local development
- Polymorphic Django models for shared animal/animal-group behavior

There is also containerized deployment support through Docker and Nginx.

---

## Project Layout

### Core Django project
- [config/](config/) contains the Django project wiring:
  - [config/urls.py](config/urls.py) routes the site
  - [config/settings/](config/settings/) splits development, production, local, and staging settings
  - [config/asgi.py](config/asgi.py) and [config/wsgi.py](config/wsgi.py) are the deployment entrypoints

### App structure
- [apps/portal/](apps/portal/) is the main business app and contains the core livestock domain.
- [apps/users/](apps/users/) contains the custom user model and authentication-related customization.
- [apps/pages/](apps/pages/) provides the simple public/landing page experience.

### Templates
- [templates/](templates/) holds the UI layer.
- The base layout is defined in [templates/base_layout.html](templates/base_layout.html).
- The portal-specific layout is in [templates/portal/layout.html](templates/portal/layout.html).
- The portal UI is currently split between search, record creation, and record viewing templates.

### Static and theme assets
- [theme/](theme/) contains the Tailwind setup and theme assets.
- [static/](static/) and [staticfiles/](staticfiles/) store static resources.

### Utilities and helpers
- [utils/lib.py](utils/lib.py) contains a small helper for Alpine-based partial template responses.

---

## Core Domain Model

The heart of the application is the livestock domain in [apps/portal/models.py](apps/portal/models.py).

### Main entities
- Farm
  - Represents a farm or operation.
  - Can have multiple users.
  - Stores location and file-based photo data.

- AnimalGroup
  - A grouping container for animals.
  - Used as a logical herd or batch concept.

- Animal
  - Represents an individual animal.
  - Includes category, breed, birth/death dates, age, name, tag ID, and grouping information.

- RecordTemplate
  - A schema definition model for dynamic forms.
  - Lets the application define reusable record types such as health logs, weight logs, or breeding events.

- LivestockRecord
  - Stores actual record instances created from a template.
  - Stores the JSON payload of the data entered for the record.

This model design is one of the strongest parts of the project because it suggests a flexible, schema-driven record system rather than a rigid one-off form system.

---

## Current Functionality

The current implementation already shows the intended flow:

1. User signs up or logs in.
2. They access the portal area.
3. They can search for farms, herds, animals, or records.
4. They can create a record template definition.
5. They can create livestock records based on a template.
6. They can view a stored record.

The routing for these actions is defined in [apps/portal/urls.py](apps/portal/urls.py), and the corresponding view logic is in [apps/portal/views.py](apps/portal/views.py).

---

## Current Implementation Status

This project is clearly still under construction. The structure is thoughtful, but several areas are only partially wired up:

- The record template creation view builds schema data in memory, but it does not appear to persist the template to the database yet.
- The dynamic record form and record display views are present, but there are signs that some pieces still need refinement.
- The UI includes placeholders and scaffolded screens rather than a fully polished product experience.
- The project planning notes describe layout and structure ideas rather than a finished feature set.

In other words, the foundation is solid, but the product is still moving from scaffold to real application behavior.

---

## Where the Project Seems to Be Heading

The repository strongly suggests the following direction:

- Build a real farm operations portal rather than just a simple Django demo.
- Make record-keeping flexible through configurable templates and JSON-backed data.
- Emphasize searchability, organization, and farm-specific workflows.
- Deliver a polished, modern interface using Tailwind and component-style templates.
- Prepare for production deployment with Docker, Nginx, PostgreSQL, and environment-based config.

The planning file in [templates/PLAN.md](templates/PLAN.md) reinforces this by describing a base layout with theme selection, account navigation, and an overall portal structure.

---

## Most Important Takeaway

This is not just a generic Django starter project. It is shaping up to be a purpose-built livestock/farm management system with:

- a strong domain model,
- a portal-first interface,
- dynamic record creation,
- and a clear path toward a more complete farm software product.
