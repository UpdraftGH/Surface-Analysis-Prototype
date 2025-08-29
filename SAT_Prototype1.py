# Copyright (c) 2025 Quintin Ashley
# All rights reserved. See LICENSE file for details.

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.lines as mlines
import matplotlib as mpl
from matplotlib.widgets import Button

#Disabling keys for functionality
mpl.rcParams['keymap.xscale'] = ''  # disables 'l' for x-axis zoom
mpl.rcParams['keymap.yscale'] = ''  # disables 'L' for y-axis zoom
mpl.rcParams['keymap.save'] = ''  # disables 's' for saving figure

# Create figure
fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.set_aspect('equal')
ax.grid(True)
drawable_artists = []


# Adjust the layout to make space for buttons
plt.subplots_adjust(bottom=0.2)

# Define button positions (x0, y0, width, height)
button_width = 0.1
button_height = 0.05

ax_default = plt.axes([0.1, 0.05, button_width, button_height])
ax_cold = plt.axes([0.1, 0.15, button_width, button_height])
ax_warm = plt.axes([0.1, 0.25, button_width, button_height])
ax_occluded = plt.axes([0.1, 0.35, button_width, button_height])
ax_stationary = plt.axes([0.1, 0.45, button_width, button_height])
ax_dryline = plt.axes([0.1, 0.55, button_width, button_height])
ax_high = plt.axes([0.1, 0.65, button_width, button_height])
ax_low = plt.axes([0.1, 0.75, button_width, button_height])

btn_default = Button(ax_default, 'Default')
btn_cold = Button(ax_cold, 'Cold Front')
btn_warm = Button(ax_warm, 'Warm Front')
btn_occluded = Button(ax_occluded, 'Occluded Front')
btn_stationary = Button(ax_stationary, 'Stationary Front')
btn_dryline = Button(ax_dryline, 'Dryline')
btn_high = Button(ax_high, 'High Marker')
btn_low = Button(ax_low, 'Low Marker')

fig.patch.set_facecolor('skyblue')  # Entire figure background
ax.set_facecolor('white')         # Inside-plot background

# Mode display text (initial default mode)
mode_text = ax.text(
    0.01, 1.01, "Mode: Default",
    transform=ax.transAxes,
    fontsize=10,
    color='black',
    verticalalignment='bottom',
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray")
)

marker_state = {'type': 'H', 'positions': []}
drawing_front = {'type': 'cold', 'points': []}

def on_key(event):
    if event.key == 'c':
        drawing_front['type'] = 'cold'
        drawing_front['points'].clear()
        marker_state['type'] = None
        mode_text.set_text("Mode: Cold Front")
        fig.canvas.draw_idle()
        print("Cold front mode (blue)")

    elif event.key == 'w':
        drawing_front['type'] = 'warm'
        drawing_front['points'].clear()
        marker_state['type'] = None
        mode_text.set_text("Mode: Warm Front")
        fig.canvas.draw_idle()
        print("Warm front mode (red)")

    elif event.key == 'o':
        drawing_front['type'] = 'occluded'
        drawing_front['points'].clear()
        marker_state['type'] = None
        mode_text.set_text("Mode: Occluded Front")
        fig.canvas.draw_idle()
        print("Occluded front mode (purple)")

    elif event.key == 's':
        drawing_front['type'] = 'stationary'
        drawing_front['points'].clear()
        marker_state['type'] = None
        mode_text.set_text("Mode: Stationary Front")
        fig.canvas.draw_idle()
        print("Stationary front mode")

    elif event.key == 'h':
        marker_state['type'] = 'H'
        mode_text.set_text("Mode: High Pressure Marker")
        fig.canvas.draw_idle()
        print("High pressure marker mode (blue H)")

    elif event.key == 'l':
        marker_state['type'] = 'L'
        mode_text.set_text("Mode: Low Pressure Marker")
        fig.canvas.draw_idle()
        print("Low pressure marker mode (red L)")

    elif event.key == 'd':
        drawing_front['type'] = 'dryline'
        drawing_front['points'].clear()
        marker_state['type'] = None
        print("Dryline mode (orange, unfilled semicircles)")


    if event.key == 'enter':
        if len(drawing_front['points']) >= 2:
            if drawing_front['type'] == 'cold':
                draw_cold_front(ax, drawing_front['points'])
            elif drawing_front['type'] == 'warm':
                draw_warm_front(ax, drawing_front['points'])
            elif drawing_front['type'] == 'occluded':
                draw_occluded_front(ax, drawing_front['points'])
            elif drawing_front['type'] == 'stationary':
                draw_stationary_front(ax, drawing_front['points'])
            elif drawing_front['type'] == 'dryline':
                draw_dryline(ax, drawing_front['points'])
            drawing_front['points'].clear()
            fig.canvas.draw()

