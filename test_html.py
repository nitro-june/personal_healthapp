from jinja2 import Environment, FileSystemLoader, Template
import functions_healthapp as hp

user = hp.get_user_info(1)
trackables = hp.get_user_trackables(1)
trackables_name = []

for trackable in trackables:
    trackables_name.append(hp.get_trackable_name(trackable[1]))

print(user)

with open('report_layout.html.jinja') as f:
    tmpl = Template(f.read())

with open("hp_report.html", "w") as fh:
    fh.write(tmpl.render(name = user[0] + " " + user[1], user_info = user, trackables = trackables_name))