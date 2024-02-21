

<h1>secondglass</h1>

A portable timer-application: simple yet efficient time management tool.

<div align="center">

![Screenshot](images/secondglass.gif)

</div>

It was **hugely** inspired by [@dziemborowicz](https://github.com/dziemborowicz)'s 
[Hourglass](https://github.com/dziemborowicz/hourglass) app.

<h2>Table of Contents</h2>

- [Goals](#goals)
  - [What is Hourglass? click to (un)fold](#what-is-hourglass-click-to-unfold)
  - [What's wrong with Hourglass?](#whats-wrong-with-hourglass)
- [Features](#features)
- [How to use](#how-to-use)

## Goals
**Why did I make it**:
- to get familiar with Python GUI toolkits (with `tkinter` in particular) to be able to use it in my other projects
- to make a proper substitution for [Hourglass](https://github.com/dziemborowicz/hourglass)

<details>
  <summary> <strong>What is Hourglass?</strong> Click to (un)fold.</summary>

### What is Hourglass? click to (un)fold

It's a countdown timer desctop GUI application for Windows;
written on C#; minimalistic in a Unix-way-ish sence.

It looks like this:

<div align="center">

![hourglass](images/hourglass.png)

</div>

### What's wrong with Hourglass?
Nothing's wrong with it. It's an ammazing app. I've being using it for 3+ years.

Though, in my humble opinion, it maybe needs some slight optimization. Its downsides are:
- unreasonably high memory consumption: **70-180 MB**, depending on the size of the window I guess
- inefficient GPU usage: **up to 30% load** on GeForce RTX 2060
  - *like why it even needs GPU?*
    - it is used to produce a fancy window flickering background effect when the timer has rang

</details>

## Features

- you type the time duration in a textbox and press the `start`-button (or just <kbd>Enter</kbd>)
  - input examples:
    - `10` becomes: **10 minutes**
    - `123` or `123 m` or `123min` becomes: **2 hours 3 minutes**
    - `30s` or `30 s` or `30 sec` becomes: **30 seconds**
    - `1h 35m` becomes: **1 hour 35 minutes**
  - the last valid input is saved between sessions
- you can **pause**, **restart** or **abort** the timer by pressing `pause`, `restart` and `stop` buttons respectively
- when the timer expires:
  - the short dinging sound is played
  - the timer window pops up above all the over windows
- the progress bar is also displayed on a taskbar plate, so it's visible even when the app is minimized

## How to use

Windows 10 is required.

1. Download the executable named `secondglass.exe`, from the [latest release](releases/latest)
2. Run the executable