def on_click(event):
    if event.inaxes != ax:
        return
    if marker_state['type'] in ['H', 'L']:
        color = 'blue' if marker_state['type'] == 'H' else 'red'
        text = ax.text(event.xdata, event.ydata, marker_state['type'], color=color, fontsize=20, fontweight='bold', ha='center', va='center')
        drawable_artists.append(text)
        fig.canvas.draw()
        print(f"Placed {marker_state['type']} at ({event.xdata:.2f}, {event.ydata:.2f})")
    else:
        drawing_front['points'].append((event.xdata, event.ydata))
        dot, = ax.plot(event.xdata, event.ydata, 'ko', markersize=6)
        drawable_artists.append(dot)
        print(f"Point added: ({event.xdata:.2f}, {event.ydata:.2f})")
        fig.canvas.draw()

#Function to clear all fronts, markers, dots, etc.
def clear_fronts_and_markers(event):
    for artist in drawable_artists:
        artist.remove()
    drawable_artists.clear()
    drawing_front['points'].clear()
    fig.canvas.draw()

def set_mode_default(event):
    drawing_front['type'] = None
    drawing_front['points'].clear()
    marker_state['type'] = None
    mode_text.set_text("Mode: Default")
    fig.canvas.draw_idle()

def set_mode_cold(event):
    drawing_front['type'] = 'cold'
    drawing_front['points'].clear()
    marker_state['type'] = None
    mode_text.set_text("Mode: Cold Front")
    fig.canvas.draw_idle()

def set_mode_warm(event):
    drawing_front['type'] = 'warm'
    drawing_front['points'].clear()
    marker_state['type'] = None
    mode_text.set_text("Mode: Warm Front")
    fig.canvas.draw_idle()

def set_mode_occluded(event):
    drawing_front['type'] = 'occluded'
    drawing_front['points'].clear()
    marker_state['type'] = None
    mode_text.set_text("Mode: Occluded Front")
    fig.canvas.draw_idle()

def set_mode_stationary(event):
    drawing_front['type'] = 'stationary'
    drawing_front['points'].clear()
    marker_state['type'] = None
    mode_text.set_text("Mode: Stationary Front")
    fig.canvas.draw_idle()

def set_mode_dryline(event):
    drawing_front['type'] = 'dryline'
    drawing_front['points'].clear()
    marker_state['type'] = None
    mode_text.set_text("Mode: Dryline")
    fig.canvas.draw_idle()

def set_mode_high(event):
    marker_state['type'] = 'H'
    drawing_front['type'] = None
    drawing_front['points'].clear()
    mode_text.set_text("Mode: High Pressure Marker")
    fig.canvas.draw_idle()

def set_mode_low(event):
    marker_state['type'] = 'L'
    drawing_front['type'] = None
    drawing_front['points'].clear()
    mode_text.set_text("Mode: Low Pressure Marker")
    fig.canvas.draw_idle()




     

def draw_cold_front(ax, points):
    x_vals, y_vals = zip(*points)
    color = 'blue'
    line, = ax.plot(x_vals, y_vals, color=color, linewidth=2)
    drawable_artists.append(line)

    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        dx, dy = x1 - x0, y1 - y0
        length = np.hypot(dx, dy)
        if length == 0:
            continue

        num_triangles = int(length / 0.5)
        for j in range(num_triangles):
            frac = (j + 0.5) / num_triangles
            xm = x0 + frac * dx
            ym = y0 + frac * dy

            # Angles
            theta = np.arctan2(dy, dx)
            theta_perp = theta + np.pi / 2

            # Triangle geometry
            base_len = 0.2
            height = 0.1

            tip_x = xm + height * np.cos(theta_perp)
            tip_y = ym + height * np.sin(theta_perp)

            base_left_x = xm - (base_len / 2) * np.cos(theta)
            base_left_y = ym - (base_len / 2) * np.sin(theta)

            base_right_x = xm + (base_len / 2) * np.cos(theta)
            base_right_y = ym + (base_len / 2) * np.sin(theta)

            triangle = np.array([
                [base_left_x, base_left_y],
                [base_right_x, base_right_y],
                [tip_x, tip_y]
            ])

            patch = ax.fill(triangle[:, 0], triangle[:, 1], color='blue', zorder=10)
            drawable_artists.extend(patch)

