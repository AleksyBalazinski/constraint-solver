import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


def animate_pendulum(x_history, y_history, l, t_span, dt):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(-l - 0.1, l + 0.1)
    ax.set_ylim(-l - 0.1, 0.1)
    ax.set_aspect("equal")  # Keeps the pendulum from looking distorted
    ax.grid(True)

    (line,) = ax.plot([], [], "o-", lw=2, color="blue", markersize=8)
    time_template = "Time = %.2fs"
    time_text = ax.text(0.05, 0.9, "", transform=ax.transAxes)

    def init():
        line.set_data([], [])
        time_text.set_text("")
        return line, time_text

    # 5. Animation function: Called sequentially for each frame (i)

    def animate(i):
        # Pendulum goes from the origin (0,0) to its current (x, y) position
        this_x = [0, x_history[i]]
        this_y = [0, y_history[i]]

        line.set_data(this_x, this_y)
        time_text.set_text(time_template % (i * dt))
        return line, time_text

    # 6. Run the animation
    # interval=10 matches your dt=0.01s (10 milliseconds per frame)
    ani = animation.FuncAnimation(
        fig,
        animate,
        frames=len(t_span),
        init_func=init,
        blit=True,
        interval=10,
        repeat=True,
    )

    return ani


def animate_double_pendulum(x_history, l1, l2, dt, t_span):
    max_len = l1 + l2 + 0.2

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-max_len, max_len)
    ax.set_ylim(-max_len, max_len)
    ax.set_aspect("equal")
    ax.grid(True)

    (line,) = ax.plot([], [], "o-", lw=2, color="blue", markersize=8)

    (trace,) = ax.plot([], [], "-", lw=1, color="red", alpha=0.5)

    time_template = "Time = %.2fs"
    time_text = ax.text(0.05, 0.92, "", transform=ax.transAxes)

    def init():
        line.set_data([], [])
        trace.set_data([], [])
        time_text.set_text("")
        return line, trace, time_text

    def animate(i):
        # Extract current positions of both bobs
        x1, y1 = x_history[0, i], x_history[1, i]
        x2, y2 = x_history[2, i], x_history[3, i]

        this_x = [0, x1, x2]
        this_y = [0, y1, y2]

        line.set_data(this_x, this_y)

        trace_start = max(0, i - 100)
        trace.set_data(
            x_history[2, trace_start:i], x_history[3, trace_start:i]
        )

        time_text.set_text(time_template % (i * dt))
        return line, trace, time_text

    ani = animation.FuncAnimation(
        fig,
        animate,
        frames=len(t_span),
        init_func=init,
        blit=True,
        interval=int(dt * 1000),
        repeat=True,
    )

    return ani


def animate_two_double_pendulums(
    x_history1,
    x_history2,
    l1,
    l2,
    dt,
    t_span,
    label1="Method 1",
    label2="Method 2",
):
    max_len = l1 + l2 + 0.2

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-max_len, max_len)
    ax.set_ylim(-max_len, max_len)
    ax.set_aspect("equal")
    ax.grid(True)

    # First pendulum (Blue)
    (line1,) = ax.plot(
        [], [], "o-", lw=2, color="tab:blue", markersize=8, label=label1
    )
    (trace1,) = ax.plot([], [], "-", lw=1, color="tab:blue", alpha=0.3)

    # Second pendulum (Orange)
    (line2,) = ax.plot(
        [], [], "o-", lw=2, color="tab:orange", markersize=8, label=label2
    )
    (trace2,) = ax.plot([], [], "-", lw=1, color="tab:orange", alpha=0.3)

    ax.legend(loc="upper right")

    time_template = "Time = %.2fs"
    time_text = ax.text(0.05, 0.92, "", transform=ax.transAxes)

    def init():
        line1.set_data([], [])
        trace1.set_data([], [])
        line2.set_data([], [])
        trace2.set_data([], [])
        time_text.set_text("")
        return line1, trace1, line2, trace2, time_text

    def animate(i):
        trace_start = max(0, i - 100)

        # Pendulum 1
        x1_1, y1_1 = x_history1[0, i], x_history1[1, i]
        x2_1, y2_1 = x_history1[2, i], x_history1[3, i]
        line1.set_data([0, x1_1, x2_1], [0, y1_1, y2_1])
        trace1.set_data(
            x_history1[2, trace_start:i], x_history1[3, trace_start:i]
        )

        # Pendulum 2
        x1_2, y1_2 = x_history2[0, i], x_history2[1, i]
        x2_2, y2_2 = x_history2[2, i], x_history2[3, i]
        line2.set_data([0, x1_2, x2_2], [0, y1_2, y2_2])
        trace2.set_data(
            x_history2[2, trace_start:i], x_history2[3, trace_start:i]
        )

        time_text.set_text(time_template % (i * dt))
        return line1, trace1, line2, trace2, time_text

    ani = animation.FuncAnimation(
        fig,
        animate,
        frames=len(t_span),
        init_func=init,
        blit=True,
        interval=int(dt * 1000),
        repeat=True,
    )

    return ani


def animate_n_pendulum(x_history, ls, dt, t_span, trace_length=100):
    """Animates an N-bob pendulum.

    Parameters:
    - x_history: np.ndarray of shape (2*n, len(t_span))
    - ls: list or array of rod lengths
    - dt: time step size
    - t_span: time array
    - trace_length: number of past frames to display for the tip trace
    """
    n = len(ls)
    max_len = sum(ls) + 0.2

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-max_len, max_len)
    ax.set_ylim(-max_len, max_len)
    ax.set_aspect("equal")
    ax.grid(True)

    # Line for the rods and bobs (including origin pivot)
    (line,) = ax.plot([], [], "o-", lw=2, color="blue", markersize=6)

    # Trace for the final (tip) bob
    (trace,) = ax.plot([], [], "-", lw=1, color="red", alpha=0.5)

    time_template = "Time = %.2fs"
    time_text = ax.text(0.05, 0.92, "", transform=ax.transAxes)

    def init():
        line.set_data([], [])
        trace.set_data([], [])
        time_text.set_text("")
        return line, trace, time_text

    def animate(i):
        # 1. Extract x and y coordinates for all bobs at frame i
        # x-coords are at even rows [0, 2, 4, ...], y-coords at odd rows [1, 3, 5, ...]
        x_coords = np.append(0, x_history[0::2, i])
        y_coords = np.append(0, x_history[1::2, i])

        line.set_data(x_coords, y_coords)

        # 2. Trace path for the tip (last bob: rows -2 and -1)
        trace_start = max(0, i - trace_length)
        trace.set_data(
            x_history[-2, trace_start:i], x_history[-1, trace_start:i]
        )

        time_text.set_text(time_template % (i * dt))
        return line, trace, time_text

    ani = animation.FuncAnimation(
        fig,
        animate,
        frames=len(t_span),
        init_func=init,
        blit=True,
        interval=int(dt * 1000),
        repeat=True,
    )

    return ani
