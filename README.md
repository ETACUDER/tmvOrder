# tmvOrder - Room Service Ordering System

A web application for managing orders from 39 rooms using QR codes and phone authentication.

## Overview

This webapp provides a streamlined ordering system where:
- Each of the 39 rooms has a unique QR code
- Guests scan the QR code to access the ordering page
- Authentication is handled via phone number
- Users can select items from a curated list

## Features

- **QR Code Integration**: Each room has a unique QR code for easy access
- **Phone Authentication**: Simple dummy authentication using phone numbers (no verification)
- **Room Management**: Support for 39 rooms
- **Item Selection**: Interactive interface for browsing and selecting items
- **Order Tracking**: Real-time order management and status updates

## Technical Stack

- QR Code generation library
- Web framework for order management
- Database for storing orders and room data

## Setup

[Installation and configuration instructions to be added]

## Usage

1. Guest scans room-specific QR code
2. Authenticates using phone number
3. Browses available items
4. Places order
5. Receives confirmation

## Room Configuration

The system supports 39 rooms, each with:
- Unique room identifier
- Associated QR code
- Order history tracking

## Menu Images — Google Maps Integration

**Status: PENDING** (applied 2026-03-26)

Goal: pull menu item images from TMV's Google Maps listing and map them to menu items in `menu.html`.

- Google Maps Place ID: `ChIJkyEMXTPlZzkR5DX8Pytu5sc`
- Google Maps link: https://maps.app.goo.gl/w13Hvy63qZPW2jac7
- GCP project: `628338757341`
- 10 general place photos downloaded to `public/images/gmap_*.jpg` (mostly ambiance, 3 food)
- Menu section data requires **Google Business Profile API** (`accounts.locations.getFoodMenus`)
- API is gated — applied for access, awaiting approval
- OAuth flow script: `get_menu.py` (uses existing YouTube OAuth client)
- Once approved: run `get_menu.py` → fetches structured menu w/ images → map to `menuData` in `menu.html`