def draw_warm_front(ax, points):
    x_vals, y_vals = zip(*points)
    color = 'red'
    line, = ax.plot(x_vals, y_vals, color=color, linewidth=2)
    drawable_artists.append(line)

    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        dx, dy = x1 - x0, y1 - y0
        length = np.hypot(dx, dy)
        if length == 0:
            continue

        # Angle of the front segment
        theta = np.arctan2(dy, dx)

        # Number of semicircles
        num_circles = int(length / 0.5)
        for j in range(num_circles):
            frac = (j + 0.5) / num_circles
            xm = x0 + frac * dx
            ym = y0 + frac * dy

            # Semicircle parameters
            radius = 0.1
            num_pts = 20  # smoothness of the semicircle

            angles = np.linspace(-np.pi / 2, np.pi / 2, num_pts)
            # Rotate semicircle to match direction of the front
            rotated_angles = angles + theta + (np.pi / 2)

            x_circle = xm + radius * np.cos(rotated_angles)
            y_circle = ym + radius * np.sin(rotated_angles)

            # Add center point to form a filled shape
            x_full = np.concatenate(([xm], x_circle))
            y_full = np.concatenate(([ym], y_circle))

            patch = ax.fill(x_full, y_full, color=color, zorder=10)
            drawable_artists.extend(patch)

def draw_occluded_front(ax, points):
    x_vals, y_vals = zip(*points)
    color = 'purple'
    line, = ax.plot(x_vals, y_vals, color=color, linewidth=2)
    drawable_artists.append(line)

    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        dx, dy = x1 - x0, y1 - y0
        length = np.hypot(dx, dy)
        if length == 0:
            continue

        theta = np.arctan2(dy, dx)
        theta_perp = theta + np.pi / 2

        num_symbols = int(length / 0.5)
        for j in range(num_symbols):
            frac = (j + 0.5) / num_symbols
            xm = x0 + frac * dx
            ym = y0 + frac * dy

            if j % 2 == 0:
                # Triangle
                base_len = 0.2
                height = 0.1

                tip_x = xm + height * np.cos(theta_perp)
                tip_y = ym + height * np.sin(theta_perp)

                base_left_x = xm - (base_len / 2) * np.cos(theta)
                base_left_y = ym - (base_len / 2) * np.sin(theta)

                base_right_x = xm + (base_len / 2) * np.cos(theta)
                base_right_y = ym + (base_len / 2) * np.sin(theta)

                triangle = np.array([
                    [base_left_x, base_left_y],
                    [base_right_x, base_right_y],
                    [tip_x, tip_y]
                ])
                patch = ax.fill(triangle[:, 0], triangle[:, 1], color=color, zorder=10)
                drawable_artists.extend(patch)

            else:
                # Semicircle
                radius = 0.1
                num_pts = 20
                angles = np.linspace(-np.pi / 2, np.pi / 2, num_pts)
                rotated_angles = angles + theta_perp

                x_circle = xm + radius * np.cos(rotated_angles)
                y_circle = ym + radius * np.sin(rotated_angles)

                x_full = np.concatenate(([xm], x_circle))
                y_full = np.concatenate(([ym], y_circle))

                patch = ax.fill(x_full, y_full, color=color, zorder=10)
                drawable_artists.extend(patch)

