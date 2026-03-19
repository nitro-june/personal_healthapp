from jinja2 import Environment, FileSystemLoader, Template
import src_python.functions_healthapp as hp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from scipy.interpolate import make_interp_spline, PchipInterpolator
import os
import pdfkit

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Plotting needs to have set axis

# ----- Plot and create matplotlib figures -----

def plot_dates_smooth_to_file(dates_str, y_values, filename, color='blue', marker=None, linestyle='-', dpi=150, ymax=None, ystep=1, trackable_name=None):
    """
    Plots a smooth and/or non-smooth figure depending on number of points
    and saves the figure to an image file.

    :param dates_str: list of dates as "YYYY-MM-DD"
    :param y_values: list of numerical values
    :param filename: path to save the image (e.g., "output/plot.png")
    """
    if not dates_str or not y_values:
        return

    # Parse and sort dates
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates_str]
    x = mdates.date2num(dates)
    y = np.array(y_values)

    sorted_idx = np.argsort(x)
    x = x[sorted_idx]
    y = y[sorted_idx]

    fig, ax = plt.subplots(figsize=(6, 4), dpi=dpi)

    try:
        if len(x) > 5:
            x_smooth = np.linspace(x.min(), x.max(), 50)
            spline = make_interp_spline(x, y, k=2)
            y_smooth = np.clip(spline(x_smooth), y.min(), y.max())

            # Smooth line
            ax.plot(mdates.num2date(x_smooth), y_smooth,
                    color=color, linestyle=linestyle, label='Smooth')

            # Original data points
            ax.plot(mdates.num2date(x), y,
                    linestyle='None', marker='o', color=color, label='Data Points')
        elif 3 <= len(x) <= 5:
            x_smooth = np.linspace(x.min(), x.max(), 50)
            pchip = PchipInterpolator(x, y)
            y_smooth = np.clip(pchip(x_smooth), y.min(), y.max())
            ax.plot(mdates.num2date(x_smooth), y_smooth, color=color, marker=marker, linestyle=linestyle, label=f'{trackable_name} Smooth')
            ax.plot(mdates.num2date(x), y, 'o', color=color, label='Data Points')
        else:
            # Less than 3 points: just plot raw points
            ax.plot(mdates.num2date(x), y, color=color, marker='o', linestyle=linestyle, label='Data Points')
    except Exception as e:
        print(f"Plotting error for {trackable_name}:", e)
        ax.plot(mdates.num2date(x), y, color=color, marker='o', linestyle=linestyle, label='Data Points')

    # Formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()

    if ymax is not None:
        ax.set_ylim(0, ymax)
        ax.set_yticks(np.arange(0, ymax + ystep, ystep))

    ax.grid(True)
    ax.legend()

    # Ensure folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save to file
    fig.savefig(filename, bbox_inches='tight')
    plt.close(fig)

# ----- Generate the PDF-report -----
def generate_report(user_id):

    user = hp.get_user_info(user_id)
    trackables = hp.get_user_trackables(user_id)

    trackables_name = []
    created_files = []

    filename_report_html = f"{user[1]}{user[0]}Report.html"
    filename_report_pdf = f"{user[1]}{user[0]}Report.pdf"
    report_html_path = os.path.join(PROJECT_ROOT, filename_report_html)
    report_pdf_path = os.path.join(PROJECT_ROOT, filename_report_pdf)
    template_path = os.path.join(PROJECT_ROOT, "report_layout.html.jinja")

    for trackable in trackables:

        track_name = hp.get_trackable_name(trackable[1])
        trackables_name.append(track_name)
        print(track_name)

        track_maxy = hp.get_trackable_maxy(trackable[1])
        track_maxy = int(track_maxy)
        print(track_maxy)

        track_tick = hp.get_trackable_tick(trackable[1])
        print(track_tick)

        file_name = os.path.join(PROJECT_ROOT, "temp_img", f"{track_name}Plot.png")
        created_files.append(file_name)

        dates_p, values_p = [], []
        get_values = hp.get_values(trackable[0])
        print(get_values)

        for value in get_values:
            dates_p.append(value[0])
            values_p.append(value[1])

        plot_dates_smooth_to_file(
            dates_p,
            values_p,
            file_name,
            ymax = track_maxy,
            ystep = track_tick,
            trackable_name = track_name
        )

    # Render HTML
    with open(template_path, encoding="utf-8") as f:
        tmpl = Template(f.read())

    with open(report_html_path, "w", encoding="utf-8") as fh:
        fh.write(tmpl.render(
            name=user[0] + " " + user[1],
            user_info=user,
            trackables=trackables_name
        ))

    # Create PDF
    config = pdfkit.configuration(
        wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    )

    options = {
        'enable-local-file-access': None
    }

    pdfkit.from_file(
        report_html_path,
        report_pdf_path,
        configuration=config,
        options=options
    )

    # for plotted_file in created_files:
    #    os.remove(plotted_file)

    return filename_report_pdf

# NOTE: remove import-time side effects; call `generate_report()` from the application when needed.