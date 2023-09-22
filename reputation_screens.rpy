# Reputation Screens
screen reputation_choice_hint():
    style_prefix "reputation_choice"

    frame:
        xalign 1.0
        xoffset -100

        background "gui/reputation/background_{}.webp".format(reputation().name.lower())

        hbox:
            spacing 5
            align (0.5, 0.5)
            xoffset 20

            add Transform("gui/reputation/logo.webp", zoom=0.2382) yalign 0.5

            text reputation().name yalign 0.5

style reputation_choice_text is syne_extra_bold_22


screen reputation_popup(required_reputation=None):
    modal True
    zorder 300

    python:
        rep = reputation()

        if required_reputation is None or required_reputation == rep:
            message = f"Congratulations! Your Key Character Trait {{b}}{rep.name}{{/b}} has just changed the outcome of a decision someone was making."
        else:
            message = f"Unfortunately, your Key Character Trait {{b}}{rep.name}{{/b}} did not change the outcome of this decision."

    use alert_template(message):
        textbutton "OK":
            align (0.5, 1.0)
            action Return()

    if config_debug:
        timer 0.1 action Return()