def draw_stationary_front(ax, points):
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        dx, dy = x1 - x0, y1 - y0
        length = np.hypot(dx, dy)
        if length == 0:
            continue

        theta = np.arctan2(dy, dx)
        theta_perp = theta + np.pi / 2

        num_symbols = int(length / 0.5)
        if num_symbols == 0:
            continue

        for j in range(num_symbols):
            # Segment endpoints
            start_frac = j / num_symbols
            end_frac = (j + 1) / num_symbols

            x_start = x0 + start_frac * dx
            y_start = y0 + start_frac * dy
            x_end = x0 + end_frac * dx
            y_end = y0 + end_frac * dy

            # Draw colored segment (connected to previous)
            color = 'blue' if j % 2 == 0 else 'red'
            line, = ax.plot([x_start, x_end], [y_start, y_end], color=color, linewidth=2)
            drawable_artists.append(line)

            # Midpoint for symbol placement
            xm = (x_start + x_end) / 2
            ym = (y_start + y_end) / 2

            if j % 2 == 0:
                # Blue triangle (cold side)
                base_len = 0.2
                height = 0.1

                tip_x = xm - height * np.cos(theta_perp)
                tip_y = ym - height * np.sin(theta_perp)

                base_left_x = xm - (base_len / 2) * np.cos(theta)
                base_left_y = ym - (base_len / 2) * np.sin(theta)

                base_right_x = xm + (base_len / 2) * np.cos(theta)
                base_right_y = ym + (base_len / 2) * np.sin(theta)

                triangle = np.array([
                    [base_left_x, base_left_y],
                    [base_right_x, base_right_y],
                    [tip_x, tip_y]
                ])
                patch = ax.fill(triangle[:, 0], triangle[:, 1], color='blue', zorder=10)
                drawable_artists.extend(patch)

            else:
                # Red semicircle (warm side)
                radius = 0.1
                num_pts = 20
                angles = np.linspace(-np.pi / 2, np.pi / 2, num_pts)
                rotated_angles = angles + theta_perp

                x_circle = xm + radius * np.cos(rotated_angles)
                y_circle = ym + radius * np.sin(rotated_angles)

                x_full = np.concatenate(([xm], x_circle))
                y_full = np.concatenate(([ym], y_circle))

                patch = ax.fill(x_full, y_full, color='red', zorder=10)
                drawable_artists.extend(patch)


def draw_dryline(ax, points):
    x_vals, y_vals = zip(*points)
    color = 'orange'
    line, = ax.plot(x_vals, y_vals, color=color, linewidth=2)
    drawable_artists.append(line)

    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        dx, dy = x1 - x0, y1 - y0
        length = np.hypot(dx, dy)
        if length == 0:
            continue

        theta = np.arctan2(dy, dx)

        num_circles = int(length / 0.2)
        for j in range(num_circles):
            frac = (j + 0.5) / num_circles
            xm = x0 + frac * dx
            ym = y0 + frac * dy

            radius = 0.1
            num_pts = 20
            angles = np.linspace(-np.pi / 2, np.pi / 2, num_pts)
            rotated_angles = angles + theta + (np.pi / 2)

            x_circle = xm + radius * np.cos(rotated_angles)
            y_circle = ym + radius * np.sin(rotated_angles)

            # Draw unfilled semicircle (outline only)
            patch = ax.plot(x_circle, y_circle, color=color, linewidth=1.5)
            drawable_artists.extend(patch)


                
fig.canvas.mpl_connect('key_press_event', on_key)
fig.canvas.mpl_connect('button_press_event', on_click)




# Function to draw cloud cover symbol
def draw_cloud_cover(ax, x, y, cover):
    """
    Draw cloud cover at (x, y) based on fractional value (0.0 to 1.0),
    converted to oktas (0–8) with specific visual patterns.
    """
    radius = 0.07
    oktas = int(round(cover * 8))  # Convert 0.0–1.0 to 0–8

    # Base circle
    circle = patches.Circle((x, y), radius, edgecolor='black', facecolor='none', linewidth=1.2)
    ax.add_patch(circle)

    if oktas == 0:
        return

    elif oktas == 1:
        ax.plot([x, x], [y + radius, y - radius], color='black', linewidth=1)

    elif oktas == 2:
        wedge = patches.Wedge((x, y), radius, 0, 90, facecolor='black', edgecolor='none')
        ax.add_patch(wedge)

    elif oktas == 3:
        wedge = patches.Wedge((x, y), radius, 0, 90, facecolor='black', edgecolor='none')
        ax.add_patch(wedge)
        ax.plot([x, x], [y + radius, y - radius], color='black', linewidth=1)

    elif oktas == 4:
        wedge = patches.Wedge((x, y), radius, 270, 90, facecolor='black', edgecolor='none')
        ax.add_patch(wedge)

    elif oktas == 5:
        wedge = patches.Wedge((x, y), radius, 270, 90, facecolor='black', edgecolor='none')
        ax.add_patch(wedge)
        ax.plot([x - radius, x + radius], [y, y], color='black', linewidth=1)

    elif oktas == 6:
        wedge = patches.Wedge((x, y), radius, 0, 270, facecolor='black', edgecolor='none')
        ax.add_patch(wedge)

    elif oktas == 7:
        full = patches.Circle((x, y), radius, edgecolor='black', facecolor='black', linewidth=1.2)
        ax.add_patch(full)
        ax.plot([x, x], [y + radius, y - radius], color='white', linewidth=1)

    elif oktas == 8:
        full = patches.Circle((x, y), radius, edgecolor='black', facecolor='black', linewidth=1.2)
        ax.add_patch(full)

def draw_wind_barb(ax, x, y, u, v):
    """
    Draws a wind barb at (x, y) using wind components u and v.
    Only draws barbs for speeds under 50 knots.
    """
    speed = np.sqrt(u**2 + v**2) * 1.94384  # Convert m/s to knots
    speed = round(speed / 5) * 5  # Round to nearest 5 kt

    angle = np.arctan2(u, v)  # wind *from* direction (in radians)

    # Shaft vector (points into the wind)
    length = 0.3
    dx = -length * np.sin(angle)
    dy = -length * np.cos(angle)
    x_end = x + dx
    y_end = y + dy

    if speed < 1:
        # Calm: Circle
        ax.add_patch(patches.Circle((x, y), 0.07, fill=False, edgecolor='black', linewidth=1.2))
        return

    # Draw main shaft
    ax.plot([x, x_end], [y, y_end], color='black', linewidth=1)

    # Start placing barbs from the end of the shaft
    barb_x = x_end
    barb_y = y_end
    barb_spacing = 0.15  # distance between barbs
    barb_len = 0.1       # base length of a full barb

    # Direction perpendicular to shaft (right-hand side)
    perp_dx = np.cos(angle)
    perp_dy = -np.sin(angle)

    def draw_barb(x0, y0, length):
        ax.plot([x0, x0 + perp_dx * length],
                [y0, y0 + perp_dy * length],
                color='black', linewidth=1)

    # Limit to speeds under 50 knots
    remaining = min(speed, 45)
    barb_pos = 0

    while remaining >= 10:
        draw_barb(barb_x - barb_pos * dx * barb_spacing,
                  barb_y - barb_pos * dy * barb_spacing,
                  barb_len)
        remaining -= 10
        barb_pos += 1

    if remaining >= 5:
        draw_barb(barb_x - barb_pos * dx * barb_spacing,
                  barb_y - barb_pos * dy * barb_spacing,
                  barb_len * 0.5)




    # Count number of flags (50 kt), full barbs (10 kt), and half barbs (5 kt)
    remaining = speed
    barb_pos = 0

    while remaining >= 10:
        draw_barb(barb_x - barb_pos * dx * barb_spacing,
                  barb_y - barb_pos * dy * barb_spacing,
                  barb_len)
        remaining -= 10
        barb_pos += 1

    if remaining >= 5:
        draw_barb(barb_x - barb_pos * dx * barb_spacing,
                  barb_y - barb_pos * dy * barb_spacing,
                  barb_len * 0.5)

# Example manual station data (x, y, temp, dewpoint, pressure, u_wind, v_wind, cloud_cover)
stations = [
    #Column 1
    {'x': 1, 'y': 1, 'temp': 30, 'dew': 20, 'pres': 122, 'u': 0, 'v': 0, 'cover': 0.1},
    {'x': 1, 'y': 2, 'temp': 30, 'dew': 20, 'pres': 122, 'u': 1, 'v': 0, 'cover': 0.2},
    {'x': 1, 'y': 3, 'temp': 30, 'dew': 20, 'pres': 122, 'u': 2, 'v': 0, 'cover': 0.3},
    {'x': 1, 'y': 4, 'temp': 30, 'dew': 30, 'pres': 122, 'u': 3, 'v': 0, 'cover': 0.4},
    {'x': 1, 'y': 5, 'temp': 30, 'dew': 30, 'pres': 122, 'u': 4, 'v': 0, 'cover': 0.5},

    #Column 2
    {'x': 2, 'y': 1, 'temp': 40, 'dew': 30, 'pres': 122, 'u': 5, 'v': 0, 'cover': 0.6},
    {'x': 2, 'y': 2, 'temp': 40, 'dew': 30, 'pres': 122, 'u': 6, 'v': 0, 'cover': 0.7},
    {'x': 2, 'y': 3, 'temp': 40, 'dew': 30, 'pres': 122, 'u': 7, 'v': 0, 'cover': 0.8},
    {'x': 2, 'y': 4, 'temp': 40, 'dew': 30, 'pres': 122, 'u': 8, 'v': 0, 'cover': 0.9},
    {'x': 2, 'y': 5, 'temp': 40, 'dew': 30, 'pres': 122, 'u': 9, 'v': 0, 'cover': 1.0},

    #Column 3
    {'x': 3, 'y': 1, 'temp': 50, 'dew': 40, 'pres': 122, 'u': 10, 'v': 0, 'cover': 0.0},
    {'x': 3, 'y': 2, 'temp': 50, 'dew': 40, 'pres': 122, 'u': 11, 'v': 0, 'cover': 0.0},
    {'x': 3, 'y': 3, 'temp': 50, 'dew': 40, 'pres': 122, 'u': 12, 'v': 0, 'cover': 0.0},
    {'x': 3, 'y': 4, 'temp': 50, 'dew': 40, 'pres': 122, 'u': 13, 'v': 0, 'cover': 0.0},
    {'x': 3, 'y': 5, 'temp': 50, 'dew': 40, 'pres': 122, 'u': 14, 'v': 0, 'cover': 0.0},

    #Column 4
    {'x': 4, 'y': 1, 'temp': 60, 'dew': 50, 'pres': 122, 'u': 15, 'v': 0, 'cover': 0.0},
    {'x': 4, 'y': 2, 'temp': 60, 'dew': 50, 'pres': 122, 'u': 16, 'v': 0, 'cover': 0.0},
    {'x': 4, 'y': 3, 'temp': 60, 'dew': 50, 'pres': 122, 'u': 17, 'v': 0, 'cover': 0.0},
    {'x': 4, 'y': 4, 'temp': 60, 'dew': 50, 'pres': 122, 'u': 18, 'v': 0, 'cover': 0.0},
    {'x': 4, 'y': 5, 'temp': 60, 'dew': 50, 'pres': 122, 'u': 19, 'v': 0, 'cover': 0.0},

    #Column 5
    {'x': 5, 'y': 1, 'temp': 70, 'dew': 60, 'pres': 122, 'u': 20, 'v': 0, 'cover': 0.0},
    {'x': 5, 'y': 2, 'temp': 70, 'dew': 60, 'pres': 122, 'u': 21, 'v': 0, 'cover': 0.0},
    {'x': 5, 'y': 3, 'temp': 70, 'dew': 60, 'pres': 122, 'u': 22, 'v': 0, 'cover': 0.0},
    {'x': 5, 'y': 4, 'temp': 70, 'dew': 60, 'pres': 122, 'u': 23, 'v': 0, 'cover': 0.0},
    {'x': 5, 'y': 5, 'temp': 70, 'dew': 60, 'pres': 122, 'u': 24, 'v': 0, 'cover': 0.0},
]

# Plot each station
for station in stations:
    x = station['x']
    y = station['y']
    temp = station['temp']
    dew = station['dew']
    pres = station['pres']
    u = station['u']
    v = station['v']
    cover = station['cover']

    draw_cloud_cover(ax, x, y, cover)
    ax.text(x - 0.3, y + 0.1, f"{temp}", fontsize=8, color='red')
    ax.text(x - 0.3, y - 0.1, f"{dew}", fontsize=8, color='green')
    ax.text(x + 0.1, y + 0.1, f"{pres}", fontsize=8, color='orange')
    draw_wind_barb(ax, x, y, u, v)



# Create button to clear fronts and pressure markers
button_ax = plt.axes([0.81, 0.01, 0.15, 0.05])  # [left, bottom, width, height]
clear_button = Button(button_ax, 'Clear All')
clear_button.on_clicked(clear_fronts_and_markers)

btn_default.on_clicked(set_mode_default)
btn_cold.on_clicked(set_mode_cold)
btn_warm.on_clicked(set_mode_warm)
btn_occluded.on_clicked(set_mode_occluded)
btn_stationary.on_clicked(set_mode_stationary)
btn_dryline.on_clicked(set_mode_dryline)
btn_high.on_clicked(set_mode_high)
btn_low.on_clicked(set_mode_low)

plt.grid(True)
plt.show()
